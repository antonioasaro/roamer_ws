from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_demo_launch


def generate_launch_description():
    moveit_config = (
        MoveItConfigsBuilder("differential_drive_robot", package_name="moveit_differential_drive_robot")
        .sensors_3d(file_path="config/sensors_3d.yaml")
        .to_moveit_configs()
    )
    return generate_demo_launch(moveit_config)