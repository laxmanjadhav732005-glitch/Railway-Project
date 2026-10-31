import cv2

camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print("Camera not detected")
    raise SystemExit(1)
print("Camera started. Press Q to exit.")
while True:
    ok, frame = camera.read()
    if not ok:
        print("Failed to capture image")
        break
    cv2.imshow("Railway Passenger Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
camera.release()
cv2.destroyAllWindows()
