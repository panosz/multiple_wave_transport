#include "wavepacket.hpp"
#include <pybind11/eigen.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

typedef WP::WavePacket WavePacket;

void bind_integrator(py::module_ &m) {
  py::class_<WP::Integrator>(m, "Integrator")
    .def(py::init<WavePacket&,double, double>(),
         py::arg("wp"),
         py::arg("atol")=WP::Integrator::ATOL_DEFAULT,
         py::arg("rtol")=WP::Integrator::RTOL_DEFAULT)
    .def("integrate", &WP::Integrator::integrate, py::arg("point"), py::arg("t_integr"));
}
