from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution, TextSubstitution
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Launch arguments
    model_arg = DeclareLaunchArgument(
        # 'model', default_value='4x4', description='Xela model type (e.g. 4x4)'
        # 'model', default_value='ahrcpcpn', description='Xela model type (e.g. 4x4)'
        # 'model', default_value='my_xela_allegro', description='Xela model type (e.g. 4x4)'
        # 'model', default_value='xela_allegro', description='Xela model type (e.g. 4x4)'
        'model', default_value='tactile_xela_allegro', description='Xela model type (e.g. 4x4)'
    )
    gui_arg = DeclareLaunchArgument(
        'gui', default_value='true', description='Use joint_state_publisher_gui if true'
    )
    rvizconfig_arg = DeclareLaunchArgument(
        'rvizconfig',
        default_value=PathJoinSubstitution([
            FindPackageShare('xela_models'),
            'rviz',
            # 'my_urdf.rviz'
            'xela_allegro.rviz'
        ]),
        description='RViz configuration file'
    )

    # Build path to .xacro file using only valid substitutions
    xacro_file = PathJoinSubstitution([
        FindPackageShare('xela_models'),
        'urdf',
        LaunchConfiguration('model')  # this will be like "4x4"
    ])

    # Append ".xacro" in the command instead of the path
    robot_description = Command([
        'xacro',
        ' ',
        xacro_file,
        # TextSubstitution(text='.xacro')    # visualization using xacro
        TextSubstitution(text='.urdf')      # visualization using urdf
    ])

    # Nodes
    joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        condition=IfCondition(LaunchConfiguration('gui'))
    )

    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        condition=UnlessCondition(LaunchConfiguration('gui'))
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
        output='screen'
    )

    return LaunchDescription([
        model_arg,
        gui_arg,
        rvizconfig_arg,
        joint_state_publisher_gui,
        joint_state_publisher,
        robot_state_publisher_node,
        rviz_node
    ])
