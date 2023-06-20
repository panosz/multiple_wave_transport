import matplotlib.pyplot as plt
import numpy as np

from multiple_wave_transport._multiple_wave_transport import ThreeWaveSystem


def angle_to_2pi(angle):
    """
     convert angle to 0 to 2pi. make sure it works for negative angles as well
    """
    return np.mod(angle, 2*np.pi)


tws = ThreeWaveSystem(1.8)

print(tws(np.array([2, 4]), 3.1))

for p_init in np.linspace(1, 30, 20):
    pc = tws.poincare([0, p_init], 10000)
    plt.plot(angle_to_2pi(pc[0]), pc[1], 'k,')

plt.show()
