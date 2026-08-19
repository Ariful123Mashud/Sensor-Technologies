import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# -------------------------------------
# Signal parameters
# -------------------------------------
duration = 1.0
switch_time = 0.5

t = np.linspace(0, duration, 5000)

# Initial sampling frequency
fs0 = 80


# -------------------------------------
# Generate signal
# -------------------------------------
def generate_signal(t):

    x = np.zeros_like(t)

    idx1 = t < switch_time
    idx2 = t >= switch_time

    # First half : 10 Hz
    x[idx1] = np.sin(2 * np.pi * 10 * t[idx1])

    # Second half : 70 Hz
    x[idx2] = np.sin(2 * np.pi * 70 * t[idx2])

    return x


def alias_frequency(f, fs):
    return abs(((f + fs / 2) % fs) - fs / 2)


signal = generate_signal(t)
##################
# -------------------------------------
# FFT of Original Signal
# -------------------------------------
dt = t[1] - t[0]

fft_original = np.fft.rfft(signal)
freq_original = np.fft.rfftfreq(len(signal), dt)
##################
sample_times = np.arange(0, duration, 1 / fs0)
sample_values = generate_signal(sample_times)

interp = np.interp(t, sample_times, sample_values)

# -------------------------------------
# Plot
# -------------------------------------
# fig, ax = plt.subplots(figsize=(14,6))
# plt.subplots_adjust(bottom=0.25)
####
fig = plt.figure(figsize=(15, 9))

gs = fig.add_gridspec(2, 2, height_ratios=[2, 1])

ax = fig.add_subplot(gs[0, :])
ax_fft_original = fig.add_subplot(gs[1, 0])
ax_fft_sampled = fig.add_subplot(gs[1, 1])

# -------------------------------------
# FFT of Original Signal
# -------------------------------------
(line_fft_original,) = ax_fft_original.plot(
    freq_original,
    2 * np.abs(fft_original) / len(signal),
    color='blue',
    lw=2,
    label='Original FFT'
)

# Mark the two frequencies
ax_fft_original.axvline(
    10,
    color='green',
    linestyle='--',
    linewidth=2,
    label='10 Hz'
)

ax_fft_original.axvline(
    70,
    color='red',
    linestyle='--',
    linewidth=2,
    label='70 Hz'
)

ax_fft_original.set_xlim(0, 100)
ax_fft_original.set_xlabel("Frequency (Hz)")
ax_fft_original.set_ylabel("Magnitude")
ax_fft_original.set_title("FFT of Original Signal")
ax_fft_original.grid(True)
ax_fft_original.legend()

fft_sampled = np.fft.rfft(sample_values)
freq_sampled = np.fft.rfftfreq(len(sample_values), 1 / fs0)

(line_fft_sampled,) = ax_fft_sampled.plot(freq_sampled, np.abs(fft_sampled), lw=2)

ax_fft_sampled.set_xlim(0, 100)
ax_fft_sampled.set_title("FFT of Sampled Signal")
ax_fft_sampled.set_xlabel("Frequency (Hz)")
ax_fft_sampled.set_ylabel("Magnitude")
ax_fft_sampled.grid(True)

plt.subplots_adjust(bottom=0.20, hspace=0.4)




#####
(line_signal,) = ax.plot(t, signal, linewidth=2, label="Original Signal")

(line_interp,) = ax.plot(t, interp, "g--", linewidth=2, label="Interpolated Signal")

points = ax.plot(sample_times, sample_values, "ro", markersize=5, label="Samples")[0]

ax.axvline(
    switch_time, color="black", linestyle="--", linewidth=2, label="Frequency Change"
)

title = ax.set_title("")
ax.set_xlabel("Time (seconds)")
ax.set_ylabel("Amplitude")
ax.set_ylim(-1.5, 1.5)
ax.grid(True)
ax.legend()

# -------------------------------------
# Slider
# -------------------------------------
ax_slider = plt.axes([0.15, 0.08, 0.7, 0.03])

slider = Slider(ax_slider, "Sampling Frequency (Hz)", 20, 200, valinit=fs0, valstep=1)


# -------------------------------------
# Update
# -------------------------------------
def update(val):

    fs = slider.val

    sample_times = np.arange(0, duration, 1 / fs)
    sample_values = generate_signal(sample_times)

    interp = np.interp(t, sample_times, sample_values)
    fft_sampled = np.fft.rfft(sample_values)
    freq_sampled = np.fft.rfftfreq(len(sample_values),1/fs)

    line_fft_sampled.set_data(
        freq_sampled,
        np.abs(fft_sampled)
    )

    ax_fft_sampled.set_xlim(0,max(100,fs/2+10))

    ax_fft_sampled.relim()
    ax_fft_sampled.autoscale_view(scaley=True)


    
    line_interp.set_ydata(interp)
    points.set_data(sample_times, sample_values)

    alias70 = alias_frequency(70, fs)

    title.set_text(
        f"Sampling = {fs:.0f} Hz   "
        f"Nyquist = {fs / 2:.1f} Hz\n"
        f"First Half = 10 Hz (always correct)\n"
        f"Second Half = 70 Hz → Appears as {alias70:.1f} Hz"
    )

    fig.canvas.draw_idle()


slider.on_changed(update)

update(None)

plt.show()
