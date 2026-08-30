import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# -------------------------------------------------
# Continuous Signal
# -------------------------------------------------
f_signal = 5          # Signal frequency (Hz)
duration = 1          # seconds

t = np.linspace(0, duration, 5000)
analog = np.sin(2*np.pi*f_signal*t)

# Initial values
fs0 = 20
bits0 = 3

# -------------------------------------------------
# Quantizer
# -------------------------------------------------
def quantize(x, bits):

    levels = 2**bits

    xmin = -1
    xmax = 1

    step = (xmax - xmin)/(levels-1)

    q = np.round((x-xmin)/step)*step + xmin

    q = np.clip(q,xmin,xmax)

    return q, step

# -------------------------------------------------
# Initial Sampled Signal
# -------------------------------------------------
sample_time = np.arange(0,duration,1/fs0)
sample_signal = np.sin(2*np.pi*f_signal*sample_time)

quantized, step = quantize(sample_signal,bits0)

# -------------------------------------------------
# Figure
# -------------------------------------------------
fig, axs = plt.subplots(3,1,figsize=(12,10))
plt.subplots_adjust(bottom=0.22,hspace=0.45)

# -------------------------------------------------
# Analog
# -------------------------------------------------
axs[0].plot(t,analog,'b',linewidth=2)

axs[0].set_title("Continuous Analog Signal")
axs[0].set_ylabel("Amplitude")
axs[0].grid(True)

# -------------------------------------------------
# Sampled
# -------------------------------------------------
axs[1].plot(t,analog,color='lightgray')

sample_plot = axs[1].stem(
    sample_time,
    sample_signal,
    linefmt='r-',
    markerfmt='ro',
    basefmt=' '
)

axs[1].set_title("Sampled Signal")
axs[1].set_ylabel("Amplitude")
axs[1].grid(True)

# -------------------------------------------------
# Quantized
# -------------------------------------------------
axs[2].plot(t,analog,color='lightgray')

quant_plot = axs[2].stem(
    sample_time,
    quantized,
    linefmt='g-',
    markerfmt='go',
    basefmt=' '
)

axs[2].step(
    sample_time,
    quantized,
    where='post',
    color='green',
    linewidth=2
)

axs[2].set_title("Quantized Samples")
axs[2].set_xlabel("Time (s)")
axs[2].set_ylabel("Amplitude")
axs[2].grid(True)

# -------------------------------------------------
# Text
# -------------------------------------------------
text = axs[2].text(
    0.02,
    0.92,
    "",
    transform=axs[2].transAxes,
    fontsize=11
)

# -------------------------------------------------
# Sliders
# -------------------------------------------------
ax_fs = plt.axes([0.18,0.10,0.65,0.03])
ax_bits = plt.axes([0.18,0.05,0.65,0.03])

slider_fs = Slider(
    ax_fs,
    "Sampling Frequency (Hz)",
    5,
    100,
    valinit=fs0,
    valstep=1
)

slider_bits = Slider(
    ax_bits,
    "ADC Bits",
    2,
    12,
    valinit=bits0,
    valstep=1
)

# -------------------------------------------------
# Update
# -------------------------------------------------
def update(val):

    fs = slider_fs.val
    bits = int(slider_bits.val)

    sample_time = np.arange(0,duration,1/fs)
    sample_signal = np.sin(2*np.pi*f_signal*sample_time)

    quantized, step = quantize(sample_signal,bits)

    # Remove old stem plots
    for artist in sample_plot.markerline, sample_plot.stemlines:
        try:
            artist.remove()
        except:
            pass

    for artist in quant_plot.markerline, quant_plot.stemlines:
        try:
            artist.remove()
        except:
            pass

    axs[1].cla()
    axs[2].cla()

    # Sampled plot
    axs[1].plot(t,analog,color='lightgray')
    axs[1].stem(sample_time,sample_signal,
                linefmt='r-',
                markerfmt='ro',
                basefmt=' ')
    axs[1].grid(True)
    axs[1].set_title("Sampled Signal")
    axs[1].set_ylabel("Amplitude")

    # Quantized plot
    axs[2].plot(t,analog,color='lightgray')
    axs[2].stem(sample_time,quantized,
                linefmt='g-',
                markerfmt='go',
                basefmt=' ')
    axs[2].step(sample_time,
                quantized,
                where='post',
                color='green',
                linewidth=2)

    axs[2].grid(True)
    axs[2].set_title("Quantized Samples")
    axs[2].set_xlabel("Time (s)")
    axs[2].set_ylabel("Amplitude")

    axs[2].text(
        0.02,
        0.92,
        f"Sampling Frequency = {fs:.0f} Hz\n"
        f"ADC Bits = {bits}\n"
        f"Levels = {2**bits}\n"
        f"Step Size = {step:.3f}",
        transform=axs[2].transAxes,
        fontsize=11
    )

    fig.canvas.draw_idle()

slider_fs.on_changed(update)
slider_bits.on_changed(update)

update(None)

plt.show()