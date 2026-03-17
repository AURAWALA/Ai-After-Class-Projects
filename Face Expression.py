import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# Load emotion model
emotion_model = load_model('emotion_model.hdf5')

# Emotion labels
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # Draw rectangle
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Extract face ROI
        roi_gray = gray[y:y+h, x:x+w]

        # Resize to model input size (48x48)
        roi_gray = cv2.resize(roi_gray, (48, 48))

        # Normalize
        roi = roi_gray / 255.0

        # Reshape for model (1, 48, 48, 1)
        roi = np.reshape(roi, (1, 48, 48, 1))

        # Predict emotion
        prediction = emotion_model.predict(roi)
        emotion_index = np.argmax(prediction)
        emotion = emotion_labels[emotion_index]

        # Display emotion
        cv2.putText(
            frame,
            emotion,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 255),
            2
        )

    # Show frame
    cv2.imshow('Face & Emotion Detection', frame)

    # Exit on Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()