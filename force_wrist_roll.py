#!/usr/bin/env python3

from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors import Motor, MotorNormMode
import time

def force_wrist_roll():
    print("Attempting to force wrist_roll motor to move...")
    
    try:
        # Connect to just the wrist_roll motor
        bus = FeetechMotorsBus('COM4', motors={'wrist_roll': Motor(5, 'sts3215', MotorNormMode.DEGREES)})
        bus.connect()
        
        print("✅ Connected to wrist_roll motor")
        
        # Try to read current position
        try:
            current_pos = bus.read("Present_Position", "wrist_roll", normalize=False)
            print(f"Current position: {current_pos}")
        except:
            print("Could not read current position")
        
        # Method 1: Try to disable torque completely
        print("\nMethod 1: Disabling torque completely...")
        bus.disable_torque()
        print("Torque disabled. Try to manually move the wrist_roll now.")
        print("Press Enter when done...")
        input()
        
        # Method 2: Try to force it with high torque
        print("\nMethod 2: Trying to force movement with high torque...")
        bus.enable_torque()
        
        # Try to set different goal positions
        test_positions = [1000, 2000, 3000, 1500, 2500]
        
        for pos in test_positions:
            try:
                print(f"Trying to force move to position {pos}...")
                bus.write("Goal_Position", "wrist_roll", pos, normalize=False)
                time.sleep(3)
                
                # Check if it moved
                try:
                    actual_pos = bus.read("Present_Position", "wrist_roll", normalize=False)
                    print(f"  Actual position: {actual_pos}")
                    if abs(actual_pos - pos) < 100:
                        print("  ✅ Motor moved successfully!")
                        break
                except:
                    print("  Could not read position")
                    
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
        # Method 3: Try to reset the motor
        print("\nMethod 3: Trying to reset motor settings...")
        try:
            # Try to reset some motor parameters
            bus.write("Torque_Enable", "wrist_roll", 0)  # Disable torque
            time.sleep(1)
            bus.write("Torque_Enable", "wrist_roll", 1)  # Re-enable torque
            print("Motor settings reset")
        except Exception as e:
            print(f"Reset failed: {e}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        try:
            bus.disconnect()
            print("Disconnected from motor bus")
        except:
            pass

if __name__ == "__main__":
    force_wrist_roll() 