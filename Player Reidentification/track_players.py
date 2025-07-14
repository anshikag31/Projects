# track_players.py
import cv2
import csv
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

# Load YOLOv8 model (custom player detection model)
yolo = YOLO('models/best.pt')

# Initialize DeepSort tracker
tracker = DeepSort(max_age=30)

# Load input video
cap = cv2.VideoCapture('videos/input.mp4')
width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
out = cv2.VideoWriter('videos/output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

# Open CSV file for logging
log_file = open('videos/tracking_log.csv', mode='w', newline='')
csv_writer = csv.writer(log_file)
csv_writer.writerow(['frame_number', 'track_id', 'x1', 'y1', 'x2', 'y2'])

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

    # Detect players
    results = yolo.predict(source=frame, imgsz=640, verbose=False)[0]
    detections = []

    for box in results.boxes.data.tolist():  # Get list of detections
        x1, y1, x2, y2, conf, cls = box
        detections.append(([x1, y1, x2, y2], conf, 'player'))

    # Track using DeepSort
    tracks = tracker.update_tracks(detections, frame=frame)

    for track in tracks:
        if not track.is_confirmed():
            continue
        x1, y1, x2, y2 = map(int, track.to_ltrb())
        tid = track.track_id

        # Log tracking data to CSV
        csv_writer.writerow([frame_number, tid, x1, y1, x2, y2])

        # Draw bounding box and ID on the frame
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f'ID:{tid}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    out.write(frame)

cap.release()
out.release()
log_file.close()

print("✅ Done! Output saved to videos/output.mp4 and tracking_log.csv")
