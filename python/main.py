import cv2 as cv
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import FaceLandmarkerOptions
from mediapipe.tasks.python.vision import FaceLandmarker
from mediapipe.tasks.python.vision import RunningMode

model_path = "../face_landmarker.task"

baseoptions = BaseOptions(
    model_asset_path=model_path,
    delegate=mp.tasks.BaseOptions.Delegate.CPU
)


options = FaceLandmarkerOptions(
    base_options=baseoptions,
    running_mode = RunningMode.IMAGE,
    num_faces=1,
    min_face_detection_confidence=0.7,
)

SLEEPING_PARAM = 30
from timeit import default_timer as timer
import sounddevice as sd
import soundfile as sf 

data, samplerate = sf.read("../audio_type.wav")
playing = False
with FaceLandmarker.create_from_options(options) as landmarker:
    cap = cv.VideoCapture(1) #macbook camera

    if not cap.isOpened():
        raise ValueError("Video cannot be opened. Check for different camera mode.")
    sleeping_timer = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Hard to read frame. Exiting...")
            break

        h, w  = frame.shape[:2]
        rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        mp_img = mp.Image(mp.ImageFormat.SRGB, rgb)
        
        res = landmarker.detect(mp_img)
        if res.face_landmarks:

            for face_idx, landmarks in enumerate(res.face_landmarks):
                
                upper_eye = landmarks[159]
                lower_eye = landmarks[145]
                end_time = 0
                if h*(lower_eye.y - upper_eye.y) < 4:
                    sleeping_timer+=1
                else:
                    sleeping_timer = 0
                
                if sleeping_timer >= SLEEPING_PARAM:
                    cv.putText(frame, "SLEEPING", (int(w/2), 100), cv.FONT_HERSHEY_COMPLEX, 5, (0, 0, 255), 2)
                    if not playing:
                        sd.play(data, samplerate, loop=True)
                        playing=True
                    
                else:
                    if playing:
                        sd.stop()
                        playing=False

                    

        cv.imshow("Image", frame)
        if cv.waitKey(1) == ord("q"):
            break
    
    cap.release()
    cv.destroyAllWindows()