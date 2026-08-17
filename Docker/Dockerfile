FROM ros:humble

ARG ROS_DISTRO=humble
ARG USERNAME=shapzonlinux
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ENV USERNAME=$USERNAME
ENV ROS_DISTRO=$ROS_DISTRO

# Delete user if it exists in container
RUN if id -u $USER_UID 2>/dev/null; then userdel `id -un $USER_UID`; fi

# Create the user with sudo access
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Install base packages (no environment variables required)
RUN apt-get update && apt-get install -y \
    ros-humble-joint-state-publisher-gui \
    ros-humble-xacro \
    ros-humble-demo-nodes-cpp \
    ros-humble-demo-nodes-py \
    ros-humble-rviz2 \
    ros-humble-rqt-reconfigure \
    python3-pip \
    git \
    wget \
    nano \
    vim \
    build-essential \
    gedit\
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Set environment variable
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

# Install RMW and MoveIt (now with env var set)
RUN apt-get update && apt-get install -y \
    ros-${ROS_DISTRO}-rmw-cyclonedds-cpp \
    ros-${ROS_DISTRO}-moveit \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    && rm -rf /var/lib/apt/lists/*

ENV SHELL /bin/bash

# Create reminder message in bashrc
RUN echo 'echo "💡 Install new packages? Add to Dockerfile, rebuild, and commit to git"' >> /home/$USERNAME/.bashrc

USER $USERNAME
RUN mkdir -p /home/$USERNAME/cobot_ws/src
WORKDIR /home/cobot_ws

CMD ["/bin/bash"]