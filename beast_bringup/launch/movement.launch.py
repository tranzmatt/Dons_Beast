#!/usr/bin/env python3
"""
Movement-only launch file for UGV Beast
Lightweight bringup for odometry/movement testing (no lidar, no robot_state_publisher)
"""
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_share = get_package_share_directory('beast_bringup')
    config_file = os.path.join(pkg_share, 'config', 'beast_params.yaml')
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation time if true'
        ),

        # ESP32 Bridge Node
        Node(
            package='beast_bringup',
            executable='esp32_bridge.py',
            name='esp32_bridge',
            parameters=[config_file, {'use_sim_time': use_sim_time}],
            output='screen',
            emulate_tty=True,
        ),

        # IMU Filter (Madgwick)
        Node(
            package='imu_filter_madgwick',
            executable='imu_filter_madgwick_node',
            name='imu_filter',
            parameters=[{
                'use_mag': True,
                'publish_tf': False,
                'world_frame': 'enu',
                'gain': 0.1,
            }],
            remappings=[
                ('imu/data_raw', 'imu/data_raw'),
                ('imu/mag',      'imu/mag'),
                ('imu/data',     'imu/data'),
            ],
            output='screen',
        ),

        # Odometry Publisher Node
        Node(
            package='beast_motion',
            executable='odom_publisher',
            name='odom_publisher',
            parameters=[config_file, {'use_sim_time': use_sim_time}],
            output='screen',
            emulate_tty=True,
        ),

        # Battery Monitor Node
        Node(
            package='beast_utils',
            executable='battery_monitor',
            name='battery_monitor',
            parameters=[config_file, {'use_sim_time': use_sim_time}],
            output='screen',
            emulate_tty=True,
        ),
    ])