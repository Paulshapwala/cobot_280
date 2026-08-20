cmake_minimum_required(VERSION 3.22)
project(mycobot_movit_config)

# find dependencies
find_package(ament_cmake REQUIRED)

ament_package()

# Copy necessary files to designated locations in the project
install (
  DIRECTORY config launch
  DESTINATION share/${PROJECT_NAME}
)

if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/launch")
  install(
    DIRECTORY launch
    DESTINATION share/${PROJECT_NAME}
    PATTERN "setup_assistant.launch" EXCLUDE)
endif()

install(DIRECTORY config DESTINATION share/${PROJECT_NAME})
install(FILES .setup_assistant DESTINATION share/${PROJECT_NAME})
