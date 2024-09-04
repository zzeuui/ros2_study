import rclpy as rp
from turtlesim.srv import TeleportAbsolute

rp.init()
test_node = rp.create_node('client_test')

service_name = '/turtle1/teleport_absolute'
cli = test_node.create_client(TeleportAbsolute, service_name)

req = TeleportAbsolute.Request()
req.x = 3.

while not cli.wait_for_service(timeout_sec=1.0):
    print('waiting for service')

cli.call_async(req)
rp.spin_once(test_node)

