"""
Question
A cantilever bending-beam load cell is used in an industrial platform scale. It has four 
identical strain gauges (gauge factor GF = 2.0, unstrained resistance R = 350 Ω) arranged 
in a four-arm Wheatstone bridge: two gauges (G1, G2) mounted on the tension face and two (G3, G4) 
on the compression face, as shown in the diagram.
The bridge is excited with 
𝑉𝑒𝑥 = 10 V DC.
Under a test load, gauges G1 and G2 experience a tensile strain of +800 microstrain (μμ), 
while G3 and G4 experience an equal and opposite compressive strain of −800 μμ.

The scale is rated for a maximum capacity of 500 kg, at which the manufacturer specifies 
a full-scale bridge output of 2 mV/V.

Find:
(a) The resistance change ΔR in each gauge
(b) The bridge output voltage V_out for the given strain
(c) The equivalent load (in kg) that produced this output, assuming linear response up
 to the rated capacity
(d) The output voltage after a downstream instrumentation amplifier with gain = 250
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

img_path = "/home/arif/D_drive/BITS_Pilani/Control and Senor Technology/Sensor_Technologies/Contact_Sessions/Simulations/Pressure_sensor/q1.png"

img = cv2.imread(img_path)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img_rgb)
plt.axis('off')

# ---------------------------
# Given data
# ---------------------------
GF = 2.0            # Gauge factor (dimensionless)
R = 350.0            # Unstrained gauge resistance, ohms
V_ex = 10.0          # Bridge excitation voltage, V
strain = 800e-6      # Applied strain magnitude (microstrain), +ve on G1/G2, -ve on G3/G4

rated_capacity_kg = 500.0   # Full-scale rated load, kg
fs_output_mV_per_V = 2.0    # Manufacturer full-scale sensitivity spec, mV/V

amp_gain = 250       # Instrumentation amplifier gain (downstream of bridge)


def resistance_change(R, GF, strain):
    """ΔR = GF * strain * R   (basic strain gauge equation, Bentley eq. 8.2)"""
    return GF * strain * R


def bridge_output_four_arm(V_ex, GF, strain):
    """
    Four-arm bridge with two gauges in tension (+strain) and two in
    compression (-strain), placed in opposite arms.
    This configuration gives full bridge sensitivity (4x a single gauge):
        V_out = GF * strain * V_ex
    (the individual +/-1 factors of each arm add constructively)
    """
    return GF * strain * V_ex


def load_from_output(V_out, V_ex, rated_capacity_kg, fs_output_mV_per_V):
    """
    Linear interpolation against the manufacturer's full-scale spec.
    fs_output_mV_per_V is defined at rated_capacity_kg.
    """
    fs_output_V = (fs_output_mV_per_V / 1000.0) * V_ex   # convert mV/V spec to volts at V_ex
    load_kg = (V_out / fs_output_V) * rated_capacity_kg
    return load_kg, fs_output_V


# ---------------------------
# (a) Resistance change per gauge
# ---------------------------
dR_tension = resistance_change(R, GF, strain)       # G1, G2
dR_compression = resistance_change(R, GF, -strain)  # G3, G4

# ---------------------------
# (b) Bridge output voltage
# ---------------------------
V_out = bridge_output_four_arm(V_ex, GF, strain)

# ---------------------------
# (c) Equivalent load
# ---------------------------
load_kg, V_fullscale = load_from_output(V_out, V_ex, rated_capacity_kg, fs_output_mV_per_V)

# ---------------------------
# (d) Amplified output
# ---------------------------
V_out_amplified = V_out * amp_gain


# ---------------------------
# Results
# ---------------------------
print("=== Strain Gauge Load Cell - Four-Arm Bridge Calculation ===\n")

print(f"(a) Resistance change per gauge:")
print(f"    G1, G2 (tension)     : dR = {dR_tension*1000:.3f} mOhm  (R = {R + dR_tension:.4f} Ohm)")
print(f"    G3, G4 (compression) : dR = {dR_compression*1000:.3f} mOhm  (R = {R + dR_compression:.4f} Ohm)\n")

print(f"(b) Bridge output voltage:")
print(f"    V_out = {V_out*1000:.3f} mV  (={V_out/V_ex*1000:.3f} mV/V)\n")

print(f"(c) Equivalent load:")
print(f"    Full-scale output at rated capacity ({rated_capacity_kg:.0f} kg) = {V_fullscale*1000:.3f} mV")
print(f"    Estimated load = {load_kg:.2f} kg\n")

print(f"(d) After instrumentation amplifier (gain = {amp_gain}):")
print(f"    V_out_amplified = {V_out_amplified:.3f} V")