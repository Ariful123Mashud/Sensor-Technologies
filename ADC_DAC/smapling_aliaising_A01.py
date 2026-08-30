import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# -------------------------
# Initial values
# -------------------------
f_signal_init = 15      # Hz
f_sample_init = 40      # Hz
duration = 1            # seconds

# Continuous signal
t = np.linspace(0, duration, 5000)

fig, ax = plt.subplots(figsize=(12,6))
plt.subplots_adjust(bottom=0.28)

# -------------------------------------------------------
# Initial plots
# -------------------------------------------------------
signal = np.sin(2*np.pi*f_signal_init*t)

sample_times = np.arange(0, duration, 1/f_sample_init)
sample_values = np.sin(2*np.pi*f_signal_init*sample_times)

interp = np.interp(t, sample_times, sample_values)

line_signal, = ax.plot(t, signal,
                       linewidth=2,
                       label="Original Signal")

line_interp, = ax.plot(t, interp,
                       '--',
                       linewidth=2,
                       label="Reconstructed from Samples")

points = ax.plot(sample_times,
                 sample_values,
                 'ro',
                 markersize=6,
                 label="Samples")[0]

title = ax.set_title("")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.grid(True)
ax.legend(loc="upper right")
ax.set_ylim(-1.5,1.5)

# -------------------------------------------------------
# Sliders
# -------------------------------------------------------
ax_freq = plt.axes([0.15,0.12,0.70,0.03])
ax_sample = plt.axes([0.15,0.06,0.70,0.03])

slider_freq = Slider(ax_freq,
                     'Signal Frequency (Hz)',
                     1,
                     60,
                     valinit=f_signal_init,
                     valstep=1)

slider_sample = Slider(ax_sample,
                       'Sampling Frequency (Hz)',
                       5,
                       120,
                       valinit=f_sample_init,
                       valstep=1)

# -------------------------------------------------------
# Alias frequency calculation
# -------------------------------------------------------
def alias_frequency(f, fs):
    """
    Returns frequency observed after sampling.
    """
    if fs <= 0:
        return 0

    f_alias = abs(((f + fs/2) % fs) - fs/2)
    return f_alias

# -------------------------------------------------------
# Update function
# -------------------------------------------------------
def update(val):

    f_signal = slider_freq.val
    fs = slider_sample.val

    signal = np.sin(2*np.pi*f_signal*t)

    sample_times = np.arange(0,duration,1/fs)
    sample_values = np.sin(2*np.pi*f_signal*sample_times)

    interp = np.interp(t,sample_times,sample_values)

    line_signal.set_ydata(signal)
    line_interp.set_ydata(interp)

    points.set_data(sample_times,sample_values)

    nyquist = fs/2
    alias = alias_frequency(f_signal,fs)

    if f_signal <= nyquist:
        status = "No Aliasing"
    else:
        status = "Aliasing!"

    title.set_text(
        f"Signal = {f_signal:.1f} Hz    "
        f"Sampling = {fs:.1f} Hz    "
        f"Nyquist = {nyquist:.1f} Hz    "
        f"Observed Frequency = {alias:.2f} Hz    "
        f"{status}"
    )

    fig.canvas.draw_idle()

slider_freq.on_changed(update)
slider_sample.on_changed(update)

update(None)

plt.show()