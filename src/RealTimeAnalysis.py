# Importing libraries
import pandas as pd
import dlib
import numpy as np
import cv2
import os
from keras.models import load_model
import preprocessing as pre

# Model Directory
mod_dir = "/".join(os.getcwd().split("/")[0:-1] + ['model/'])

# Initiating the video capture
cap = cv2.VideoCapture(0)

# Importing models
face_detector = dlib.get_frontal_face_detector()
eyes_cascade = eye_cascade = cv2.CascadeClassifier(mod_dir+'haarcascade_eye.xml')
emotions = load_model(mod_dir + 'gpu_mini_XCEPTION.63-0.64.hdf5')

# emotion_labels
emo = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'sad', 5: 'surprise', 6: 'neutral'}

while(True):
    #font = cv2.FONT_HERSHEY_SIMPLEX
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # detecting faces
    faces = face_detector(gray, 0)

    # Getting boundaries for the faces
    for j in enumerate(faces):
        k, d = j
        x, y, w, h = (d.left(), d.top(), d.right() - d.left(), d.bottom() - d.top())
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        # Detecting eyes inside every face
        eyes = eye_cascade.detectMultiScale(roi_gray)
        # Getting boundaries for every eye
        # for (ex,ey,ew,eh) in eyes:
        #     cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        roi_gray = cv2.resize(roi_gray, (48,48))
        face_emo = pre.preprocess_predict(roi_gray)
        emotion = emotions.predict(face_emo)
        emotion_probability = np.max(emotion)
        emotion_label_arg = np.argmax(emotion)
        print(emotion_label_arg)
        font = cv2.FONT_HERSHEY_TRIPLEX
        cv2.putText(frame, emo[emotion_label_arg],(x+w,y), font, 1, (0,255,0), 2)


    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
