<h1 style="text-align: center;">HandTrack</h1>
<h2>What is this?</h2>
HandTrack is a python implementation of google's mediapipe library, using their Hand-Landmarker AI model and OpenCV. (All rights for the model belong to them, I do not own the model nor the mediapipe library)<br>
Included in the project is also another script using the same library with the same model, OpenCV, and pygame, to allow the user to paint on a canvas using their hands.

## Installation
Clone the project to your computer using git clone or by downloading it as a zip file. Make sure to install all the required python packages using ```pip install -r requirements.txt```.

## Usage
As stated in the introduction, there are two main scripts included in this repository.
### show_landmarks.py
This script will take the video from your webcam and draw hand landmarks on it using the mediapipe library and the Hand-Landmarker model (located at model/hand_landmarker.task). The resulting
video will be shown in an OpenCV window. <br>
To start the script, use the command ```python3 your/path/to/show_landmarks.py```.<br>
At runtime, press ***h*** to hide the camera footage and only show the landmarks, press ***q*** to stop the script.<br>
<img width="60%" alt="hand landmarks" src="https://github.com/MarshiDev/HandMouse/assets/97107764/fff6333b-cd53-4c6e-ba4c-7329eb99af32">
### paint.py
This script will take the video from your webcam and use either the position of your wrist or the position of your pointer finger (depending on the configuration of the variable 'mode' at the top; default: 'pointer')
to draw a red dot inside a pygame window, and ultimately let your control a paint brush with it. To start the script, use the command ```python3 your/path/to/paint.py```.
When you move your and (and in pointer mode also your pointer finger), the red dot moves with it. If you only want to move your brush (the red dot) without painting, hold your hand straight and parallel to the front of your camera.
To start painting, tilt your hand about 70° forward (so that your fingertips are <b>almost</b> pointing straight at the camera).
