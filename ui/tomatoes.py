from flask import Flask, jsonify
from ultralytics import YOLO
import cv2
import threading

app = Flask(__name__)

# Load your trained YOLO model
model = YOLO("/home/sylas/tomatoes/best.pt")

# Global variable to store last detection
latest_detections = []

# Background thread for continuous inference
def detection_loop():
    global latest_detections
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        results = model.predict(frame, verbose=False)
        detections = []

        for r in results:
            for box in r.boxes:
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                if conf >= 0.80:
                    detections.append({
                        "class": model.names[cls],
                        "confidence": round(conf, 2)
                    })

        latest_detections = detections  # update shared variable

    cap.release()

@app.route('/')
def home():
    return jsonify({"message": "Tomato detection API is running!"})

@app.route('/predict', methods=['GET'])
def predict():
    return jsonify({"detections": latest_detections})

if __name__ == '__main__':
    # Start background thread
    thread = threading.Thread(target=detection_loop, daemon=True)
    thread.start()

    # Start Flask API
    app.run(host='0.0.0.0', port=5000)
