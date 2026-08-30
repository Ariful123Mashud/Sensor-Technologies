import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ============================================================
# DIGITAL WEIGHING SCALE SIMULATION
# ============================================================

# -----------------------------
# System parameters
# -----------------------------

MAX_WEIGHT = 100.0       # kg
LOAD_CELL_SENSITIVITY = 2.0   # mV/V
EXCITATION_VOLTAGE = 5.0      # V

# Load cell output at maximum weight:
# 2 mV/V × 5 V = 10 mV
LOAD_CELL_FULL_SCALE = (
    LOAD_CELL_SENSITIVITY * EXCITATION_VOLTAGE
) / 1000       # Volts

# Amplifier gain
AMPLIFIER_GAIN = 250

# ADC
ADC_BITS = 12
ADC_LEVELS = 2**ADC_BITS
ADC_MAX_CODE = ADC_LEVELS - 1
VREF = 3.3

# Amplifier output at maximum weight
AMPLIFIED_FULL_SCALE = (
    LOAD_CELL_FULL_SCALE * AMPLIFIER_GAIN
)


# ============================================================
# Functions
# ============================================================

def load_cell_voltage(weight):
    """
    Convert weight to load-cell output voltage.
    """

    return (
        weight / MAX_WEIGHT
    ) * LOAD_CELL_FULL_SCALE


def amplify_voltage(load_voltage):
    """
    Instrumentation amplifier.
    """

    return load_voltage * AMPLIFIER_GAIN


def adc_convert(voltage):
    """
    ADC quantization and encoding.
    """

    # Prevent ADC over-range
    voltage = np.clip(voltage, 0, VREF)

    # Convert voltage to ADC count
    code = round(
        voltage / VREF * ADC_MAX_CODE
    )

    # Convert decimal count to binary
    binary = format(
        code,
        f"0{ADC_BITS}b"
    )

    # Voltage represented by quantized code
    quantized_voltage = (
        code / ADC_MAX_CODE
    ) * VREF

    return code, binary, quantized_voltage


def calculate_weight(adc_code):
    """
    Microcontroller converts ADC code back into weight.
    """

    voltage = (
        adc_code / ADC_MAX_CODE
    ) * VREF

    amplified_voltage = voltage

    load_cell_voltage = (
        amplified_voltage / AMPLIFIER_GAIN
    )

    weight = (
        load_cell_voltage
        / LOAD_CELL_FULL_SCALE
        * MAX_WEIGHT
    )

    return weight


# ============================================================
# Initial weight
# ============================================================

initial_weight = 72.5

load_voltage = load_cell_voltage(initial_weight)

amplified_voltage = amplify_voltage(load_voltage)

adc_code, binary_code, quantized_voltage = adc_convert(
    amplified_voltage
)

calculated_weight = calculate_weight(adc_code)


# ============================================================
# Figure
# ============================================================

fig = plt.figure(figsize=(14, 10))

gs = fig.add_gridspec(
    4,
    2,
    height_ratios=[1.1, 1.1, 1.1, 1.4]
)

# ------------------------------------------------------------
# Axes
# ------------------------------------------------------------

ax_weight = fig.add_subplot(gs[0, :])
ax_loadcell = fig.add_subplot(gs[1, 0])
ax_amplifier = fig.add_subplot(gs[1, 1])
ax_adc = fig.add_subplot(gs[2, 0])
ax_binary = fig.add_subplot(gs[2, 1])
ax_display = fig.add_subplot(gs[3, :])

plt.subplots_adjust(
    bottom=0.15,
    hspace=0.7
)


# ============================================================
# 1. WEIGHT
# ============================================================

ax_weight.set_xlim(0, MAX_WEIGHT)
ax_weight.set_ylim(0, 1)

weight_bar = ax_weight.barh(
    0.5,
    initial_weight,
    height=0.35
)

ax_weight.set_title(
    "1. Physical Quantity — Weight",
    fontsize=14,
    fontweight="bold"
)

ax_weight.set_xlabel("Weight (kg)")
ax_weight.set_yticks([])

weight_text = ax_weight.text(
    initial_weight,
    0.5,
    f"  {initial_weight:.1f} kg",
    va="center",
    fontsize=12
)


# ============================================================
# 2. LOAD CELL
# ============================================================

ax_loadcell.set_xlim(0, LOAD_CELL_FULL_SCALE * 1000 * 1.1)
ax_loadcell.set_ylim(0, 1)

load_bar = ax_loadcell.barh(
    0.5,
    load_voltage * 1000,
    height=0.35
)

ax_loadcell.set_title(
    "2. Load Cell Output",
    fontsize=13,
    fontweight="bold"
)

ax_loadcell.set_xlabel("Output Voltage (mV)")
ax_loadcell.set_yticks([])

load_text = ax_loadcell.text(
    load_voltage * 1000,
    0.5,
    f"  {load_voltage*1000:.3f} mV",
    va="center"
)


# ============================================================
# 3. AMPLIFIER
# ============================================================

ax_amplifier.set_xlim(
    0,
    VREF * 1.05
)

ax_amplifier.set_ylim(0, 1)

amp_bar = ax_amplifier.barh(
    0.5,
    amplified_voltage,
    height=0.35
)

ax_amplifier.axvline(
    VREF,
    linestyle="--",
    linewidth=2
)

ax_amplifier.text(
    VREF,
    0.8,
    "ADC Vref",
    ha="right"
)

ax_amplifier.set_title(
    "3. Instrumentation Amplifier",
    fontsize=13,
    fontweight="bold"
)

ax_amplifier.set_xlabel("Amplified Voltage (V)")
ax_amplifier.set_yticks([])

amp_text = ax_amplifier.text(
    amplified_voltage,
    0.5,
    f"  {amplified_voltage:.3f} V",
    va="center"
)


# ============================================================
# 4. ADC
# ============================================================

ax_adc.set_xlim(0, VREF)
ax_adc.set_ylim(0, 1)

adc_bar = ax_adc.barh(
    0.5,
    quantized_voltage,
    height=0.35
)

ax_adc.axvline(
    VREF,
    linestyle="--",
    linewidth=2
)

ax_adc.set_title(
    f"4. ADC — {ADC_BITS}-bit",
    fontsize=13,
    fontweight="bold"
)

ax_adc.set_xlabel("ADC Input Voltage (V)")
ax_adc.set_yticks([])

adc_text = ax_adc.text(
    quantized_voltage,
    0.5,
    f"  Code = {adc_code}",
    va="center"
)


# ============================================================
# 5. BINARY ENCODING
# ============================================================

ax_binary.axis("off")

ax_binary.set_title(
    "5. Binary Encoding",
    fontsize=13,
    fontweight="bold"
)

binary_text = ax_binary.text(
    0.5,
    0.55,
    binary_code,
    ha="center",
    va="center",
    fontsize=28,
    fontweight="bold",
    family="monospace"
)

binary_decimal_text = ax_binary.text(
    0.5,
    0.25,
    f"Decimal ADC Count = {adc_code}",
    ha="center",
    fontsize=12
)


# ============================================================
# 6. MICROCONTROLLER + DISPLAY
# ============================================================

ax_display.axis("off")

ax_display.set_title(
    "6. Microcontroller → Weight Calculation → Display",
    fontsize=14,
    fontweight="bold"
)

# Pipeline
ax_display.text(
    0.05,
    0.55,
    "ADC\n"
    f"{binary_code}",
    ha="center",
    va="center",
    fontsize=12,
    bbox=dict(boxstyle="round,pad=0.5")
)

ax_display.text(
    0.25,
    0.55,
    "→",
    fontsize=25,
    ha="center"
)

ax_display.text(
    0.40,
    0.55,
    "Microcontroller\n"
    f"ADC Count = {adc_code}",
    ha="center",
    va="center",
    fontsize=12,
    bbox=dict(boxstyle="round,pad=0.5")
)

ax_display.text(
    0.60,
    0.55,
    "→",
    fontsize=25,
    ha="center"
)

ax_display.text(
    0.75,
    0.55,
    "Weight Calculation",
    ha="center",
    va="center",
    fontsize=12,
    bbox=dict(boxstyle="round,pad=0.5")
)

ax_display.text(
    0.92,
    0.55,
    f"{calculated_weight:.2f} kg",
    ha="center",
    va="center",
    fontsize=20,
    fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.6")
)

display_texts = ax_display.texts


# ============================================================
# Slider
# ============================================================

ax_slider = plt.axes(
    [0.20, 0.055, 0.60, 0.035]
)

weight_slider = Slider(
    ax_slider,
    "Weight (kg)",
    0,
    MAX_WEIGHT,
    valinit=initial_weight,
    valstep=0.1
)


# ============================================================
# Update function
# ============================================================

def update(val):

    weight = weight_slider.val

    # -------------------------
    # Load cell
    # -------------------------

    load_voltage = load_cell_voltage(weight)

    # -------------------------
    # Amplifier
    # -------------------------

    amplified_voltage = amplify_voltage(
        load_voltage
    )

    # -------------------------
    # ADC
    # -------------------------

    adc_code, binary_code, quantized_voltage = adc_convert(
        amplified_voltage
    )

    # -------------------------
    # Microcontroller
    # -------------------------

    calculated_weight = calculate_weight(
        adc_code
    )

    # ========================================================
    # Update weight
    # ========================================================

    weight_bar[0].set_width(weight)

    weight_text.set_position(
        (weight, 0.5)
    )

    weight_text.set_text(
        f"  {weight:.1f} kg"
    )

    # ========================================================
    # Load cell
    # ========================================================

    load_bar[0].set_width(
        load_voltage * 1000
    )

    load_text.set_position(
        (load_voltage * 1000, 0.5)
    )

    load_text.set_text(
        f"  {load_voltage*1000:.3f} mV"
    )

    # ========================================================
    # Amplifier
    # ========================================================

    amp_bar[0].set_width(
        amplified_voltage
    )

    amp_text.set_position(
        (amplified_voltage, 0.5)
    )

    amp_text.set_text(
        f"  {amplified_voltage:.3f} V"
    )

    # ========================================================
    # ADC
    # ========================================================

    adc_bar[0].set_width(
        quantized_voltage
    )

    adc_text.set_position(
        (quantized_voltage, 0.5)
    )

    adc_text.set_text(
        f"  Code = {adc_code}"
    )

    # ========================================================
    # Binary
    # ========================================================

    binary_text.set_text(
        binary_code
    )

    binary_decimal_text.set_text(
        f"Decimal ADC Count = {adc_code}"
    )

    # ========================================================
    # Display
    # ========================================================

    # Remove old display text
    for text in display_texts:
        text.remove()

    # Recreate display
    display_texts.clear()

    ax_display.text(
        0.05,
        0.55,
        "ADC\n"
        f"{binary_code}",
        ha="center",
        va="center",
        fontsize=12,
        bbox=dict(boxstyle="round,pad=0.5")
    )

    ax_display.text(
        0.25,
        0.55,
        "→",
        fontsize=25,
        ha="center"
    )

    ax_display.text(
        0.40,
        0.55,
        "Microcontroller\n"
        f"ADC Count = {adc_code}",
        ha="center",
        va="center",
        fontsize=12,
        bbox=dict(boxstyle="round,pad=0.5")
    )

    ax_display.text(
        0.60,
        0.55,
        "→",
        fontsize=25,
        ha="center"
    )

    ax_display.text(
        0.75,
        0.55,
        "Weight Calculation",
        ha="center",
        va="center",
        fontsize=12,
        bbox=dict(boxstyle="round,pad=0.5")
    )

    ax_display.text(
        0.92,
        0.55,
        f"{calculated_weight:.2f} kg",
        ha="center",
        va="center",
        fontsize=20,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.6")
    )

    fig.canvas.draw_idle()


# ============================================================
# Connect slider
# ============================================================

weight_slider.on_changed(update)

plt.show()