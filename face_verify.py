"""Face comparison with two interchangeable engines.

1. 'dlib'   -> the `face_recognition` package (best accuracy, hard to install on Windows)
2. 'opencv' -> OpenCV YuNet + SFace ONNX models (pure pip, run `python download_models.py`)

Result of compare_faces() is one of:
    MATCH | MISMATCH | UNABLE TO VERIFY
A match NEVER proves identity: it is a decision aid for a human.
"""
import os
import cv2
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE, "models")
YUNET = os.path.join(MODEL_DIR, "face_detection_yunet_2023mar.onnx")
SFACE = os.path.join(MODEL_DIR, "face_recognition_sface_2021dec.onnx")

try:
    import face_recognition as _fr
    HAS_DLIB = True
except Exception:
    _fr = None
    HAS_DLIB = False


def _opencv_ready():
    return (os.path.exists(YUNET) and os.path.getsize(YUNET) > 10_000
            and os.path.exists(SFACE) and os.path.getsize(SFACE) > 10_000
            and hasattr(cv2, "FaceDetectorYN"))


def backend():
    if HAS_DLIB:
        return "dlib"
    if _opencv_ready():
        return "opencv"
    return None


# Default thresholds (demo values - calibrate on your own test data!)
DLIB_MAX_DISTANCE = 0.50      # lower distance = more similar
SFACE_MIN_COSINE = 0.363      # higher cosine  = more similar (OpenCV docs value)


def _decode(image_bytes):
    arr = np.frombuffer(image_bytes, np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)


def _encode_dlib(bgr):
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    encs = _fr.face_encodings(rgb)
    return encs[0] if len(encs) == 1 else None


def _encode_opencv(bgr):
    h, w = bgr.shape[:2]
    det = cv2.FaceDetectorYN.create(YUNET, "", (w, h), 0.8, 0.3, 5000)
    _, faces = det.detect(bgr)
    if faces is None or len(faces) != 1:
        return None
    rec = cv2.FaceRecognizerSF.create(SFACE, "")
    aligned = rec.alignCrop(bgr, faces[0])
    return rec.feature(aligned).flatten()


def encode_face(image_bytes):
    """Return a feature vector, or None if there is not exactly one usable face."""
    bgr = _decode(image_bytes)
    if bgr is None:
        return None
    b = backend()
    if b == "dlib":
        return _encode_dlib(bgr)
    if b == "opencv":
        return _encode_opencv(bgr)
    raise RuntimeError("No face engine available. See README.md")


def compare_vectors(known, captured, dlib_threshold=None, cosine_threshold=None):
    """Returns (result, score). score = distance (dlib) or cosine (opencv)."""
    if known is None or captured is None:
        return "UNABLE TO VERIFY", None
    if backend() == "dlib":
        t = DLIB_MAX_DISTANCE if dlib_threshold is None else dlib_threshold
        dist = float(np.linalg.norm(np.asarray(known) - np.asarray(captured)))
        return ("MATCH" if dist < t else "MISMATCH"), dist
    t = SFACE_MIN_COSINE if cosine_threshold is None else cosine_threshold
    a = np.asarray(known, np.float32).flatten()
    b = np.asarray(captured, np.float32).flatten()
    cos = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
    return ("MATCH" if cos >= t else "MISMATCH"), cos


def compare_faces(known_bytes, captured_bytes, **kw):
    return compare_vectors(encode_face(known_bytes), encode_face(captured_bytes), **kw)
