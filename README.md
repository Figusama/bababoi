### Sleep Detector Using OpenCV and MediaPipe

This is working Sleep Detector project that detects whether the user sleeps or not. 

OpenCV is used to get the frames from the webcamera (use different camera, mine is initialized as 1 `cv.VideoCapture()` )
MediaPipe is used to detect the face landmarks (eyes, mouth e.t.c). This project only extracted two points of eye (the lower and higher point `upper_eye = landmarks[159], lower_eye = landmarks[145]` ) so that when their difference is lower than 4 it will track user as sleeping.
Also, in order to get rid of the misses when user blinks, this project set the sleeping phase to 30 frames (if lower than nothing will appear ).
Those it skips when user blinks.

Also to wake up the user, sounddevice library is used to put the alarm when user is sleeping.
You can change it by pasting the path of the song in .wav (`data, samplerate = sf.read("../audio_type.wav")`) as i put the goofy one.

