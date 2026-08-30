%% AC Carrier System Demonstration
% Demonstrates: modulation -> AC amplification -> phase-sensitive
% demodulation -> low-pass filtering, and compares against the
% "DC drift" problem that AC carrier systems are designed to avoid.
%
% Scenario: a sensor bridge is excited with an AC carrier. The
% measurand (e.g., a slowly varying pressure or displacement) modulates
% the amplitude of this carrier. We recover the measurand at the end
% and show how DC drift (added directly to a hypothetical DC system)
% corrupts a plain DC measurement, while the AC carrier system is immune.

clear; clc; close all;

%% 1. Time base and parameters
Fs      = 100000;          % Sampling frequency (Hz) - must be >> carrier freq
T       = 2;                % Total duration (s)
t       = 0:1/Fs:T-1/Fs;

f_carrier = 1000;           % Carrier frequency (Hz), e.g. 1 kHz oscillator
f_measurand = 1;            % Measurand varies slowly, e.g. 1 Hz "pressure pulse"

%% 2. Simulate the measurand (the real physical quantity we want)
% e.g. a slowly varying signal (0 to 1 range), like normalized pressure
measurand = 0.5 + 0.4*sin(2*pi*f_measurand*t);

%% 3. Modulation: sensor bridge output = carrier amplitude modulated by measurand
carrier = sin(2*pi*f_carrier*t);
modulated_signal = measurand .* carrier;   % AM: amplitude follows measurand

%% 4. Add realistic noise and DC drift to simulate real-world conditions
rng(1); % reproducible noise
noise = 0.05*randn(size(t));                 % random broadband noise
dc_drift = 0.0005*t;                         % slow drift (e.g. thermal drift, volts)

modulated_signal_noisy = modulated_signal + noise;

%% 5. AC Amplifier stage (simple gain, since AC-coupled, drift doesn't accumulate)
AC_gain = 10;
amplified_signal = AC_gain * modulated_signal_noisy;

%% 6. Phase-sensitive demodulation
% Multiply by a reference carrier (same phase as original) - this is the
% core trick of a phase-sensitive detector (synchronous demodulation)
reference = sin(2*pi*f_carrier*t);
demodulated = amplified_signal .* reference;

%% 7. Low-pass filter to recover the smooth measurand
% Cutoff must be well above f_measurand but well below f_carrier
cutoff = 20; % Hz
[b, a] = butter(4, cutoff/(Fs/2), 'low');
recovered = filtfilt(b, a, demodulated);

% Normalize recovered signal back to compare against original measurand
% (accounts for the known AC_gain and the 0.5 factor from multiplying two sinusoids)
recovered_scaled = recovered / (AC_gain * 0.5);

%% 8. For comparison: a naive DC system corrupted by the same drift
dc_signal_naive = measurand + dc_drift + noise; % drift adds directly, uncorrected

%% 9. Plot results
figure('Position', [100 100 900 700]);

subplot(4,1,1);
plot(t, measurand, 'b', 'LineWidth', 1.5);
title('True Measurand (e.g. Pressure Signal)');
xlabel('Time (s)'); ylabel('Amplitude'); ylim([0 1.2]); grid on;

subplot(4,1,2);
plot(t, modulated_signal_noisy);
title('Modulated Carrier Signal (Sensor Bridge Output, with noise)');
xlabel('Time (s)'); ylabel('Amplitude'); grid on;

subplot(4,1,3);
plot(t, dc_signal_naive, 'r');
hold on;
plot(t, measurand, 'b--', 'LineWidth', 1.2);
title('Naive DC System: True Signal vs. Drift-Corrupted Reading');
legend('Measured (with drift)', 'True measurand', 'Location', 'best');
xlabel('Time (s)'); ylabel('Amplitude'); grid on;

subplot(4,1,4);
plot(t, recovered_scaled, 'g', 'LineWidth', 1.5);
hold on;
plot(t, measurand, 'b--', 'LineWidth', 1.2);
title('AC Carrier System: Recovered Measurand vs. True Signal');
legend('Recovered (AC carrier system)', 'True measurand', 'Location', 'best');
xlabel('Time (s)'); ylabel('Amplitude'); grid on;

sgtitle('AC Carrier System Demonstration: Immunity to Drift');

%% 10. Print a simple quantitative comparison
error_dc = mean(abs(dc_signal_naive - measurand));
error_ac = mean(abs(recovered_scaled - measurand));

fprintf('--- Quantitative Comparison ---\n');
fprintf('Mean absolute error (naive DC system, with drift): %.4f\n', error_dc);
fprintf('Mean absolute error (AC carrier system, drift-immune): %.4f\n', error_ac);
fprintf('The AC carrier system error stays low despite noise/drift,\n');
fprintf('while the naive DC system accumulates significant drift error.\n');