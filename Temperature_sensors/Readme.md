# Sensor-Technologies
# Sensor Technologies — Course Code & Demos (BTEEZC419)

Simulation code, demos, and teaching material developed for **BTEEZC419: Introduction to Sensor Technologies**, part of the BITS Pilani WILP postgraduate program.

This repository collects Python-based simulations and interactive demos used to illustrate core sensor concepts — from static/dynamic sensor characteristics to signal conditioning and sensor-failure scenarios in autonomous driving contexts.

---

## 📖 Course Context

| | |
|---|---|
| **Course** | BTEEZC419 – Introduction to Sensor Technologies |
| **Program** | BITS Pilani, Work-Integrated Learning Programme (WILP) |
| **Format** | Online, 14-session schedule |
| **Instructor** | Ariful Islam, Assistant Professor, EEE |

---

## 📂 Repository Structure

```
.
├── wheatstone_bridge/
│   └── wheatstone_bridge_sim.py     # Wheatstone bridge with noise injection + low-pass filtering
├── sensor_fundamentals/
│   ├── static_dynamic_characteristics.py
│   └── hall_effect_sensor.py
├── signal_conditioning/
│   ├── transfer_function_time_constants.py
│   └── bode_plot_demo.py
├── control_demos/
│   └── lqr_state_space.py
├── av_sensor_demo/
│   └── sensor_failure_demo_2min.py  # CARLA live demo: catastrophic sensor failure in AVs
├── slides/
│   └── BTEEZC419_lecture_slides.pptx
├── requirements.txt
└── README.md
```

> Update the tree above to match your actual folder/file names before publishing.

---

## 🧪 Topics Covered

- **Sensor fundamentals** — static vs. dynamic characteristics, sensitivity, accuracy, resolution
- **Wheatstone bridge circuits** — balance conditions, noise injection, low-pass filtering for signal recovery
- **Hall effect sensors** — working principle and simulation
- **Signal conditioning** — transfer functions, time constants, amplification, filtering
- **Frequency-domain analysis** — Bode plots for sensor response characterization
- **State-space control** — LQR-based control relevant to sensor-in-the-loop systems
- **Sensor fusion & failure modes** — live CARLA simulation demonstrating sensor failure effects in autonomous vehicles

---

## ⚙️ Requirements

```bash
pip install numpy scipy matplotlib control
```

For the CARLA-based AV sensor demo, see [`av_sensor_demo/README.md`](av_sensor_demo/README.md) for CARLA setup and WSL2/Windows networking notes.

---

## 🚀 Usage

Each script is standalone and runnable directly:

```bash
python wheatstone_bridge/wheatstone_bridge_sim.py
```

Most simulations generate `matplotlib` plots illustrating the relevant sensor behavior (e.g., bridge output vs. noise level, filtered vs. unfiltered signal, Bode magnitude/phase response).

---

## 🎓 Intended Audience

These materials are designed for postgraduate WILP students studying sensor technologies, and are aligned session-by-session with the official BITS WILP BTEEZC419 course schedule.

---

## 📄 License

Educational use — © Ariful
---

## 📬 Contact

For questions related to this material, reach out via the course forum or institutional email.
