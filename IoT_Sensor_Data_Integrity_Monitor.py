# sensor_integrity.py
# -*- coding: utf-8 -*-

"""
IoT Sensor Data Integrity Monitor (best beginner version)

- Reads sensor values from a text file (one reading per line) OR uses sample data.
- Flags anomalies using:
    1) absolute jump threshold between consecutive readings
    2) deviation from a moving average over a window (percent)
- Prints detailed anomaly log and a final summary.
- No external libraries required.
"""

from typing import List, Optional

def read_readings_from_file(path: str) -> List[float]:
    readings = []
    try:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    readings.append(float(line))
                except ValueError:
                    # ignore non-numeric lines but warn
                    print(f"Warning: ignored non-numeric line: {line}")
    except FileNotFoundError:
        print(f"Error: file not found: {path}")
    return readings

def get_sample_readings() -> List[float]:
    # realistic example with anomalies
    return [24.0, 24.5, 24.7, 25.0, 24.9, 80.0, 81.2, 25.1, 25.0, 24.8, 300.0, 25.2]

def moving_average(window: List[float]) -> float:
    return sum(window) / len(window)

def analyze_readings(readings: List[float],
                     jump_threshold: float = 20.0,
                     ma_window: int = 3,
                     ma_percent_threshold: float = 100.0) -> List[str]:
    """
    Analyze readings and return a list of anomaly messages.
    - jump_threshold: absolute difference between consecutive readings to flag (e.g., 20.0 degrees)
    - ma_window: window size for moving average (>=1)
    - ma_percent_threshold: percent deviation from moving average to flag (e.g., 50.0 means 50%)
    """
    anomalies = []
    if not readings:
        return anomalies

    # iterate through readings
    for i in range(len(readings)):
        curr = readings[i]

        # 1) check absolute jump vs previous reading
        if i > 0:
            prev = readings[i - 1]
            diff = abs(curr - prev)
            if diff >= jump_threshold:
                msg = (f"Index {i+1}: value={curr} (jump {diff:.2f} from prev {prev}) "
                       f"→ SUDDEN JUMP (threshold={jump_threshold})")
                anomalies.append(msg)

        # 2) check deviation from moving average of previous 'ma_window' readings
        if ma_window >= 1 and i >= ma_window:
            window = readings[i - ma_window:i]  # previous ma_window readings
            ma = moving_average(window)
            if ma == 0:
                percent_dev = float('inf') if curr != 0 else 0.0
            else:
                percent_dev = abs((curr - ma) / ma) * 100.0
            if percent_dev >= ma_percent_threshold:
                msg = (f"Index {i+1}: value={curr} (MA={ma:.2f}, dev={percent_dev:.1f}%) "
                       f"→ MOVING-AVG DEVIATION (threshold={ma_percent_threshold}%)")
                anomalies.append(msg)

    return anomalies

def pretty_print(readings: List[float], anomalies: List[str]) -> None:
    print("=== SENSOR INTEGRITY MONITOR ===")
    for i, v in enumerate(readings, start=1):
        print(f"Reading {i}: {v}")
    print("\n=== ANOMALY LOG ===")
    if anomalies:
        for a in anomalies:
            print(a)
    else:
        print("No anomalies detected.")
    print(f"\nSummary: {len(anomalies)} anomalies detected out of {len(readings)} readings.")

def save_report(path: str, readings: List[float], anomalies: List[str]) -> None:
    try:
        with open(path, "w") as f:
            f.write("SENSOR READINGS\n")
            for i, v in enumerate(readings, start=1):
                f.write(f"Reading {i}: {v}\n")
            f.write("\nANOMALY LOG\n")
            if anomalies:
                for a in anomalies:
                    f.write(a + "\n")
            else:
                f.write("No anomalies detected.\n")
            f.write(f"\nSummary: {len(anomalies)} anomalies detected out of {len(readings)} readings.\n")
        print(f"Report saved to: {path}")
    except Exception as e:
        print(f"Error saving report: {e}")

def main():
    print("=== IoT Sensor Data Integrity Monitor ===")
    choice = input("Load readings from file? (enter path) or press Enter to use sample data: ").strip()
    if choice:
        readings = read_readings_from_file(choice)
        if not readings:
            print("No valid readings found in file. Exiting.")
            return
    else:
        readings = get_sample_readings()
        print("Using sample readings.")

    # parameters
    try:
        jump_threshold = float(input("Jump threshold (absolute, default 20.0): ").strip() or "20.0")
    except ValueError:
        jump_threshold = 20.0
    try:
        ma_window = int(input("Moving-average window (integer >=1, default 3): ").strip() or "3")
        if ma_window < 1:
            ma_window = 3
    except ValueError:
        ma_window = 3
    try:
        ma_percent_threshold = float(input("MA percent threshold (e.g., 100 for 100%, default 100): ").strip() or "100.0")
    except ValueError:
        ma_percent_threshold = 100.0

    anomalies = analyze_readings(readings,
                                 jump_threshold=jump_threshold,
                                 ma_window=ma_window,
                                 ma_percent_threshold=ma_percent_threshold)

    pretty_print(readings, anomalies)

    save = input("Save report to file? (y/N): ").strip().lower()
    if save == "y":
        path = input("Enter filename (e.g., report.txt): ").strip() or "sensor_report.txt"
        save_report(path, readings, anomalies)

if __name__ == "__main__":
    main()
