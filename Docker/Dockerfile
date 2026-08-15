FROM ros:humble

ARG USERNAME=shapzonlinux
ARG USER_UID=1000
ARG USER_GID=$USER_UID

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
    cmake \
    && rm -rf /var/lib/apt/lists/*

ENV SHELL /bin/bash

# Copy setup scripts into container (from Docker/ subdirectory)
COPY Docker/environment-variables.sh /home/$USERNAME/environment-variables.sh
COPY Docker/setup.sh /home/$USERNAME/setup.sh
COPY Docker/entrypoint.sh /home/$USERNAME/entrypoint.sh

# Make scripts executable and owned by user
RUN chmod +x /home/$USERNAME/setup.sh \
    && chmod +x /home/$USERNAME/environment-variables.sh \
    && chmod +x /home/$USERNAME/entrypoint.sh \
    && chown $USERNAME:$USERNAME /home/$USERNAME/setup.sh \
    && chown $USERNAME:$USERNAME /home/$USERNAME/environment-variables.sh \
    && chown $USERNAME:$USERNAME /home/$USERNAME/entrypoint.sh

# Create reminder message in bashrc
RUN echo '' >> /home/$USERNAME/.bashrc && \
    echo '# Reminder on login' >> /home/$USERNAME/.bashrc && \
    echo 'echo "╔═════════════════════════════════════════════════════════╗"' >> /home/$USERNAME/.bashrc && \
    echo 'echo "║   REMINDER: Update your requirements files!             ║"' >> /home/$USERNAME/.bashrc && \
    echo 'echo "╚═════════════════════════════════════════════════════════╝"' >> /home/$USERNAME/.bashrc && \
    echo 'echo ""' >> /home/$USERNAME/.bashrc && \
    echo 'echo "If you installed packages: sudo apt install <package>"' >> /home/$USERNAME/.bashrc && \
    echo 'echo "Do BEFORE exiting:"' >> /home/$USERNAME/.bashrc && \
    echo 'echo "1. sudo apt-mark showmanual"' >> /home/$USERNAME/.bashrc && \
    echo 'echo "2. Add to: Docker/requirements.txt"' >> /home/$USERNAME/.bashrc && \
    echo 'echo "3. Update: Docker/environment-variables.sh (if needed)"' >> /home/$USERNAME/.bashrc && \
    echo 'echo "4. git add Docker/requirements.txt && git commit"' >> /home/$USERNAME/.bashrc && \
    echo 'echo ""' >> /home/$USERNAME/.bashrc

USER $USERNAME
WORKDIR /home/ws

# Run entrypoint.sh which runs setup.sh and then bash
ENTRYPOINT ["/home/shapzonlinux/entrypoint.sh"]