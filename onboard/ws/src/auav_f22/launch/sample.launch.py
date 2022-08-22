from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        # MicroDDS agent to translate PX4 msgs to ROS2
        #ExecuteProcess(
        #    cmd='MicroXRCEAgent udp4 -p 15555'.split(' '),
        #    output='log'
        #),
        ExecuteProcess(
            cmd='micrortps_agent -t UDP -i 172.16.238.11'.split(' '),
            output='screen',
            shell=True,
        ),
        #Node(
        #    package='auav_f22',
        #    executable='offboard',
        #    name='offboard',
        #    output='screen'
        #),
    ])
