# Deep-Drowsiness-Detection using OpenCV

This project is a real-time drowsiness detection system built with Python and OpenCV.
It uses Haar Cascade classifiers to detect the face and eyes from a webcam feed, then analyzes the eye aspect ratio (height/width of detected eye region) to determine whether the person is:

🟢 Active → Eyes open
🟠 Drowsy → Eyes half closed for a few frames
🔴 Sleeping → Eyes fully closed for several frames

The system shows the current status on the video feed and can be extended to trigger alarms for driver safety.

🔧 How It Works

1.Face Detection → Haar cascade detects the face in the video frame.

2.Eye Detection → Haar cascade detects eyes in the upper half of the face.

3.Eye Ratio Calculation → Eye openness is estimated using the height/width ratio of the eye bounding box.

4.Frame Counters → Status changes only if a condition (Active/Drowsy/Sleeping) is detected for several consecutive frames (to avoid flickering).

5.Status Display → The detected state is shown as text on the video window.

📦 Requirements

1.Python 3.x
2.OpenCV (pip install opencv-python)
3.Webcam

⚡ Future Improvements

1.Add an alarm sound when “SLEEPING” is detected

2.Support for glasses (using haarcascade_eye_tree_eyeglasses.xml)

3.Use deep learning models (Dlib, Mediapipe, or CNNs) for more accurate eye detection

🎯 Use Cases

Driver drowsiness detection system 🚗💤

Workplace fatigue monitoring

Real-time eye tracking applications
