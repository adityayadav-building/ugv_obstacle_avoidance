from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ugv_obstacle_avoidance',
            executable='avoider_node',
            name='avoider_node',
            output='screen',
            parameters=[
                {'safe_distance': 0.6} 
            ]
        )
    ])