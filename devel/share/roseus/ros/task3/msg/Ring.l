;; Auto-generated. Do not edit!


(when (boundp 'task3::Ring)
  (if (not (find-package "TASK3"))
    (make-package "TASK3"))
  (shadow 'Ring (find-package "TASK3")))
(unless (find-package "TASK3::RING")
  (make-package "TASK3::RING"))

(in-package "ROS")
;;//! \htmlinclude Ring.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(defclass task3::Ring
  :super ros::object
  :slots (_color _distance _position ))

(defmethod task3::Ring
  (:init
   (&key
    ((:color __color) "")
    ((:distance __distance) 0.0)
    ((:position __position) (instance geometry_msgs::PoseStamped :init))
    )
   (send-super :init)
   (setq _color (string __color))
   (setq _distance (float __distance))
   (setq _position __position)
   self)
  (:color
   (&optional __color)
   (if __color (setq _color __color)) _color)
  (:distance
   (&optional __distance)
   (if __distance (setq _distance __distance)) _distance)
  (:position
   (&rest __position)
   (if (keywordp (car __position))
       (send* _position __position)
     (progn
       (if __position (setq _position (car __position)))
       _position)))
  (:serialization-length
   ()
   (+
    ;; string _color
    4 (length _color)
    ;; float32 _distance
    4
    ;; geometry_msgs/PoseStamped _position
    (send _position :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _color
       (write-long (length _color) s) (princ _color s)
     ;; float32 _distance
       (sys::poke _distance (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; geometry_msgs/PoseStamped _position
       (send _position :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _color
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _color (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; float32 _distance
     (setq _distance (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; geometry_msgs/PoseStamped _position
     (send _position :deserialize buf ptr-) (incf ptr- (send _position :serialization-length))
   ;;
   self)
  )

(setf (get task3::Ring :md5sum-) "7bea905b7bcc3afe55c73f5ff0b51f52")
(setf (get task3::Ring :datatype-) "task3/Ring")
(setf (get task3::Ring :definition-)
      "string color
float32 distance
geometry_msgs/PoseStamped position

================================================================================
MSG: geometry_msgs/PoseStamped
# A Pose with reference coordinate frame and timestamp
Header header
Pose pose

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: geometry_msgs/Pose
# A representation of pose in free space, composed of position and orientation. 
Point position
Quaternion orientation

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w

")



(provide :task3/Ring "7bea905b7bcc3afe55c73f5ff0b51f52")


