import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():

    robot_name_in_model = 'ugv_bot'
    package_name = 'ugv_bot'
    urdf_relative_path = 'model/robot.xacro'

    pkg_path = get_package_share_directory(package_name)
    absolute_model_path = os.path.join(pkg_path, urdf_relative_path)

    robot_description_config = xacro.process_file(absolute_model_path)
    robot_description = {'robot_description': robot_description_config.toxml()}

    gazebo_ros_pkg = get_package_share_directory('ros_gz_sim')
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(gazebo_ros_pkg, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': '-r empty.sdf'}.items()
    )

    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description', '-name', robot_name_in_model],
        output='screen'
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description, {'use_sim_time': True}]
    )

    bridge_parameters_relative_path = 'parameters/bridge_parameters.yaml'
    bridge_parameters_absolute_path = os.path.join(pkg_path, bridge_parameters_relative_path)

    ros_gz_bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={bridge_parameters_absolute_path}'
        ],
        output='screen'
    )

    ld = LaunchDescription()
    ld.add_action(gazebo_launch)
    ld.add_action(robot_state_publisher_node)
    ld.add_action(ros_gz_bridge_node)
    ld.add_action(spawn_entity)

    return ld