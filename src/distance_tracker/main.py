import cv2
import mediapipe as mp



# MediaPipe initialization
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)




# Initialize the Face Detection model
with mp_face_detection.FaceDetection(
        model_selection=0, min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        # Get image dimensions (height and width) to convert normalized coordinates to pixels
        ih, iw, _ = image.shape

        # Convert the image from BGR to RGB for MediaPipe processing
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image_rgb)

        # Convert back to BGR for OpenCV visualization
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)


        if results.detections:
            for detection in results.detections:
                # Draw standard detection markers
                mp_drawing.draw_detection(image, detection)

                # Get keypoints for eyes
                keypoints = detection.location_data.relative_keypoints
                left_eye = keypoints[0]
                right_eye = keypoints[1]

                # Get keypoints for nose
                nose = keypoints[2]

                # Convert normalized (0-1) coordinates to pixel coordinates
                le_x, le_y = int(left_eye.x * iw), int(left_eye.y * ih)
                re_x, re_y = int(right_eye.x * iw), int(right_eye.y * ih)
                nose_x, nose_y = int(nose.x * iw), int(nose.y * ih)

                # Calculate Euclidean distance in pixels
                # Formula: sqrt((x2-x1)^2 + (y2-y1)^2)
                eye_dist_px = ((re_x - le_x) ** 2 + (re_y - le_y) ** 2) ** 0.5


                # 5. Draw visual indicators for eyes
                cv2.circle(image, (le_x, le_y), 5, (255, 0, 0), cv2.FILLED)
                cv2.circle(image, (re_x, re_y), 5, (255, 0, 0), cv2.FILLED)
                cv2.line(image, (le_x, le_y), (re_x, re_y), (0, 255, 255), 2)


        cv2.imshow('Face & Eye Distance Tracker', image)

        if cv2.waitKey(5) & 0xFF == 27:  # Press ESC to exit
            break

cap.release()
cv2.destroyAllWindows()