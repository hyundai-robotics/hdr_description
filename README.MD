# HD Hyundai Robotics Description

### Table of Contents
- [Overview](#overview)
- [Package Structure](#package-structure)
- [Installation](#installation)
- [Usage](#usage)

---

## 1. Overview
A collection of robot model descriptions, meshes, and visualization configurations for HD Hyundai Robotics (HDR) robots in ROS2.



## 2. Package Structure
This package contains the following packages:
| Package             | Description                                                                                  |
|---------------------|----------------------------------------------------------------------------------------------|
| `launch/`           | Contains launch file to visualize HDR robots in RViz.                               |
| `rviz/`             | RViz configuration for display_robot.launch.py. |
| `urdf/` | Contains the robot description files used to define the physical, visual, and control properties of HD Hyundai Robotics robots in ROS2.<br>**hdr.urdf.xacro**: Top-level macro including all components.<br>**hdr_transmissions.xacro**: Defines joint transmissions.<br>**hdr.ros2_control.xacro**: Includes ros2_control macros.<br>**robots/**: Model-specific sub-directories with robot XACROs (e.g., `ha006b.urdf.xacro`). |
| `meshes/`           | Catains collision and visual meshes for all models.                                  |

---

## 3. Installation

#### Build the package
##### Create a ROS2 workspace

```bash
# Skip if you already have a workspace
mkdir -p ~/ros2_ws/src/
```

##### Clone the latest repositories

```bash
cd ~/ros2_ws
git clone https://github.com/hyundai-robotics/hdr_description src
```

##### Install ROS2 dependencies

```bash
rosdep update
rosdep install --from-paths src --ignore-src --rosdistro $ROS_DISTRO -y
```

##### Build and source environment
```bash
colcon build --symlink-install --cmake-args=-DCMAKE_BUILD_TYPE=Release
source install/setup.bash
```

---

## 4. Usage

#### Example

##### Visualize a Robot in RViz
The following launch file enables robot control in RViz using a mock hardware interface provided by `mock_components/GenericSystem`.<br>
The joint_state_publisher_gui is launched, allowing manual control of the robot through the GUI.

```bash
ros2 launch hdr_description display_robot.launch.py robot_model:=ha006b
```


#### Configuration Options
The following launch arguments are available in `display_robot.launch.py`:

| Argument Name         | Type   | Default          | Description                                                                 |
|-----------------------|--------|------------------|-----------------------------------------------------------------------------|
| `robot_model`         | string | `ha006b`         | HDR robot model to use. Choose from `[ha006b, hdf7_9, hdf8_8, hdr50_22, hdr220_26, hh020]` |
| `description_package` | string | `hdr_description` | Package containing robot URDF/XACRO files                                  |
| `description_file`    | string | `hdr.urdf.xacro`  | Defines the robot's URDF/XACRO configuration file                          |

---

## Maintainers and License

- **Maintainer**: HD Hyundai Robotics R&D Team
- **License**: This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE)
- **Contact**: <vewry12@hd.com>