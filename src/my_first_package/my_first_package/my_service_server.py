from my_first_package_msgs.srv import MultiSpawn
from turtlesim.srv import Spawn

import rclpy as rp
from rclpy.node import Node
import numpy as np
import time

def calc_position(n, r):
    gap_theta = 2*np.pi / n

    theta = [i*gap_theta for i in range(n)]
    x = [r*np.cos(th) for th in theta]
    y = [r*np.sin(th) for th in theta]

    return x, y, theta

class MultiSpawning(Node):
    def __init__(self):
        super().__init__('multi_spawn')
        self.server = self.create_service(MultiSpawn, 'multi_spawn', self.callback_service)
        self.spawn = self.create_client(Spawn, '/spawn')
        self.req_spawn = Spawn.Request()
        self.center_x = 5.54
        self.center_y = 5.54

    def callback_service(self, request, response):
        x, y, theta = calc_position(request.num, 3)
        for i, j, th in zip(x, y, theta):
            self.req_spawn.x = i + self.center_x
            self.req_spawn.y = j + self.center_y
            self.req_spawn.theta = th
            self.spawn.call_async(self.req_spawn)
            time.sleep(1)

        response.x = x
        response.y = y
        response.theta = theta

        return response

def main(args=None):
    rp.init(args=args)
    multi_spawn = MultiSpawning()
    rp.spin(multi_spawn)
    rp.shutdown()

if __name__=='__main__':
    main()
