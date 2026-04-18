import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
import math

class ControllerNode(Node):
    def __init__(self, xd, yd, ka, kr, k_theta, g_star, eps_orient, eps_control):
        super().__init__('control_node')
        #Goal position
        self.xd = xd
        self.yd = yd
        
        self.ka = ka                  
        self.kr = kr               
        self.k_theta = k_theta       
        self.g_star = g_star          
        self.eps_orient = eps_orient 
        self.eps_control = eps_control 

        self.odom_msg = Odometry()
        self.lidar_msg = LaserScan()
        
        # publishers and subscribers
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.odom_sub = self.create_subscription(Odometry, '/odom1', self.callback_pose, 10)
        self.lidar_sub = self.create_subscription(LaserScan, '/scan', self.callback_lidar, 10)
        
        
        self.timer = self.create_timer(0.05, self.control_loop)

    def callback_pose(self, msg):
        self.odom_msg = msg

    def callback_lidar(self, msg):
        self.lidar_msg = msg

    def euler_from_quaternion(self, x, y, z, w):
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw = math.atan2(t3, t4)
        return yaw

    def orientation_error(self, theta_d, theta):
        err = theta_d - theta
        if theta_d > math.pi/2 and theta < -math.pi/2:
            err = (theta_d - 2*math.pi) - theta
        elif theta_d < -math.pi/2 and theta > math.pi/2:
            err = (theta_d + 2*math.pi) - theta
        
        while err > math.pi: err -= 2.0 * math.pi
        while err < -math.pi: err += 2.0 * math.pi
        return err

    def control_loop(self):
        if not self.lidar_msg.ranges:
            return 
        
        #current pos
        x = self.odom_msg.pose.pose.position.x
        y = self.odom_msg.pose.pose.position.y
        
        # Current orientation Yaw theta
        q = self.odom_msg.pose.pose.orientation
        theta = self.euler_from_quaternion(q.x, q.y, q.z, q.w)
        
        #stopping
        dist_to_goal = math.hypot(self.xd - x, self.yd - y)
        if dist_to_goal < self.eps_control:
            self.cmd_pub.publish(Twist()) 
            self.get_logger().info('Goal Reached!')
            return

        # att force
        F_att_x = -self.ka * (x - self.xd)
        F_att_y = -self.ka * (y - self.yd)

        # rep force
        F_rep_x = 0.0
        F_rep_y = 0.0
        
        angle_min = self.lidar_msg.angle_min
        angle_inc = self.lidar_msg.angle_increment
        
        for i, r in enumerate(self.lidar_msg.ranges):
            if math.isinf(r) or r > self.g_star or r <= 0.0:
                continue
            
            alpha = angle_min + i * angle_inc
            gamma = alpha + theta
            
            # X/Y of obstacle
            xo = x + r * math.cos(gamma)
            yo = y + r * math.sin(gamma)
            
            # repulsive gradient math
            factor = self.kr * (1.0/r - 1.0/self.g_star) * (1.0 / (r**3))
            F_rep_x += factor * (x - xo)
            F_rep_y += factor * (y - yo)

        #sum of forces
        F_x = F_att_x + F_rep_x
        F_y = F_att_y + F_rep_y

        theta_d = math.atan2(F_y, F_x)
        e_orient = self.orientation_error(theta_d, theta)

        #cmd
        msg = Twist()
        if abs(e_orient) > self.eps_orient:
            msg.linear.x = 0.1 
            msg.angular.z = self.k_theta * e_orient
        else:
            v = math.hypot(F_x, F_y)
            msg.linear.x = min(v, 0.6)
            msg.angular.z = self.k_theta * e_orient

        self.cmd_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = ControllerNode(10.0, -10.0, 2.0, 2.0, 0.5, 0.8, 0.2, 0.5)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()