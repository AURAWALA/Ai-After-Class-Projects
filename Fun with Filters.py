import cv2
import numpy as np

# Start webcam
cap = cv2.VideoCapture(0)

# Create a window
cv2.namedWindow('Color Filter')

# Create trackbars for RGB adjustment
def nothing(x):
    pass

cv2.createTrackbar('R', 'Color Filter', 100, 200, nothing)
cv2.createTrackbar('G', 'Color Filter', 100, 200, nothing)
cv2.createTrackbar('B', 'Color Filter', 100, 200, nothing)

img_counter = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Get trackbar values
    r = cv2.getTrackbarPos('R', 'Color Filter') / 100
    g = cv2.getTrackbarPos('G', 'Color Filter') / 100
    b = cv2.getTrackbarPos('B', 'Color Filter') / 100

    # Split channels
    B, G, R = cv2.split(frame)

    # Apply scaling
    B = np.clip(B * b, 0, 255).astype(np.uint8)
    G = np.clip(G * g, 0, 255).astype(np.uint8)
    R = np.clip(R * r, 0, 255).astype(np.uint8)

    # Merge back
    filtered_frame = cv2.merge([B, G, R])

    # Display text
    cv2.putText(filtered_frame, "Press S to Save | Q to Quit",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 255), 2)

    # Show output
    cv2.imshow('Color Filter', filtered_frame)

    key = cv2.waitKey(1) & 0xFF

    # Save image
    if key == ord('s'):
        filename = f'filtered_{img_counter}.jpg'
        cv2.imwrite(filename, filtered_frame)
        print(f"Saved: {filename}")
        img_counter += 1

    # Quit
    elif key == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()