import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ---------------------------------------------------
# Fixed frequencies in the original signal
# ---------------------------------------------------
f1 = 10      # Hz (always below Nyquist)
f2 = 70      # Hz (will alias if fs < 140 Hz)

duration = 1
t = np.linspace(0, duration, 5000)

# Initial sampling frequency
fs0 = 80

fig, ax = plt.subplots(figsize=(13,6))
plt.subplots_adjust(bottom=0.25)

# ---------------------------------------------------
# Function to calculate aliased frequency
# ---------------------------------------------------
def alias_frequency(f, fs):
    return abs(((f + fs/2) % fs) - fs/2)

# ---------------------------------------------------
# Original continuous signal
# ---------------------------------------------------
signal = np.sin(2*np.pi*f1*t) + np.sin(2*np.pi*f2*t)

sample_times = np.arange(0, duration, 1/fs0)
sample_values = (np.sin(2*np.pi*f1*sample_times) +
                 np.sin(2*np.pi*f2*sample_times))

interp = np.interp(t, sample_times, sample_values)

line_signal, = ax.plot(
    t,
    signal,
    linewidth=2,
    label="Original Signal (10 Hz + 70 Hz)"
)

line_interp, = ax.plot(
    t,
    interp,
    '--',
    linewidth=2,
    label="Reconstructed from Samples"
)

points = ax.plot(
    sample_times,
    sample_values,
    'ro',
    markersize=5,
    label="Samples"
)[0]

title = ax.set_title("")
ax.set_xlabel("Time (seconds)")
ax.set_ylabel("Amplitude")
ax.grid(True)
ax.legend()
ax.set_ylim(-2.5,2.5)

# ---------------------------------------------------
# Slider
# ---------------------------------------------------
ax_fs = plt.axes([0.15,0.08,0.7,0.03])

slider_fs = Slider(
    ax_fs,
    "Sampling Frequency (Hz)",
    20,
    200,
    valinit=fs0,
    valstep=1
)

# ---------------------------------------------------
# Update
# ---------------------------------------------------
def update(val):

    fs = slider_fs.val

    signal = np.sin(2*np.pi*f1*t) + np.sin(2*np.pi*f2*t)

    sample_times = np.arange(0,duration,1/fs)

    sample_values = (
        np.sin(2*np.pi*f1*sample_times) +
        np.sin(2*np.pi*f2*sample_times)
    )

    interp = np.interp(t,sample_times,sample_values)

    line_signal.set_ydata(signal)
    line_interp.set_ydata(interp)
    points.set_data(sample_times,sample_values)

    alias70 = alias_frequency(f2,fs)

    title.set_text(
        f"Sampling = {fs:.0f} Hz    "
        f"Nyquist = {fs/2:.1f} Hz\n"
        f"Original Frequencies: 10 Hz + 70 Hz    "
        f"Observed 70 Hz Component = {alias70:.1f} Hz"
    )

    fig.canvas.draw_idle()

slider_fs.on_changed(update)

update(None)

plt.show()