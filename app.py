# from flask import Flask, render_template, request, redirect, url_for, session, flash, Response
# import cv2
# import mediapipe as mp
# import math
# import matplotlib.pyplot as plt
#
# # Initialize Flask app
# app = Flask(__name__)
#
# # Initialize mediapipe pose class
# mp_pose = mp.solutions.pose
#
# # Setting up the Pose function
# pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)
#
# # Initializing mediapipe drawing class, useful for annotation.
# mp_drawing = mp.solutions.drawing_utils
#
# def detectPose(image, pose, display=True):
#     '''
#     This function performs pose detection on an image.
#     Args:
#         image: The input image with a prominent person whose pose landmarks needs to be detected.
#         pose: The pose setup function required to perform the pose detection.
#         display: A boolean value that is if set to true the function displays the original input image, the resultant image,
#                 and the pose landmarks in 3D plot and returns nothing.
#     Returns:
#         output_image: The input image with the detected pose landmarks drawn.
#         landmarks: A list of detected landmarks converted into their original scale.
#     '''
#
#     # Create a copy of the input image.
#     output_image = image.copy()
#
#     # Convert the image from BGR into RGB format.
#     imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#
#     # Perform the Pose Detection.
#     results = pose.process(imageRGB)
#
#     # Retrieve the height and width of the input image.
#     height, width, _ = image.shape
#
#     # Initialize a list to store the detected landmarks.
#     landmarks = []
#
#     # Check if any landmarks are detected.
#     if results.pose_landmarks:
#
#         # Draw Pose landmarks on the output image.
#         mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks,
#                                 connections=mp_pose.POSE_CONNECTIONS)
#
#         # Iterate over the detected landmarks.
#         for landmark in results.pose_landmarks.landmark:
#
#             # Append the landmark into the list.
#             landmarks.append((int(landmark.x * width), int(landmark.y * height),
#                                 (landmark.z * width)))
#
#
#     return output_image,landmarks
#
#
# def calculateAngle(landmark1, landmark2, landmark3):
#     '''
#     This function calculates angle between three different landmarks.
#     Args:
#         landmark1: The first landmark containing the x,y and z coordinates.
#         landmark2: The second landmark containing the x,y and z coordinates.
#         landmark3: The third landmark containing the x,y and z coordinates.
#     Returns:
#         angle: The calculated angle between the three landmarks.
#
#     '''
#
#     # Get the required landmarks coordinates.
#     x1, y1, _ = landmark1
#     x2, y2, _ = landmark2
#     x3, y3, _ = landmark3
#
#     # Calculate the angle between the three points
#     angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
#
#     # Check if the angle is less than zero.
#     if angle < 0:
#
#         # Add 360 to the found angle.
#         angle += 360
#
#     # Return the calculated angle.
#     return angle
#
#
# def classifyPose(landmarks, output_image, display=False):
#     '''
#     This function classifies yoga poses depending upon the angles of various body joints.
#     Args:
#         landmarks: A list of detected landmarks of the person whose pose needs to be classified.
#         output_image: A image of the person with the detected pose landmarks drawn.
#         display: A boolean value that is if set to true the function displays the resultant image with the pose label
#         written on it and returns nothing.
#     Returns:
#         output_image: The image with the detected pose landmarks drawn and pose label written.
#         label: The classified pose label of the person in the output_image.
#
#     '''
#
#     # Initialize the label of the pose. It is not known at this stage.
#     label = 'Unknown Pose'
#
#     # Specify the color (Red) with which the label will be written on the image.
#     color = (0, 0, 255)
#
#     # Calculate the required angles.
#     #----------------------------------------------------------------------------------------------------------------
#
#     # Get the angle between the left shoulder, elbow and wrist points.
#     left_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
#                                       landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
#                                       landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])
#
#     # Get the angle between the right shoulder, elbow and wrist points.
#     right_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
#                                        landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
#                                        landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])
#
#     # Get the angle between the left elbow, shoulder and hip points.
#     left_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
#                                          landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
#                                          landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])
#
#     # Get the angle between the right hip, shoulder and elbow points.
#     right_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
#                                           landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
#                                           landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])
#
#     # Get the angle between the left hip, knee and ankle points.
#     left_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
#                                      landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
#                                      landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])
#
#     # Get the angle between the right hip, knee and ankle points
#     right_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
#                                       landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
#                                       landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])
#
#     #----------------------------------------------------------------------------------------------------------------
#
#     # Check if it is the warrior II pose or the T pose.
#     # As for both of them, both arms should be straight and shoulders should be at the specific angle.
#     #----------------------------------------------------------------------------------------------------------------
#
#     if (165 < left_knee_angle < 195) and (165 < right_knee_angle < 195) \
#         and (130 < left_elbow_angle < 180) and (175 < right_elbow_angle < 220) \
#         and (100 < left_shoulder_angle < 200) and (50 < right_shoulder_angle < 130):
#
#         # Specify the label of the pose as Trikonasana Pose
#         label = 'T Pose'
#     #----------------------------------------------------------------------------------------------------------------
#
#     # Check if the both arms are straight.
#     if left_elbow_angle > 165 and left_elbow_angle < 195 and right_elbow_angle > 165 and right_elbow_angle < 195:
#
#         # Check if shoulders are at the required angle.
#         if left_shoulder_angle > 80 and left_shoulder_angle < 110 and right_shoulder_angle > 80 and right_shoulder_angle < 110:
#
#     # Check if it is the warrior II pose.
#     #----------------------------------------------------------------------------------------------------------------
#
#             # Check if one leg is straight.
#             if left_knee_angle > 165 and left_knee_angle < 195 or right_knee_angle > 165 and right_knee_angle < 195:
#
#                 # Check if the other leg is bended at the required angle.
#                 if left_knee_angle > 90 and left_knee_angle < 120 or right_knee_angle > 90 and right_knee_angle < 120:
#
#                     # Specify the label of the pose that is Warrior II pose.
#                     label = 'Warrior II Pose'
#
#     #----------------------------------------------------------------------------------------------------------------
#
#     # Check if it is the T pose.
#     #----------------------------------------------------------------------------------------------------------------
#
#             # Check if both legs are straight
#             # if left_knee_angle > 160 and left_knee_angle < 195 and right_knee_angle > 160 and right_knee_angle < 195:
#
#             #     # Specify the label of the pose that is tree pose.
#             #     label = 'T Pose'
#
#     #----------------------------------------------------------------------------------------------------------------
#
#     # Check if it is the tree pose.
#     #----------------------------------------------------------------------------------------------------------------
#
#     # Check if one leg is straight
#     if left_knee_angle > 165 and left_knee_angle < 195 or right_knee_angle > 165 and right_knee_angle < 195:
#
#         # Check if the other leg is bended at the required angle.
#         if left_knee_angle > 315 and left_knee_angle < 335 or right_knee_angle > 25 and right_knee_angle < 45:
#
#             # Specify the label of the pose that is tree pose.
#             label = 'Tree Pose'
#
#     #----------------------------------------------------------------------------------------------------------------
#
#
#
#     # Check if the pose is classified successfully
#     if label != 'Unknown Pose':
#
#         # Update the color (to green) with which the label will be written on the image.
#         color = (0, 255, 0)
#
#     # Write the label on the output image.
#     cv2.putText(output_image, label, (10, 30),cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
#
#     # Check if the resultant image is specified to be displayed.
#     if display:
#
#         # Display the resultant image.
#         plt.figure(figsize=[10,10])
#         plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');
#
#     else:
#
#         # Return the output image and the classified label.
#         return output_image, label

# # Release the VideoCapture object and close the windows
# def webcam_feed():
#     # Initialize the VideoCapture object to read from the webcam
#     camera_video = cv2.VideoCapture('downdog_warrior2.mp4')
#     camera_video.set(3, 960)
#     camera_video.set(4, 1380)
#
#     while camera_video.isOpened():
#         # Read a frame
#         ok, frame = camera_video.read()
#
#         if not ok:
#             continue
#
#         # Flip the frame horizontally for natural (selfie-view) visualization
#         frame = cv2.flip(frame, 1)
#
#         # Get the width and height of the frame
#         frame_height, frame_width, _ = frame.shape
#
#         # Resize the frame while keeping the aspect ratio
#         frame = cv2.resize(frame, (int(frame_width * (640 / frame_height)), 640))
#
#         # Perform Pose landmark detection
#         frame, landmarks = detectPose(frame, pose, display=False)
#
#         if landmarks:
#             # Perform the Pose Classification
#             frame, _ = classifyPose(landmarks, frame, display=False)
#
#         # Convert the frame to JPEG format
#         ret, jpeg = cv2.imencode('.jpg', frame)
#         frame = jpeg.tobytes()
#
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#
#     camera_video.release()
#     cv2.destroyAllWindows()
#
# @app.route('/')
# def home():
#     return render_template('home.html')
#
# @app.route('/practice')
# def practice():
#     return render_template('practice.html')
#
# @app.route('/video_feed1')
# def video_feed1():
#     return Response(webcam_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')
# @app.route('/classes')
# def classes():
#     return redirect(url_for('home', _anchor='classes'))
#
# @app.route('/contact')
# def contact():
#     return redirect(url_for('home', _anchor='contact'))
#
# @app.route('/booking')
# def booking():
#     return render_template('booking.html')
#
# #
# @app.route('/login')
# def login():
#     return render_template('login.html')
# #
# #
# @app.route('/register')
# def register():
#     return render_template('register.html')
# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, session, flash, Response
import cv2
import mediapipe as mp
import math
import matplotlib.pyplot as plt
import os
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov'}

# Initialize mediapipe pose class
mp_pose = mp.solutions.pose

# Setting up the Pose function
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)

# Initializing mediapipe drawing class, useful for annotation.
mp_drawing = mp.solutions.drawing_utils


# (Keep all your existing pose detection functions here: detectPose, calculateAngle, classifyPose)
def detectPose(image, pose, display=True):
    '''
    This function performs pose detection on an image.
    Args:
        image: The input image with a prominent person whose pose landmarks needs to be detected.
        pose: The pose setup function required to perform the pose detection.
        display: A boolean value that is if set to true the function displays the original input image, the resultant image,
                and the pose landmarks in 3D plot and returns nothing.
    Returns:
        output_image: The input image with the detected pose landmarks drawn.
        landmarks: A list of detected landmarks converted into their original scale.
    '''

    # Create a copy of the input image.
    output_image = image.copy()

    # Convert the image from BGR into RGB format.
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Perform the Pose Detection.
    results = pose.process(imageRGB)

    # Retrieve the height and width of the input image.
    height, width, _ = image.shape

    # Initialize a list to store the detected landmarks.
    landmarks = []

    # Check if any landmarks are detected.
    if results.pose_landmarks:

        # Draw Pose landmarks on the output image.
        mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks,
                                connections=mp_pose.POSE_CONNECTIONS)

        # Iterate over the detected landmarks.
        for landmark in results.pose_landmarks.landmark:

            # Append the landmark into the list.
            landmarks.append((int(landmark.x * width), int(landmark.y * height),
                                (landmark.z * width)))


    return output_image,landmarks


def calculateAngle(landmark1, landmark2, landmark3):
    '''
    This function calculates angle between three different landmarks.
    Args:
        landmark1: The first landmark containing the x,y and z coordinates.
        landmark2: The second landmark containing the x,y and z coordinates.
        landmark3: The third landmark containing the x,y and z coordinates.
    Returns:
        angle: The calculated angle between the three landmarks.

    '''

    # Get the required landmarks coordinates.
    x1, y1, _ = landmark1
    x2, y2, _ = landmark2
    x3, y3, _ = landmark3

    # Calculate the angle between the three points
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))

    # Check if the angle is less than zero.
    if angle < 0:

        # Add 360 to the found angle.
        angle += 360

    # Return the calculated angle.
    return angle


def classifyPose(landmarks, output_image, display=False):
    '''
    This function classifies yoga poses depending upon the angles of various body joints.
    Args:
        landmarks: A list of detected landmarks of the person whose pose needs to be classified.
        output_image: A image of the person with the detected pose landmarks drawn.
        display: A boolean value that is if set to true the function displays the resultant image with the pose label
        written on it and returns nothing.
    Returns:
        output_image: The image with the detected pose landmarks drawn and pose label written.
        label: The classified pose label of the person in the output_image.

    '''

    # Initialize the label of the pose. It is not known at this stage.
    label = ' '

    # Specify the color (Red) with which the label will be written on the image.
    color = (0, 0, 255)

    # Calculate the required angles.
    #----------------------------------------------------------------------------------------------------------------

    # Get the angle between the left shoulder, elbow and wrist points.
    left_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])

    # Get the angle between the right shoulder, elbow and wrist points.
    right_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])

    # Get the angle between the left elbow, shoulder and hip points.
    left_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])

    # Get the angle between the right hip, shoulder and elbow points.
    right_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])

    # Get the angle between the left hip, knee and ankle points.
    left_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])

    # Get the angle between the right hip, knee and ankle points
    right_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])

    #----------------------------------------------------------------------------------------------------------------

    # Check if it is the warrior II pose or the T pose.
    # As for both of them, both arms should be straight and shoulders should be at the specific angle.
    #----------------------------------------------------------------------------------------------------------------

    if (165 < left_knee_angle < 195) and (165 < right_knee_angle < 195) \
        and (130 < left_elbow_angle < 180) and (175 < right_elbow_angle < 220) \
        and (100 < left_shoulder_angle < 200) and (50 < right_shoulder_angle < 130):

        # Specify the label of the pose as Trikonasana Pose
        label = 'T Pose'
    #----------------------------------------------------------------------------------------------------------------

    # Check if the both arms are straight.
    if left_elbow_angle > 165 and left_elbow_angle < 195 and right_elbow_angle > 165 and right_elbow_angle < 195:

        # Check if shoulders are at the required angle.
        if left_shoulder_angle > 80 and left_shoulder_angle < 110 and right_shoulder_angle > 80 and right_shoulder_angle < 110:

    # Check if it is the warrior II pose.
    #----------------------------------------------------------------------------------------------------------------

            # Check if one leg is straight.
            if left_knee_angle > 165 and left_knee_angle < 195 or right_knee_angle > 165 and right_knee_angle < 195:

                # Check if the other leg is bended at the required angle.
                if left_knee_angle > 90 and left_knee_angle < 120 or right_knee_angle > 90 and right_knee_angle < 120:

                    # Specify the label of the pose that is Warrior II pose.
                    label = 'Warrior II Pose'

    #----------------------------------------------------------------------------------------------------------------

    # Check if it is the T pose.
    #----------------------------------------------------------------------------------------------------------------

            # Check if both legs are straight
            # if left_knee_angle > 160 and left_knee_angle < 195 and right_knee_angle > 160 and right_knee_angle < 195:

            #     # Specify the label of the pose that is tree pose.
            #     label = 'T Pose'

    #----------------------------------------------------------------------------------------------------------------

    # Check if it is the tree pose.
    #----------------------------------------------------------------------------------------------------------------

    # Check if one leg is straight
    if left_knee_angle > 165 and left_knee_angle < 195 or right_knee_angle > 165 and right_knee_angle < 195:

        # Check if the other leg is bended at the required angle.
        if left_knee_angle > 315 and left_knee_angle < 335 or right_knee_angle > 25 and right_knee_angle < 45:

            # Specify the label of the pose that is tree pose.
            label = 'Tree Pose'

    #----------------------------------------------------------------------------------------------------------------



    # Check if the pose is classified successfully
    if label != ' ':

        # Update the color (to green) with which the label will be written on the image.
        color = (0, 255, 0)

    # Write the label on the output image.
    cv2.putText(output_image, label, (10, 30),cv2.FONT_HERSHEY_PLAIN, 2, color, 2)

    # Check if the resultant image is specified to be displayed.
    if display:

        # Display the resultant image.
        plt.figure(figsize=[10,10])
        plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');

    else:

        # Return the output image and the classified label.
        return output_image, label

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def get_video_source(source_type, filename=None):
    if source_type == 'webcam':
        return cv2.VideoCapture(0)  # 0 for default webcam
    elif source_type == 'upload' and filename:
        return cv2.VideoCapture(filename)
    else:
        return None


def generate_frames(source_type='webcam', filename=None):
    camera_video = get_video_source(source_type, filename)
    if not camera_video or not camera_video.isOpened():
        return

    camera_video.set(3, 1900)
    camera_video.set(4, 1080)

    try:
        while camera_video.isOpened():
            ok, frame = camera_video.read()
            if not ok:
                break

            frame = cv2.flip(frame, 1)
            frame_height, frame_width, _ = frame.shape
            frame = cv2.resize(frame, (int(frame_width * (640 / frame_height)), 640))

            frame, landmarks = detectPose(frame, pose, display=False)
            if landmarks:
                frame, _ = classifyPose(landmarks, frame, display=False)

            ret, jpeg = cv2.imencode('.jpg', frame)
            frame = jpeg.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    finally:
        # Always release resources even if an error occurs
        camera_video.release()
        cv2.destroyAllWindows()

        # Delete the uploaded video file after playing
        if source_type == 'upload' and filename:
            try:
                os.remove(filename)
                print(f"Deleted uploaded video: {filename}")
            except Exception as e:
                print(f"Error deleting file {filename}: {e}")


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/practice', methods=['GET', 'POST'])
def practice():
    uploaded_filename = None
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            session['uploaded_video'] = filepath
            uploaded_filename = filename
            return render_template('practice.html', uploaded_filename=uploaded_filename)

    return render_template('practice.html', uploaded_filename=uploaded_filename)


@app.route('/video_feed1')
def video_feed1():
    source_type = request.args.get('source', 'webcam')
    if source_type == 'upload' and 'uploaded_video' in session:
        filepath = session['uploaded_video']
        if os.path.exists(filepath):
            return Response(generate_frames(source_type='upload', filename=filepath),
                            mimetype='multipart/x-mixed-replace; boundary=frame')

    # Default to webcam if upload fails or not selected
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
# (Keep all your other routes here: classes, contact, booking, login, register)
@app.route('/classes')
def classes():
    return redirect(url_for('home', _anchor='classes'))

@app.route('/contact')
def contact():
    return redirect(url_for('home', _anchor='contact'))

@app.route('/booking')
def booking():
    return render_template('booking.html')

#
@app.route('/login')
def login():
    return render_template('login.html')
#
#
@app.route('/register')
def register():
    return render_template('register.html')
if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.secret_key = 'super_secret_key'  # Needed for session
    app.run(debug=True)