from keras.models import load_model
import os
import face_recognition
import cv2
import numpy as np

# author: Ruochen Liu
# revised by Lixuan Zhang at 2020/01/14
# the integration of face detection, recognition and male classifier


class FaceDetector:
    def __init__(self):

        self.known_face_encoding = []
        self.known_face_names = []
        self.gender_classifier = load_model(
            "classifier/gender_models/simple_CNN.81-0.96.hdf5")
        self.gender_labels = {0: 'female', 1: 'male'}

        self.process_this_frame = True

        path = "img/face_recognition"
        for fn in os.listdir(path):  # fn indicate the filename
            print(path + "/" + fn)
            self.known_face_encoding.append(face_recognition.face_encodings(
                face_recognition.load_image_file(path + "/" + fn))[0])
            # cut out the image name (The filename of file in image should be their name)
            fn = fn[:(len(fn) - 4)]
            self.known_face_names.append(fn)  # image name list

    def detect(self, frame):
        try:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        except:
            return None
        # convert the image from BGR format to RGB format (used in face_recognition)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = []
        face_encodings = []
        face_names = []
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)

        face_names = []

        # compare the face encoding infromation cut off in video with face library to confirm the name.
        for face_encoding in face_encodings:
            # whether mathed with knowen faces
            matches = face_recognition.compare_faces(
                self.known_face_encoding, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(
                self.known_face_encoding, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]

            face_names.append(name)

        faces = []  # the tuple containing location, face name, gender, waited to be returned
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # gender recognition
            face = frame[(right - 60):(right + left + 60),
                         (top - 30):(top + bottom + 30)]
            try:
                face = cv2.resize(face, (48, 48))
            except:
                continue
            face = np.expand_dims(face, 0)
            face = face / 255.0
            gender_label_arg = np.argmax(self.gender_classifier.predict(face))
            gender = self.gender_labels[gender_label_arg]
            faces.append((top, right, bottom, left, name, gender))

            # the codes listed blow are used to debug
            # draw a reactangle cotaining the face
            # cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # draw label
            # cv2.rectangle(frame, (left, bottom - 35),
            #               (right, bottom), (0, 0, 255), cv2.FILLED)
            # font = cv2.FONT_HERSHEY_DUPLEX
            # cv2.putText(frame, name, (left + 6, bottom - 6),
            #             font, 1.0, (255, 255, 255), 1)
            # cv2.putText(frame, gender, (left + 6, top - 6),
            #            font, 1.0, (255, 255, 255), 1)

            return faces

    def verifyfaces(self, faces):
        valid = False
        try:
            for _, _, _, _, name, gender in faces:
                if name in self.known_face_names and gender == self.gender_labels[1]:
                    valid = True
                    break
        except:
            pass
        return valid
