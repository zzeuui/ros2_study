import rclpy as rp
from geometry_msgs.msg import Twist

rp.init()
test_node = rp.create_node('pub_test')

msg = Twist()
msg.linear.x = 2.0
msg.angular.z = 2.0

pub = test_node.create_publisher(Twist, '/turtle1/cmd_vel', 10)
#pub.publish(msg)

cnt = 0
def timer_callback():
    global cnt

    cnt += 1
    print(cnt)
    pub.publish(msg)

    if cnt > 3:
        raise Exception("Publishing Stop")

timer_period = 1
timer = test_node.create_timer(timer_period, timer_callback)
rp.spin(test_node)
#test_node.destroy_node()
