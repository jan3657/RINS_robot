;; Auto-generated. Do not edit!


(when (boundp 'task3::FacePose)
  (if (not (find-package "TASK3"))
    (make-package "TASK3"))
  (shadow 'FacePose (find-package "TASK3")))
(unless (find-package "TASK3::FACEPOSE")
  (make-package "TASK3::FACEPOSE"))

(in-package "ROS")
;;//! \htmlinclude FacePose.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(defclass task3::FacePose
  :super ros::object
  :slots (_name _position _x1 _y1 _x2 _y2 ))

(defmethod task3::FacePose
  (:init
   (&key
    ((:name __name) "")
    ((:position __position) (instance geometry_msgs::PoseStamped :init))
    ((:x1 __x1) 0)
    ((:y1 __y1) 0)
    ((:x2 __x2) 0)
    ((:y2 __y2) 0)
    )
   (send-super :init)
   (setq _name (string __name))
   (setq _position __position)
   (setq _x1 (round __x1))
   (setq _y1 (round __y1))
   (setq _x2 (round __x2))
   (setq _y2 (round __y2))
   self)
  (:name
   (&optional __name)
   (if __name (setq _name __name)) _name)
  (:position
   (&rest __position)
   (if (keywordp (car __position))
       (send* _position __position)
     (progn
       (if __position (setq _position (car __position)))
       _position)))
  (:x1
   (&optional __x1)
   (if __x1 (setq _x1 __x1)) _x1)
  (:y1
   (&optional __y1)
   (if __y1 (setq _y1 __y1)) _y1)
  (:x2
   (&optional __x2)
   (if __x2 (setq _x2 __x2)) _x2)
  (:y2
   (&optional __y2)
   (if __y2 (setq _y2 __y2)) _y2)
  (:serialization-length
   ()
   (+
    ;; string _name
    4 (length _name)
    ;; geometry_msgs/PoseStamped _position
    (send _position :serialization-length)
    ;; uint64 _x1
    8
    ;; uint64 _y1
    8
    ;; uint64 _x2
    8
    ;; uint64 _y2
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _name
       (write-long (length _name) s) (princ _name s)
     ;; geometry_msgs/PoseStamped _position
       (send _position :serialize s)
     ;; uint64 _x1
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _x1 (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _x1) (= (length (_x1 . bv)) 2)) ;; bignum
              (write-long (ash (elt (_x1 . bv) 0) 0) s)
              (write-long (ash (elt (_x1 . bv) 1) -1) s))
             ((and (class _x1) (= (length (_x1 . bv)) 1)) ;; big1
              (write-long (elt (_x1 . bv) 0) s)
              (write-long (if (>= _x1 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _x1 s)(write-long (if (>= _x1 0) 0 #xffffffff) s)))
     ;; uint64 _y1
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _y1 (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _y1) (= (length (_y1 . bv)) 2)) ;; bignum
              (write-long (ash (elt (_y1 . bv) 0) 0) s)
              (write-long (ash (elt (_y1 . bv) 1) -1) s))
             ((and (class _y1) (= (length (_y1 . bv)) 1)) ;; big1
              (write-long (elt (_y1 . bv) 0) s)
              (write-long (if (>= _y1 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _y1 s)(write-long (if (>= _y1 0) 0 #xffffffff) s)))
     ;; uint64 _x2
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _x2 (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _x2) (= (length (_x2 . bv)) 2)) ;; bignum
              (write-long (ash (elt (_x2 . bv) 0) 0) s)
              (write-long (ash (elt (_x2 . bv) 1) -1) s))
             ((and (class _x2) (= (length (_x2 . bv)) 1)) ;; big1
              (write-long (elt (_x2 . bv) 0) s)
              (write-long (if (>= _x2 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _x2 s)(write-long (if (>= _x2 0) 0 #xffffffff) s)))
     ;; uint64 _y2
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _y2 (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _y2) (= (length (_y2 . bv)) 2)) ;; bignum
              (write-long (ash (elt (_y2 . bv) 0) 0) s)
              (write-long (ash (elt (_y2 . bv) 1) -1) s))
             ((and (class _y2) (= (length (_y2 . bv)) 1)) ;; big1
              (write-long (elt (_y2 . bv) 0) s)
              (write-long (if (>= _y2 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _y2 s)(write-long (if (>= _y2 0) 0 #xffffffff) s)))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _name
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _name (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; geometry_msgs/PoseStamped _position
     (send _position :deserialize buf ptr-) (incf ptr- (send _position :serialization-length))
   ;; uint64 _x1
     
#+(or :alpha :irix6 :x86_64)
      (setf _x1 (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _x1 (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; uint64 _y1
     
#+(or :alpha :irix6 :x86_64)
      (setf _y1 (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _y1 (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; uint64 _x2
     
#+(or :alpha :irix6 :x86_64)
      (setf _x2 (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _x2 (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; uint64 _y2
     
#+(or :alpha :irix6 :x86_64)
      (setf _y2 (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _y2 (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;;
   self)
  )

(setf (get task3::FacePose :md5sum-) "fba59784293eab073312c8d62c229f5c")
(setf (get task3::FacePose :datatype-) "task3/FacePose")
(setf (get task3::FacePose :definition-)
      "string name
geometry_msgs/PoseStamped position
uint64 x1
uint64 y1
uint64 x2
uint64 y2

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



(provide :task3/FacePose "fba59784293eab073312c8d62c229f5c")


