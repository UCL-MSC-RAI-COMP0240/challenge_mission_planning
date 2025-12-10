# Mission Planning Challenge

This repository contains the first coursework for the UCL Aerial Robotics Module COMP0240.

![scenario1](docs/images/scenario1.png)

This challenge has been developed on top of the aerostack2 platform 

## Challenge 

You have the challenge of solving the problem of finding the most optimal way of visiting a series of locations and taking pictures of markers, while avoiding the obstacles in the environment. This mirrors real life autonomous inspection scenarios which are the majority of current day use cases with autonomous drones. 

### Structural Inspection Path Planning 

The structural inspection path planning problem is often broken down into three different problems

1. 3D Viewpoint generation, in which a 2.5D or CAD model of the structure is used to determine the optimal set of camera positions which need to be visited in order to generate enough data for a reconstruction. 
2. [This Challenge] Coverage Path Planning / Tour Optimisation & Trajectory Generation, then tries to find the optimal ordering of viewpoints to visit, potentially including the optimal trajectory itself. This often attempts to minimise time, travel distance, energy or other factors. 
3. Trajectory Following & Control is then the lower level controller which attempts to follow the calculated optimal coverage path as close as possible in order to capture the images in a location as close as specified. 

> For further information on structural inspection path planning, see [this article](https://www.autonomousrobotslab.com/structural-inspection-path-planning.html)

### Your Challenge

In this challenge we focus on the second step of finding the optimal route around a set of viewpoints. 

You will be given a *scenario* which specifies:

1. The drone starting location
2. The position and orientation (pose) of each of the viewpoints which you are being requested to visit
3. The location of cuboid shaped obstacles to avoid 

A set of scenarios have been given within the `scenarios` folder for you to use for development and testing. 

Your challenge will be in implementing and comparing a set of methods for controlling a drone to fly around the viewpoints, verifying that all of the specified aruco targets have been seen and visited, whilst avoiding the obstacles. You will need to consider the following:

- Optimal routing and finding a solution to the path planning problem 
- Motion planning and how to route from one viewpoint to another to avoid collisions while preserving energy
- Logging to ensure that your solution has collected "data" and visited every target to proove completion to a potential client. 
- Calculation of relevant metrics (time, distance, speed, etc) for comparison of various methods.

### Interesting things to look up to get you started

- Travelling Salesman Problem
- Combinatorial Optimisation 
- Complete routing graph of all the connectivity of the viewpoints
- Consider the value of the weight on each edge on the routing graph
- Dubins Paths 
- Visualise your paths, maps and routes
- Python Libraries:
  - scipy
  - numpy
  - python_tsp
  - networkx
  - matplotlib

## Installation

To install this project, first setup a ros2 workspace as used to, and pull in required repos

> Make sure that you have sourced ros2: `source /opt/ros/humble/setup.bash` (Add this line to the bottom of your `~/.bashrc`)

```bash
source /opt/ros/humble/setup.bash
mkdir -p /mission_planning_ws/src
cd /mission_planning_ws/src
git clone https://github.com/UCL-MSC-RAI-COMP0240/aerostack2.git
git clone https://github.com/MOCAP4ROS2-Project/mocap4r2_msgs
git clone https://github.com/UCL-MSC-RAI-COMP0240/as2_platform_crazyflie
```

Then also clone the repository:

```bash
git clone https://github.com/UCL-MSC-RAI-COMP0240/challenge_mission_planning.git
```

Build the workspace as normal within ros2 
```bash
cd /mission_planning_ws
colcon build 
```


To start using this project, please go to the root folder of the project.
```bash
cd /mission_planning_ws/src/challenge_mission_planning
```

## Execution

![gazebo_rviz](docs/images/gazebo_rviz.png)

### 1. Launch aerostack2 nodes for each drone
To launch aerostack2 nodes for each drone, execute once the following command in a terminal from the root folder of this repository:

```bash
./launch_as2.bash
```

The flags for the components launcher are:

- **-s**: selects a scenario to run. Defaults to 'scenarios/scenario1.yaml
- **-n**: select drones namespace to launch, values are comma separated. By default, it will get all drones from world description file
- **-c**: if set, the real crazyflie interface will be launched instead of the simulation. Defaults to false
- **-g**: launch using gnome-terminal instead of tmux. Default not set

### 2. Launch aerostack2 nodes for the ground station
To launch aerostack2 nodes for the ground station, execute once the following command:

```bash
./launch_ground_station.bash
```

This launches the visualisation (rviz2) and monitoring elements of the aerostack2 stack. You will be able to monitor the camera views from this command. 

The flags for the components launcher are:

- **-t**: launch keyboard teleoperation. Default not launch
- **-v**: open rviz. Launches by default
- **-r**: record rosbag. Default not launch
- **-n**: drone namespaces, comma separated. Default get from world description config file
- **-g**: launch using gnome-terminal instead of tmux. Default not set

### 3. Launch a mission
There are several missions that can be executed:

- **AS2 keyboard teleoperation control**: You can use the keyboard teleoperation launched with the ground station, using the flag `-t`:
  ```bash
  ./launch_ground_station.bash -t
  ```
  You can launch a **swarm of drones** with the flag `-m` and control them with the keyboard teleoperation, as:
  ```bash
  ./launch_as2.bash -m
  ```
  ```bash
  ./launch_ground_station.bash -m -t
  ```
- **AS2 Python API single drone mission**: You can execute a mission that used AS2 Python API, launching the mission with:
  ```bash
  python3 mission.py
  ```
- **AS2 Mission Interpreter single drone mission**: You can execute a mission that used AS2 Mission Interpreter, launching the mission with:
  ```bash
  python3 mission_interpreter.py
  ```
- **AS2 Behavior Trees single drone mission**: You can execute a mission that used AS2 Behavior Trees, launching the mission with:
  ```bash
  python3 mission_behavior_tree.py
  ```
- **AS2 Python API sample scenario mission**: You can execute a mission that used AS2 Python API and gives an initial simple solution to solving the challenge, launching the mission with:
  ```bash
  python3 mission_scenario.py scenarios/scenario1.yaml
  ```
  By default scenario1 takes 145 seconds to run! 

### 4. End the execution

If you are using tmux, you can end the execution with the following command:

```bash
./stop.bash
```

You can force the end of all tmux sessions with the command:
```bash
tmux kill-server
```

If you are using gnome-terminal, you can end the execution by closing the terminal.


## More Information

Please refer to https://aerostack2.github.io/_02_examples/gazebo/project_gazebo/index.html for more information.


## Developers guide

All projects in aerostack2 are structured in the same way. The project is divided into the following directories:

- **tmuxinator**: Contains the tmuxinator launch file, which is used to launch all aerostack2 nodes.
  - **aerostack2.yaml**: Tmuxinator launch file for each drone. The list of nodes to be launched is defined here.
  - **ground_station.yaml**: Tmuxinator launch file for the ground station. The list of nodes to be launched is defined here.
- **config_sim**: Contains the simulation configuration files for the launchers of the nodes in the drones.
- **config_sim/config/**: Contains the configuration files for the launchers of the nodes in the drones for simulation.
- **config_sim/config_ground_station/**: Contains the configuration files for the launchers of the nodes in the ground station for simulation.
- **config_real**: Contains the real crazyflie configuration files for the launchers of the nodes in the drones.
- **config_real/config/**: Contains the configuration files for the launchers of the nodes in the crazyflies.
- **config_real/config_ground_station/**: Contains the configuration files for the launchers of the nodes in the ground station for crazyflie.
- **launch_as2.bash**: Script to launch nodes defined in *tmuxinator/aerostack2.yaml*.
- **launch_ground_station.bash**: Script to launch nodes defined in *tmuxinator/ground_station.yaml*.
- **mission_\*.py**: Differents python mission files that can be executed.
- **stop.bash**: Script to stop all nodes launched by *launch_as2.bash* and *launch_ground_station.bash*.
- **rosbag/record_rosbag.bash**: Script to record a rosbag. Can be modified to record only the topics that are needed.
- **trees\***: Contains the behavior trees that can be executed. They can be selected in the *aerostack2.yaml* file.
- **utils**: Contains utils scripts for launchers.

Both python and bash scripts have a help message that can be displayed by running the script with the `-h` option. For example, `./launch_as2.bash -h` will display the help message for the `launch_as2.bash` script.

**Note**: For knowing all parameters for each launch, you can execute the following command:

```bash
ros2 launch my_package my_launch.py -s
```

Also, you can see them in the default config file of the package, in the *config* folder. If you want to modify the default parameters, you can add the parameter to the config file.
