from fastapi import FastAPI, File, UploadFile
from ultralytics import YOLO
import cv2
import numpy as np
import io
from PIL import Image

app = FastAPI()

# تحميل الموديل
try:
    body_model = YOLO("body_best.pt")
except Exception as e:
    print(f"Error: {e}")

@app.get("/")
def home():
    return {"status": "Mahd Backend is Live 🌙"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    frame = np.array(image)
    results = body_model.predict(frame, conf=0.25, verbose=False)
    detections = []
    for r in results:
        for box in r.boxes:
            detections.append({
                "class": int(box.cls),
                "confidence": float(box.conf),
                "bbox": [float(x) for x in box.xyxy[0].tolist()]
            })
    return {"detections": detections}
