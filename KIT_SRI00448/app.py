from flask import Flask, request, render_template, redirect, url_for, request, jsonify

from flask_socketio import SocketIO
import subprocess
app = Flask(__name__)
from flask import Flask, render_template, Response,jsonify
import cv2
import numpy as np
import mediapipe as mp
import math
import matplotlib.pyplot as plt
from flask_pymongo import PyMongo
from math import radians, sin, cos, sqrt, atan2

app.config['MONGO_URI'] = 'mongodb+srv://Healthcare:svasthya@cluster0.n6qsfnz.mongodb.net/Helathcare'

mongo = PyMongo(app)

pharmacies_collection = mongo.db.pharmacies

locations = [
    {'name': 'Area Hospital', 'lat': 12.79288551575399, 'lng': 80.22096888910694},
    {'name': 'GMR Varalakshmi Care Hospital', 'lat': 12.799407667894487 , 'lng': 80.21719227733956},
    {'name': 'Amrutha Hospital', 'lat': 12.742826561359013, 'lng': 80.19436077266634},
    {'name': 'Sri Venkata Padma Hospital', 'lat': 12.788538396011399, 'lng': 80.22098467895333}]

api_key = 'AIzaSyAIuFz3oQQTp4lwGYGRwBnztgAQw_nszK0'

# Initialize user location as None
user_lat = None
user_lng = None

def find_nearest_pharmacy(tablet_name, user_lat, user_lng):
    nearest_pharmacy = None
    min_distance = float("inf")

    for pharmacy in pharmacies_collection.find({"inventory.medicine.name": tablet_name}):
        pharmacy_location = pharmacy["location"]
        pharmacy_lat = float(str(pharmacy_location[0]))  # Convert Decimal128 to float
        pharmacy_lng = float(str(pharmacy_location[1]))  # Convert Decimal128 to float

        # Calculate distance using Haversine formula
        distance = haversine(user_lat, user_lng, pharmacy_lat, pharmacy_lng)

        if distance < min_distance:
            min_distance = distance
            nearest_pharmacy = {
                "name": pharmacy["name"],
                "description": pharmacy["inventory"][0]["medicine"]["description"],
                "manufacturer": pharmacy["inventory"][0]["medicine"]["manufacturer"],
                "price": pharmacy["inventory"][0]["medicine"]["price"]
            }

    return nearest_pharmacy

@app.route('/find_nearest_location', methods=['POST'])
def find_nearest_location():
    try:
        lat = float(request.form['lat'])
        lng = float(request.form['lng'])

        # Calculate distances and find the nearest location
        nearest_location = None
        min_distance = float('inf')  # Initialize with a large value

        for location in locations:
            location_lat = location['lat']
            location_lng = location['lng']

            # Calculate distance using Haversine formula
            distance = haversine(lat, lng, location_lat, location_lng)

            if distance < min_distance:
                min_distance = distance
                nearest_location = location

        if nearest_location:
            return jsonify({'location': nearest_location['name'], 'distance': min_distance})
        else:
            return jsonify({'location': 'No results found'})

    except Exception as e:
        return jsonify({'error': str(e)})

def haversine(lat1, lon1, lat2, lon2):
    
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']

    # Choose the collection based on the role
    if role == 'patient':
        collection = mongo.db.patients
    elif role == 'doctor':
        collection = mongo.db.doctors
    elif role == 'hospital':
        collection = mongo.db.hospitals
    elif role == 'pharmacist':
        collection = mongo.db.pharmacists

    # Insert user details into the chosen collection
    collection.insert_one({'username': username, 'password': password})

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']

    # Choose the collection based on the role
    if role == 'patient':
        collection = mongo.db.patients
        redirect_page = 'patient_home.html'
    elif role == 'doctor':
        collection = mongo.db.doctors
        redirect_page = 'doctor_home.html'
    elif role == 'hospital':
        collection = mongo.db.hospitals
        redirect_page = 'hospital_home.html'
    elif role == 'pharmacist':
        collection = mongo.db.pharmacists
        redirect_page = 'pharmacist_home.html'
    else:
        # Handle an invalid or unknown role here
        return render_template('index.html')

    user = collection.find_one({'username': username, 'password': password})

    if user:
        # User authenticated successfully
        # Implement your authentication logic here
        return render_template(redirect_page)  # Redirect to the appropriate page

    # User authentication failed
    return render_template('index.html')

# Initialize Flask app

# Initialize mediapipe pose class
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)

mp_drawing = mp.solutions.drawing_utils

show_message = False
counter_left = 0  # Define global variables for counters
counter_right = 0


# Function to calculate the angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle 

# Function to stream the video with landmarks and angles displayed
def video_stream():
    global counter_left, counter_right
    cap = cv2.VideoCapture(0)
    counter_left = 0
    counter_right = 0
    stage_left = None
    stage_right = None

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
        
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            
            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Calculate angles for left arm (similarly for right arm)
                # Left Arm
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                angle_left = calculate_angle(left_shoulder, left_elbow, left_wrist)

                # Right Arm
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                angle_right = calculate_angle(right_shoulder, right_elbow, right_wrist)

                # Visualize angle for left arm
                cv2.putText(image, f"Left Angle: {angle_left:.2f}", tuple(np.multiply(left_elbow, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                # Visualize angle for right arm
                cv2.putText(image, f"Right Angle: {angle_right:.2f}", tuple(np.multiply(right_elbow, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                # Counter logic for left arm
                
                if angle_left > 160 and stage_left != 'down':
                    stage_left = "down"
                if angle_left < 30 and stage_left == 'down':
                    stage_left = "up"
                    # Increase count value only when all landmarks are visible
                    counter_left += 1
                    if counter_left == 25:
                        counter_left = 0

                # Inside the code block for right arm count
                
                if angle_right > 160 and stage_right != 'down':
                    stage_right = "down"
                if angle_right < 30 and stage_right == 'down':
                    stage_right = "up"
                    # Increase count value only when all landmarks are visible

                    counter_right += 1
                    if counter_right == 25:
                        counter_right = 0


            except:
                pass
            
            # Render counters
            cv2.putText(image, f"Left Count: {counter_left}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, f"Right Count: {counter_right}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
            
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()
    
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
    label = 'Unknown Pose'

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
    if label != 'Unknown Pose':
        
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

# Release the VideoCapture object and close the windows
def webcam_feed():
    # Initialize the VideoCapture object to read from the webcam
    camera_video = cv2.VideoCapture(0)
    camera_video.set(3, 1380)
    camera_video.set(4, 960)

    while camera_video.isOpened():
        # Read a frame
        ok, frame = camera_video.read()

        if not ok:
            continue

        # Flip the frame horizontally for natural (selfie-view) visualization
        frame = cv2.flip(frame, 1)

        # Get the width and height of the frame
        frame_height, frame_width, _ = frame.shape

        # Resize the frame while keeping the aspect ratio
        frame = cv2.resize(frame, (int(frame_width * (640 / frame_height)), 640))

        # Perform Pose landmark detection
        frame, landmarks = detectPose(frame, pose, display=False)

        if landmarks:
            # Perform the Pose Classification
            frame, _ = classifyPose(landmarks, frame, display=False)

        # Convert the frame to JPEG format
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera_video.release()
    cv2.destroyAllWindows()
    
@app.route('/yoga_try')
def yoga_try():
    return render_template('yoga_try.html')

@app.route('/video_feed1')
def video_feed1():
    return Response(webcam_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')


# Route for the index page
@app.route('/ph_index')
def ph_index():
    return render_template('ph-index1.html')

@app.route('/restart')
def restart():
    return render_template('index1.html')

@app.route('/get_counts')
def get_counts():
    global counter_left, counter_right
    # Return updated counts as JSON response
    return jsonify({'counter_left': counter_left, 'counter_right': counter_right})


@app.route('/phy_health')
def phy_health():
    global counter_left, counter_right  
    print(counter_left)
    print(counter_right)
    return render_template('ph-index.html',counter_left=counter_left, counter_right=counter_right)

@app.route("/nearby_pharmacy", methods=["GET", "POST"])
def nearby_pharmacy():
    nearest_pharmacy = None

    global user_lat, user_lng

    if request.method == "POST":
        tablet_name = request.form["tablet_name"]
        nearest_pharmacy = find_nearest_pharmacy(tablet_name, user_lat, user_lng)

    return render_template("nearby_pharmacy.html", nearest_pharmacy=nearest_pharmacy)

@app.route('/patient_home')
def patient_home():
    # Add your logic for the patient home page here
    return render_template('patient_home.html')


@app.route('/logout')
def logout():
    return render_template('index.html')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/hospital')
def hospital():
    return render_template('hospital.html')

@app.route("/get_location", methods=["POST"])
def get_location():
    global user_lat, user_lng  

    if "latitude" in request.form and "longitude" in request.form:
        user_lat = float(request.form["latitude"])
        user_lng = float(request.form["longitude"])

    return jsonify({"message": "Location received."})

# Route for video feed
@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
# Route to the main page
@app.route('/games_index')
def games_index():
    return render_template('games_index.html')

@app.route('/home_return')
def home_return():
    return render_template('games_index.html')

@app.route('/pacman')
def pacman():
    return render_template('pacman-index.html')

@app.route('/pacman_index1')
def pacman_index1():
    return render_template('pacman-index1.html')

@app.route('/diet_plan')
def diet_plan():
    return render_template('diet-index.html')

@app.route('/child_index')
def child_index():
    return render_template('child_index.html')

@app.route('/ma_index')
def ma_index():
    return render_template('ma_index.html')

@app.route('/old_index')
def old_index():
    return render_template('old_index.html')

@app.route('/child_physical_page')
def child_physical_page():
    return render_template('child_physical_page.html')

@app.route('/child_mental_page')
def child_mental_page():
    return render_template('child_mental_page.html')

@app.route('/child_ar')
def child_ar():
    return render_template('child_ar.html')

@app.route('/child_culture')
def child_culture():
    return render_template('child_culture.html')

@app.route('/child_hygiene')
def child_hygiene():
    return render_template('child_hygiene.html')

@app.route('/ma_physical_page')
def ma_physical_page():
    return render_template('ma_physical_page.html')

@app.route('/ma_mental_page')
def ma_mental_page():
    return render_template('ma_mental_page.html')

@app.route('/ma_ar')
def ma_ar():
    return render_template('ma_ar.html')

@app.route('/ma_culture')
def ma_culture():
    return render_template('ma_culture.html')

@app.route('/ma_hygiene')
def ma_hygiene():
    return render_template('ma_hygiene.html')

@app.route('/ma_reflexology')
def ma_reflexology():
    return render_template('ma_reflexology.html')

@app.route('/ma_yoga')
def ma_yoga():
    return render_template('ma_yoga.html')


@app.route('/old_physical_page')
def old_physical_page():
    return render_template('old_physical_page.html')

@app.route('/old_mental_page')
def old_mental_page():
    return render_template('old_mental_page.html')

@app.route('/old_ar')
def old_ar():
    return render_template('old_ar.html')

@app.route('/old_culture')
def old_culture():
    return render_template('old_culture.html')


@app.route('/old_reflexology')
def old_reflexology():
    return render_template('old_reflexology.html')

@app.route('/old_yoga')
def old_yoga():
    return render_template('old_yoga.html')

@app.route('/memory_game')
def memory_game():
    return render_template('memory-index.html')

@app.route('/tower_block')
def tower_block():
    return render_template('tower-index.html')

@app.route('/guess_word')
def guess_word():
    return render_template('guess-index.html')

@app.route('/reflexology_click')
def reflexology_click():
    return render_template('reflexology-index.html')

@app.route('/reflexology_new')
def reflexology_new():
    return render_template('reflexology-new.html')

@app.route('/drag_drop')
def drag_drop():
    return render_template('dragdrop-index.html')

@app.route('/anatomy')
def anatomy():
    return render_template('anatomy.html')

@app.route('/girl_hygiene')
def girl_hygiene():
    return render_template('girl_hygiene.html')

@app.route('/cam_hygiene')
def cam_hygiene():
    return render_template('cam_hygiene.html')

@app.route('/reflexology_try')
def reflexology_try():
    return render_template('reflexology_try.html')

socketio = SocketIO(app)



# Route to start the game
@app.route('/play_game')
def play_game():
    socketio.emit('game_result', {'result': 'Game started!'}, namespace='/game')
    subprocess.Popen(['python', 'pacman.py'])
    return ''

# Route to start the game
@app.route('/play_game_elders')
def play_game_elders():
    socketio.emit('game_result', {'result': 'Game started!'}, namespace='/game')
    subprocess.Popen(['python', 'pacman-elders.py'])
    return ''

# SocketIO event handler for game results
@socketio.on('game_result', namespace='/game')
def handle_game_result(data):
    print(data['result'])

@app.route('/img_puzzle')
def img_puzzle():
    return render_template('img_puzzle-index.html')

@app.route('/yoga')
def yoga():
    return render_template('yoga-index.html')

@app.route('/dial')
def dial():
    return render_template('dial-index.html')
@app.route('/run_game', methods=['POST'])
def run_game():
    # Run the game.py script using subprocess
    subprocess.run(['python', 'game.py'])
    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(debug=True)