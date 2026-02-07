import asyncio
from telegram import Bot
import os
from dotenv import load_dotenv

# Load env to get token
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def get_updates():
    if not TOKEN:
        print("Error: No token found.")
        return

    bot = Bot(token=TOKEN)
    print(f"Checking updates for bot: {TOKEN[:5]}...")
    
    try:
        # Get updates
        updates = await bot.get_updates()
        if not updates:
            print("No updates found. Please send a message 'Hello' to your bot on Telegram first!")
            print(f"Bot Username: @{bot.username} (Search for this in Telegram)")
            return

        print("\n--- Recent Messages ---")
        for u in updates:
            if u.message:
                chat_id = u.message.chat.id
                user = u.message.from_user.username or u.message.from_user.first_name
                text = u.message.text
                print(f"User: {user} | Text: {text} | CHAT ID: {chat_id}")
                print(f"--> YOUR CHAT ID IS: {chat_id}")
        print("-----------------------")
        print("Copy the CHAT ID above and put it in your .env file as TELEGRAM_CHAT_ID")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(get_updates())
