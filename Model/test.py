import numpy as np
import tensorflow as tf
import cv2
import os

# Memuat model TFLite
interpreter = tf.lite.Interpreter(model_path = "Model\Human_detection.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def detection(cap):
    detected_people = {}  # Kamus untuk melacak ID orang yang terdeteksi dan kotak pembatasnya
    count = 0  # Penghitung untuk menyimpan gambar yang ditangkap
    frame_threshold = 30  # Jumlah frame sebelum menganggap seseorang "keluar dari frame"
    captured_ids = set()  # Set untuk menyimpan ID yang telah ditangkap saat melewati garis

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        height, width, _ = frame.shape
        center_line = width // 2  # Tentukan posisi garis vertikal

        # Pra-proses frame
        input_frame = cv2.resize(frame, (input_details[0]['shape'][2], input_details[0]['shape'][1]))
        input_data = np.array(input_frame, dtype=np.float32)
        input_data = np.expand_dims(input_data, axis=0)
        input_data /= 255.0  # Normalisasi

        # Atur tensor input
        interpreter.set_tensor(input_details[0]['index'], input_data)

        # Jalankan inferensi
        interpreter.invoke()

        # Ambil tensor output
        output_data = interpreter.get_tensor(output_details[0]['index'])

        for i in range(output_data.shape[1]):
            confidence = output_data[0][i][4]
            if confidence > 0.85:  # Ambang batas kepercayaan
                x1, y1, x2, y2 = (output_data[0][i][:4]).astype(int)
                person_id = None

                # Cek jika objek telah dilacak sebelumnya
                for obj_id, (box, frames_left) in list(detected_people.items()):
                    if abs(x1 - box[0]) < 50 and abs(y1 - box[1]) < 50:
                        person_id = obj_id
                        break

                # Jika tidak dilacak, tetapkan ID baru
                if person_id is None:
                    person_id = count
                    detected_people[person_id] = [(x1, y1, x2, y2), frame_threshold]
                    count += 1
                    # Simpan gambar saat ini dengan ID baru
                    capture_filename = f"Model/Hasil/captured_person_{person_id}.png"
                    cv2.imwrite(capture_filename, frame)
                    print(f"Captured person with ID: {person_id} and saved as {capture_filename}")
                else:
                    # Perbarui bounding box dan reset penghitung frame
                    detected_people[person_id][0] = (x1, y1, x2, y2)
                    detected_people[person_id][1] = frame_threshold

                # # Logika untuk menangkap orang yang melewati garis tengah
                # if x1 < center_line < x2 and person_id not in captured_ids:
                #     # Jika objek melewati garis tengah dan belum ditangkap
                #     capture_filename = f"Model/Hasil/captured_person_crossed_{person_id}.png"
                #     cv2.imwrite(capture_filename, frame)
                #     print(f"Captured person crossing the line with ID: {person_id} and saved as {capture_filename}")
                #     captured_ids.add(person_id)  # Tambahkan ID ke set yang ditangkap

        # Kurangi penghitung frame untuk semua orang yang dilacak
        for obj_id in list(detected_people):
            detected_people[obj_id][1] -= 1
            if detected_people[obj_id][1] <= 0:
                del detected_people[obj_id]
                captured_ids.discard(obj_id)  # Hapus ID dari set jika keluar dari frame

        # Gambar kotak pembatas dengan ID orang
        for obj_id, (box, _) in detected_people.items():
            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (255, 0, 0), 2)
            cv2.putText(frame, f'ID: {obj_id}', (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Gambar garis tengah
        cv2.line(frame, (center_line, 0), (center_line, height), (0, 255, 0), 2)

        # Tampilkan frame dengan deteksi
        cv2.imshow('Deteksi Orang dengan Garis Tengah', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def main():
    input_path = input("Masukkan path Video: ")
    if not os.path.isfile(input_path):
        print("File tidak ditemukan. Silakan masukkan path yang valid.")
        return
    cap = cv2.VideoCapture(input_path)
    detection(cap)
    cap.release()
    cv2.destroyAllWindows()

main()
