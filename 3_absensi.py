import cv2
import sqlite3
from datetime import datetime
import os

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')

faceCascade = cv2.CascadeClassifier(
    'haarcascade_frontalface_default.xml'
)

font = cv2.FONT_HERSHEY_SIMPLEX

cam = cv2.VideoCapture(0)

# Connect ke database
conn = sqlite3.connect("absensi.db")
cursor = conn.cursor()

while True:

    ret, img = cam.read()

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(100, 100)
    )

    for (x, y, w, h) in faces:

        cv2.rectangle(
            img,
            (x, y),
            (x+w, y+h),
            (0, 255, 0),
            2
        )

        id, confidence = recognizer.predict(
            gray[y:y+h, x:x+w]
        )

        # Jika confidence rendah (semakin rendah = semakin cocok)
        if confidence < 70:
            
            # Ambil data mahasiswa dari database berdasarkan id wajah
            cursor.execute("SELECT nim, nama FROM mahasiswa WHERE id=?", (id,))
            result = cursor.fetchone()

            if result:
                nim = result[0]
                nama = result[1]
                
                waktu = datetime.now()
                tanggal_str = waktu.strftime("%d-%m-%Y")
                jam_str = waktu.strftime("%H:%M:%S")

                # Cek apakah sudah absen hari ini supaya tidak tercatat ganda terus menerus
                cursor.execute("SELECT * FROM absensi WHERE nama=? AND tanggal=?", (nama, tanggal_str))
                is_absen = cursor.fetchone()

                if not is_absen:
                    cursor.execute("INSERT INTO absensi (nim, nama, tanggal, jam) VALUES (?, ?, ?, ?)", (nim, nama, tanggal_str, jam_str))
                    conn.commit()
                    print(f"Berhasil menyimpan absen untuk {nama} pada {jam_str}!")

                text = nama
            else:
                text = "Data tdk ada"

        else:
            text = "Unknown"

        cv2.putText(
            img,
            text,
            (x, y-10),
            font,
            0.8,
            (255, 255, 255),
            2
        )

    cv2.imshow(
        'Sistem Absensi Wajah',
        img
    )

    k = cv2.waitKey(10) & 0xff

    # Tekan 'Esc' untuk keluar
    if k == 27:
        break

cam.release()
conn.close()
cv2.destroyAllWindows()