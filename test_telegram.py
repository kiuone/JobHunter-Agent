import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv

# Load env
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def test_telegram():
    print("--- Telegram Tester ---")
    if not TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN not found in .env")
        return
    if not CHAT_ID:
        print("ERROR: TELEGRAM_CHAT_ID not found in .env")
        return
    
    print(f"Token: {TOKEN[:5]}...{TOKEN[-5:]}")
    print(f"Chat ID: {CHAT_ID}")
    
    bot = Bot(token=TOKEN)
    try:
        print("Sending test message...")
        await bot.send_message(chat_id=CHAT_ID, text="🤖 JobHunter Agent: Hello via Telegram! Configuration is correct.")
        print("SUCCESS! Check your Telegram.")
    except Exception as e:
        print(f"FAILED: {e}")
        print("\nTroubleshooting:")
        print("1. Did you start a conversation with the bot? Search for your bot username and click 'Start'.")
        print("2. Is the Chat ID correct? It's usually a number (e.g., 123456789).")
        print("   You can get your ID by messaging @userinfobot on Telegram.")

if __name__ == "__main__":
    asyncio.run(test_telegram())
