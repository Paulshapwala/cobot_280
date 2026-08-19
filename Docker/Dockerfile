FROM ros:jazzy

ARG ROS_DISTRO=jazzy
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

# Install base packages and ROS dependencies using variable substitution
RUN apt-get update && apt-get install -y \
    ros-${ROS_DISTRO}-joint-state-publisher-gui \
    ros-${ROS_DISTRO}-xacro \
    ros-${ROS_DISTRO}-demo-nodes-cpp \
    ros-${ROS_DISTRO}-demo-nodes-py \
    ros-${ROS_DISTRO}-rviz2 \
    ros-${ROS_DISTRO}-rqt-reconfigure \
    python3-pip \
    git \
    wget \
    nano \
    vim \
    build-essential \
    gedit \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Set environment variable
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

# Install RMW, MoveIt, and ROS2 Control
RUN apt-get update && apt-get install -y \
    ros-${ROS_DISTRO}-rmw-cyclonedds-cpp \
    ros-${ROS_DISTRO}-moveit \
    ros-${ROS_DISTRO}-ros2-control \
    ros-${ROS_DISTRO}-ros2-controllers \
    && rm -rf /var/lib/apt/lists/*

# Install gazebo and gazebo pkgs
RUN apt-get update && apt-get install -y \
    apt-get install ros-${ROS_DISTRO}-ros-gz \
    && rm -rf /var/lib/apt/lists/*

ENV SHELL /bin/bash

# Create reminder message in bashrc
RUN echo 'echo "💡 Install new packages? Add to Dockerfile, rebuild, and commit to git"' >> /home/$USERNAME/.bashrc

USER $USERNAME
# path consistency to place workspace in user home directory
RUN mkdir -p /home/$USERNAME/cobot_ws/src
WORKDIR /home/$USERNAME/cobot_ws

CMD ["/bin/bash"]