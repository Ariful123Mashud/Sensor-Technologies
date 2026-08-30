"""
Bode plot for a piezoelectric transducer + charge/voltage amplifier stage:

    dVL/dF (s) = [ d / (C_N + C_C) ] * [ tau*s / (1 + tau*s) ] * [ 1 / (s^2/wn^2 + 2*xi*s/wn + 1) ]

where:
    d           = piezoelectric charge sensitivity (C/N or similar)
    C_N, C_C    = transducer capacitance, cable capacitance (F)
    tau         = R_L * (C_N + C_C)   -> electrical time constant (s)
    wn          = mechanical natural frequency (rad/s)
    xi          = mechanical damping ratio

Structure: high-pass (1st order, from RC loading) x low-pass (2nd order,
mechanical resonance) -> classic bandpass shape of a piezo sensor's usable range.

*** EDIT THE PARAMETERS BELOW WITH YOUR EXACT VALUES ***
"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# >>> EDIT THESE PARAMETERS <<<
# ============================================================
C_N = 1600e-9         # transducer capacitance, F            (EDIT)
C_C = 600e-9         # cable capacitance, F                 (EDIT)
R_L = 1.0e6          # load resistance, ohms                (EDIT)
fn = 27e3

wn = np.pi *fn            # mechanical natural frequency, rad/s  (EDIT)
xi = 0.01             # mechanical damping ratio             (EDIT)

d = 1         # piezoelectric sensitivity, e.g. C/N  (EDIT)

# ============================================================
# Derived parameters
# ============================================================
sensitivity =1      # static gain term, V/N (units depend on d)
tau = R_L * (C_N + C_C)            # electrical time constant, s

print(f"Sensitivity term d/(C_N+C_C) = {sensitivity:.4e}")
print(f"Electrical time constant tau = {tau:.4e} s  (1/tau = {1/tau:.4e} rad/s)")
print(f"Mechanical wn = {wn:.2f} rad/s, xi = {xi:.2f}")

# ============================================================
# Frequency sweep (rad/s) - wide enough to show both corner
# frequencies: 1/tau (high-pass corner) and wn (resonance)
# ============================================================
w_lo = min(1/tau, wn) / 100
w_hi = max(1/tau, wn) * 100
w = np.logspace(np.log10(w_lo), np.log10(w_hi), 3000)

# ============================================================
# Transfer function H(jw) = sensitivity * H_highpass(jw) * H_lowpass2(jw)
# ============================================================
s = 1j * w
 
H_highpass = (tau * s) / (1 + tau * s)
H_lowpass2 = 1.0 / ((s**2) / wn**2 + (2 * xi * s) / wn + 1)
 
H = sensitivity * H_highpass * H_lowpass2
 
magnitude_dB = 20 * np.log10(np.abs(H))
phase_deg = np.angle(H, deg=True)
 
# H_lowpass2 alone (mechanical second-order stage only, no sensitivity
# scaling and no electrical high-pass term) -> for direct comparison
magnitude_dB_lp2 = 20 * np.log10(np.abs(H_lowpass2))
phase_deg_lp2 = np.angle(H_lowpass2, deg=True)
 
# ============================================================
# Plot - full transfer function vs. mechanical (2nd-order) stage alone
# ============================================================
fig, (ax_mag, ax_phase) = plt.subplots(2, 1, figsize=(8, 8), sharex=True)
 
ax_mag.semilogx(w, magnitude_dB, color='tab:blue', linewidth=1.8,
                 label=r'Without amplifier: $\Delta V_L/\Delta F(s)$')
ax_mag.semilogx(w, magnitude_dB_lp2, color='tab:orange', linewidth=1.8,
                 linestyle='-.', label=r'Without amplifier: $\Delta V_L/\Delta F(s)$')
# ax_mag.axvline(1/tau, color='gray', linestyle='--', linewidth=1, label=f'1/tau = {1/tau:.2f} rad/s')
ax_mag.axvline(wn, color='red', linestyle='--', linewidth=1, label=f'wn = {wn:.2f} rad/s')
ax_mag.set_ylabel("Magnitude (dB)")
ax_mag.set_title("Piezoelectric sesnsor measurement system - Bode plot\n"
                  )
ax_mag.grid(True, which='both', alpha=0.3)
ax_mag.legend(fontsize=8)
 
ax_phase.semilogx(w, phase_deg, color='tab:blue', linewidth=1.8, label='')
ax_phase.semilogx(w, phase_deg_lp2, color='tab:orange', linewidth=1.8,
                   linestyle='-.', label='')
ax_phase.axvline(1/tau, color='gray', linestyle='--', linewidth=1)
ax_phase.axvline(wn, color='red', linestyle='--', linewidth=1)
ax_phase.set_xlabel("Frequency w (rad/s)")
ax_phase.set_ylabel("Phase (degrees)")
ax_phase.grid(True, which='both', alpha=0.3)
ax_phase.legend(fontsize=8)
 
plt.tight_layout()

plt.show()
 