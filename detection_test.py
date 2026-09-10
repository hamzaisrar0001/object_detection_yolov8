import cv2
from ultralytics import YOLO

model = YOLO("yolov8s.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.track(frame, conf=0.5, persist=True, tracker="bytetrack.yaml")

    annotated_frame = results[0].plot()

    cv2.imshow("YOLO Detection + Tracking", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()