import rclpy as rp #ros common library python
from turtlesim.msg import Pose

rp.init()
test_node = rp.create_node('sub_test')

cnt = 0
def callback(data):
    global cnt
    cnt += 1
    print(f'cnt: {cnt}')
    print("--->")
    print("/turtle1/pose : ",  data)
    print("X: ", data.x)
    print("Y: ", data.y)
    print("Theta: ", data.theta)

    if cnt > 3:
        raise Exception("Subscription Stop")

test_node.create_subscription(Pose, '/turtle1/pose', callback, 10)

#rp.spin_once(test_node) #get a topic once
rp.spin(test_node) #get topics continuously
