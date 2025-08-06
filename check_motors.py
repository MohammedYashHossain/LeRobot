#!/usr/bin/env python3

from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors import Motor, MotorNormMode

def check_motors():
    # Test each motor individually
    motor_configs = {
        'shoulder_pan': (1, MotorNormMode.DEGREES),
        'shoulder_lift': (2, MotorNormMode.DEGREES),
        'elbow_flex': (3, MotorNormMode.DEGREES),
        'wrist_flex': (4, MotorNormMode.DEGREES),
        'wrist_roll': (5, MotorNormMode.DEGREES),
        'gripper': (6, MotorNormMode.RANGE_0_100)
    }
    
    working_motors = []
    
    for name, (motor_id, mode) in motor_configs.items():
        try:
            print(f"Testing {name} (ID {motor_id})...")
            bus = FeetechMotorsBus('COM4', motors={name: Motor(motor_id, 'sts3215', mode)})
            bus.connect()
            pos = bus.motors[name].get_position()
            print(f"  ✅ {name} working - position: {pos}")
            working_motors.append(name)
            bus.disconnect()
        except Exception as e:
            print(f"  ❌ {name} failed - {e}")
    
    print(f"\nWorking motors: {working_motors}")

if __name__ == "__main__":
    check_motors() 