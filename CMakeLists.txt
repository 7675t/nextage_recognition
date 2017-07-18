cmake_minimum_required(VERSION 2.8.3)
project(nextage_recognition)

find_package(catkin REQUIRED COMPONENTS opencv_apps roscpp rospy sensor_msgs)
catkin_package()

install(DIRECTORY launch/ DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
install(PROGRAMS
  script/gaze_plane_projector.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
