import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )
    
    use_sim_time = LaunchConfiguration('use_sim_time')
    
    efk_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=['/home/ubuntu/roamer_ws/src/gazebo_differential_drive_robot/config/ekf.yaml'],
        remappings=[('/imu/data', '/imu_state_broadcaster/imu')]
    )
    
    return LaunchDescription([
        use_sim_time_arg,
        efk_node
    ])
    
