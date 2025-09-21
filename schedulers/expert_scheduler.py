# expert_scheduler.py
import schedule
import time
import subprocess
from datetime import datetime

def generate_daily_expert_content():
    """Generate expert content for the day"""
    print(f"\n🌅 {datetime.now().strftime('%Y-%m-%d %H:%M')} - Generating daily expert content...")
    subprocess.run(["python", "expert_content_generator.py"])

def post_scheduled_content():
    """Check and post any scheduled content"""
    subprocess.run(["python", "post_expert_content.py"])

def run_expert_scheduler():
    """Run the expert content scheduler"""
    print("🤖 Expert Content Scheduler Started")
    print("📅 Schedule:")
    print("  - Daily content generation: 7:00 AM")
    print("  - Posting times: 9:00, 10:30, 11:45, 14:00, 15:30, 17:00, 18:30")
    
    # Generate content every morning
    schedule.every().day.at("07:00").do(generate_daily_expert_content)
    
    # Check for posts throughout the day
    post_times = ["09:00", "10:30", "11:45", "14:00", "15:30", "17:00", "18:30"]
    for time_slot in post_times:
        schedule.every().day.at(time_slot).do(post_scheduled_content)
    
    # Also check every 30 minutes as backup
    schedule.every(30).minutes.do(post_scheduled_content)
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    run_expert_scheduler()