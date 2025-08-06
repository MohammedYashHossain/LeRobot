#!/usr/bin/env python3
"""
Fixed follower arm configuration with correct motor mapping.
This fixes the wrist_roll and gripper swap issue.
"""

import sys
import os
from pathlib import Path

# Add the lerobot package to the path
sys.path.insert(0, str(Path(__file__).parent / "lerobot" / "src"))

from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors import Motor, MotorNormMode, MotorCalibration
import json
import time

def create_fixed_calibration():
    print("=" * 60)
    print("CREATING FIXED FOLLOWER ARM CALIBRATION")
    print("=" * 60)
    print()
    print("This will create a calibration with the correct motor mapping:")
    print("- Motor ID 5 = gripper (not wrist_roll)")
    print("- Motor ID 6 = wrist_roll (not gripper)")
    print()
    
    # Get the port from user input
    print("Please enter the port where your SO101 follower arm is connected.")
    port = input("Enter the port: ").strip()
    if not port:
        print("Error: Port is required!")
        return
    
    try:
        # Connect with the CORRECT motor mapping
        bus = FeetechMotorsBus(port, motors={
            'shoulder_pan': Motor(1, 'sts3215', MotorNormMode.DEGREES),
            'shoulder_lift': Motor(2, 'sts3215', MotorNormMode.DEGREES),
            'elbow_flex': Motor(3, 'sts3215', MotorNormMode.DEGREES),
            'wrist_flex': Motor(4, 'sts3215', MotorNormMode.DEGREES),
            'gripper': Motor(5, 'sts3215', MotorNormMode.RANGE_0_100),  # This is actually gripper
            'wrist_roll': Motor(6, 'sts3215', MotorNormMode.DEGREES)   # This is actually wrist_roll
        })
        
        print(f"Connecting to motors on port {port} with FIXED mapping...")
        bus.connect()
        print("✅ Connected to all motors")
        
        # Disable torque for manual movement
        print("\nDisabling torque for manual movement...")
        bus.disable_torque()
        
        print("\n" + "=" * 60)
        print("MANUAL CALIBRATION WITH FIXED MAPPING")
        print("=" * 60)
        print("Now move each joint manually to test the correct mapping:")
        print("1. Move the gripper (should be controlled by 'gripper' motor)")
        print("2. Move the wrist_roll (should be controlled by 'wrist_roll' motor)")
        print()
        
        input("Press ENTER when ready to start calibration...")
        
        # Enable torque for calibration
        bus.enable_torque()
        
        print("\nMove the arm to the middle of its range of motion and press ENTER...")
        input()
        
        # Set homing offsets
        homing_offsets = bus.set_half_turn_homings()
        
        print("\nMove all joints sequentially through their entire ranges of motion.")
        print("Recording positions. Press ENTER to stop...")
        input()
        
        range_mins, range_maxes = bus.record_ranges_of_motion()
        
        # Create calibration with correct mapping
        calibration = {}
        for motor, m in bus.motors.items():
            calibration[motor] = MotorCalibration(
                id=m.id,
                drive_mode=0,
                homing_offset=homing_offsets[motor],
                range_min=range_mins[motor],
                range_max=range_maxes[motor],
            )
        
        # Save the fixed calibration
        calibration_file = Path("calibration/robots/so101_follower/fixed_follower_arm.json")
        calibration_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(calibration_file, 'w') as f:
            json.dump(calibration, f, indent=4)
        
        print(f"\n✅ Fixed calibration saved to: {calibration_file}")
        print("\nNow you can use this fixed calibration for teleoperation!")
        print("The wrist_roll and gripper should now work correctly.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        try:
            bus.disconnect()
            print("Disconnected from motor bus")
        except:
            pass

if __name__ == "__main__":
    create_fixed_calibration() 