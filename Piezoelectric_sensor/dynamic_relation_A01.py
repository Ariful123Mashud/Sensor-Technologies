"""
Second-order sensing element frequency response
Delta_x_tilde / Delta_F (s) = (1/k) / ( s^2/wn^2 + 2*xi*s/wn + 1 )

Parameters:
    k  = 1           (spring stiffness, normalized so 1/k = 1)
    wn = 80 rad/s    (natural frequency)
    xi = 0.1 to 1.5  (damping ratio, swept)

Reference: Bentley, Principles of Measurement Systems, Ch. 8
(elastic sensing elements / seismic-mass second-order dynamics)
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------
# Parameters
# ---------------------------
k = 1.0
wn = 80.0                              # rad/s
xi_values = np.arange(0.1, 1.6, 0.1)   # 0.1, 0.2, ..., 1.5

# Frequency range for the plot (rad/s), spanning well below and above wn
w = np.logspace(np.log10(wn / 50), np.log10(wn * 50), 2000)
freq_ratio = w / wn                    # normalized frequency, u = w/wn

# ---------------------------
# Compute magnitude and phase for each damping ratio
# ---------------------------
fig, (ax_mag, ax_phase) = plt.subplots(2, 1, figsize=(8, 9), sharex=True)

cmap = plt.cm.viridis(np.linspace(0, 1, len(xi_values)))

for xi, color in zip(xi_values, cmap):
    u = freq_ratio
    # H(jw) = (1/k) / [ (1 - u^2) + j*2*xi*u ]
    denom = (1 - u**2) + 1j * (2 * xi * u)
    H = (1 / k) / denom

    magnitude = np.abs(H)
    magnitude_dB = 20 * np.log10(magnitude / (1 / k))   # normalized to DC gain 1/k
    phase_deg = np.angle(H, deg=True)

    ax_mag.semilogx(u, magnitude_dB, color=color, label=f"xi = {xi:.1f}")
    ax_phase.semilogx(u, phase_deg, color=color, label=f"xi = {xi:.1f}")

# ---------------------------
# Formatting
# ---------------------------
ax_mag.axvline(1.0, color='gray', linestyle='--', linewidth=1)
ax_mag.set_ylabel("Normalized magnitude (dB)")
ax_mag.set_title(f"Second-order sensing element frequency response\n(k=1, wn={wn:.0f} rad/s, xi = 0.1 to 1.5)")
ax_mag.grid(True, which='both', alpha=0.3)

ax_phase.axvline(1.0, color='gray', linestyle='--', linewidth=1)
ax_phase.set_xlabel("Frequency ratio  w / wn")
ax_phase.set_ylabel("Phase (degrees)")
ax_phase.set_yticks([0, -45, -90, -135, -180])
ax_phase.grid(True, which='both', alpha=0.3)

# Single shared legend outside the plot
handles, labels = ax_mag.get_legend_handles_labels()
fig.legend(handles, labels, loc='center left', bbox_to_anchor=(1.0, 0.5),
           fontsize=8, title="Damping ratio")

plt.tight_layout()
fig.subplots_adjust(right=0.82)   # reserve ~18% of figure width for the legend
plt.show()