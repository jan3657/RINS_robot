// Generated by gencpp from file yocs_msgs/WallList.msg
// DO NOT EDIT!


#ifndef YOCS_MSGS_MESSAGE_WALLLIST_H
#define YOCS_MSGS_MESSAGE_WALLLIST_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <yocs_msgs/Wall.h>

namespace yocs_msgs
{
template <class ContainerAllocator>
struct WallList_
{
  typedef WallList_<ContainerAllocator> Type;

  WallList_()
    : obstacles()  {
    }
  WallList_(const ContainerAllocator& _alloc)
    : obstacles(_alloc)  {
  (void)_alloc;
    }



   typedef std::vector< ::yocs_msgs::Wall_<ContainerAllocator> , typename ContainerAllocator::template rebind< ::yocs_msgs::Wall_<ContainerAllocator> >::other >  _obstacles_type;
  _obstacles_type obstacles;





  typedef boost::shared_ptr< ::yocs_msgs::WallList_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::yocs_msgs::WallList_<ContainerAllocator> const> ConstPtr;

}; // struct WallList_

typedef ::yocs_msgs::WallList_<std::allocator<void> > WallList;

typedef boost::shared_ptr< ::yocs_msgs::WallList > WallListPtr;
typedef boost::shared_ptr< ::yocs_msgs::WallList const> WallListConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::yocs_msgs::WallList_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::yocs_msgs::WallList_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::yocs_msgs::WallList_<ContainerAllocator1> & lhs, const ::yocs_msgs::WallList_<ContainerAllocator2> & rhs)
{
  return lhs.obstacles == rhs.obstacles;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::yocs_msgs::WallList_<ContainerAllocator1> & lhs, const ::yocs_msgs::WallList_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace yocs_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::yocs_msgs::WallList_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::yocs_msgs::WallList_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::yocs_msgs::WallList_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::yocs_msgs::WallList_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::yocs_msgs::WallList_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::yocs_msgs::WallList_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::yocs_msgs::WallList_<ContainerAllocator> >
{
  static const char* value()
  {
    return "2879979aabb372fc7f6d782228e53412";
  }

  static const char* value(const ::yocs_msgs::WallList_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x2879979aabb372fcULL;
  static const uint64_t static_value2 = 0x7f6d782228e53412ULL;
};

template<class ContainerAllocator>
struct DataType< ::yocs_msgs::WallList_<ContainerAllocator> >
{
  static const char* value()
  {
    return "yocs_msgs/WallList";
  }

  static const char* value(const ::yocs_msgs::WallList_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::yocs_msgs::WallList_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# Virtual wall obstacles\n"
"\n"
"Wall[] obstacles\n"
"================================================================================\n"
"MSG: yocs_msgs/Wall\n"
"# Virtual wall obstacle;\n"
"#  - Assumed to be a plan, so width is ignored by now\n"
"#  - The yaw provides the orientation of x-axis\n"
"#  - Assumed vertically aligned (roll and pitch must be 0)\n"
"#  - Z provides the lower border of the wall (normally 0)\n"
"\n"
"string  name\n"
"float32 length\n"
"float32 width\n"
"float32 height\n"
"geometry_msgs/PoseWithCovarianceStamped pose\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/PoseWithCovarianceStamped\n"
"# This expresses an estimated pose with a reference coordinate frame and timestamp\n"
"\n"
"Header header\n"
"PoseWithCovariance pose\n"
"\n"
"================================================================================\n"
"MSG: std_msgs/Header\n"
"# Standard metadata for higher-level stamped data types.\n"
"# This is generally used to communicate timestamped data \n"
"# in a particular coordinate frame.\n"
"# \n"
"# sequence ID: consecutively increasing ID \n"
"uint32 seq\n"
"#Two-integer timestamp that is expressed as:\n"
"# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')\n"
"# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')\n"
"# time-handling sugar is provided by the client library\n"
"time stamp\n"
"#Frame this data is associated with\n"
"string frame_id\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/PoseWithCovariance\n"
"# This represents a pose in free space with uncertainty.\n"
"\n"
"Pose pose\n"
"\n"
"# Row-major representation of the 6x6 covariance matrix\n"
"# The orientation parameters use a fixed-axis representation.\n"
"# In order, the parameters are:\n"
"# (x, y, z, rotation about X axis, rotation about Y axis, rotation about Z axis)\n"
"float64[36] covariance\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Pose\n"
"# A representation of pose in free space, composed of position and orientation. \n"
"Point position\n"
"Quaternion orientation\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Point\n"
"# This contains the position of a point in free space\n"
"float64 x\n"
"float64 y\n"
"float64 z\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Quaternion\n"
"# This represents an orientation in free space in quaternion form.\n"
"\n"
"float64 x\n"
"float64 y\n"
"float64 z\n"
"float64 w\n"
;
  }

  static const char* value(const ::yocs_msgs::WallList_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::yocs_msgs::WallList_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.obstacles);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct WallList_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::yocs_msgs::WallList_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::yocs_msgs::WallList_<ContainerAllocator>& v)
  {
    s << indent << "obstacles[]" << std::endl;
    for (size_t i = 0; i < v.obstacles.size(); ++i)
    {
      s << indent << "  obstacles[" << i << "]: ";
      s << std::endl;
      s << indent;
      Printer< ::yocs_msgs::Wall_<ContainerAllocator> >::stream(s, indent + "    ", v.obstacles[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // YOCS_MSGS_MESSAGE_WALLLIST_H
