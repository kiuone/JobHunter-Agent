import time
import schedule
from src.graph import app

def run_watchdog_cycle():
    print("Starting Watchdog (72h cycle)...")
    try:
        app.invoke({"companies": [], "job_urls": [], "analyzed_jobs": []})
        print("Cycle completed.")
    except Exception as e:
        print(f"Error in cycle: {e}")

async def send_startup_msg():
    from telegram import Bot
    import os
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if token and chat_id:
        try:
            bot = Bot(token=token)
            await bot.send_message(chat_id=chat_id, text="🚀 JobHunter Agent Started (v1.0 - Free Tier Mode)")
        except:
            pass

def main():
    print("JobHunter Agent Starting...")
    import asyncio
    try:
        asyncio.run(send_startup_msg())
    except:
        pass
    
    # Run immediately on startup
    run_watchdog_cycle()

    # Schedule: Every 3 days (72 hours)
    schedule.every(3).days.do(run_watchdog_cycle)
    
    print("Scheduler active. Press Ctrl+C to exit.")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
