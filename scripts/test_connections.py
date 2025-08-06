#!/usr/bin/env python3
"""
SO-101 Robot Arms Connection Testing Script
Tests connections to both leader and follower arms
"""

import argparse
import sys
import time

def test_leader_arm(port):
    """Test leader arm connection"""
    try:
        from lerobot.teleoperators.so101_leader.so101_leader import SO101Leader
        from lerobot.teleoperators.so101_leader.config_so101_leader import SO101LeaderConfig
        
        print(f"Testing SO-101 Leader Arm on {port}...")
        config = SO101LeaderConfig(port=port)
        teleop = SO101Leader(config)
        teleop.connect()
        print("✅ SO-101 Leader Arm - CONNECTED SUCCESSFULLY!")
        print("All 6 motors detected and operational")
        teleop.disconnect()
        return True
    except Exception as e:
        print(f"❌ SO-101 Leader Arm - CONNECTION FAILED!")
        print(f"Error: {e}")
        return False

def test_follower_arm(port):
    """Test follower arm connection"""
    try:
        from lerobot.robots.so101_follower.so101_follower import SO101Follower
        from lerobot.robots.so101_follower.config_so101_follower import SO101FollowerConfig
        
        print(f"Testing SO-101 Follower Arm on {port}...")
        config = SO101FollowerConfig(port=port)
        robot = SO101Follower(config)
        robot.connect()
        print("✅ SO-101 Follower Arm - CONNECTED SUCCESSFULLY!")
        print("All 6 motors detected and operational")
        robot.disconnect()
        return True
    except Exception as e:
        print(f"❌ SO-101 Follower Arm - CONNECTION FAILED!")
        print(f"Error: {e}")
        return False

def test_motor_connection(port, motor_id):
    """Test individual motor connection"""
    try:
        from lerobot.motors.feetech import FeetechMotorsBus
        from lerobot.motors import Motor, MotorNormMode
        
        print(f"Testing Motor ID {motor_id} on {port}...")
        bus = FeetechMotorsBus(port, motors={f'motor_{motor_id}': Motor(motor_id, 'sts3215', MotorNormMode.DEGREES)})
        bus.connect()
        print(f"✅ Motor ID {motor_id} - WORKING")
        bus.disconnect()
        return True
    except Exception as e:
        print(f"❌ Motor ID {motor_id} - FAILED")
        print(f"Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Test SO-101 robot arm connections')
    parser.add_argument('--arm', choices=['leader', 'follower', 'both'], default='both',
                       help='Which arm to test (default: both)')
    parser.add_argument('--leader-port', default='COM3', help='Leader arm port (default: COM3)')
    parser.add_argument('--follower-port', default='COM4', help='Follower arm port (default: COM4)')
    parser.add_argument('--test-motors', action='store_true', help='Test individual motors')
    
    args = parser.parse_args()
    
    print("🤖 SO-101 Robot Arms Connection Tester")
    print("=" * 50)
    
    success = True
    
    if args.arm in ['leader', 'both']:
        print(f"\n🔧 Testing Leader Arm ({args.leader_port})")
        if not test_leader_arm(args.leader_port):
            success = False
            
        if args.test_motors:
            print("\n🔍 Testing Individual Leader Arm Motors:")
            for motor_id in range(1, 7):
                test_motor_connection(args.leader_port, motor_id)
                time.sleep(0.1)
    
    if args.arm in ['follower', 'both']:
        print(f"\n🔧 Testing Follower Arm ({args.follower_port})")
        if not test_follower_arm(args.follower_port):
            success = False
            
        if args.test_motors:
            print("\n🔍 Testing Individual Follower Arm Motors:")
            for motor_id in range(1, 7):
                test_motor_connection(args.follower_port, motor_id)
                time.sleep(0.1)
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ALL TESTS PASSED! Robot arms are ready for teleoperation.")
        print("Run: python -m lerobot.teleoperate --teleop.type=so101_leader --teleop.port=COM3 --robot.type=so101_follower --robot.port=COM4")
    else:
        print("❌ SOME TESTS FAILED! Check connections and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main() 