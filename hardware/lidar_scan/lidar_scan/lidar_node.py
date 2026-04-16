import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

class LidarHardware(Node):
    def __init__(self):
        super().__init__('lidar_hardware_node')
        self.publisher_ = self.create_publisher(LaserScan, '/scan', 10)
        
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info("Hardware Layer: LiDAR Sensor Online.")

    def timer_callback(self):
        msg = LaserScan()
        msg.ranges = [5.0] * 360
        for i in range(5):
            msg.ranges[i] = 0.3

        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = LidarHardware()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

