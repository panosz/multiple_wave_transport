#include "perturbed_pendulum.hpp"
#include <pybind11/eigen.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

typedef WP::PerturbedPendulum PerturbedPendulum;
typedef WP::UnperturbedPendulum UnperturbedPendulum;

void bind_pendulum(py::module_ &m) {
  py::class_<PerturbedPendulum>(m, "PerturbedPendulum")
      .def(py::init<double>(), py::arg("epsilon"))
      .def("__call__", &PerturbedPendulum::call, py::arg("s"), py::arg("t"))
      .def("poincare", &PerturbedPendulum::poincare, py::arg("s"),
           py::arg("t_max"))
      .def("get_loss_time", &PerturbedPendulum::get_loss_time, py::arg("s_init"),
           py::arg("t_max"));

  py::class_<UnperturbedPendulum>(m, "UnperturbedPendulum")
      .def(py::init<>())
      .def("integrate", &UnperturbedPendulum::integrate, py::arg("s"), py::arg("t"))
      .def("energy", &UnperturbedPendulum::energy, py::arg("s"))
    ;
}
