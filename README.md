# SO-101 Robot Arms Teleoperation Configuration

This repository contains the complete configuration and calibration data for SO-101 Leader and Follower robot arms teleoperation using LeRobot framework.

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- LeRobot framework
- SO-101 robot arms with Feetech motors (sts3215)
- USB connections for both arms

### Installation
```bash
# Clone this repository
git clone https://github.com/MohammedYashHossain/LeRobot.git
cd LeRobot

# Install LeRobot with required dependencies
pip install -e lerobot[pygame-dep,transformers-dep]

# Copy calibration data
cp -r calibration/ ~/.cache/huggingface/lerobot/
```

### Hardware Setup
- **Leader Arm**: COM3 (USB connection)
- **Follower Arm**: COM4 (USB connection)
- **Motor IDs**: 1, 2, 3, 4, 5, 6 (both arms)
- **Motor Model**: sts3215 (model number 777)
- **Baudrate**: 1,000,000

### Run Teleoperation
```bash
python -m lerobot.teleoperate --teleop.type=so101_leader --teleop.port=COM3 --robot.type=so101_follower --robot.port=COM4
```

## 📁 Repository Structure

```
LeRobot/
├── calibration/                 # Calibration data
│   ├── robots/
│   │   └── so101_follower/
│   │       └── None.json       # Follower arm calibration
│   └── teleoperators/
│       └── so101_leader/
│           └── None.json       # Leader arm calibration
├── config/                      # Configuration files
│   ├── motor_config.txt        # Motor specifications
│   └── hardware_specs.txt      # Hardware requirements
├── scripts/                     # Utility scripts
│   ├── setup_motors.py         # Motor setup script
│   ├── test_connections.py     # Connection testing
│   └── run_teleop.py          # Teleoperation launcher
└── README.md                   # This file
```

## 🔧 Configuration Details

### Motor Configuration
- **Shoulder Pan**: ID 1, sts3215, Degrees mode
- **Shoulder Lift**: ID 2, sts3215, Degrees mode  
- **Elbow Flex**: ID 3, sts3215, Degrees mode
- **Wrist Flex**: ID 4, sts3215, Degrees mode
- **Wrist Roll**: ID 5, sts3215, Degrees mode
- **Gripper**: ID 6, sts3215, Range 0-100 mode

### Calibration Data
The calibration files contain:
- **Min/Max positions** for each joint
- **Current position ranges**
- **Safety limits**
- **Normalization parameters**

## 🎮 Usage

### Testing Connections
```bash
# Test leader arm
python scripts/test_connections.py --arm=leader --port=COM3

# Test follower arm  
python scripts/test_connections.py --arm=follower --port=COM4
```

### Setup Motors
```bash
# Setup leader arm motors
python -m lerobot.setup_motors --teleop.type=so101_leader --teleop.port=COM3

# Setup follower arm motors
python -m lerobot.setup_motors --robot.type=so101_follower --robot.port=COM4
```

### Find Ports
```bash
python -m lerobot.find_port
```

## 📊 Performance
- **Teleoperation Frequency**: ~58-59 Hz
- **Response Time**: ~17ms
- **Connection**: Stable USB serial communication

## 🔍 Troubleshooting

### Common Issues
1. **Port not found**: Run `python -m lerobot.find_port`
2. **Motors not detected**: Check USB connections and power
3. **Calibration errors**: Re-run motor setup process

### Port Changes
If COM ports change on different computers:
1. Run `python -m lerobot.find_port`
2. Update port numbers in commands
3. Test connections before running teleoperation

## 📝 Notes
- Calibration data is specific to this hardware setup
- Motor IDs must match exactly (1-6)
- Same motor models (sts3215) required
- USB connections must be stable

## 🤝 Contributing
This configuration is specific to SO-101 robot arms with Feetech motors. For different hardware, adjust motor IDs, models, and calibration data accordingly.

## 📄 License
This configuration is provided as-is for educational and research purposes. 