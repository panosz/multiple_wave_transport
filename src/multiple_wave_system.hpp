#ifndef MULTIPLE_WAVE_SYSTEM_IEY4EIL5
#define MULTIPLE_WAVE_SYSTEM_IEY4EIL5
#include "type_definitions.hpp"

namespace WP {
class ThreeWaveSystem {
  double epsilon;

public:
  explicit ThreeWaveSystem(double _epsilon) noexcept : epsilon(_epsilon){};
  State call(const State &s, double t) const noexcept;
  void operator()(const State &s, State &dsdt, double t) const noexcept;
  OrbitPoints repeat_state(const State &s) const noexcept;
  OrbitPoints poincare(const State &s, double t_max) const noexcept;
};
} // namespace WP

#endif // end of include guard: MULTIPLE_WAVE_SYSTEM_IEY4EIL5
