"""Demo ticket card + QR generation and QR decoding."""
import os
import cv2
import numpy as np
import qrcode
from PIL import Image, ImageDraw

from database import TICKETS_DIR


def make_ticket(ticket_id, name, seat, train="DEMO EXPRESS"):
    """Create tickets/<id>.png : a demo ticket card containing a QR code."""
    os.makedirs(TICKETS_DIR, exist_ok=True)
    qr = qrcode.make(ticket_id).convert("RGB").resize((260, 260))
    card = Image.new("RGB", (640, 320), "white")
    d = ImageDraw.Draw(card)
    d.rectangle([0, 0, 639, 50], fill=(20, 60, 140))
    d.text((15, 18), "DEMO RAILWAY TICKET - ACADEMIC PROTOTYPE", fill="white")
    d.text((20, 80), f"Ticket ID : {ticket_id}", fill="black")
    d.text((20, 115), f"Passenger : {name}", fill="black")
    d.text((20, 150), f"Seat      : {seat}", fill="black")
    d.text((20, 185), f"Train     : {train}", fill="black")
    d.text((20, 280), "Synthetic data - not a valid railway ticket", fill="gray")
    card.paste(qr, (360, 50))
    path = os.path.join(TICKETS_DIR, f"{ticket_id}.png")
    card.save(path)
    return path


def decode_qr(image_bytes):
    """Return the text inside a QR code found in an image, or None."""
    arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        return None
    det = cv2.QRCodeDetector()
    text, _, _ = det.detectAndDecode(img)
    if text:
        return text.strip()
    # retry upscaled (small QR codes)
    big = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    text, _, _ = det.detectAndDecode(big)
    return text.strip() if text else None
