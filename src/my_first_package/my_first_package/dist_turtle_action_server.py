import rclpy as rp
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.executors import MultiThreadedExecutor
import time
import math
from geometry_msgs.msg import Twist

from my_first_package.my_subscriber import TurtlesimSubscriber

from turtlesim.msg import Pose
from my_first_package_msgs.action import DistTurtle

class DistTurtleActionServer(Node):
    def __init__(self):
        super().__init__('dist_turtle_action_server')
        self.cur_pose = Pose()
        self.pre_pose = Pose()
        self.first_time = True

        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        self.total_dist = 0
        
        self.action_server = ActionServer(
                self,
                DistTurtle,
                'dist_turtle',
                self.execute_callback,
                )

    def calc_diff(self):
        if self.first_time:
            self.pre_pose.x = self.cur_pose.x
            self.pre_pose.y = self.cur_pose.y
            self.first_time = False

        diff = math.sqrt((self.cur_pose.x - self.pre_pose.x)**2
                        + (self.cur_pose.y - self.pre_pose.y)**2)

        return diff

    def execute_callback(self, goal_handle):

        msg = Twist()
        msg.linear.x = goal_handle.request.linear_x
        msg.angular.z = goal_handle.request.angular_z

        feedback = DistTurtle.Feedback()

        while True:
            self.total_dist += self.calc_diff()
            feedback.remained_dist = goal_handle.request.dist - self.total_dist
            goal_handle.publish_feedback(feedback)
            self.pub.publish(msg)
            time.sleep(0.05)

            if feedback.remained_dist < 0.2:
                break

        goal_handle.succeed()
        result = DistTurtle.Result()
        result.pos_x = self.cur_pose.x
        result.pos_y = self.cur_pose.y
        result.pos_theta = self.cur_pose.theta
        result.result_dist = self.total_dist

        self.total_dist = 0
        self.first_time = True

        return result

class TurtlePosetoAction(TurtlesimSubscriber):
    def __init__(self, ac_server):
        super().__init__()
        self.ac_server = ac_server

    def callback(self, msg):
        self.ac_server.cur_pose = msg

def main(args=None):
    rp.init(args=args)

    action_server = DistTurtleActionServer()
    sub_pose = TurtlePosetoAction(action_server)

    executor = MultiThreadedExecutor()

    executor.add_node(action_server)
    executor.add_node(sub_pose)

    try:
        executor.spin()
    finally:
        executor.shutdown()
        action_server.destroy_node()
        sub_pose.destroy_node()
        rp.shutdown()

if __name__=='__main__':
    main()
