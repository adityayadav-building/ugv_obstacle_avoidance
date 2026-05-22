# Autonomous UGV Obstacle Avoidance Pipeline 🚙🎯

A complete ROS 2 and Gazebo simulation pipeline for a custom differential-drive Unmanned Ground Vehicle (UGV). This project implements an **Artificial Potential Field (APF)** algorithm from scratch in Python, processing real-time LiDAR point clouds to autonomously navigate a robot to a target coordinate while dynamically avoiding spatial obstacles.

## 🛠️ Technology Stack
* **Framework:** ROS 2 (Jazzy)
* **Simulation:** Gazebo (ros_gz_sim)
* **Languages:** Python, XML (URDF/Xacro)
* **Sensors:** GPU LiDAR 
* **Kinematics:** Differential Drive

---

## 🏗️ System Architecture

### 1. Physical Robot Modeling (`robot.xacro` & `robot.gazebo`)
* Modeled a custom two-wheel differential drive chassis with a stabilizing caster wheel.
* Calculated and defined accurate mass and inertia matrices for the body , wheels , and caster  to ensure realistic physics simulation.
* Configured a GPU LiDAR sensor to cast 120 samples horizontally , spanning a full 360-degree field of view ($-\pi$ to $\pi$ radians)with a detection range of 0.15m to 12.0m[cite: 294]. Gaussian noise was added to the sensor feed to simulate real-world hardware inaccuracies.

### 2. ROS-Gazebo Bridge (`bridge_parameters.yaml` & `gazebo_model.launch.py`)
* Engineered a seamless integration between ROS 2 nodes and the Gazebo simulation using `ros_gz_bridge`.
* Mapped critical bidirectional topics: Odometry (`/odom1`), Lidar scans (`/scan`), Joint States, and Velocity Commands (`/cmd_vel`).

### 3. Navigation Controller (`controller_final.py`)
The core autonomous navigation node processes spatial data to calculate force vectors based on the Artificial Potential Field (APF) method:

* **Attractive Force ($F_{att}$):** Pulls the robot toward the target destination $(x_d, y_d)$ using a proportional gain constant $k_a$.
  $$F_{att} = -k_a(p - p_d)$$
* **Repulsive Force ($F_{rep}$):** Pushes the robot away from obstacles detected by the LiDAR. Only obstacles within a critical threshold ($g^*$) exert force, calculated using the distance $r$ and a repulsion gain $k_r$.
  $$F_{rep} = \sum k_r \left(\frac{1}{r} - \frac{1}{g^*}\right) \frac{1}{r^3} (p - p_o)$$
* **Kinematic Translation:** The sum of these vector forces determines the desired orientation ($\theta_d$). The robot calculates the orientation error and outputs precise linear ($v_x$) and angular ($\omega_z$) velocity commands to align and drive the differential wheels.

