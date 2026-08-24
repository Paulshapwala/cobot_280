import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Get package directories
    robot_desc_pkg = get_package_share_directory('your_robot_description')
    moveit_config_pkg = get_package_share_directory('your_robot_moveit_config')
    
    # Load robot description
    robot_description_content = open(
        os.path.join(robot_desc_pkg, 'urdf', 'your_robot.urdf.xacro')
    ).read()
    
    robot_description = {
        'robot_description': robot_description_content
    }
    
    # Gazebo
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'world': os.path.join(robot_desc_pkg, 'worlds', 'pick_place.world')}.items(),
    )
    
    # Spawn robot
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'robot_arm'],
        output='screen',
    )
    
    # Robot state publisher
    robot_state_pub = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description],
    )
    
    # Start MoveIt
    move_group = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(moveit_config_pkg, 'launch', 'move_group.launch.py')
        ),
        launch_arguments={'allow_trajectory_execution': 'true'}.items(),
    )
    
    return LaunchDescription([
        robot_state_pub,
        gazebo_launch,
        spawn_robot,
        move_group,
    ])