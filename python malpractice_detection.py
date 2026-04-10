import cv2

# Load face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 
                                     'haarcascade_frontalface_default.xml')

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Camera not detected")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    face_count = len(faces)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

    if face_count == 0:
        cv2.putText(frame, "Malpractice: No Face Detected", (30,50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    elif face_count > 1:
        cv2.putText(frame, "Malpractice: Multiple Faces", (30,50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    else:
        cv2.putText(frame, "Student Present", (30,50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("AI Malpractice Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()