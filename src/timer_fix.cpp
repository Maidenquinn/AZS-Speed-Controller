#define WIN32_LEAN_AND_MEAN
#define NOMINMAX
#include <windows.h>
#include <MinHook.h>
#include <cstddef>
#include <cstring>
#ifdef _MSC_VER
#include <intrin.h>
#endif
#include "timer_fix.h"
#include "timer_policy.h"

namespace {
using RustSleepFn = void (*)(std::uint64_t, std::uint32_t);
RustSleepFn originalSleep = nullptr;
LONG (*getSpeed)() = nullptr;
volatile LONG* activeStatus = nullptr;
std::uintptr_t imageBase = 0;

// xor ecx,ecx ; mov edx,25000000 ; call rel32
constexpr unsigned char kCallerPrefix[] = {
  0x31,0xc9,0xba,0x40,0x78,0x7d,0x01,0xe8
};
// Rust sleep prologue observed on 0.127.0 and 0.139.0 Windows x64 builds.
constexpr unsigned char kSleepStart[] = {
  0x55,0x41,0x57,0x41,0x56,0x56,0x57,0x53,0x48,0x83,0xec,0x48,
  0x48,0x8d,0x6c,0x24,0x40,0x89,0xd6,0x48,0x89,0xcf,0x41,0x89
};

bool bytesAt(const unsigned char* base, std::size_t rva, const unsigned char* expected,
    std::size_t length, std::size_t imageSize) {
  if(rva > imageSize || length > imageSize - rva) return false;
  MEMORY_BASIC_INFORMATION info{};
  if(!VirtualQuery(base + rva, &info, sizeof(info)) || info.State != MEM_COMMIT ||
      (info.Protect & (PAGE_NOACCESS | PAGE_GUARD))) return false;
  const auto remaining = static_cast<const unsigned char*>(info.BaseAddress) + info.RegionSize - (base + rva);
  return remaining >= static_cast<std::ptrdiff_t>(length) &&
      std::memcmp(base + rva, expected, length) == 0;
}

std::uintptr_t followThunk(const unsigned char* base, std::uintptr_t target,
    std::size_t imageSize) {
  // Optional near jmp thunk (same displacement family as 0.127/0.139).
  if(bytesAt(base, target, reinterpret_cast<const unsigned char*>("\xe9"), 1, imageSize)) {
    std::int32_t rel = 0;
    std::memcpy(&rel, base + target + 1, 4);
    return target + 5 + rel;
  }
  return target;
}

bool resolveCaller(const unsigned char* base, std::size_t callerRva, std::size_t imageSize,
    std::uintptr_t* sleepRva, std::uintptr_t* returnRva) {
  if(!bytesAt(base, callerRva, kCallerPrefix, sizeof(kCallerPrefix), imageSize)) return false;
  const std::uintptr_t callSite = callerRva + 7; // after xor + mov
  if(callSite + 5 > imageSize) return false;
  std::int32_t rel = 0;
  std::memcpy(&rel, base + callSite + 1, 4);
  std::uintptr_t target = callSite + 5 + rel;
  target = followThunk(base, target, imageSize);
  if(!bytesAt(base, target, kSleepStart, sizeof(kSleepStart), imageSize)) return false;
  *sleepRva = target;
  *returnRva = callerRva + 12; // instruction after call (often a NOP)
  return true;
}

bool findSimulationSleep(const unsigned char* base, const IMAGE_NT_HEADERS64* pe,
    std::uintptr_t* sleepRva, std::uintptr_t* returnRva) {
  const auto imageSize = static_cast<std::size_t>(pe->OptionalHeader.SizeOfImage);
  auto* section = IMAGE_FIRST_SECTION(pe);
  int hits = 0;
  std::uintptr_t foundSleep = 0, foundReturn = 0;
  for(unsigned i = 0; i < pe->FileHeader.NumberOfSections; ++i) {
    if(!(section[i].Characteristics & IMAGE_SCN_MEM_EXECUTE)) continue;
    const auto start = static_cast<std::size_t>(section[i].VirtualAddress);
    const auto size = static_cast<std::size_t>(section[i].Misc.VirtualSize);
    if(start >= imageSize || size < sizeof(kCallerPrefix) || size > imageSize - start) continue;
    for(std::size_t off = 0; off + sizeof(kCallerPrefix) <= size; ++off) {
      const auto rva = start + off;
      if(std::memcmp(base + rva, kCallerPrefix, sizeof(kCallerPrefix)) != 0) continue;
      std::uintptr_t sleep = 0, ret = 0;
      if(!resolveCaller(base, rva, imageSize, &sleep, &ret)) continue;
      if(hits == 0) { foundSleep = sleep; foundReturn = ret; }
      else if(foundSleep != sleep || foundReturn != ret) return false; // ambiguous
      ++hits;
    }
  }
  if(hits != 1) return false;
  *sleepRva = foundSleep;
  *returnRva = foundReturn;
  return true;
}

#ifdef _MSC_VER
__declspec(noinline)
#else
__attribute__((noinline))
#endif
void hookedRustSleep(std::uint64_t seconds, std::uint32_t nanos) {
#ifdef _MSC_VER
  auto caller = reinterpret_cast<std::uintptr_t>(_ReturnAddress());
#else
  auto caller = reinterpret_cast<std::uintptr_t>(__builtin_return_address(0));
#endif
  const auto rva = caller >= imageBase ? caller - imageBase : 0;
  if(rva == azs::timerSleepReturnRva && seconds == 0 && nanos == azs::simulationSleepNs) {
    InterlockedCompareExchange(activeStatus, 3, 2);
    nanos = azs::timerSleepNanoseconds(rva, seconds, nanos, getSpeed());
  }
  originalSleep(seconds, nanos);
}
}

bool prepareTimerFix(LONG (*readSpeed)(), volatile LONG* active) {
  auto* base = reinterpret_cast<unsigned char*>(GetModuleHandleW(nullptr));
  if(!base || sizeof(void*) != 8) return false;
  auto* dos = reinterpret_cast<const IMAGE_DOS_HEADER*>(base);
  if(dos->e_magic != IMAGE_DOS_SIGNATURE || dos->e_lfanew <= 0 || dos->e_lfanew > 4096) return false;
  auto* pe = reinterpret_cast<const IMAGE_NT_HEADERS64*>(base + dos->e_lfanew);
  if(pe->Signature != IMAGE_NT_SIGNATURE || pe->FileHeader.Machine != IMAGE_FILE_MACHINE_AMD64)
    return false;

  std::uintptr_t sleepRva = 0, returnRva = 0;
  if(!findSimulationSleep(base, pe, &sleepRva, &returnRva)) return false;

  imageBase = reinterpret_cast<std::uintptr_t>(base);
  azs::timerSleepReturnRva = returnRva;
  getSpeed = readSpeed;
  activeStatus = active;
  return MH_CreateHook(base + sleepRva, reinterpret_cast<LPVOID>(hookedRustSleep),
      reinterpret_cast<LPVOID*>(&originalSleep)) == MH_OK;
}
