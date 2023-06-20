#include <iostream>
#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include "my_lib.hpp"
#include "type_definitions.hpp"
#include "wavepacket.hpp"
// #include "integrator.hpp"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)


namespace py = pybind11;

typedef WP::WavePacket WavePacket;

void bind_wavepacket(py::module_ &m);
void bind_integrator(py::module_ &m);
void bind_three_wave_system(py::module_ &m);

PYBIND11_MODULE(_multiple_wave_transport, m) {
  m.doc() = R"pbdoc(
  A python package modelling the interaction of charged particles with an electrostatic pulse.
  -----------------------

  .. currentmodule:: _multiple_wave_transport

  .. autosummary::
  :toctree: _generate

  WavePacket
  )pbdoc";


  #ifdef VERSION_INFO
  m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
  #else
  m.attr("__version__") = "dev";
  #endif

  bind_wavepacket(m);
  bind_integrator(m);
  bind_three_wave_system(m);

}
