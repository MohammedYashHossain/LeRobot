#!/usr/bin/env python3

from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors import Motor, MotorNormMode
import time

def fix_wrist_roll():
    print("Attempting to fix stuck wrist_roll motor...")
    
    try:
        # Connect to just the wrist_roll motor
        bus = FeetechMotorsBus('COM4', motors={'wrist_roll': Motor(5, 'sts3215', MotorNormMode.DEGREES)})
        bus.connect()
        
        current_pos = bus.read("Present_Position", "wrist_roll")
        print(f"Current wrist_roll position: {current_pos}")
        
        # Try to disable torque first
        print("Disabling torque...")
        bus.disable_torque()
        time.sleep(1)
        
        # Try to manually move it to different positions
        test_positions = [current_pos - 100, current_pos + 100, 2048, 1024, 3072]
        
        for pos in test_positions:
            try:
                print(f"Trying to move wrist_roll to {pos}...")
                bus.write("Goal_Position", "wrist_roll", pos)
                time.sleep(2)
                actual_pos = bus.read("Present_Position", "wrist_roll")
                print(f"  Actual position: {actual_pos}")
                
                if abs(actual_pos - pos) < 50:  # If it moved successfully
                    print("  ✅ Wrist_roll is now responding!")
                    break
                    
            except Exception as e:
                print(f"  ❌ Error: {e}")
                # Try to disable torque again
                try:
                    bus.disable_torque()
                    time.sleep(1)
                except:
                    pass
        
        # Re-enable torque
        print("Re-enabling torque...")
        bus.enable_torque()
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        try:
            bus.disconnect()
        except:
            pass

if __name__ == "__main__":
    fix_wrist_roll() 