#!/usr/bin/env python3

from lerobot.robots.so101_follower.so101_follower import SO101Follower
from lerobot.robots.so101_follower.config_so101_follower import SO101FollowerConfig

def test_motor_ranges():
    config = SO101FollowerConfig(port='COM4')
    robot = SO101Follower(config)
    
    try:
        robot.connect()
        print("Motor positions and ranges:")
        print("-" * 40)
        
        for name, motor in robot.bus.motors.items():
            pos = motor.get_position()
            print(f"{name}: position = {pos}")
            
        print("\nTesting gripper movement:")
        gripper = robot.bus.motors['gripper']
        current_pos = gripper.get_position()
        print(f"Current gripper position: {current_pos}")
        
        # Try to move gripper to different positions
        test_positions = [0, 50, 100]
        for pos in test_positions:
            try:
                print(f"Trying to move gripper to {pos}...")
                gripper.set_position(pos)
                actual_pos = gripper.get_position()
                print(f"  Actual position: {actual_pos}")
            except Exception as e:
                print(f"  Error: {e}")
                
        print("\nTesting shoulder pan movement:")
        shoulder_pan = robot.bus.motors['shoulder_pan']
        current_pos = shoulder_pan.get_position()
        print(f"Current shoulder pan position: {current_pos}")
        
        # Try to move shoulder pan
        test_positions = [-90, 0, 90]
        for pos in test_positions:
            try:
                print(f"Trying to move shoulder pan to {pos}...")
                shoulder_pan.set_position(pos)
                actual_pos = shoulder_pan.get_position()
                print(f"  Actual position: {actual_pos}")
            except Exception as e:
                print(f"  Error: {e}")
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        robot.disconnect()

if __name__ == "__main__":
    test_motor_ranges() 