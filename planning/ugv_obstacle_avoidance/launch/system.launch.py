from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        
        Node(
            package='lidar_scan',
            executable='lidar_node',
            name='lidar_scan_data',
            output='screen'
        ),
        
        
        Node(
            package='ugv_obstacle_avoidance',
            executable='avoider_node',
            name='avoider_node',
            output='screen',
            parameters=[
                {'safe_distance': 0.5,
                'linear_speed': 0.2,
                'angular_speed': 0.5}
            ]
        )
    ])
