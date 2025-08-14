from flask import Flask, request, render_template, jsonify
from tensorflow.keras.models import load_model
import numpy as np
import os
import requests
import neurokit2 as nk

app = Flask(__name__)
ESP32_IP = "http://192.168.137.247"  # Replace with actual ESP32 IP

# Load model
model_path = "D:/RUPP/RUPP/RUPP Y3S1/Machine Learning/FinalProject/AF_Detection/dataset/AFIB Detection Model.keras"
model = load_model(model_path)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    if not data or 'signal' not in data:
        return jsonify({'error': 'No ECG signal provided'}), 400

    try:
        raw_ecg = np.array(data['signal'], dtype=np.float32)

        # Normalize raw ECG
        raw_ecg = (raw_ecg - np.min(raw_ecg)) / (np.max(raw_ecg) - np.min(raw_ecg) + 1e-6)

        # RRI extraction using neurokit2
        signals, info = nk.ecg_process(raw_ecg, sampling_rate=250)
        rpeaks = info["ECG_R_Peaks"]

        # RR Intervals (in seconds)
        rri = np.diff(rpeaks) / 250.0

        if len(rri) < 39:
            return jsonify({'error': f'Not enough RR intervals: {len(rri)}'}), 400

        desired_len = model.input_shape[1]  # 39
        if len(rri) > desired_len:
            rri = rri[:desired_len]
        else:
            rri = np.pad(rri, (0, desired_len - len(rri)), mode='constant')

        # Correct shape: (1, 39, 1)
        model_input = rri.reshape(1, desired_len, 1)

        # Predict
        score = model.predict(model_input)[0][0]
        result = "Atrial Fibrillation Detected" if score > 0.5 else "Normal Rhythm"

        # ESP32 Command
        esp_status = "DETECT" if score > 0.9 else "UNDETECTED"
        send_to_esp32(esp_status)

        return jsonify({
            'prediction': result,
            'score': f"{score * 100:.2f}%",  # formats score as percentage with 2 decimal places            
            'esp32_status': esp_status
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def send_to_esp32(command):
    try:
        url = f"{ESP32_IP}/{command}"
        requests.get(url, timeout=2)
        print(f"[ESP32] Sent: {command}")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] ESP32 not reachable: {e}")

@app.route('/status')
def status():
    return jsonify({"status": "running"})

if __name__ == '__main__':
    app.run(debug=True)
