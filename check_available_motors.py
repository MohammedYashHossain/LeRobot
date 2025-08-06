#!/usr/bin/env python3
"""
Script to check which motors are actually available on the follower arm.
"""

import sys
import os
from pathlib import Path

# Add the lerobot package to the path
sys.path.insert(0, str(Path(__file__).parent / "lerobot" / "src"))

from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors import Motor, MotorNormMode
import time

def check_available_motors():
    print("=" * 60)
    print("CHECKING AVAILABLE MOTORS ON FOLLOWER ARM")
    print("=" * 60)
    print()
    
    # Get the port from user input
    print("Please enter the port where your SO101 follower arm is connected.")
    port = input("Enter the port (e.g., COM4): ").strip()
    if not port:
        print("Error: Port is required!")
        return
    
    try:
        # Try to connect and see what motors are available
        print(f"\nScanning for motors on port {port}...")
        
        # Try different motor configurations
        motor_configs = [
            {
                'shoulder_pan': Motor(1, 'sts3215', MotorNormMode.DEGREES),
                'shoulder_lift': Motor(2, 'sts3215', MotorNormMode.DEGREES),
                'elbow_flex': Motor(3, 'sts3215', MotorNormMode.DEGREES),
                'wrist_flex': Motor(4, 'sts3215', MotorNormMode.DEGREES),
                'gripper': Motor(5, 'sts3215', MotorNormMode.RANGE_0_100),
                'wrist_roll': Motor(6, 'sts3215', MotorNormMode.DEGREES)
            },
            {
                'shoulder_pan': Motor(1, 'sts3215', MotorNormMode.DEGREES),
                'shoulder_lift': Motor(2, 'sts3215', MotorNormMode.DEGREES),
                'gripper': Motor(5, 'sts3215', MotorNormMode.RANGE_0_100),
                'wrist_roll': Motor(6, 'sts3215', MotorNormMode.DEGREES)
            }
        ]
        
        for i, motors in enumerate(motor_configs):
            print(f"\nTrying configuration {i+1} with {len(motors)} motors...")
            try:
                bus = FeetechMotorsBus(port, motors=motors)
                bus.connect()
                print(f"✅ Successfully connected to {len(motors)} motors!")
                print("Available motors:")
                for name, motor in motors.items():
                    print(f"  - {name}: ID {motor.id}")
                
                # Disable torque to free up motors
                print("\nDisabling torque on all motors...")
                bus.disable_torque()
                print("✅ Torque disabled - motors should be free to move")
                
                bus.disconnect()
                return motors
                
            except Exception as e:
                print(f"❌ Configuration {i+1} failed: {e}")
                continue
        
        print("\n❌ No working motor configuration found!")
        print("Please check:")
        print("1. The port is correct")
        print("2. The follower arm is powered on")
        print("3. The USB connection is working")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_available_motors() 