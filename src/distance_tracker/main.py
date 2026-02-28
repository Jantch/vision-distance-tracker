import cv2
import mediapipe as mp
from pathlib import Path
import datetime


from distance_calculation import DistanceCalculator, dis_t_calibration, save_calibration
from head_rot_comp import FaceRotComp
from head_pose_tracker import HeadPoseTracker
from posture_tracker import PostureTracker, pos_t_calibration

# MediaPipe initialization
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

config_file = Path("data_files/calibration_data.txt")

if config_file.exists():
    str_const = config_file.read_text()
    if str_const != "":
        const = float(str_const)
        dist_calc = DistanceCalculator(const, True)
else:
    dist_calc = DistanceCalculator()

face_rot_comp = FaceRotComp()
head_pose_tracker = HeadPoseTracker()
post_truck = PostureTracker()

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

        date = datetime.datetime.now().strftime("%H:%M")
        cv2.putText(image, f"{date}",
                    (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

        if results.detections:
            x_disp_shift = 30
            y_disp_shift = 25
            red = (0, 0, 255)
            green = (0, 255, 0)
            yellow = (0, 255, 255)
            for detection in results.detections:
                # Draw standard detection markers
                mp_drawing.draw_detection(image, detection)

                # Get keypoints for eyes
                keypoints = detection.location_data.relative_keypoints
                left_eye = keypoints[0]
                right_eye = keypoints[1]
                bbox = detection.location_data.relative_bounding_box

                # Get coordinates of the box
                x_min = int(bbox.xmin * iw)
                y_min = int(bbox.ymin * ih)
                bbox_width = int(bbox.width * iw)
                bbox_height = int(bbox.height * ih)

                # Coordinates of the lower, right point
                x_max = x_min + bbox_width
                y_max = y_min + bbox_height

                # Get keypoints for nose
                nose = keypoints[2]

                # Convert normalized (0-1) coordinates to pixel coordinates
                le_x, le_y = int(left_eye.x * iw), int(left_eye.y * ih)
                re_x, re_y = int(right_eye.x * iw), int(right_eye.y * ih)
                nose_x, nose_y = int(nose.x * iw), int(nose.y * ih)

                # Calculate Euclidean distance in pixels
                # Formula: sqrt((x2-x1)^2 + (y2-y1)^2)
                eye_dist_px = ((re_x - le_x) ** 2 + (re_y - le_y) ** 2) ** 0.5
                if not dist_calc.get_status():
                    cv2.putText(image, f"press d to start dist. calibration",
                            (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('d'):
                        dis_t_calibration(dist_calc, eye_dist_px)
                        save_calibration(config_file, dist_calc.get_constant())

                if not post_truck.get_status():
                    cv2.putText(image, f"press p to start post. calibration",
                                (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('p'):
                        pos_t_calibration(post_truck, re_y, le_y, curr_dist)

                if head_pose_tracker.should_calculate():
                    angle = head_pose_tracker.calculate_angle(re_x, re_y, le_x, le_y)
                    if -2 <= angle <= 2 :
                        a_disp_color = green
                    elif -4 <= angle <= 4 :
                        a_disp_color = yellow
                    else:
                        a_disp_color = red
                cv2.putText(image, f"Head angle: {int(angle)}",
                            (x_min, y_max+2*y_disp_shift), cv2.FONT_HERSHEY_SIMPLEX, 0.8, a_disp_color, 1)

                if dist_calc.get_status():
                    if dist_calc.should_calculate():
                        dist_calc.time_update()
                        face_rot_comp.calculate_correction(re_x, le_x, nose_x, eye_dist_px)
                        eye_dist_px_corr = eye_dist_px * face_rot_comp.get_correction()

                        curr_dist = dist_calc.get_dist(eye_dist_px_corr)
                        curr_dist_raw = dist_calc.get_dist(eye_dist_px)
                        if curr_dist >= 60:
                            d_disp_color = green
                        elif 50 <= curr_dist < 60:
                            d_disp_color = yellow
                        else:
                            d_disp_color = red
                    cv2.putText(image, f"Distance: {int(curr_dist)}[cm]",
                                (x_min, y_max+y_disp_shift), cv2.FONT_HERSHEY_SIMPLEX, 0.8, d_disp_color, 1)

                if post_truck.should_calculate():
                    posture = post_truck.check_pos(re_y, le_y, curr_dist)
                    if post_truck.if_bad():
                        cv2.putText(image, f"Please sit up straight",
                                    (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

                # 5. Draw visual indicators for eyes
                cv2.circle(image, (le_x, le_y), 5, (255, 0, 0), cv2.FILLED)
                cv2.circle(image, (re_x, re_y), 5, (255, 0, 0), cv2.FILLED)
                cv2.line(image, (le_x, le_y), (re_x, re_y), (0, 255, 255), 2)


        cv2.imshow('Face & Eye Distance Tracker', image)

        if cv2.waitKey(5) & 0xFF == 27:  # Press ESC to exit
            break

cap.release()
cv2.destroyAllWindows()