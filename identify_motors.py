#!/usr/bin/env python3
"""
Script to identify which motor ID corresponds to which joint on the follower arm.
This will help fix the wrist_roll and gripper swap issue.
"""

import sys
import os
from pathlib import Path

# Add the lerobot package to the path
sys.path.insert(0, str(Path(__file__).parent / "lerobot" / "src"))

from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors import Motor, MotorNormMode
import time

def identify_motors():
    print("=" * 60)
    print("MOTOR IDENTIFICATION FOR FOLLOWER ARM")
    print("=" * 60)
    print()
    
    # Get the port from user input
    print("Please enter the port where your SO101 follower arm is connected.")
    print("Common ports:")
    print("  - Windows: COM3, COM4, etc.")
    print("  - Linux/Mac: /dev/ttyUSB0, /dev/ttyACM0, etc.")
    print()
    
    port = input("Enter the port: ").strip()
    if not port:
        print("Error: Port is required!")
        return
    
    try:
        # Connect to all motors
        bus = FeetechMotorsBus(port, motors={
            'shoulder_pan': Motor(1, 'sts3215', MotorNormMode.DEGREES),
            'shoulder_lift': Motor(2, 'sts3215', MotorNormMode.DEGREES),
            'elbow_flex': Motor(3, 'sts3215', MotorNormMode.DEGREES),
            'wrist_flex': Motor(4, 'sts3215', MotorNormMode.DEGREES),
            'wrist_roll': Motor(5, 'sts3215', MotorNormMode.DEGREES),
            'gripper': Motor(6, 'sts3215', MotorNormMode.RANGE_0_100)
        })
        
        print(f"Connecting to motors on port {port}...")
        bus.connect()
        print("✅ Connected to all motors")
        
        print("\n" + "=" * 60)
        print("MOTOR IDENTIFICATION TEST")
        print("=" * 60)
        print("This test will help identify which motor ID controls which joint.")
        print("For each motor, we'll try to move it slightly and you can observe which joint moves.")
        print()
        
        # Test each motor individually
        for motor_name in bus.motors:
            print(f"\nTesting {motor_name} (Motor ID {bus.motors[motor_name].id})...")
            print(f"  Current position: {bus.read('Present_Position', motor_name)}")
            
            # Try to move the motor slightly
            try:
                current_pos = bus.read('Present_Position', motor_name)
                test_pos = current_pos + 100  # Move 100 units
                
                print(f"  Moving to position {test_pos}...")
                bus.write('Goal_Position', motor_name, test_pos)
                time.sleep(2)
                
                new_pos = bus.read('Present_Position', motor_name)
                print(f"  New position: {new_pos}")
                
                if abs(new_pos - test_pos) < 50:
                    print(f"  ✅ {motor_name} moved successfully!")
                else:
                    print(f"  ⚠️  {motor_name} may be stuck or not responding")
                
                # Move back to original position
                bus.write('Goal_Position', motor_name, current_pos)
                time.sleep(1)
                
            except Exception as e:
                print(f"  ❌ Error testing {motor_name}: {e}")
            
            print(f"  Which joint moved? (Enter the joint name or 'none' if nothing moved)")
            observed_joint = input("  Your observation: ").strip().lower()
            
            if observed_joint != 'none':
                print(f"  📝 Motor ID {bus.motors[motor_name].id} ({motor_name}) controls {observed_joint}")
        
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print("Based on your observations, we can determine if the wrist_roll and gripper are swapped.")
        print("If Motor ID 5 controls the gripper and Motor ID 6 controls the wrist_roll,")
        print("then they are swapped and we need to fix the configuration.")
        print()
        
        print("To fix the swap issue, you can either:")
        print("1. Physically swap the motor connections on the follower arm")
        print("2. Update the motor configuration in the code")
        print()
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        try:
            bus.disconnect()
            print("Disconnected from motor bus")
        except:
            pass

if __name__ == "__main__":
    identify_motors() 