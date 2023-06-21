import matplotlib.pyplot as plt
import numpy as np

from multiple_wave_transport._multiple_wave_transport import ThreeWaveSystem


def angle_to_2pi(angle):
    """
    convert angle to 0 to 2pi. make sure it works for negative angles as well
    """
    return np.mod(angle, 2 * np.pi)

def generate_random_pairs(n, xmin, xmax, ymin, ymax):
    # Generate n random x values in the range [xmin, xmax]
    x_values = np.random.uniform(xmin, xmax, n)
    
    # Generate n random y values in the range [ymin, ymax]
    y_values = np.random.uniform(ymin, ymax, n)

    # Combine x and y values into pairs
    pairs = list(zip(x_values, y_values))

    return pairs


tws = ThreeWaveSystem(3.8)

print(tws(np.array([2, 4]), 3.1))

T_integr = 500

print(tws.get_loss_time([2, 8], p_max=20, t_max=T_integr))

initial_states = generate_random_pairs(200000, 0, 2*np.pi, 6, 17)
p_init_v = np.array([p_init for _, p_init in initial_states])

loss_times = np.array(
    [tws.get_loss_time(s, p_max=20, t_max=T_integr) for s in initial_states]
)

actual_loss_times = loss_times[loss_times < T_integr]


fig, ax = plt.subplots(1, 1)
ax.plot(p_init_v[loss_times < T_integr], actual_loss_times, "k.")

fig, (ax, ax_freq) = plt.subplots(2, 1)
ax.hist(actual_loss_times[actual_loss_times<100], bins=1000)

hist, times = np.histogram(actual_loss_times[actual_loss_times<100], bins=1000)
Y = np.fft.fft(hist)
dt = times[1] - times[0]
frequencies = np.fft.fftfreq(len(hist), dt)

# Plot the amplitudes
# We usually plot the absolute value of the FFT output, as it can be complex
# Also, usually the relevant part of the FFT is the positive frequencies (frequencies >= 0)
mask = frequencies >= 0
ax_freq.plot(frequencies[mask], np.abs(Y[mask]))


fig, ax = plt.subplots(1, 1)
for p_init in np.linspace(1, 30, 20):
    pc = tws.poincare([0, p_init], 10000)
    ax.plot(angle_to_2pi(pc[0]), pc[1], "k,")

plt.show()
