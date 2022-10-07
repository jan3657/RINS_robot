#!/usr/bin/python3
import os
import warnings
from queue import Empty
import sys
import rospy
import cv2
import actionlib
import numpy as np
import random
import tf2_geometry_msgs
import tf2_ros
import tf
import copy
import math
from matplotlib import pyplot as plt

from os.path import dirname, join

from std_msgs.msg import String
from tf2_geometry_msgs import do_transform_point
from geometry_msgs.msg import PoseStamped, Quaternion, Point, PoseWithCovarianceStamped, TransformStamped, PoseArray
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionResult
from sensor_msgs.msg import Image
from geometry_msgs.msg import PointStamped, Vector3, Pose, Twist
from nav_msgs.msg import OccupancyGrid
from cv_bridge import CvBridge, CvBridgeError
from visualization_msgs.msg import Marker, MarkerArray
from std_msgs.msg import ColorRGBA
from actionlib_msgs.msg import GoalID
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from task3.msg import Ring
from task3.msg import Cylinder
from task3.msg import FacePose
from pathlib import Path


class Movement:

    def __init__(self):

        rospy.init_node('movement', anonymous=True)

        # subscribers
        self.result_sub = rospy.Subscriber(
            "/move_base/result", MoveBaseActionResult, self.result_sub_callback
        )
        self.ring_sub = rospy.Subscriber(
            "/detected_ring", Ring, self.find_rings_callback
        )
        self.cylinder_sub = rospy.Subscriber(
            "/detected_cylinder_color", Cylinder, self.find_cylinders_callback
        )
        self.face_sub = rospy.Subscriber(
            "/detected_face", FacePose, self.find_faces_callback
        )
        self.odom_sub = rospy.Subscriber(
            "/amcl_pose", PoseWithCovarianceStamped, self.amcl_callback
        )
        self.map_msg = rospy.wait_for_message("/map", OccupancyGrid)

        # publishers

        self.cancel_goal_publisher = rospy.Publisher(
            "/move_base/cancel", GoalID, queue_size=10
        )
        self.pose_pub = rospy.Publisher(
            "/move_base_simple/goal", PoseStamped, queue_size=10
        )
        self.markers_pub = rospy.Publisher(
            'MarkerArray', MarkerArray, queue_size=1000
        )
        self.cancel_goal_pub = rospy.Publisher(
            "/move_base/cancel", GoalID, queue_size=10
        )
        self.twist_pub = rospy.Publisher(
            "/cmd_vel_mux/input/teleop", Twist, queue_size=10
        )
        self.arm_control_pub = rospy.Publisher(
            "/arm_command", String, queue_size=10
        )
        self.food_image_pub = rospy.Publisher(
            "/food_image", Image, queue_size=10
        )
        self.food_message_pub = rospy.Publisher(
            "/food_msg_command", String, queue_size=10
        )
        self.speech_message_pub = rospy.Publisher(
            "/speech_msg_command", String, queue_size=10
        )

        self.tf_buf = tf2_ros.Buffer()
        self.tf2_listener = tf2_ros.TransformListener(self.tf_buf)

        self.bridge = CvBridge()

        self.seq = 0

        self.marker_array = MarkerArray()
        self.face_marker_num = 1
        self.ring_marker_num = 1
        self.cylinder_marker_num = 1
        self.marker_numb = 1

        self.faces = list()
        self.rings = list()
        self.cylinders = list()

        self.number_of_rings = 4
        self.number_of_cylinders = 4

        self.state = "get_next_waypoint"
        self.robot_pose = Pose()

        self.objectLocationX = 0.0
        self.objectLocationY = 0.0

        self.params = {
            "horizontal_space": 100,
            "vertical_space": 170,
            "cylinder_detection_min_dis": 0.6
        }

        # Ring and cylinder approach
        self.forward_counter = 0
        self.back_counter = None
        self.move_forward = False
        self.last_turn = None
        self.goal_reached = False
        self.cylinder_color = ""

        # Map and segmentation
        mod_path = Path(__file__).parent
        relative_path = '../maps'
        src_path_1 = (mod_path / relative_path).resolve()
        img_path = str(src_path_1) + "/good_map_fixed.pgm"
        self.map = cv2.imread(img_path)
        self.map_width = self.map.shape[0]
        self.map_height = self.map.shape[1]
        self.distance_from_wall = 10  # How close to the face do you want to get ?

        self.ring_approaching_points = list()

        self.orders = list()
        self.delivery_order = list()
        self.QR_location = None

    def mover(self):

        waypoints = [[-0.27499982230365205, 2.375000217184425], [0.8500001944601543, 2.400000217556954],
                     [0.9250001955777414, 1.375000202283264], [1.0500001974403865, 0.30000018626451563],
                     [2.225000214949251, 0.2750001858919866], [2.375000217184425, 1.375000202283264],
                     [1.9250002104789026, 2.425000217929483], [-0.224999821558594, 0.625000191107393],
                     [-0.19999982118606496, -0.5999998271465294], [-1.4249998394399874, -0.12499982006847787],
                     [-1.4249998394399874, 1.7750002082437284], [1.0000001966953285, -1.3499998383224003],
                     [2.25000021532178, -0.8499998308718197], [3.200000229477883, -0.34999982342123914]]

        i = 0

        rate = rospy.Rate(1)

        while self.pose_pub.get_num_connections() < 1:
            rate.sleep()

        while not rospy.is_shutdown():
            # print("status = ",self.state)
            # print("Numb of rings : ",len(self.rings), "Numb of Cili", len(self.cylinders))

            if self.state == "parking":

                self.cancel_goal_publisher.publish(GoalID())
                self.state = "approach_parking"

                if self.ring_approaching_points:

                    print("Going to park!")
                    self.move_to(1, 1, self.ring_approaching_points[0])
                    #self.ring_approaching_points.clear()
                else:
                    print("I checked all possible locations and couldn't find my parking spot.")

            #elif self.state == "check_parking":

                #self.arm_control_pub.publish("extend")
                #rospy.sleep(3)
                #self.arm_control_pub.publish("retract")
                #self.state = "parking"

            elif self.state == "read_qr":

                print("Reading QR code.")
                order_msg = str(rospy.wait_for_message("/order_msg", String))
                order_msg = order_msg[9:-2]
                print(order_msg)

                if order_msg == "No QR code found.":
                    print(order_msg)
                    print("Checking next location.")
                    self.state = "parking"
                    self.ring_approaching_points.pop(0)

                else:
                    self.QR_location = self.ring_approaching_points[0]
                    order_msg = str(rospy.wait_for_message("/order_msg", String))
                    order_msg = order_msg[9:-2]
                    temp_order = order_msg.split(', ')

                    for order in temp_order:
                        self.orders.append(order.split(" "))

                    self.state = "process_order"

            elif self.state == "process_order":

                for order in self.orders:

                    person = order[0]
                    food = order[1]

                    for cylinder in self.cylinders:
                        if cylinder.food == food:
                            self.delivery_order.append(("food", cylinder.pose.point.x, cylinder.pose.point.y))

                    for face in self.faces:
                        if face.name == person:
                            self.delivery_order.append(("face", face.goal_pose))

                self.state = "begin_delivery"

            elif self.state == "begin_delivery":

                if self.delivery_order:
                    go_to = self.delivery_order[0]
                    print("Number of locations left to visit:", len(self.delivery_order))
                    self.delivery_order.pop(0)

                    if go_to[0] == "face":
                        self.state = "move_to_face"
                        self.move_to(1, 1, go_to[1])

                    else:
                        self.state = "move_to_restaurant"
                        self.move_to(1, 1, self.find_pose_goal(go_to[1], go_to[2]))

                else:
                    self.state = "going_home"
                    print("All food delivered!")

            elif self.state == "going_home":
                print("I'm going home after a hard day's work. :)")
                self.state = "END"
                self.move_to(1, 1, self.QR_location)

            elif self.state == "talk_to_face":

                print("R: Hey, {}! Here is your {} order.".format(self.orders[0][0], self.orders[0][1]))
                print("P: Thank you.")
                print("R: Will you pay with cash or credit card?")

                self.speech_message_pub.publish("SPEAK")
                human_input = str(rospy.wait_for_message("/speech_msg", String))

                if human_input:
                    print("H: {}".format(human_input[7:-1]).capitalize())

                    if "card" in human_input:
                        self.arm_control_pub.publish("right")
                        rospy.sleep(2)
                        self.arm_control_pub.publish("retract")
                    elif "cash" in human_input:
                        self.arm_control_pub.publish("left")
                        rospy.sleep(2)
                        self.arm_control_pub.publish("retract")

                    rospy.sleep(2)

                human_input = ""

                print("R: How satisfied were you with the service on the scale from 1 to 5?")
                self.speech_message_pub.publish("SPEAK")
                human_input = str(rospy.wait_for_message("/speech_msg", String))

                if human_input:
                    human_input = human_input[7:-1]
                    print("H: {}".format(human_input))
                    if "1" in human_input or "2" in human_input:
                        print("R: {}... I'm sorry to hear that. I'll do a better job next time!".format(human_input))
                    elif "3" in human_input:
                        print("R: {}! Not great, not terrible. I'll try harder next time!".format(human_input))
                    elif "4" in human_input or "5" in human_input:
                        print("R: {}! Thank you!".format(human_input))

                self.orders.pop(0)
                self.state = "begin_delivery"

            elif self.state == "talk_to_restaurant":
                print("R: Hello! One {}, please.".format(self.orders[0][1]))
                self.state = "begin_delivery"

            elif self.number_of_rings == len(self.rings) and self.number_of_cylinders == len(self.cylinders) and self.state == "get_next_waypoint":
                self.state = "ring_state"
                self.cancel_goal_publisher.publish(GoalID())
                rospy.sleep(1)

                self.find_ring_approaching_point()

            elif self.state == "get_next_waypoint":

                self.state = "moving"
                i = (i % (len(waypoints) - 1)) + 1
                self.move_to(waypoints[i][0], waypoints[i][1])

            elif self.state == "moving":
                pass

            elif self.state == "cylinder_approach":
                self.cylinder_approach()

            rate.sleep()

    def find_rings_callback(self, data):

        place_marker = True

        if self.rings:
            for ring in self.rings:
                if (np.sqrt((data.position.pose.position.x - ring.pose.pose.position.x) ** 2 + (
                        data.position.pose.position.y - ring.pose.pose.position.y) ** 2) < 1):
                    place_marker = False
                    if data.distance < ring.distance:
                        ring.pose = data.position

        if place_marker and len(self.rings) < self.number_of_rings:
            pose = data.position
            color = data.color
            ring = Ringy(pose, self.marker_numb, color, data.distance)
            self.ring_marker_num += 1
            self.marker_numb += 1
            self.rings.append(ring)
            self.marker_array.markers.append(ring.to_marker())
            self.objectLocationX = data.position.pose.position.x
            self.objectLocationY = data.position.pose.position.y
            print("Hello", color, "ring")

        self.markers_pub.publish(self.marker_array)

    def find_ring_approaching_point(self):

        #cwd = Path.cwd()
        #mod_path = Path(__file__).parent
        #relative_path = '../maps'
        #src_path_1 = (mod_path / relative_path).resolve()
        #img_path = str(src_path_1) + "/good_map_fixed.pgm"
        #map = cv2.imread(img_path)
        #map = cv2.imread("/home/mateja/Rins2/src/task3/scripts/cake/good_map_fixed.pgm")
        #map_copy = cv2.imread("/home/mateja/Rins2/src/task3/scripts/cake/good_map_fixed.pgm")
        width, height, _ = self.map.shape
        h_x0 = 0
        h_y0 = int(height / 2)
        h_x1 = width
        h_y1 = int(height / 2)
        horizontal_line = ((h_x0, h_y0), (h_x1, h_y1))

        dx = h_x1 - h_x0
        dy = h_y1 - h_y0

        a = (dx * dx - dy * dy) / (dx * dx + dy * dy)
        b = 2 * dx * dy / (dx * dx + dy * dy)

        px = 0
        py = 0

        for ring in self.rings:
            if ring.color == "green":
                x = int((ring.pose.pose.position.x + 12.2) / 0.05)
                y = int((ring.pose.pose.position.y + 12.2) / 0.05)

                px = int(a * (x - h_x0) + b * (y - h_y0) + h_x0)
                py = int(b * (x - h_x0) - a * (y - h_y0) + h_y0)

        region = self.try_column(self.map, px, py)
        pixel_locations = self.find_column(region)

        visit_locations = list()

        for pixel in pixel_locations:
            if self.check_wall(self.map, pixel[0], pixel[1]):
                visit_locations.append(pixel)

        lx = 0
        ly = 0
        temp_points = list()

        for location in visit_locations:

            dist = math.dist((location[0], location[1]), (px, py))

            lx = (a * (location[0] - h_x0) + b * (location[1] - h_y0) + h_x0)
            ly = (b * (location[0] - h_x0) - a * (location[1] - h_y0) + h_y0)

            x = (lx * 0.05) - 12.2
            y = (ly * 0.05) - 12.2

            temp_points.append((dist, x, y, location[2]))

        temp_points.sort(key=lambda a: a[0])

        for i in range(0, 4):
            goal_pose = Pose()
            goal_pose.position.x = float(temp_points[i][1])
            goal_pose.position.y = float(temp_points[i][2])
            direction = temp_points[i][3]

            if direction == "up":
                goal_pose.orientation.z = -0.7
                goal_pose.orientation.w = 0.7
            elif direction == "down":
                goal_pose.orientation.z = 0.7
                goal_pose.orientation.w = 0.7
            elif direction == "right":
                goal_pose.orientation.z = -1
            else:
                goal_pose.orientation.w = 1

            self.ring_approaching_points.append(goal_pose)

        self.state = "parking"

    def try_column(self, map, px, py):

        region = np.zeros(map.shape)
        region.fill(255)
        region[py - 15: py + 15, px - 15: px + 15] = map[py - 15: py + 15, px - 15: px + 15]

        return region

    def find_column(self, map):

        region = map.astype(np.uint8)

        gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        gray = 255 - gray

        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        x = 0
        y = 0
        w = 0
        h = 0

        for c in cnts:
            result = np.full_like(region, (255, 255, 255))
            x, y, w, h = cv2.boundingRect(c)

        pixel_locations = [(x + w - 1 + self.distance_from_wall, y + int(h / 2), "right"),
                           (x - self.distance_from_wall, y + int(h / 2), "left"),
                           (x + int(w / 2), y - self.distance_from_wall, "up"),
                           (x + int(w / 2), y + h + self.distance_from_wall, "down")]

        return pixel_locations

    def check_wall(self, map, x, y):

        region = map[y - 5 : y + 5, x - 5 : x + 5]

        mask = 255 * ((region[:, :, 0] == 0) & (region[:, :, 1] == 0) & (region[:, :, 2] == 0))
        number_of_black = cv2.countNonZero(mask)

        if number_of_black == 0:
            return True
        else:
            return False

    def find_cylinders_callback(self, data):

        place_marker = True

        if self.cylinders:
            for cylinder in self.cylinders:
                if not (abs(data.position.point.x - cylinder.pose.point.x) > 1 or abs(
                        data.position.point.y - cylinder.pose.point.y) > 1):
                    place_marker = False

        if place_marker:
            self.state = "move_to_remembered_point"
            pose = data.position
            color = data.color
            cylinder = Cylindy(pose, self.marker_numb, "", color, self.robot_pose)
            print("Hello", color, "cylinder")
            self.cylinder_marker_num += 1
            self.marker_numb += 1
            self.cylinders.append(cylinder)
            self.marker_array.markers.append(cylinder.to_marker())
            self.move_to(1, 1, self.find_pose_goal(data.position.point.x, data.position.point.y))

        self.markers_pub.publish(self.marker_array)

    def find_faces_callback(self, data):

        place_marker = True

        if self.faces:
            for face in self.faces:
                if (np.sqrt((data.position.pose.position.x - face.pose_stamped.pose.position.x) ** 2) + ((
                        data.position.pose.position.y - face.pose_stamped.pose.position.y) ** 2) < 1):
                    # faces close, check if they are the same
                    #if face.name == data.name:
                    place_marker = False

        if place_marker:
            print("Hello", data.name)
            goal_pose = self.find_face_goal(data)
            detected_face = Face(data.position, self.marker_numb, data.name, self.robot_pose, goal_pose)
            self.faces.append(detected_face)
            self.face_marker_num += 1
            self.marker_numb += 1
            self.marker_array.markers.append(detected_face.to_marker())

        self.markers_pub.publish(self.marker_array)

    def move_to(self, x_goal=None, y_goal=None, pose=None):
        msg = PoseStamped()
        msg.header.frame_id = "map"
        msg.header.seq = self.seq
        msg.header.stamp = rospy.Time.now()

        if pose is not None:
            msg.pose = pose
        else:
            msg.pose.position.x = x_goal
            msg.pose.position.y = y_goal
            msg.pose.orientation.w = 1.0

        self.pose_pub.publish(msg)

    def result_sub_callback(self, data):

        res_status = data.status.status
        # print("Res status: ", res_status)
        # print("Self state: ", self.state)
        # print("Numb of rings : ",len(self.rings), "Numb of Cili", len(self.cylinders))

        if self.state == "moving":
            if res_status == 3 or res_status == 4:
                self.seq += 1
                self.state = "get_next_waypoint"

        elif self.state == "approach_parking":
            if res_status == 3 or res_status == 4:
                #self.state = "check_parking"
                self.state = "read_qr"
                #self.state = "end"

        elif self.state == "move_to_remembered_point":
            if res_status == 3 or res_status == 4:
                self.state = "cylinder_approach"

        elif self.state == "move_to_face":
            if res_status == 3 or res_status ==4:
                self.state = "talk_to_face"

        elif self.state == "move_to_restaurant":
            if res_status == 3 or res_status ==4:
                self.state = "talk_to_restaurant"

    def cylinder_approach(self):

        warnings.filterwarnings(action='ignore', message='Mean of empty slice')
        color = self.cylinder_color

        try:
            image = self.bridge.imgmsg_to_cv2(
                rospy.wait_for_message("/camera/rgb/image_raw", Image), "bgr8"
            )
        except CvBridgeError as e:
            print(e)

        lower_limit = np.array([0, 10, 65])
        upper_limit = np.array([255, 255, 255])

        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(
            hsv_image, lower_limit, upper_limit
        )
        countour, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(countour) > 0:
            depth_image = rospy.wait_for_message("/camera/depth/image_raw", Image)
            depth_image = self.bridge.imgmsg_to_cv2(depth_image, "32FC1")

            y = int(image.shape[0] / 2)
            x = int(image.shape[1] / 2)

            yd = int(depth_image.shape[0] / 2)
            xd = int(depth_image.shape[1] / 2)
            dist = np.nanmean(depth_image[yd - 5: yd + 5, xd - 5: xd + 5])

            cont = max(countour, key=cv2.contourArea)
            m = cv2.moments(cont)
            cx = int(m["m10"] / m["m00"])
            cy = int(m["m01"] / m["m00"])

            c_dist = depth_image[cy, cx]

            cv2.circle(image, (cx, cy), 3, (0, 255, 0))
            cv2.drawContours(image, [cont], -1, (0, 255, 0), 2)

            image[
            self.params["vertical_space"]: -self.params["vertical_space"],
            0: self.params["horizontal_space"],
            ] = (0, 0, 255)

            image[
            self.params["vertical_space"]: -self.params["vertical_space"],
            image.shape[1] - self.params["horizontal_space"]:,
            ] = (0, 0, 255)

            temp_left = list()
            for i in range(
                    self.params["vertical_space"],
                    depth_image.shape[0] - self.params["vertical_space"],
            ):
                for j in range(self.params["horizontal_space"]):
                    if mask[i, j] != 255:
                        temp_left.append(depth_image[i, j])
            temp_left = np.array(temp_left)

            temp_right = list()
            for i in range(
                    self.params["vertical_space"],
                    depth_image.shape[0] - self.params["vertical_space"],
            ):
                for j in range(
                        depth_image.shape[1] - self.params["horizontal_space"],
                        depth_image.shape[1],
                ):
                    if mask[i, j] != 255:
                        temp_right.append(depth_image[i, j])
            temp_right = np.array(temp_right)

            left = np.nanmean(temp_left)
            right = np.nanmean(temp_right)

            msg = Twist()

            if not self.goal_reached:
                if self.last_turn != None and cy < 100:
                    if self.last_turn == "left":
                        msg.angular.z = -0.5
                    else:
                        msg.angular.z = 0.5

                if (np.isnan(left) or left < 0.5) and c_dist > self.params[
                    "cylinder_detection_min_dis"
                ]:
                    msg.angular.z = -0.5
                    self.last_turn = "right"
                    self.move_forward = 1
                elif (np.isnan(right) or right < 0.5) and c_dist > self.params[
                    "cylinder_detection_min_dis"
                ]:
                    msg.angular.z = 0.5
                    self.last_turn = "left"
                    self.move_forward = 1
                elif self.move_forward > 0:
                    self.move_forward -= 1
                    if c_dist > self.params["cylinder_detection_min_dis"]:
                        msg.linear.x = 0.2
                    elif c_dist > 0.5:
                        msg.linear.x = 0.05
                    elif c_dist > 0.4:
                        msg.linear.x = 0.01
                    else:
                        self.move_forward = 0
                elif self.last_turn != None:
                    self.last_turn = None
                    if c_dist > self.params["cylinder_detection_min_dis"]:
                        if self.last_turn == "left":
                            msg.angular.z = -0.5
                        else:
                            msg.angular.z = 0.5
                else:
                    # Set rotation step
                    step = 0.15
                    if abs(cx - x) < 5:
                        step = 0.005
                    elif abs(cx - x) < 20:
                        step = 0.01
                    elif abs(cx - x) < 30:
                        step = 0.03
                    elif abs(cx - x) < 50:
                        step = 0.1

                    if abs(cx - x) < 2:
                        if not np.isnan(dist):
                            if dist > 0.55:
                                msg.linear.x = 0.3
                            elif dist > 0.46:
                                msg.linear.x = 0.1
                            else:
                                msg.linear.x = 0.01
                        elif self.forward_counter < 12:
                            msg.linear.x = 0.01
                            self.forward_counter += 1
                        elif self.forward_counter < 17:
                            msg.linear.x = 0.005
                            self.forward_counter += 1
                        else:
                            self.arm_control_pub.publish("lift")
                            rospy.sleep(5)
                            try:
                               food_image = self.bridge.imgmsg_to_cv2(
                                   rospy.wait_for_message("/arm_camera/rgb/image_raw", Image), "bgr8"
                               )
                            except CvBridgeError as e:
                               print(e)

                            cwd = Path.cwd()
                            mod_path = Path(__file__).parent
                            relative_path = '../scripts/cake'
                            src_path_1 = (mod_path / relative_path).resolve()
                            # img_path = str(src_path_1) + "/good_map_fixed.pgm"
                            #images_path = '/home/mateja/Rins2/src/task3/scripts/cake'
                            os.chdir(src_path_1)
                            cv2.imwrite('food.jpg', food_image)

                            self.food_message_pub.publish("yep")

                            food_name = str(rospy.wait_for_message("/food_msg", String))
                            food_name = food_name[7:-1]
                            print("I found a restaurant that serves {}.".format(food_name))
                            self.cylinders[-1].food = food_name

                            self.arm_control_pub.publish("retract")
                            self.goal_reached = True
                            self.back_counter = 2
                    else:
                        if cx > x:
                            msg.angular.z = -step
                        elif cy < x:
                            msg.angular.z = step
            else:
                if self.back_counter > 0:
                    msg.linear.x = -0.2
                    self.back_counter -= 1
                else:
                    self.forward_counter = 0
                    self.move_forward = 0
                    self.last_turn = None
                    self.goal_reached = False
                    self.back_counter = None
                    self.state = "get_next_waypoint"

            self.twist_pub.publish(msg)

    def amcl_callback(self, data):
        self.robot_pose = data.pose.pose

    def find_pose_goal(self, x=None, y=None, face_pose=None):
        if (face_pose != None):
            x = int((face_pose.position.pose.position.x + 12.2) / 0.05)
            y = int((face_pose.position.pose.position.y + 12.2) / 0.05)
        else:
            x = int((x + 12.2) / 0.05)
            y = int((y + 12.2) / 0.05)

        px = int(x)
        py = int(self.map_height - y)

        map = cv2.circle(self.map, (0, 0), radius=0,
                         color=(0, 255, 0), thickness=1)
        closest_wall_x = px
        closest_wall_y = py
        wall_location = ""
        step = 1
        if ((map[py][px] == [255, 255, 255]).all()):
            while (px + step < 480 and px - step > 0 and py + step < 480 and py - step > 0):
                if ((map[py + step][px] == [0, 0, 0]).all()):
                    closest_wall_y = py + step
                    closest_wall_x = px
                    wall_location = "up"
                    break
                elif ((map[py - step][px] == [0, 0, 0]).all()):
                    closest_wall_y = py - step
                    closest_wall_x = px
                    wall_location = "down"
                    break
                elif ((map[py][px + step] == [0, 0, 0]).all()):
                    closest_wall_y = py
                    closest_wall_x = px + step
                    wall_location = "right"
                    break
                elif ((map[py][px - step] == [0, 0, 0]).all()):
                    closest_wall_y = py
                    closest_wall_x = px - step
                    wall_location = "left"
                    break
                else:
                    step += 1

        elif ((map[py][px] == [0, 0, 0]).all()):
            while (px + step < 480 and px - step > 0 and py + step < 480 and py - step > 0):
                if ((map[py + step][px] == [255, 255, 255]).all()):
                    closest_wall_y = py + step
                    closest_wall_x = px
                    wall_location = "down"
                    break
                elif ((map[py - step][px] == [255, 255, 255]).all()):
                    closest_wall_y = py - step
                    closest_wall_x = px
                    wall_location = "up"
                    break
                elif ((map[py][px + step] == [255, 255, 255]).all()):
                    closest_wall_y = py
                    closest_wall_x = px + step
                    wall_location = "left"
                    break
                elif ((map[py][px - step] == [255, 255, 255]).all()):
                    closest_wall_y = py
                    closest_wall_x = px - step
                    wall_location = "right"
                    break
                else:
                    step += 1

        goal_pose = Pose()

        if wall_location == "up":
            goal_x = closest_wall_x
            goal_y = closest_wall_y - self.distance_from_wall
            goal_pose.orientation.z = -0.7
            goal_pose.orientation.w = 0.7
        elif wall_location == "down":
            goal_x = closest_wall_x
            goal_y = closest_wall_y + self.distance_from_wall
            goal_pose.orientation.z = 0.7
            goal_pose.orientation.w = 0.7
        elif wall_location == "left":
            goal_x = closest_wall_x + self.distance_from_wall
            goal_y = closest_wall_y
            goal_pose.orientation.z = -1
        else:
            goal_x = closest_wall_x - self.distance_from_wall
            goal_y = closest_wall_y
            goal_pose.orientation.w = 1

        goal_pose.position.x = (goal_x * 0.05) - 12.2
        goal_pose.position.y = ((self.map_height - goal_y) * 0.05) - 12.2

        # ---------------------------Show image for debuging-------------------------------
        # map = cv2.circle(map, (goal_x, goal_y), radius=0, color=(255, 0, 0), thickness=2)
        # res = map [170:290,180:340]
        # res = cv2.pyrUp(res,dstsize=(int((340-180) * 2),int((290-170) *2)))
        # cv2.imshow("res2",res)
        # cv2.waitKey(1)
        # ---------------------------------------------------------------------------------

        return goal_pose

    def find_face_goal(self, face_pose):
        x = int((face_pose.position.pose.position.x + 12.2) / 0.05)
        y = int((face_pose.position.pose.position.y + 12.2) / 0.05)

        px = int(x)
        py = int(self.map_height - y)

        map = cv2.circle(self.map, (0, 0), radius=0,
                         color=(0, 255, 0), thickness=1)
        closest_wall_x = px
        closest_wall_y = py
        wall_location = ""
        step = 1
        if ((map[py][px] == [255, 255, 255]).all()):
            while (px + step < 480 and px - step > 0 and py + step < 480 and py - step > 0):
                if ((map[py + step][px] == [0, 0, 0]).all()):
                    closest_wall_y = py + step
                    closest_wall_x = px
                    wall_location = "up"
                    break
                elif ((map[py - step][px] == [0, 0, 0]).all()):
                    closest_wall_y = py - step
                    closest_wall_x = px
                    wall_location = "down"
                    break
                elif ((map[py][px + step] == [0, 0, 0]).all()):
                    closest_wall_y = py
                    closest_wall_x = px + step
                    wall_location = "right"
                    break
                elif ((map[py][px - step] == [0, 0, 0]).all()):
                    closest_wall_y = py
                    closest_wall_x = px - step
                    wall_location = "left"
                    break
                else:
                    step += 1

        elif ((map[py][px] == [0, 0, 0]).all()):
            while (px + step < 480 and px - step > 0 and py + step < 480 and py - step > 0):
                if ((map[py + step][px] == [255, 255, 255]).all()):
                    closest_wall_y = py + step
                    closest_wall_x = px
                    wall_location = "down"
                    break
                elif ((map[py - step][px] == [255, 255, 255]).all()):
                    closest_wall_y = py - step
                    closest_wall_x = px
                    wall_location = "up"
                    break
                elif ((map[py][px + step] == [255, 255, 255]).all()):
                    closest_wall_y = py
                    closest_wall_x = px + step
                    wall_location = "left"
                    break
                elif ((map[py][px - step] == [255, 255, 255]).all()):
                    closest_wall_y = py
                    closest_wall_x = px - step
                    wall_location = "right"
                    break
                else:
                    step += 1

        goal_pose = Pose()

        if wall_location == "up":
            goal_x = closest_wall_x
            goal_y = closest_wall_y - self.distance_from_wall
            goal_pose.orientation.z = -0.7
            goal_pose.orientation.w = 0.7
        elif wall_location == "down":
            goal_x = closest_wall_x
            goal_y = closest_wall_y + self.distance_from_wall
            goal_pose.orientation.z = 0.7
            goal_pose.orientation.w = 0.7
        elif wall_location == "left":
            goal_x = closest_wall_x + self.distance_from_wall
            goal_y = closest_wall_y
            goal_pose.orientation.z = -1
        else:
            goal_x = closest_wall_x - self.distance_from_wall
            goal_y = closest_wall_y
            goal_pose.orientation.w = 1

        goal_pose.position.x = (goal_x * 0.05) - 12.2
        goal_pose.position.y = ((self.map_height - goal_y) * 0.05) - 12.2

        # ---------------------------Show image for debuging-------------------------------
        # map = cv2.circle(map, (goal_x, goal_y), radius=0, color=(255, 0, 0), thickness=2)
        # res = map [170:290,180:340]
        # res = cv2.pyrUp(res,dstsize=(int((340-180) * 2),int((290-170) *2)))
        # cv2.imshow("res2",res)
        # cv2.waitKey(1)
        # ---------------------------------------------------------------------------------

        return goal_pose

class Ringy:

    def __init__(self, pose, rId, color, distance):
        self.distance = distance
        self.pose = pose
        self.id = rId
        self.color = color
        if self.color == "red":
            self.rgba = [1, 0, 0, 1]
        elif self.color == "green":
            self.rgba = [0, 1, 0, 1]
        elif self.color == "blue":
            self.rgba = [0, 0, 1, 1]
        elif self.color == "cyan":
            self.rgba = [0, 1, 1, 1]
        elif self.color == "magenta":
            self.rgba = [1, 0, 1, 1]
        elif self.color == "yellow":
            self.rgba = [1, 1, 0, 1]
        elif self.color == "black":
            self.rgba = [0, 0, 0, 1]
        elif self.color == "gray":
            self.rgba = [0, 0, 0, 1]

    def to_marker(self):
        marker = Marker()
        # marker.header.stamp = self.pose.header.stamp
        # marker.header.frame_id = self.pose.header.frame_id
        marker.header.frame_id = "map"
        marker.type = Marker.CUBE
        marker.action = Marker.ADD
        marker.frame_locked = False
        marker.scale = Vector3(0.1, 0.1, 0.1)
        # marker.scale = Vector3(1, 1, 1)
        marker.pose = self.pose.pose
        # marker.color = ColorRGBA(0, 1, 0, 1)
        marker.color = ColorRGBA(self.rgba[0], self.rgba[1], self.rgba[2], self.rgba[3])
        marker.id = self.id
        return marker

class Cylindy:

    def __init__(self, pose, cId, food, color, robot_pose):
        self.pose = pose
        self.id = cId
        self.food = food
        self.color = color
        self.robot_pose = robot_pose

        if self.color == "red":
            self.rgba = [1, 0, 0, 1]
        elif self.color == "green":
            self.rgba = [0, 1, 0, 1]
        elif self.color == "blue":
            self.rgba = [0, 0, 1, 1]
        elif self.color == "cyan":
            self.rgba = [0, 1, 1, 1]
        elif self.color == "magenta":
            self.rgba = [1, 0, 1, 1]
        elif self.color == "yellow":
            self.rgba = [1, 1, 0, 1]
        elif self.color == "black":
            self.rgba = [0, 0, 0, 1]
        elif self.color == "gray":
            self.rgba = [0, 0, 0, 1]

    def to_marker(self):

        marker = Marker()
        # marker.header.stamp = self.point_world.header.stamp
        # marker.header.frame_id = self.point_world.header.frame_id
        marker.header.frame_id = "map"
        marker.type = Marker.CYLINDER
        marker.action = Marker.ADD
        marker.frame_locked = False
        marker.scale = Vector3(0.1, 0.1, 0.1)
        marker.pose.position.x = self.pose.point.x
        marker.pose.position.y = self.pose.point.y
        marker.pose.position.z = self.pose.point.z
        # marker.color = ColorRGBA(0, 1, 0, 1)
        marker.color = ColorRGBA(self.rgba[0], self.rgba[1], self.rgba[2], self.rgba[3])
        marker.id = self.id
        return marker

class Face:

    def __init__(self, pose, fId, name, robot_pose, goal_pose):
        self.goal_pose = goal_pose
        self.pose_stamped = pose
        self.id = fId
        self.name = name
        self.robot_pose = robot_pose

    def to_marker(self):
        marker = Marker()
        marker.header.frame_id = "map"
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        marker.frame_locked = False
        marker.scale = Vector3(0.1, 0.1, 0.1)
        marker.pose = self.pose_stamped.pose
        marker.color = ColorRGBA(1, 1, 1, 1)
        marker.id = self.id
        return marker

def main():
    move = Movement()
    rate = rospy.Rate(1)
    move.mover()

if __name__ == '__main__':
    main()

