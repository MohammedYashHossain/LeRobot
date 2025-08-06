#!/usr/bin/env python3
"""
SO-101 Robot Arms Teleoperation Launcher
Easy-to-use script to start teleoperation
"""

import argparse
import subprocess
import sys
import time
import signal
import os

def run_teleoperation(leader_port='COM3', follower_port='COM4', duration=None):
    """Run teleoperation with specified parameters"""
    
    print("🎮 SO-101 Robot Arms Teleoperation Launcher")
    print("=" * 50)
    print(f"Leader Arm: {leader_port}")
    print(f"Follower Arm: {follower_port}")
    if duration:
        print(f"Duration: {duration} seconds")
    else:
        print("Duration: Unlimited")
    print("=" * 50)
    
    # Build command
    cmd = [
        'python', '-m', 'lerobot.teleoperate',
        '--teleop.type=so101_leader',
        f'--teleop.port={leader_port}',
        '--robot.type=so101_follower',
        f'--robot.port={follower_port}'
    ]
    
    if duration:
        cmd.append(f'--teleop_time_s={duration}')
    
    print(f"Starting teleoperation...")
    print(f"Command: {' '.join(cmd)}")
    print("\nPress Ctrl+C to stop teleoperation")
    print("-" * 50)
    
    try:
        # Run teleoperation
        process = subprocess.Popen(cmd)
        
        if duration:
            print(f"Teleoperation will run for {duration} seconds...")
            time.sleep(duration)
            process.terminate()
            print("Teleoperation completed!")
        else:
            # Wait for user to stop
            process.wait()
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping teleoperation...")
        if 'process' in locals():
            process.terminate()
            process.wait()
        print("Teleoperation stopped.")
    except Exception as e:
        print(f"❌ Error running teleoperation: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Launch SO-101 robot arms teleoperation')
    parser.add_argument('--leader-port', default='COM3', help='Leader arm port (default: COM3)')
    parser.add_argument('--follower-port', default='COM4', help='Follower arm port (default: COM4)')
    parser.add_argument('--duration', type=int, help='Duration in seconds (default: unlimited)')
    parser.add_argument('--test-first', action='store_true', help='Test connections before starting')
    
    args = parser.parse_args()
    
    # Test connections first if requested
    if args.test_first:
        print("🔍 Testing connections first...")
        test_cmd = [
            'python', 'scripts/test_connections.py',
            '--leader-port', args.leader_port,
            '--follower-port', args.follower_port
        ]
        
        try:
            result = subprocess.run(test_cmd, check=True)
            print("✅ Connection test passed!")
        except subprocess.CalledProcessError:
            print("❌ Connection test failed! Please check your setup.")
            sys.exit(1)
    
    # Run teleoperation
    run_teleoperation(args.leader_port, args.follower_port, args.duration)

if __name__ == "__main__":
    main() 