# IoT Sensor Data Integrity Monitor

A beginner-friendly Python tool that demonstrates how simple iteration and conditional logic can detect anomalies in sensor data for cyber-physical systems (IoT).
This project is designed to be readable, configurable, and directly useful for demos, firmware audits, or teaching sessions about data integrity and security in embedded systems.

---

## What this project is / why it exists

Sensor readings are the inputs that drive decisions in IoT devices, industrial controllers, and smart systems. A single corrupted, spoofed, or faulty reading can cause incorrect actions, downtime, or safety hazards.

This monitor is a compact proof-of-concept that:

* Shows how to **detect suspicious readings** using only Python basics (iteration, conditionals, I/O).
* Produces a human-readable anomaly log and can save a UTF-8 report file for later analysis.
* Teaches the core ideas behind anomaly detection used in production monitoring and intrusion detection systems for cyber-physical devices.

> Built intentionally simple so it’s easy to explain, extend, and include in a portfolio or technical demo.

---

## Features

* Load sensor readings from a plain text file (`sensor_data.txt`) or use built-in sample data.
* Two complementary anomaly checks:

  * **Sudden jump detection** — flags big absolute changes between consecutive readings.
  * **Moving-average deviation** — flags readings that deviate significantly from recent history.
* Configurable thresholds (jump threshold, moving average window, percent deviation).
* Prints a detailed anomaly log and a final summary in the terminal.
* Optionally saves a UTF-8 encoded report file (so emoji/Unicode characters are supported).
* No external libraries required — pure Python.

---

## How it forms / design rationale

1. **Input**: the tool accepts a simple list of numeric sensor values (one per line) to mimic a stream or log of sensor outputs.
2. **Iteration**: using `for` loops, it examines each reading sequentially — this mirrors how live systems process sensor streams.
3. **Comparison checks**:

   * **Jump check**: compares the absolute difference between the current and previous reading. Large jumps often indicate spikes, sensor faults, or tampering.
   * **Moving average check**: computes the average of the previous *N* readings and checks percentage deviation of the current reading from that average. This catches sudden deviations relative to recent history (useful for drifting or step changes).
4. **Output**: Each anomaly is logged with index, value, reason and numeric details; a summary reports total anomalies and optionally writes a report file.

These simple checks are intentionally orthogonal — together they reduce false negatives (e.g., a gradual change might not trigger a jump check but will show up against the moving average).

---

## How to run

1. Clone or download this repository and open it in VS Code (or any editor).
2. Ensure you have Python 3 installed.
3. (Optional) Create a `sensor_data.txt` file in the same folder — one numeric reading per line (no headers).

**Example `sensor_data.txt`:**

```
24
24.5
24.7
25.0
24.9
80
81.2
25.1
25.0
24.8
300
25.2
```

4. Run the script:

```bash
python sensor_integrity.py
```

5. When prompted you can:

* Press **Enter** to use sample readings, or type the path to your `sensor_data.txt` file (e.g., `sensor_data.txt`).
* Enter values for:

  * **Jump threshold** (absolute difference; default `20.0`)
  * **Moving-average window** (integer window size; default `3`)
  * **MA percent threshold** (percent deviation from moving average; default `100.0`)
* Choose whether to save a UTF-8 report file.

---

## How it works (details)

### Sudden Jump

For each reading `r[i]` (i > 0), compute:

```
diff = abs(r[i] - r[i-1])
```

If `diff >= jump_threshold`, flag as a **SUDDEN JUMP**.

### Moving Average Deviation

For each reading where at least `ma_window` prior readings exist:

```
ma = average(r[i-ma_window] ... r[i-1])
percent_dev = abs((r[i] - ma) / ma) * 100
```

If `percent_dev >= ma_percent_threshold`, flag as **MOVING-AVG DEVIATION**.

These two checks run independently — a reading can trigger one or both checks. The parameters let you tune sensitivity to your sensor’s normal variability.

---

## ⚙️ Recommended parameter guidance

* **Jump threshold (absolute)**:

  * Use lower values (e.g., `5`–`10`) for sensors that should change slowly (temperature in a room).
  * Use higher values (e.g., `30`–`100`) for sensors that naturally fluctuate or for noisier environments.

* **Moving average window**:

  * Small window (2–5) for responsive detection.
  * Larger window (10+) smooths normal variability but may delay detection.

* **MA percent threshold**:

  * `50`–`100%` is a common starting point. Lower values are more sensitive.

Start with defaults (Jump = 20, MA window = 3, Percent = 100) and tune using representative data.

---

## Example runs

**Short demo (fast):**

* Use a small `max_range` or small verification set — good for classroom/demo.

**Full test (realistic):**

* Supply a long `sensor_data.txt` with live or logged readings and set window/threshold to realistic values for your device.

**Output sample:**

```
=== SENSOR INTEGRITY MONITOR ===
Reading 3: 80.0 → SUDDEN JUMP (Δ = 55.0)
Reading 11: 300.0 → MOVING-AVG DEVIATION (dev = 250.0%)
Summary: 2 anomalies detected out of 12 readings.
Report saved to: sensor_report_2025-10-16_07-40-12.txt
```

---

##  Why this is crucial (real-world usefulness)

* **Prevents cascading failures**: Early detection of bad readings prevents incorrect actuator commands or unsafe decisions.
* **Supports firmware testing**: Use as a quick static or dynamic test to surface sensors that require calibration or hardware checks.
* **Easy to integrate**: The monitor is a simple building block; it can be extended into a CI test, a device health dashboard, or an alerting pipeline (email, webhook, MQTT).
* **Communicates risk**: A concise anomaly report is useful for engineering teams, QA, and product owners to prioritize fixes.

---

## Extensions & next steps (ideas to make it production-ready)

* Add timestamps (CSV input) and include time-based thresholds and rate checks.
* Stream readings from a serial port (UART) or from MQTT topics to analyze live device telemetry.
* Write anomalies to a structured log (JSON) for ingestion by SIEM or log analytics.
* Build a lightweight dashboard (Flask/Streamlit) to visualize readings and anomalies.
* Add statistical detectors (z-score), exponential smoothing, or simple ML for better detection.

---

## Troubleshooting

* **Unicode/encoding errors when saving reports**: Ensure script opens files with `encoding="utf-8"` (this project does).
* **Non-numeric lines in `sensor_data.txt`**: The loader ignores blank or invalid lines and prints warnings.
* **No anomalies found but you expect some**: Lower thresholds or reduce MA window to increase sensitivity.

---

## Files in this repo

* `sensor_integrity.py` — main script (runs in terminal; configurable)
* `sensor_data.txt` — optional sample data (one numeric reading per line)
* `README.md` — this document

---

## 🧾 License & attribution

Feel free to reuse, extend, and incorporate this project into audits, demos, or client PoCs. If you build on it, a star on GitHub or a quick citation is appreciated.

---

## 👤 Author / Contact

**OYEDELE HAMEED ABIODUN** — Cyber-Physical Hardware Security enthusiast
GitHub: `https://github.com/Abdulhameed-001`
LinkedIn: `https://www.linkedin.com/in/oyedele-hameed-abiodun-a6a352368?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app`

# IoT-Sensor-Data-Integrity-Monitor
