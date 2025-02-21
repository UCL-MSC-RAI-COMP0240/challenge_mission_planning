import yaml
import json
import math
import argparse
import os
from jinja2 import Template

# Template for SDF file
SDF_TEMPLATE = """<?xml version="1.0" ?>
<sdf version="1.6">
  <model name="{{ model_name }}">
    <static>true</static>
    <link name="link">
      <visual name="visual">
        <geometry>
          <box>
            <size>{{ width }} {{ depth }} {{ height }}</size>
          </box>
        </geometry>
        <material>
          <ambient>1.0 0.5 0.5 1.0</ambient>
          <diffuse>1.0 0.5 0.5 1.0</diffuse>
        </material>
      </visual>
      <collision name="collision">
        <geometry>
          <box>
            <size>{{ width }} {{ depth }} {{ height }}</size>
          </box>
        </geometry>
      </collision>
    </link>
  </model>
</sdf>
"""

# Template for model.config
MODEL_CONFIG_TEMPLATE = """<?xml version="1.0" ?>
<model>
  <name>{{ model_name }}</name>
  <version>1.0</version>
  <sdf version="1.6">{{ model_name }}.sdf</sdf>
  <author>
    <name>Your Name</name>
    <email>your.email@example.com</email>
  </author>
  <description>
    A cuboid model with dimensions: Width={{ width }}, Depth={{ depth }}, Height={{ height }}
  </description>
</model>
"""

def generate_cuboid_model(output_dir, model_name, width, depth, height):
    """Generate SDF and model.config for a cuboid."""
    model_dir = os.path.join(output_dir, model_name)
    os.makedirs(model_dir, exist_ok=True)
    
    # Render SDF file
    sdf_content = Template(SDF_TEMPLATE).render(
        model_name=model_name,
        width=width,
        depth=depth,
        height=height
    )
    with open(os.path.join(model_dir, f"{model_name}.sdf"), "w") as sdf_file:
        sdf_file.write(sdf_content)
    
    # Render model.config
    config_content = Template(MODEL_CONFIG_TEMPLATE).render(
        model_name=model_name,
        width=width,
        depth=depth,
        height=height
    )
    with open(os.path.join(model_dir, "model.config"), "w") as config_file:
        config_file.write(config_content)

# Function to calculate marker pose
# Marker is placed 1 meter in front of the viewpoint's orientation (yaw)
def calculate_marker_pose(viewpoint, marker_distance=1.0):
    x = viewpoint['x'] + marker_distance * math.cos(viewpoint['w'])
    y = viewpoint['y'] + marker_distance * math.sin(viewpoint['w'])
    z = viewpoint['z']  # Assuming marker is at the same height as the viewpoint
    return {'x': x, 'y': y, 'z': z}

# Read the YAML scenario file
def read_scenario(file_path):
    with open(file_path, 'r') as file:
        scenario = yaml.safe_load(file)
    return scenario

def get_start_pose(scenario: dict):
    start_pose = list(scenario["drone_start_pose"].values())
    return (start_pose)
# Write the JSON world configuration
def write_world_config(scenario, model_type, world_name, output_folder, world_file_name, marker_distance):
    os.makedirs(output_folder, exist_ok=True)
    start_pose = get_start_pose(scenario)
    start_pose[2] = 0.5
    world_config = {
        "world_name": world_name,
        "origin": {
            "latitude": 40.4405287,
            "longitude": -3.6898277,
            "altitude": 100.0
        },
        "drones": [
            {
                "model_type": model_type,
                "model_name": "drone0",
                "xyz": start_pose, 
                "rpy": [0, 0, 0.0],
                "flight_time": 60,
                "payload": [
                    {
                        "model_name": "hd_camera",
                        "model_type": "hd_camera",
                        "rpy": [0.0, 0.0, 0.0]
                    }
                ]
            }
        ],
        "objects": []
    }

    # Add obstacles as objects
    for key, obstacle in scenario.get('obstacles', {}).items():
        model_name = f"obstacle_{key}"
        world_config['objects'].append({
            "model_type": model_name,
            "model_name": model_name,
            "xyz": [obstacle['x'], obstacle['y'], obstacle['z']],
            "rpy": [0, 0, 0]
        })
        generate_cuboid_model(
            os.path.join(output_folder, "models"), model_name, 
            obstacle['w'], obstacle['d'], obstacle['h'])

    # Add viewpoint markers as ArUco markers
    # As in config_sim/gazebo/models all aruco models are idX4_marker
    for key, viewpoint in scenario.get('viewpoint_poses', {}).items():
        marker_pose = calculate_marker_pose(viewpoint, marker_distance)
        model_type = f"aruco_id{(key%8) + 1}4_marker"
        world_config['objects'].append({
            "model_type": model_type,
            "model_name": f"id{key}",
            "xyz": [marker_pose['x'], marker_pose['y'], marker_pose['z']],
            "rpy": [0, math.pi/2.0, viewpoint['w'] - math.pi]
        })

    with open(os.path.join(output_folder, world_file_name), 'w') as file:
        yaml.dump(world_config, file)
        # json.dump(world_config, file, indent=4)

# Main function
def main():
    parser = argparse.ArgumentParser(description="Generate JSON world configuration from YAML scenario.")
    parser.add_argument('input_file', type=str, help="Path to the input YAML scenario file.")
    parser.add_argument('output_folder', type=str, help="Folder to the output YAML world configuration file and generated models")
    parser.add_argument('--model_type', type=str, default="quadrotor_base", help="Model type for the drone.")
    parser.add_argument('--world_name', type=str, default="empty", help="Name of the world.")
    parser.add_argument('--world_file_name', type=str, default="world.yaml", help="Name of the world.")
    parser.add_argument('--marker_distance', type=float, default=1.0, help="Distance away from viewpoint to generate marker.")

    args = parser.parse_args()

    scenario = read_scenario(args.input_file)
    write_world_config(scenario, args.model_type, args.world_name, args.output_folder, args.world_file_name, args.marker_distance)
    print(f"Scenario from {args.input_file} world configuration written to {args.output_folder}")

if __name__ == "__main__":
    main()
