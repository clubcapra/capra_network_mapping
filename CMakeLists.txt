cmake_minimum_required(VERSION 3.0.2)
project(capra_signal_strength)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  rtabmap_ros
  message_generation
  std_msgs
)

add_message_files(
  FILES
  WifiStrength.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS roscpp rospy rtabmap_ros message_runtime std_msgs
)

catkin_install_python(PROGRAMS
  scripts/wifi_signal_pub.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

include_directories(${catkin_INCLUDE_DIRS})

add_executable(wifi_mapper_node src/wifi_mapper.cpp)
target_link_libraries(wifi_mapper_node ${catkin_LIBRARIES})
set_target_properties(wifi_mapper_node PROPERTIES OUTPUT_NAME "wifi_mapper_node")

