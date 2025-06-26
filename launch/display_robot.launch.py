#!/usr/bin/env python3
import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    OpaqueFunction,
)
from launch.substitutions import (
    Command,
    FindExecutable,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    """Declare launch arguments and return the LaunchDescription."""
    declared_arguments = [
        DeclareLaunchArgument(
            "robot_model",
            default_value='ha006b',
            choices=['ha006b', 'hdf7_9', 'hdf8_8', 'hdr50_22', 'hdr220_26', 'hh020'],
            description="HDR robot model to use.",
        ),
        DeclareLaunchArgument(
            'description_package',
            default_value='hdr_description',
            description='Package containing robot URDF/XACRO files.',
        ),
        DeclareLaunchArgument(
            'description_file',
            default_value='hdr.urdf.xacro',
            description="Defines the robot's URDF/XACRO configuration file.",
        ),
    ]

    return LaunchDescription(declared_arguments + [
            OpaqueFunction(function=launch_setup)
    ])
    

def launch_setup(context, *args, **kwargs):
    """Set up and return the nodes to display the HDR robot in Rviz."""
    robot_model = LaunchConfiguration("robot_model").perform(context)
    description_package = LaunchConfiguration("description_package")
    description_file = LaunchConfiguration("description_file")
    
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [FindPackageShare(description_package), "urdf", description_file]
            ),
            " use_sim:=", "false",
            " use_mock_hardware:=", "true",
            " robot_model:=", robot_model,
            " name:=", "hdr",
        ]
    )
            
    robot_description = {'robot_description': robot_description_content}

    rviz_config_path = PathJoinSubstitution([
        FindPackageShare(description_package),
        'rviz',
        'display_robot.rviz',
    ])

    joint_state_publisher_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='both',
        parameters=[robot_description],
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='log',
        arguments=['-d', rviz_config_path],
    )

    return [joint_state_publisher_node, robot_state_publisher_node, rviz_node]