import cv2

# Load face and eye detector files from OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade  = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

# Eye ratio cutoffs
CLOSED_EYE_RATIO = 0.22   # smaller than this = eyes closed
DROWSY_EYE_RATIO = 0.30   # between closed and this = drowsy

# Counters to keep track of states (so results don’t flicker)
sleep_frames = 0
drowsy_frames = 0
active_frames = 0

# How many frames in a row before we show the status
SLEEP_LIMIT = 6
DROWSY_LIMIT = 6
ACTIVE_LIMIT = 6

# Open webcam (0 = default camera)
cap = cv2.VideoCapture(0)

# Function to calculate eye ratio = height / width
def eye_ratio(eye_rect):
    _, _, w, h = eye_rect
    return h / w if w > 0 else 0

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Convert image to black & white (needed for detector)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    # Default status if nothing is found
    status = "No Face"
    color = (0, 255, 255)  # yellow

    for (x, y, w, h) in faces:
        # Draw a green box around the face
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

        # Look for eyes only in the top half of the face
        roi_gray = gray[y:y+h//2, x:x+w]

        # Detect eyes in that area
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 5, minSize=(20,8))

        # Find ratio for each eye (height/width)
        ratios = [eye_ratio(e) for e in eyes]

        if ratios:  # if eyes are found
            avg = sum(ratios) / len(ratios)  # average ratio

            # Show ratio number on the screen
            cv2.putText(frame, f"Ratio: {avg:.2f}", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

            # Count how many frames the eyes are closed/drowsy/active
            if avg < CLOSED_EYE_RATIO:      # eyes closed
                sleep_frames += 1
                drowsy_frames = 0
                active_frames = 0
            elif avg < DROWSY_EYE_RATIO:    # eyes half closed
                drowsy_frames += 1
                sleep_frames = 0
                active_frames = 0
            else:                           # eyes open
                active_frames += 1
                sleep_frames = 0
                drowsy_frames = 0

            # Decide status only if the same result is seen for many frames
            if sleep_frames >= SLEEP_LIMIT:
                status, color = "SLEEPING", (0,0,255)   # red
            elif drowsy_frames >= DROWSY_LIMIT:
                status, color = "Drowsy", (0,165,255)   # orange
            elif active_frames >= ACTIVE_LIMIT:
                status, color = "Active", (0,255,0)     # green

        else:
            # If eyes are not detected
            status, color = "Eyes Not Found", (0,140,255)

    # Write status text on the video
    cv2.putText(frame, status, (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)

    # Show the video
    cv2.imshow("Drowsiness Detector", frame)

    # If ESC key is pressed → exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Close the webcam and windows
cap.release()
cv2.destroyAllWindows()
