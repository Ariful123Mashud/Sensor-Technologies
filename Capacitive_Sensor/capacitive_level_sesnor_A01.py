"""
Capacitive level sensor - concentric cylindrical probe
BTEEZC419 - Introduction to Sensor Technologies
Reference: Bentley / Patranabis - capacitive sensing elements (dielectric-based level sensing)

    C(h) = (2*pi*eps0 / ln(b/a)) * [ eps_r_air*(L-h) + eps_r_liquid*h ]

where:
    a  = inner electrode radius
    b  = outer electrode radius
    L  = total immersed probe length
    h  = liquid level (height of liquid covering the probe)
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------
# Given data
# ---------------------------
eps0 = 8.854e-12          # permittivity of free space, F/m
eps_r_air = 1.0            # relative permittivity of air
eps_r_liquid = 2.5         # relative permittivity of transformer oil

a = 6e-3                   # inner electrode radius, m
b = 10e-3                  # outer electrode radius, m
L = 1.2                    # total probe length, m

C_measured = 145e-12       # measured capacitance, F (for part c)


def capacitance(h, a, b, L, eps_r_air, eps_r_liquid):
    """Total capacitance as a function of liquid level h (parallel combination)."""
    k = 2 * np.pi * eps0 / np.log(b / a)
    return k * (eps_r_air * (L - h) + eps_r_liquid * h)


# ---------------------------
# (a) Empty and full capacitance
# ---------------------------
C_empty = capacitance(0.0, a, b, L, eps_r_air, eps_r_liquid)
C_full = capacitance(L, a, b, L, eps_r_air, eps_r_liquid)

# ---------------------------
# (b) Calibration curve
# ---------------------------
h_range = np.linspace(0, L, 200)
C_range = capacitance(h_range, a, b, L, eps_r_air, eps_r_liquid)

# ---------------------------
# (c) Level from measured capacitance (invert the linear relationship)
#     C(h) = C_empty + (C_full - C_empty) * (h / L)   -> linear in h
# ---------------------------
h_solved = (C_measured - C_empty) / (C_full - C_empty) * L

# ---------------------------
# (d) Sensitivity (slope), pF per cm
# ---------------------------
sensitivity_pF_per_m = (C_full - C_empty) * 1e12 / L
sensitivity_pF_per_cm = sensitivity_pF_per_m / 100

# ---------------------------
# Results
# ---------------------------
print("=== Capacitive Level Sensor Calculation ===\n")
print(f"(a) C_empty (h=0)   = {C_empty*1e12:.3f} pF")
print(f"    C_full  (h=L)   = {C_full*1e12:.3f} pF\n")

print(f"(b) Calibration curve computed for h = 0 to {L} m "
      f"({len(h_range)} points) - see plot\n")

print(f"(c) Measured C = {C_measured*1e12:.1f} pF  ->  Level h = {h_solved:.4f} m "
      f"({h_solved*100:.2f} cm, {h_solved/L*100:.1f}% full)\n")

print(f"(d) Sensitivity = {sensitivity_pF_per_m:.4f} pF/m  = {sensitivity_pF_per_cm:.4f} pF/cm")

# ---------------------------
# Plot calibration curve
# ---------------------------
plt.figure(figsize=(7, 5))
plt.plot(h_range * 100, C_range * 1e12, color='tab:blue', linewidth=2, label='C(h) calibration curve')
plt.scatter([h_solved * 100], [C_measured * 1e12], color='red', zorder=5,
            label=f'Measured point: h={h_solved*100:.1f} cm, C={C_measured*1e12:.1f} pF')
plt.axhline(C_measured * 1e12, color='red', linestyle='--', linewidth=0.8, alpha=0.6)
plt.axvline(h_solved * 100, color='red', linestyle='--', linewidth=0.8, alpha=0.6)

plt.xlabel("Liquid level h (cm)")
plt.ylabel("Capacitance C (pF)")
plt.title("Capacitive Level Sensor - Calibration Curve\n"
          f"(a={a*1000:.0f} mm, b={b*1000:.0f} mm, L={L} m, oil eps_r={eps_r_liquid})")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()
