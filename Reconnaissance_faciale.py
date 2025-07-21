import cv2
import face_recognition
import numpy as np
import sqlite3
import datetime

import pygame
pygame.init()
pygame.mixer.init()
alarmsound=pygame.mixer.Sound('alarm.wav')


# Chargement du fichier de SignaturesAll
SignaturesAll = np.load('SignaturesAll.npy')
signatures = SignaturesAll[:, :-1].astype('float')
noms = SignaturesAll[:, -1]

# Base de données
conn = sqlite3.connect("database.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS detections (nom TEXT, date TEXT)")
conn.commit()

capture = cv2.VideoCapture(0)

while True:
    reponse, image = capture.read()
    if reponse:
        image_reduit = cv2.resize(image, (0, 0), None, 0.25, 0.25)
        emplacement_face = face_recognition.face_locations(image_reduit)
        cararac_face = face_recognition.face_encodings(image_reduit, emplacement_face)

        for encode, loc in zip(cararac_face, emplacement_face):
            match = face_recognition.compare_faces(signatures, encode)
            distance = face_recognition.face_distance(signatures, encode)
            minDist = np.argmin(distance)

            y1, x2, y2, x1 = loc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4

            if match[minDist]:
                name = noms[minDist]
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(image, name, (x1, y2 + 25), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            else:
                name = 'Inconnu'
                cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(image, name, (x1, y2 + 25), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                alarmsound.play()

            # Sauvegarde dans la base
            time_detection = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute("INSERT INTO detections VALUES (?, ?)", (name, time_detection))
            conn.commit()

        cv2.imshow('Cam', image)
        if cv2.waitKey(3) == ord('q'):
            break
    else:
        break

capture.release()
cv2.destroyAllWindows()
conn.close()