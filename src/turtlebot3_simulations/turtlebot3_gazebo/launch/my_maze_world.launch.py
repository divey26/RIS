from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Get package directories
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_tb3_gazebo = get_package_share_directory('turtlebot3_gazebo')
    pkg_tb3_description = get_package_share_directory('turtlebot3_description')

    # Path to your custom world file
    world = os.path.join(pkg_tb3_gazebo, 'worlds', 'my_maze_world.world')

    # URDF model path
    robot_urdf = os.path.join(pkg_tb3_description, 'urdf', 'turtlebot3_burger.urdf')

    # Allow toggling Gazebo client (GUI) for WSL compatibility
    gui = LaunchConfiguration('gui')

    return LaunchDescription([
        # Expose gui argument (true by default)
        DeclareLaunchArgument(
            'gui', default_value='true',
            description='Launch Gazebo client (gzclient) if true'
        ),
        # Launch Gazebo with custom world
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
            ),
            launch_arguments={'world': world, 'gui': gui}.items(),
        ),

        # Spawn the TurtleBot3 robot
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_tb3_gazebo, 'launch', 'spawn_turtlebot3.launch.py')
            ),
        ),
    ])
