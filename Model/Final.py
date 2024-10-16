import torch
import cv2
import os
import warnings
import logging

warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.CRITICAL)

model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5n.pt')
model.classes = [0]  # COCO class index for 'person'
model.conf = 0.85
model.iou = 0.66

def detection(cap):
    detected_people = {}  # Dictionary to keep track of detected person IDs and their bounding boxes
    count = 0  # Counter for saving captured images
    frame_threshold = 30  # Number of frames before considering a person as "left the frame"

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Perform detection
        results = model(frame)

        # Iterate through detected objects
        for person in results.xyxy[0]:  # Assuming results.xyxy returns detection results
            class_id = int(person[5])  # Class ID (assuming the 6th element is the class ID)
            if class_id == 0:  # Class ID for 'person'
                x1, y1, x2, y2 = map(int, person[:4])  # Get bounding box
                person_id = None

                # Check if the object has been tracked before
                for obj_id, (box, frames_left) in list(detected_people.items()):
                    if abs(x1 - box[0]) < 50 and abs(y1 - box[1]) < 50:  # Simple distance threshold
                        person_id = obj_id
                        break

                # If not tracked, assign new ID
                if person_id is None:
                    person_id = count
                    detected_people[person_id] = [(x1, y1, x2, y2), frame_threshold]  # Add new person
                    count += 1
                    # Save the current frame with new ID
                    capture_filename = f"Model/Hasil/captured_person_{person_id}.png"
                    cv2.imwrite(capture_filename, frame)
                    print(f"Captured person with ID: {person_id} and saved as {capture_filename}")
                else:
                    # Update bounding box and reset frame counter
                    detected_people[person_id][0] = (x1, y1, x2, y2)
                    detected_people[person_id][1] = frame_threshold

        # Decrease frame count for all tracked people
        for obj_id in list(detected_people):
            detected_people[obj_id][1] -= 1
            if detected_people[obj_id][1] <= 0:  # Remove people who have left the frame
                del detected_people[obj_id]

        # Render bounding boxes with person IDs
        for obj_id, (box, _) in detected_people.items():
            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (255, 0, 0), 2)
            cv2.putText(frame, f'ID: {obj_id}', (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Display the frame with detections
        cv2.imshow('YOLOv5 Person Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def main():
        input_path = input("Masukkan path Video : ")
        if not os.path.isfile(input_path):
                print("File tidak ditemukan. Silakan masukkan path yang valid.")
                return
        cap = cv2.VideoCapture(input_path)
        detection(cap)
        cap.release()
        cv2.destroyAllWindows()

main()