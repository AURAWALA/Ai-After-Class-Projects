import cv2

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# Start webcam
cap = cv2.VideoCapture(0)

# Settings
brightness = 30        # Adjust brightness (-100 to 100)
rotation_mode = 0      # 0 = no rotation, 1 = 90°, 2 = 180°, 3 = 270°
save_faces = True      # Set False if you don’t want to save faces

img_counter = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # -------- Image Manipulations -------- #

    # Brightness Adjustment
    frame = cv2.convertScaleAbs(frame, alpha=1, beta=brightness)

    # Rotation
    if rotation_mode == 1:
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    elif rotation_mode == 2:
        frame = cv2.rotate(frame, cv2.ROTATE_180)
    elif rotation_mode == 3:
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # -------- Face Detection -------- #
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    # -------- Drawing + Cropping -------- #
    for (x, y, w, h) in faces:
        # Draw rectangle
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Crop face
        face_crop = frame[y:y+h, x:x+w]

        # Save face
        if save_faces:
            cv2.imwrite(f"face_{img_counter}.jpg", face_crop)
            img_counter += 1

    # -------- People Count -------- #
    people_count = len(faces)

    # Display text
    cv2.putText(
        frame,
        f'People Count: {people_count}',
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    cv2.putText(
        frame,
        "Press Q to Quit",
        (10, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    # -------- Display -------- #
    cv2.imshow('Final Project - Face Tracking & Counter', frame)

    # Exit key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()