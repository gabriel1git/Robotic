import rclpy
from rclpy.node import Node
from builtin_interfaces.msg import Duration
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class Trajectory_publisher(Node):
    
    def __init__(self):
        super().__init__('trajectory_publisher_node')
        publish_topic ="/joint_trajectory_controller/joint_trajectory"
        self.trajectory_publisher = self.create_publisher(JointTrajectory, publish_topic, 10)
        timer_period = 2
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.joints = ['joint_2', 'joint_3', 'joint_5']
        self.goal_positions = [3.14, 0.32, -1.68]
        self.i = 0

    def move(self):
        if self.i == 1:
            self.goal_positions = [3.14, -1.57, 0.0]
        if self.i == 2:
            self.goal_positions = [1.57, 0.32, -1.68]
        if self.i == 3:
            self.goal_positions = [1.57, -1.57, 0.0]
        if self.i == 4:
            self.goal_positions = [0.0, 0.32, -1.68]
        if self.i == 5:
            self.goal_positions = [0.0, -1.57, 0.0]
        if self.i == 6:
            self.goal_positions = [-1.57, 0.32, -1.68]
        if self.i == 7:
            self.goal_positions = [-1.57, -1.57, 0.0]
        if self.i == 8:
            self.goal_positions = [3.14, 0.32, -1.68]
            self.i = 0



    def timer_callback(self):
        robot_trajectory_msg = JointTrajectory()
        robot_trajectory_msg.joint_names = self.joints
        point = JointTrajectoryPoint()
        point.positions = self.goal_positions
        point.time_from_start = Duration(sec=1)
        robot_trajectory_msg.points.append(point)
        self.trajectory_publisher.publish(robot_trajectory_msg)
        self.i += 1
        self.move()

def main(args=None):
    rclpy.init(args=args)
    joint_trajectory_object = Trajectory_publisher()
    rclpy.spin(joint_trajectory_object)
    joint_trajectory_object.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()