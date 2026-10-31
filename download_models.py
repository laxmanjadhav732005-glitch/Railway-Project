"""Downloads the OpenCV face models (only needed if face_recognition/dlib is not installed)."""
import os
import urllib.request

BASE = "https://github.com/opencv/opencv_zoo/raw/main/models/"
FILES = {
    "face_detection_yunet_2023mar.onnx": BASE + "face_detection_yunet/face_detection_yunet_2023mar.onnx",
    "face_recognition_sface_2021dec.onnx": BASE + "face_recognition_sface/face_recognition_sface_2021dec.onnx",
}
os.makedirs("models", exist_ok=True)
for name, url in FILES.items():
    dest = os.path.join("models", name)
    print("Downloading", name, "...")
    urllib.request.urlretrieve(url, dest)
    size = os.path.getsize(dest)
    print("  saved", size, "bytes")
    if size < 10_000:
        print("  WARNING: file too small - download the .onnx manually from opencv_zoo on GitHub")
print("Done.")
