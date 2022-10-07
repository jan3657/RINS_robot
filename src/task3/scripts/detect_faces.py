#!/usr/bin/python3
from ctypes import sizeof
from pathlib import Path
import sys
import rospy
import dlib
import cv2
import actionlib
import numpy as np
import tf2_geometry_msgs
import tf2_ros
import face_recognition
import copy
import math

from matplotlib import pyplot as plt

from os.path import dirname, join

from geometry_msgs.msg import PoseStamped, Quaternion, Point, PoseWithCovarianceStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionResult
from sensor_msgs.msg import Image
from geometry_msgs.msg import PointStamped, Vector3, Pose, Twist
from cv_bridge import CvBridge, CvBridgeError
from visualization_msgs.msg import Marker, MarkerArray
from std_msgs.msg import ColorRGBA
from actionlib_msgs.msg import GoalID
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from message_filters import ApproximateTimeSynchronizer, Subscriber
from task3.msg import FacePose


class face_localizer:
    def __init__(self):
        cwd = Path.cwd()
        mod_path = Path(__file__).parent
        relative_path = '../meshes/faces/'
        src_path_1 = (mod_path / relative_path).resolve()
        path = str(src_path_1)

        ana = cv2.imread(path + '/Ana.png')
        gargamel = cv2.imread(path + '/Gargamel.png')
        irena = cv2.imread(path + '/Irena.png')
        mateja = cv2.imread(path + '/Mateja.png')
        nina = cv2.imread(path + '/nina.png')
        maja = cv2.imread(path + '/Maja.png')
        marija = cv2.imread(path + '/Marija.png')
        mojca = cv2.imread(path + '/Mojca.png')
        andreja = cv2.imread(path + '/Andreja.png')
        natasa = cv2.imread(path + '/Natasa.png')

        self.known_faces = {}
        print("start")
        self.known_faces["Ana"] = face_recognition.face_encodings(ana)[0]
        self.known_faces["Gargamel"] = face_recognition.face_encodings(gargamel)[0]
        self.known_faces["Irena"] = face_recognition.face_encodings(irena)[0]
        self.known_faces["Mateja"] = face_recognition.face_encodings(mateja)[0]
        self.known_faces["Nina"] = face_recognition.face_encodings(nina)[0]
        self.known_faces["Maja"] = face_recognition.face_encodings(maja)[0]
        self.known_faces["Marija"] = face_recognition.face_encodings(marija)[0]
        self.known_faces["Mojca"] = face_recognition.face_encodings(mojca)[0]
        self.known_faces["Andreja"] = face_recognition.face_encodings(andreja)[0]
        self.known_faces["Nataša"] = face_recognition.face_encodings(natasa)[0]
        print("done")
        rospy.init_node('face_localizer', anonymous=True)

        # An object we use for converting images between ROS format and OpenCV format
        self.bridge = CvBridge()

        # The function for performin HOG face detection
        # self.face_detector = dlib.get_frontal_face_detector()
        protoPath = join(dirname(__file__), "deploy.prototxt.txt")
        modelPath = join(dirname(__file__), "res10_300x300_ssd_iter_140000.caffemodel")

        self.face_net = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

        # A help variable for holding the dimensions of the image
        self.dims = (0, 0, 0)

        # Marker array object used for showing markers in Rviz
        self.marker_array = MarkerArray()
        self.marker_num = 0

        # Subscribe to the image and/or depth topic
        # self.image_sub = rospy.Subscriber("/camera/rgb/image_raw", Image, self.image_callback)
        # self.depth_sub = rospy.Subscriber("/camera/depth/image_raw", Image, self.depth_callback)
        self.image_sub = Subscriber("/camera/rgb/image_raw", Image)
        self.depth_sub = Subscriber("/camera/depth/image_raw", Image)

        ats = ApproximateTimeSynchronizer([self.image_sub, self.depth_sub], queue_size=10, slop=0.01)
        ats.registerCallback(self.find_faces)

        # Publisher for the visualization markers
        self.markers_pub = rospy.Publisher('face_markers', MarkerArray, queue_size=1000)
        self.face_pose_pub = rospy.Publisher('detected_face', FacePose, queue_size=1000)

        # Object we use for transforming between coordinate frames
        self.tf_buf = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buf)

        self.faces = list()
        #self.numb_of_faces = 3
        # self.botLocationX = 0.0
        # self.botLocationY = 0.0
        # self.quarternion = [None] * 4

    def get_pose(self, coords, dist, stamp):
        # Calculate the position of the detected face

        k_f = 554  # kinect focal length in pixels

        x1, x2, y1, y2 = coords

        face_x = self.dims[1] / 2 - (x1 + x2) / 2.
        face_y = self.dims[0] / 2 - (y1 + y2) / 2.

        angle_to_target = np.arctan2(face_x, k_f)

        # Get the angles in the base_link relative coordinate system
        x, y = dist * np.cos(angle_to_target), dist * np.sin(angle_to_target)

        ### Define a stamped message for transformation - directly in "base_link"
        # point_s = PointStamped()
        # point_s.point.x = x
        # point_s.point.y = y
        # point_s.point.z = 0.3
        # point_s.header.frame_id = "base_link"
        # point_s.header.stamp = rospy.Time(0)

        # Define a stamped message for transformation - in the "camera rgb frame"
        point_s = PointStamped()
        point_s.point.x = -y
        point_s.point.y = 0
        point_s.point.z = x
        point_s.header.frame_id = "camera_rgb_optical_frame"
        point_s.header.stamp = stamp

        # Get the point in the "map" coordinate system
        try:
            point_world = self.tf_buf.transform(point_s, "map")

            pose = PoseStamped()
            pose.header.frame_id = "camera_rgb_optical_frame"
            pose.header.stamp = stamp
            pose.pose.position.x = point_world.point.x
            pose.pose.position.y = point_world.point.y
            pose.pose.position.z = point_world.point.z

        except Exception as e:
            print(e)
            pose = None

        return pose

    def find_faces(self, image, depth):
        # print('I got a new image!')

        # Convert the images into a OpenCV (numpy) format
        try:
            rgb_image = self.bridge.imgmsg_to_cv2(image, "bgr8")
            depth_image = self.bridge.imgmsg_to_cv2(depth, "32FC1")
        except CvBridgeError as e:
            print(e)

        # Set the dimensions of the image
        self.dims = rgb_image.shape
        h = self.dims[0]
        w = self.dims[1]

        # Tranform image to gayscale
        # gray = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)

        # Do histogram equlization
        # img = cv2.equalizeHist(gray)

        # Detect the faces in the image
        # face_rectangles = self.face_detector(rgb_image, 0)
        blob = cv2.dnn.blobFromImage(cv2.resize(rgb_image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
        self.face_net.setInput(blob)
        face_detections = self.face_net.forward()

        for i in range(0, face_detections.shape[2]):

            confidence = face_detections[0, 0, i, 2]
            if confidence > 0.5:
                box = face_detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                box = box.astype('int')
                x1, y1, x2, y2 = box[0], box[1], box[2], box[3]
                # print(box)
                cv2.rectangle(rgb_image, (x1, y1), (x2, y2), 200, 1)
                # Extract region containing face
                face_region = rgb_image[y1:y2, x1:x2]

                # Visualize the extracted face
                # cv2.imshow("ImWindow", face_region)
                # cv2.waitKey(10)

                # Find the distance to the detected face
                face_distance = float(np.nanmean(depth_image[y1:y2, x1:x2]))

                # print('Distance to face', face_distance)

                # Get the time that the depth image was recieved
                depth_time = depth.header.stamp

                # Find the location of the detected face
                pose_stamped = self.get_pose((x1, x2, y1, y2), face_distance, depth_time)
                # print(pose)

                if pose_stamped is not None:
                    detected_person = FacePose()
                    face_encoding = face_recognition.face_encodings(face_region)
                    if (len(face_encoding) != 0):
                        for person in self.known_faces:
                            if (face_recognition.compare_faces([self.known_faces[person]], face_encoding[0], 0.5)[0]):
                                detected_person.name = person
                                print(detected_person.name)
                                detected_person.position = pose_stamped
                                detected_person.x1 = x1
                                detected_person.y1 = y1
                                detected_person.x2 = x2
                                detected_person.y2 = y2
                                self.face_pose_pub.publish(detected_person)

                ''' 



                    if len(face_encoding) != 0:





                        #for face in self.faces:

                        #    if not (abs(pose.pose.position.x - face.pose.pose.position.x) > 1 or abs(
                        #            pose.pose.position.y - face.pose.pose.position.y) > 1):
                                # faces are close, check if they are the same
                        #        if face_recognition.compare_faces([face.enc], face_encoding)[0]:
                        #            place_marker = False

                        face_name = ""

                        #for name, person in known_faces:

                        #    person_encoding = face_recognition.face_encodings(person)[0]

                        #    if face_recognition.compare_faces([person_encoding], face_encoding)[0]:
                        #       face_name = name

                        print(face_name)

                        self.marker_num += 1
                        face = Face(pose, face_encoding, self.marker_num, face_name)
                        self.faces.append(face)
                        self.marker_array.markers.append(face.to_marker())

                    faceMsg = FacePose()
                    faceMsg.position = pose
                    face_publisher = rospy.Publisher('detected_face', Face, queue_size=1)
                    face_publisher.publish(faceMsg)


                    self.markers_pub.publish(self.marker_array)'''


class Face:

    def __init__(self, pose, enc, mId, name):
        self.pose = pose
        self.enc = copy.deepcopy(enc)
        self.id = mId
        self.name = name

    def to_marker(self):
        marker = Marker()
        marker.header.frame_id = "map"
        marker.type = Marker.CUBE
        marker.action = Marker.ADD
        marker.frame_locked = False
        marker.scale = Vector3(0.1, 0.1, 0.1)
        marker.pose = self.pose.pose
        marker.color = ColorRGBA(0, 1, 0, 1)
        marker.id = self.id
        return marker


def main():
    face_finder = face_localizer()
    # rate = rospy.Rate(1)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
