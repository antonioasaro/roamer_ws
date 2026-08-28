from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_share = get_package_share_directory('gazebo_differential_drive_robot')
    
    use_sim_time = LaunchConfiguration('use_sim_time')

    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )

    efk_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[
            '/home/ubuntu/roamer_ws/src/gazebo_differential_drive_robot/config/ekf.yaml',
            {'use_sime_time': use_sim_time}
            ],
        remappings=[('/imu/data', '/imu_state_broadcaster/imu')]
    )
    
    return LaunchDescription([
        use_sim_time_arg,
        efk_node
    ])
    
