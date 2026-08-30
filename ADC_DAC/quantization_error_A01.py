import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# --------------------------------------------------------
# Signal Parameters
# --------------------------------------------------------
fs = 1000          # Sampling frequency
f = 5              # Signal frequency
duration = 1       # seconds

t = np.linspace(0, duration, fs, endpoint=False)

# Initial values
bits0 = 3
amp0 = 1.0

# ADC range
Vmin = -1
Vmax = 1

# --------------------------------------------------------
# Quantizer
# --------------------------------------------------------
def quantize(signal, bits):

    levels = 2**bits

    step = (Vmax - Vmin) / (levels - 1)

    q = np.round((signal - Vmin)/step)*step + Vmin

    q = np.clip(q, Vmin, Vmax)

    return q, step

# --------------------------------------------------------
# Initial Signal
# --------------------------------------------------------
analog = amp0*np.sin(2*np.pi*f*t)

quantized, step = quantize(analog, bits0)

error = analog - quantized

# --------------------------------------------------------
# Figure
# --------------------------------------------------------
fig = plt.figure(figsize=(14,9))

gs = fig.add_gridspec(2,1,height_ratios=[2,1])

ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

plt.subplots_adjust(bottom=0.25)

# --------------------------------------------------------
# Top Plot
# --------------------------------------------------------
line_analog, = ax1.plot(
    t,
    analog,
    linewidth=2,
    label="Original Analog Signal"
)

line_quant, = ax1.step(
    t,
    quantized,
    where='mid',
    linewidth=2,
    color='red',
    label="Quantized Signal"
)

samples = ax1.plot(
    t,
    quantized,
    'ko',
    markersize=3,
    label="Quantized Samples"
)[0]

ax1.set_xlim(0,1)
ax1.set_ylim(-1.2,1.2)
ax1.grid(True)
ax1.set_ylabel("Amplitude")
ax1.set_title("Signal Quantization")
ax1.legend()

# --------------------------------------------------------
# Error Plot
# --------------------------------------------------------
line_error, = ax2.plot(
    t,
    error,
    color='magenta',
    linewidth=2
)

ax2.set_xlim(0,1)
ax2.grid(True)
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Error")

# --------------------------------------------------------
# Text
# --------------------------------------------------------
text = ax1.text(
    0.02,
    0.95,
    "",
    transform=ax1.transAxes,
    fontsize=11,
    verticalalignment='top'
)

# --------------------------------------------------------
# Sliders
# --------------------------------------------------------
ax_bits = plt.axes([0.15,0.12,0.70,0.03])
ax_amp = plt.axes([0.15,0.06,0.70,0.03])

slider_bits = Slider(
    ax_bits,
    "ADC Bits",
    2,
    12,
    valinit=bits0,
    valstep=1
)

slider_amp = Slider(
    ax_amp,
    "Amplitude",
    0.2,
    1.0,
    valinit=amp0
)

# --------------------------------------------------------
# Update
# --------------------------------------------------------
def update(val):

    bits = int(slider_bits.val)
    amp = slider_amp.val

    analog = amp*np.sin(2*np.pi*f*t)

    quantized, step = quantize(analog,bits)

    error = analog - quantized

    line_analog.set_ydata(analog)
    line_quant.set_ydata(quantized)

    samples.set_data(t,quantized)

    line_error.set_ydata(error)

    text.set_text(
        f"ADC Resolution = {bits} bits\n"
        f"Levels = {2**bits}\n"
        f"Step Size = {step:.4f}\n"
        f"Maximum Quantization Error = ±{step/2:.4f}"
    )

    fig.canvas.draw_idle()

slider_bits.on_changed(update)
slider_amp.on_changed(update)

update(None)

plt.show()