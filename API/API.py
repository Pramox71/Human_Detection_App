from flask import Flask, Response
import cv2
import numpy as np
import tensorflow as tf

app = Flask(__name__)

# Muat model TFLite
interpreter = tf.lite.Interpreter(model_path="Model/Human_detection.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def process_frame(frame):
    detected_people = {}
    count = 0
    frame_threshold = 30
    captured_ids = set()
    height, width, _ = frame.shape
    center_line = width // 2

    # Pra-proses frame
    input_frame = cv2.resize(frame, (input_details[0]['shape'][2], input_details[0]['shape'][1]))
    input_data = np.array(input_frame, dtype=np.float32)
    input_data = np.expand_dims(input_data, axis=0)
    input_data /= 255.0

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])

    for i in range(output_data.shape[1]):
        confidence = output_data[0][i][4]
        if confidence > 0.85:
            x1, y1, x2, y2 = (output_data[0][i][:4]).astype(int)
            person_id = None

            for obj_id, (box, frames_left) in list(detected_people.items()):
                if abs(x1 - box[0]) < 50 and abs(y1 - box[1]) < 50:
                    person_id = obj_id
                    break

            if person_id is None:
                person_id = count
                detected_people[person_id] = [(x1, y1, x2, y2), frame_threshold]
                count += 1
            else:
                detected_people[person_id][0] = (x1, y1, x2, y2)
                detected_people[person_id][1] = frame_threshold

    for obj_id in list(detected_people):
        detected_people[obj_id][1] -= 1
        if detected_people[obj_id][1] <= 0:
            del detected_people[obj_id]
            captured_ids.discard(obj_id)

    for obj_id, (box, _) in detected_people.items():
        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (255, 0, 0), 2)
        cv2.putText(frame, f'ID: {obj_id}', (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    cv2.line(frame, (center_line, 0), (center_line, height), (0, 255, 0), 2)

    ret, buffer = cv2.imencode('.jpg', frame)
    return buffer.tobytes()

def generate_frames(video_source):
    cap = cv2.VideoCapture(video_source)

    if not cap.isOpened():
        print("Error: Cannot open video stream")
        return None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_data = process_frame(frame)

        
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')

    cap.release()

@app.route('/video_feed', methods=['GET'])
def video_feed():
    video_source = 'rtsp://admin:admin1234@192.168.2.210:554/cam/realmonitor?' 
    return Response(generate_frames(video_source), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1040)
