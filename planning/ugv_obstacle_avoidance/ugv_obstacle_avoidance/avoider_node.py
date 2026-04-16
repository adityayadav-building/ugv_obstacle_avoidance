import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ObstacleAvoidance(Node):
    def __init__(self):
        super().__init__('avoider_node')

        self.declare_parameter('safe_distance', 0.8)
        self.declare_parameter('linear_speed', 0.2)
        self.declare_parameter('angular_speed', 0.5)
        
        self.subscription = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        
        self.get_logger().info("Lidar Obstacle Avoidance Node Started!!!!!!!!!!!!!!!!!!!!!!!")

    def scan_callback(self, msg):
        threshold = self.get_parameter('safe_distance').get_parameter_value().double_value
        lin_speed = self.get_parameter('linear_speed').get_parameter_value().double_value
        ang_speed = self.get_parameter('angular_speed').get_parameter_value().double_value
        
        front = msg.ranges[-20:] + msg.ranges[0:20]
       
        
        valid_ranges = []
        
       
        for distance in front:
            
            if 0.1 < distance < 12.0:
                valid_ranges.append(distance)
        twist = Twist()

        if valid_ranges and min(valid_ranges) < threshold:
            self.get_logger().warn('Obstacle detected within ' + str(threshold) + 'meters !!!!!!!! Avoiding...')
            twist.linear.x = 0.05
            twist.angular.z = ang_speed
        else:
            twist.linear.x = lin_speed
            twist.angular.z = 0.0
            
        self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidance()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()