#!/usr/bin/env python
"""Check system status"""
import sys
import json
sys.path.append('..')

def check_status():
    print("📊 System Status\n")
    
    # Check queues
    for queue_file in ['content_queue.json', 'expert_queue.json']:
        try:
            with open(f'data/{queue_file}', 'r') as f:
                items = json.load(f)
                print(f"{queue_file}: {len(items)} items")
        except:
            print(f"{queue_file}: Empty or not found")
    
    print("\n✅ System ready")

if __name__ == "__main__":
    check_status()