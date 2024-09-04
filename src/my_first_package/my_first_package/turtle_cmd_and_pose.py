import rclpy as rp
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from my_first_package_msgs.msg import CmdAndPoseVel

class CmdAndPose(Node):
    def __init__(self):
        super().__init__('turtle_cmd_pose')
        self.sub_pose = self.create_subscription(
                Pose, '/turtle1/pose', self.callback_pose, 10)
        self.sub_cmdvel = self.create_subscription(
                Twist, '/turtle1/cmd_vel', self.callback_cmd, 10)
        self.pub = self.create_publisher(CmdAndPoseVel, '/cmd_and_pose', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.cmd_pose = CmdAndPoseVel()

    def callback_pose(self, msg):
        self.cmd_pose.pose_x = msg.x
        self.cmd_pose.pose_y = msg.y
        self.cmd_pose.linear_vel = msg.linear_velocity
        self.cmd_pose.angular_vel = msg.angular_velocity

    def callback_cmd(self, msg):
        self.cmd_pose.cmd_vel_linear = msg.linear.x
        self.cmd_pose.cmd_vel_angular = msg.angular.z

    def timer_callback(self):
        self.pub.publish(self.cmd_pose)

def main():
    rp.init()

    node = CmdAndPose()
    rp.spin(node)

    node.destroy_node()
    rp.shutdown()

if __name__=='__main__':
    main()
