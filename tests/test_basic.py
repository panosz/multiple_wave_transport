import numpy as np
import numpy.testing as nt
import multiple_wave_transport 


def test_version():
    assert multiple_wave_transport.__version__ == "0.0.1"

def test_Wavepacket():
    w = multiple_wave_transport.WavePacket(1,2,3,4)
    nt.assert_allclose(w(0,0), 0, atol=1e-16)
    nt.assert_allclose(w(t=0,z=0), 0, atol=1e-16)
    assert w.A == 1
    assert w.sigma == 2
    assert w.k == 3
    assert w.vp == 4


def test_Wavepacket_construct_kwargs():
    kw = dict(A=1, sigma=2, k=3, vp=4) 
    w = multiple_wave_transport.WavePacket(**kw)

def test_Wavepacket_vector_call():
    w = multiple_wave_transport.WavePacket(1,2,3,4)
    z = np.array([1,2])
    t = np.array([0.2, 3.8])

    vector_result = w(z, t)

    scalar_result = [w(zi, ti) for zi, ti in zip(z,t)]

    nt.assert_allclose(vector_result, scalar_result, atol=1e-16, rtol=1e-16)


def test_Wavepacket_vector_dz_call():
    w = multiple_wave_transport.WavePacket(1,2,3,4)
    z = np.array([1,2])
    t = np.array([0.2, 3.8])

    vector_result = w.dz(z, t)

    scalar_result = [w.dz(zi, ti) for zi, ti in zip(z,t)]

    nt.assert_allclose(vector_result, scalar_result, atol=1e-16, rtol=1e-16)


def test_Wavepacket_system_call():
    w = multiple_wave_transport.WavePacket(1,2,3,4)
    w.system([1,2], 3)

def test_Wavepacket_repr():
    w = multiple_wave_transport.WavePacket(1,2,3,4)
    assert "A=1" in str(w)
