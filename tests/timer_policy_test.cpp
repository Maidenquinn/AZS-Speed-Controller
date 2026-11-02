#include "timer_policy.h"
#include <cassert>
#include <cmath>
#include <iostream>

int main() {
  using namespace azs;
  timerSleepReturnRva = 0x5ddaf48;
  for(long speed : {100L, 200L, 500L, 1000L, 1500L, 2500L}) {
    auto delay = timerSleepNanoseconds(timerSleepReturnRva, 0, simulationSleepNs, speed);
    auto expected = static_cast<std::uint32_t>((std::uint64_t(simulationSleepNs) * 100) / speed);
    assert(delay == expected);
    double physicalStep = simulationSleepNs / 1e9 * 100.0 / speed;
    double newRate = std::min(physicalStep * (speed / 100.0), 0.1) / physicalStep;
    std::cout << "x" << (speed / 100.0) << " sleep_ns=" << delay
              << " ideal_sim_rate~=" << newRate << "\n";
  }
  assert(timerSleepNanoseconds(0x1111, 0, simulationSleepNs, 500) == simulationSleepNs);
  assert(timerSleepNanoseconds(timerSleepReturnRva, 1, simulationSleepNs, 500) == simulationSleepNs);
  assert(timerSleepNanoseconds(timerSleepReturnRva, 0, 1000, 500) == 1000);
  assert(timerSleepNanoseconds(timerSleepReturnRva, 0, simulationSleepNs, 50) == simulationSleepNs);
  timerSleepReturnRva = 0;
  assert(timerSleepNanoseconds(0x5ddaf48, 0, simulationSleepNs, 500) == simulationSleepNs);
  std::cout << "timer_policy ok\n";
  return 0;
}
