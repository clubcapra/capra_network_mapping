cmake_minimum_required(VERSION 3.0.2)
project(capra_signal_strength)

find_package(catkin REQUIRED COMPONENTS
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