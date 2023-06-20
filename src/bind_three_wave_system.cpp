#include "multiple_wave_system.hpp"
#include <pybind11/eigen.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

typedef WP::ThreeWaveSystem ThreeWaveSystem;

void bind_three_wave_system(py::module_ &m) {
  py::class_<ThreeWaveSystem>(m, "ThreeWaveSystem")
      .def(py::init<double>(), py::arg("epsilon"))
      .def("__call__", &ThreeWaveSystem::call, py::arg("s"), py::arg("t"))
      .def("repeat_state", &ThreeWaveSystem::repeat_state, py::arg("s"))
      .def("poincare", &ThreeWaveSystem::poincare, py::arg("s"), py::arg("t_max"))
  ;
}
