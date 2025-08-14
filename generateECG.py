import os
import wfdb
import numpy as np
import scipy.signal as sp
import matplotlib.pyplot as plt
from pathlib import Path

script_dir = Path(__file__).parent.resolve()

# Define the output folder relative to the script directory
output_folder = script_dir / "Generated_ecg"
output_folder.mkdir(exist_ok=True)

# Define paths and record info
base_dir = Path(r"D:/RUPP/RUPP/RUPP Y3S1/Machine Learning/FinalProject/AF_Detection/dataset/afdb")
record_name = "04043"
record_path = base_dir / record_name

print("Exists?", record_path.with_suffix(".hea").exists())  # Should print True

# Load full record and annotation once
record = wfdb.rdrecord(str(record_path))
ann = wfdb.rdann(str(record_path), 'atr')

print("Record path: ", record_path)
print("Record loaded. Shape:", record.p_signal.shape)
print("Annotations sample:", ann.aux_note[:5])

def bandpass_filter(x, lowcut=0.5, highcut=40, fs=250, order=4):
    nyq = fs / 2
    b, a = sp.butter(order, [lowcut / nyq, highcut / nyq], btype='band')
    return sp.filtfilt(b, a, x)

def normalize_signal(sig):
    sig_min = np.min(sig)
    sig_max = np.max(sig)
    range_ = sig_max - sig_min
    if range_ == 0:
        return np.zeros_like(sig)  # or just return sig unchanged
    return 2 * (sig - sig_min) / range_ - 1

def extract_real_ecg_segments(record, ann, label_filter, max_samples=100, window_sec=30, lead=0):
    fs = record.fs
    window_size = int(fs * window_sec)

    signal = record.p_signal[:, lead] + record.p_signal[:, lead + 1]
    segments = []
    count = 0

    for i in range(len(ann.sample) - 1):
        label = ann.aux_note[i].strip("() ")
        # Remove next_label check

        if label not in label_filter:
            continue

        start = ann.sample[i]
        end = ann.sample[i + 1]

        for s in range(start, end - window_size, window_size):
            seg = signal[s:s + window_size]
            if len(seg) < window_size:
                continue
            seg = bandpass_filter(seg, fs=fs)
            seg = normalize_signal(seg)
            segments.append((seg, label))
            count += 1
            if count >= max_samples:
                return segments

    return segments

import json

def save_ecg_json(segment, label, index, subfolder):
    folder = script_dir / subfolder
    folder.mkdir(parents=True, exist_ok=True)

    filename = f"{label}_{index}.json"
    path = folder / filename

    data = {
        "label": label,
        "signal": segment.tolist()
    }

    with open(path, 'w') as f:
        json.dump(data, f)

if __name__ == "__main__":
    afib_segments = extract_real_ecg_segments(record, ann, label_filter=["AFIB"], max_samples=100)
    normal_segments = extract_real_ecg_segments(record, ann, label_filter=["N"], max_samples=100)
    
    print(f"Extracted {len(afib_segments)} AFIB segments and {len(normal_segments)} Normal segments.")

    for i, (seg, _) in enumerate(afib_segments):
        save_ecg_json(seg, "AFIB", i, "Generated_json/AFIB")

    for i, (seg, _) in enumerate(normal_segments):
        save_ecg_json(seg, "Normal", i, "Generated_json/Normal")

    print("JSON files saved in Generated_json/")
    print(f"AFIB JSON saved: {len(afib_segments)}")
    print(f"Normal JSON saved: {len(normal_segments)}")