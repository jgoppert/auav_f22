from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([get_package_share_directory('ros_ign_gazebo'), '/launch/ign_gazebo.launch.py']),
            launch_arguments={
                'ign_args': 'iris.sdf -r --render-engine ogre2 /usr/share/mavlink_sitl_ign_gazebo/worlds/iris.world --gui-config /home/docker/.ignition/gazebo/6/gui.config'
            }.items(),
        )
    ])