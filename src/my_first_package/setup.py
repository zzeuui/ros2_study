from setuptools import find_packages, setup

package_name = 'my_first_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='linuxbrew',
    maintainer_email='linuxbrew@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'my_first_node = my_first_package.my_first_node:main',
            'my_subscriber = my_first_package.my_subscriber:main',
            'my_publisher = my_first_package.my_publisher:main',
            'turtle_cmd_and_pose = my_first_package.turtle_cmd_and_pose:main',
            'my_service_server = my_first_package.my_service_server:main',
            'dist_turtle_action_server = my_first_package.dist_turtle_action_server:main',
            'my_multi_thread = my_first_package.my_multi_thread:main',
        ],
    },
)
