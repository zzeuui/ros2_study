import rclpy as rp
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor

from cv_bridge import CvBridge

from std_msgs.msg import String
from sensor_msgs.msg import Image

import cv2
import websockets
import asyncio
import time

class UserMsgPublisher(Node):
    def __init__(self):
        super().__init__('user_msg_pulisher')
        self.pub_msg = self.create_publisher(String, '/esp/msg', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)

    def timer_callback(self):
        while rp.ok():
            try:
                user_input = input("Enter a message: ")
                if user_input.lower() == 'exit':
                    break

                msg = String()
                msg.data = user_input
                print(msg)

                self.pub_msg.publish(msg)
                print('pub')

            except KeyboardInterrupt:
                break

class UserImgSubscription(Node):
    def __init__(self):
        super().__init__('user_img_subscription')
        self.sub_img = self.create_subscription(Image, '/esp/image', self.callback_img, 10)

        self.bridge = CvBridge()
        self.image_received = None

    def callback_img(self, msg):
        self.image_received = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        if self.image_received is not None:
            cv2.imshow("esp32cam", self.image_received)
            cv2.waitKey(1)
        else:
            cv2.waitKey(100)

def main():
    rp.init()

    pub_msg = UserMsgPublisher()
    sub_img = UserImgSubscription()

    executor = MultiThreadedExecutor()

    executor.add_node(pub_msg)
    executor.add_node(sub_img)

    try:
        executor.spin()
    finally:
        executor.shutdown()
        pub_msg.destroy_node()
        sub_img.destroy_node()
        cv2.destroyAllWindows()
        rp.shutdown()

if __name__ == "__main__":
    main()
