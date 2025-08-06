#!/usr/bin/env python3

from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors import Motor, MotorNormMode
import time

def disable_all_torque():
    print("Disabling torque on ALL motors...")
    
    try:
        # Connect to all motors
        bus = FeetechMotorsBus('COM4', motors={
            'shoulder_pan': Motor(1, 'sts3215', MotorNormMode.DEGREES),
            'shoulder_lift': Motor(2, 'sts3215', MotorNormMode.DEGREES),
            'elbow_flex': Motor(3, 'sts3215', MotorNormMode.DEGREES),
            'wrist_flex': Motor(4, 'sts3215', MotorNormMode.DEGREES),
            'wrist_roll': Motor(5, 'sts3215', MotorNormMode.DEGREES),
            'gripper': Motor(6, 'sts3215', MotorNormMode.RANGE_0_100)
        })
        bus.connect()
        
        print("✅ Connected to all motors")
        
        # Disable torque on all motors
        print("Disabling torque on all motors...")
        bus.disable_torque()
        
        print("✅ ALL MOTORS ARE NOW LOOSE!")
        print("You can now manually move any motor to reset their positions.")
        print("Press Enter when you're done...")
        
        input()  # Wait for user to press Enter
        
        # Re-enable torque
        print("Re-enabling torque on all motors...")
        bus.enable_torque()
        print("✅ All motors torque re-enabled!")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        try:
            bus.disconnect()
            print("Disconnected from motor bus")
        except:
            pass

if __name__ == "__main__":
    disable_all_torque() 