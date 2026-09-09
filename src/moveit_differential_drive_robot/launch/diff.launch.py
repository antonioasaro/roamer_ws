import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import RegisterEventHandler, TimerAction
from launch.event_handlers import OnProcessExit
from launch.event_handlers import OnProcessStart
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_demo_launch
import xacro

def generate_launch_description():
    # 1. Load MoveIt Configuration
    # Replace 'your_moveit_config_package' with your actual MoveIt config package name
    moveit_config = (
        MoveItConfigsBuilder("differential_drive_robot", package_name="moveit_differential_drive_robot")
        .sensors_3d(file_path="config/sensors_3d.yaml")
        .to_moveit_configs()
    )
    
    pkg_share = get_package_share_directory('gazebo_differential_drive_robot')
    xacro_file = os.path.join(pkg_share, 'urdf', 'robot.xacro')
    robot_description_raw = xacro.process_file(xacro_file).toxml()    
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description_raw
        }]
    )

    # 2. Path to ros2_control configuration
    ros2_control_config = os.path.join(
        get_package_share_directory("moveit_differential_drive_robot"),
        "config",
        "ros2_controllers.yaml"
    )

    # 3. Controller Manager Node
    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[moveit_config.robot_description, ros2_control_config],
        output="screen",
    )

    # 4. Move Group Node
    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[moveit_config.to_dict()],
    )

    # 5. Spawners for ros2_control
    joint_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    )

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_drive_controller", "--controller-manager", "/controller_manager"],
    )

    imu_sensor_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['imu_sensor_broadcaster']
    )

    arm_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['arm_controller']
    )
   
    gripper_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['gripper_controller']
    )    
    
    # Ensure controllers spawn AFTER the controller manager is up
    delay_diff_drive = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_broadcaster_spawner,
            on_exit=[diff_drive_spawner],
        )
    )
        
    delay_imu_sensor = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_broadcaster_spawner,
            on_exit=[imu_sensor_spawner],
        )
    )

    delay_arm_controller = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_broadcaster_spawner,
            on_exit=[arm_controller_spawner],
        )
    )

    delay_gripper_controller = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_broadcaster_spawner,
            on_exit=[gripper_controller_spawner],
        )
    )
    
    return LaunchDescription([
        generate_demo_launch(moveit_config),
        robot_state_publisher,
        delay_diff_drive,
        delay_imu_sensor,
        delay_arm_controller,
        delay_gripper_controller
    ])
