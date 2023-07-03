#include "perturbed_pendulum.hpp"
#include <pybind11/eigen.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

typedef WP::PerturbedPendulum PerturbedPendulum;
typedef WP::UnperturbedPendulum UnperturbedPendulum;
typedef WP::PerturbedPendulumWithLowFrequency PerturbedPendulumWithLowFrequency;
typedef WP::PerturbedPendulumOnlyLowFrequency PerturbedPendulumOnlyLowFrequency;

void bind_pendulum(py::module_ &m) {
  py::enum_<WP::BoundaryType>(m, "BoundaryType")
      .value("X", WP::BoundaryType::X)
      .value("P", WP::BoundaryType::P);

  py::class_<PerturbedPendulum>(m, "PerturbedPendulum")
      .def(py::init<double>(), py::arg("epsilon"))
      .def("__call__", &PerturbedPendulum::call, py::arg("s"), py::arg("t"))
      .def("poincare", &PerturbedPendulum::poincare, py::arg("s"),
           py::arg("t_max"))
      .def("get_loss_time", &PerturbedPendulum::get_loss_time,
           py::arg("s_init"), py::arg("t_max"),
           py::arg("boundary_type") = WP::BoundaryType::X);

  py::class_<PerturbedPendulumWithLowFrequency>(
      m, "PerturbedPendulumWithLowFrequency")
      .def(py::init<double, double>(), py::arg("epsilon_high"),
           py::arg("epsilon_low"))
      .def("__call__", &PerturbedPendulumWithLowFrequency::call, py::arg("s"),
           py::arg("t"))
      .def("poincare", &PerturbedPendulumWithLowFrequency::poincare,
           py::arg("s"), py::arg("t_max"))
      .def("get_loss_time", &PerturbedPendulumWithLowFrequency::get_loss_time,
           py::arg("s_init"), py::arg("t_max"),
           py::arg("boundary_type") = WP::BoundaryType::X);

  py::class_<PerturbedPendulumOnlyLowFrequency>(m, "PerturbedPendulumOnlyLowFrequency")
      .def(py::init<double>(), py::arg("epsilon"))
      .def("__call__", &PerturbedPendulumOnlyLowFrequency::call, py::arg("s"), py::arg("t"))
      .def("poincare", &PerturbedPendulumOnlyLowFrequency::poincare, py::arg("s"),
           py::arg("t_max"))
      .def("get_loss_time", &PerturbedPendulumOnlyLowFrequency::get_loss_time,
           py::arg("s_init"), py::arg("t_max"),
           py::arg("boundary_type") = WP::BoundaryType::X);

  py::class_<UnperturbedPendulum>(m, "UnperturbedPendulum")
      .def(py::init<>())
      .def("integrate", &UnperturbedPendulum::integrate, py::arg("s"),
           py::arg("t"))
      .def("energy", &UnperturbedPendulum::energy, py::arg("s"));
}

