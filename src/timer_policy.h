#pragma once
#include <cstdint>

namespace azs {
// Filled by prepareTimerFix after a successful signature scan (0 = unarmed).
inline std::uintptr_t timerSleepReturnRva = 0;
constexpr std::uint32_t simulationSleepNs = 25000000;

// Only the identified local simulation call may change; other Rust sleeps pass through.
inline std::uint32_t timerSleepNanoseconds(std::uintptr_t callerRva,
    std::uint64_t seconds, std::uint32_t nanos, long speed100) {
  if(timerSleepReturnRva == 0 || callerRva != timerSleepReturnRva || seconds != 0 ||
      nanos != simulationSleepNs || speed100 < 100 || speed100 > 2500) return nanos;
  return static_cast<std::uint32_t>((std::uint64_t(nanos) * 100) / speed100);
}
}
