import threading
import cv2
from flask import Flask, request, jsonify, render_template
"""
from ultralytics import YOLO
"""
from fastapi import FastAPI
import random

# app = Flask(__name__)
# model = None  # Model loading disabled for UI testing


latest_detections = []

def generate_mock_prediction():
    """Generate a single mock prediction for API testing."""
    classes = ['fresh tomato', 'rotten tomato']
    pred_class = random.choice(classes)
    confidence = round(random.uniform(80, 100), 2)
    return {"class": pred_class, "confidence": confidence}

def generate_mock_detections(num=5):
    """Generate a list of mock detections for UI testing."""
    return [generate_mock_prediction() for _ in range(num)]

def detection_loop():
    global latest_detections
    # For UI testing, just use mock detections
    latest_detections = generate_mock_detections()
    
# @app.route('/')
# def home():
#     # For UI testing, use mock data
#     mock_detections = generate_mock_detections()
#     return jsonify({"detections": mock_detections})
#     mock_detections = generate_mock_detections()
#     return render_template('index.html', detections=mock_detections)


# @app.route('/predict', methods=['POST'])
# def predict():
#     # Accept image file but ignore it for mock
#     if 'file' not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400
#     # file = request.files['file']
#     # You can process the image here if needed
#     mock_result = generate_mock_prediction()
#     return jsonify(mock_result)

app = FastAPI()

@app.post("/predict")
def fastapi_predict():
    classes = ['fresh tomato', 'rotten tomato']
    pred_class = random.choice(classes)
    confidence = round(random.uniform(80, 100), 2)
    return {"class": pred_class, "confidence": confidence}


if __name__ == '__main__':
    detection_thread = threading.Thread(target=detection_loop)
    detection_thread.daemon = True
    detection_thread.start()
    app.run(host='0.0.0.0', port=5000)