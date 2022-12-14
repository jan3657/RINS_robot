// Generated by gencpp from file task3/FacePose.msg
// DO NOT EDIT!


#ifndef TASK3_MESSAGE_FACEPOSE_H
#define TASK3_MESSAGE_FACEPOSE_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <geometry_msgs/PoseStamped.h>

namespace task3
{
template <class ContainerAllocator>
struct FacePose_
{
  typedef FacePose_<ContainerAllocator> Type;

  FacePose_()
    : name()
    , position()
    , x1(0)
    , y1(0)
    , x2(0)
    , y2(0)  {
    }
  FacePose_(const ContainerAllocator& _alloc)
    : name(_alloc)
    , position(_alloc)
    , x1(0)
    , y1(0)
    , x2(0)
    , y2(0)  {
  (void)_alloc;
    }



   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _name_type;
  _name_type name;

   typedef  ::geometry_msgs::PoseStamped_<ContainerAllocator>  _position_type;
  _position_type position;

   typedef uint64_t _x1_type;
  _x1_type x1;

   typedef uint64_t _y1_type;
  _y1_type y1;

   typedef uint64_t _x2_type;
  _x2_type x2;

   typedef uint64_t _y2_type;
  _y2_type y2;





  typedef boost::shared_ptr< ::task3::FacePose_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::task3::FacePose_<ContainerAllocator> const> ConstPtr;

}; // struct FacePose_

typedef ::task3::FacePose_<std::allocator<void> > FacePose;

typedef boost::shared_ptr< ::task3::FacePose > FacePosePtr;
typedef boost::shared_ptr< ::task3::FacePose const> FacePoseConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::task3::FacePose_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::task3::FacePose_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::task3::FacePose_<ContainerAllocator1> & lhs, const ::task3::FacePose_<ContainerAllocator2> & rhs)
{
  return lhs.name == rhs.name &&
    lhs.position == rhs.position &&
    lhs.x1 == rhs.x1 &&
    lhs.y1 == rhs.y1 &&
    lhs.x2 == rhs.x2 &&
    lhs.y2 == rhs.y2;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::task3::FacePose_<ContainerAllocator1> & lhs, const ::task3::FacePose_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace task3

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::task3::FacePose_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::task3::FacePose_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::task3::FacePose_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::task3::FacePose_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::task3::FacePose_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::task3::FacePose_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::task3::FacePose_<ContainerAllocator> >
{
  static const char* value()
  {
    return "fba59784293eab073312c8d62c229f5c";
  }

  static const char* value(const ::task3::FacePose_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xfba59784293eab07ULL;
  static const uint64_t static_value2 = 0x3312c8d62c229f5cULL;
};

template<class ContainerAllocator>
struct DataType< ::task3::FacePose_<ContainerAllocator> >
{
  static const char* value()
  {
    return "task3/FacePose";
  }

  static const char* value(const ::task3::FacePose_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::task3::FacePose_<ContainerAllocator> >
{
  static const char* value()
  {
    return "string name\n"
"geometry_msgs/PoseStamped position\n"
"uint64 x1\n"
"uint64 y1\n"
"uint64 x2\n"
"uint64 y2\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/PoseStamped\n"
"# A Pose with reference coordinate frame and timestamp\n"
"Header header\n"
"Pose pose\n"
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

  static const char* value(const ::task3::FacePose_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::task3::FacePose_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.name);
      stream.next(m.position);
      stream.next(m.x1);
      stream.next(m.y1);
      stream.next(m.x2);
      stream.next(m.y2);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct FacePose_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::task3::FacePose_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::task3::FacePose_<ContainerAllocator>& v)
  {
    s << indent << "name: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.name);
    s << indent << "position: ";
    s << std::endl;
    Printer< ::geometry_msgs::PoseStamped_<ContainerAllocator> >::stream(s, indent + "  ", v.position);
    s << indent << "x1: ";
    Printer<uint64_t>::stream(s, indent + "  ", v.x1);
    s << indent << "y1: ";
    Printer<uint64_t>::stream(s, indent + "  ", v.y1);
    s << indent << "x2: ";
    Printer<uint64_t>::stream(s, indent + "  ", v.x2);
    s << indent << "y2: ";
    Printer<uint64_t>::stream(s, indent + "  ", v.y2);
  }
};

} // namespace message_operations
} // namespace ros

#endif // TASK3_MESSAGE_FACEPOSE_H
