import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node

def generate_launch_description():
    package_dir = get_package_share_directory('3_DOF')
    urdf = os.path.join(package_dir, 'gazebo.urdf')

    controller_file = os.path.join(package_dir, "config", "jtc.yaml")
    robot_description = {"/robot_description": urdf}

    return LaunchDescription([
        ExecuteProcess(
            cmd=["gazebo", "--verbose", "-s", "libgazebo_ros_factory.so"],
            output="screen",),
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=["-topic","/robot_description","-entity","3_DOF"]),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            arguments=[urdf]),
        Node(
            package="controller_manager",
            executable="ros2_control_node",
            parameters=[robot_description, controller_file],
            output={
                "stdout": "screen",
                "stderr": "screen",},),
        Node(
            package="controller_manager",
            executable="spawner",
            arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],),
        Node(
            package="controller_manager",
            executable="spawner",
            arguments=["joint_trajectory_controller", "-c", "/controller_manager"],
        ),
        Node(
            package="3_DOF",
            executable="trajectory_msg",
        ),
    ])