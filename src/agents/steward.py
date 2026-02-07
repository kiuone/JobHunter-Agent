from typing import List, Dict, Any
import asyncio
from telegram import Bot
from src.core.config import get_supabase_client, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

class Steward:
    def __init__(self):
        self.supabase = get_supabase_client()
        self.bot = Bot(token=TELEGRAM_BOT_TOKEN) if TELEGRAM_BOT_TOKEN else None
        self.chat_id = TELEGRAM_CHAT_ID

    def check_exists(self, url: str) -> bool:
        response = self.supabase.table("jobs").select("id").eq("application_url", url).execute()
        return len(response.data) > 0

    async def send_telegram_alert(self, job: Dict[str, Any]):
        if not self.bot or not self.chat_id:
            return

        category = job.get("fit_category", "UNKNOWN")
        if category in ["TRASH"]:
            return

        icon = "🏆" if category == "GOLD" else "✨" if category == "SILVER" else "❓"
        title = job.get("title", "No Title")
        
        # Get company name if not present
        company_name = "Unknown Company"
        if job.get("company_id"):
            try:
                 companies = self.supabase.table("companies").select("name").eq("id", job.get("company_id")).execute()
                 if companies.data:
                     company_name = companies.data[0]["name"]
            except:
                pass

        msg = (
            f"{icon} *NEW {category} OPPORTUNITY*\n\n"
            f"**Role**: {title}\n"
            f"**Company**: {company_name}\n"
            f"**Location**: {job.get('details', {}).get('location', 'Unknown')}\n"
            f"**Link**: {job.get('application_url')}\n\n"
            f"_{job.get('details', {}).get('fit_reason', '')}_"
        )
        
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=msg, parse_mode="Markdown")
        except Exception as e:
            print(f"Failed to send Telegram alert: {e}")

    async def save_and_notify(self, jobs: List[Dict[str, Any]]):
        if not jobs:
            return

        from thefuzz import fuzz

        new_jobs = []
        for job in jobs:
            url = job.get("application_url") or job.get("url") # Fallback
            title = job.get("title", "").lower()
            company_id = job.get("company_id")

            # 1. URL Check
            if url and self.check_exists(url):
                print(f"Duplicate URL: {url}")
                continue

            # 2. Content Check (Fuzzy)
            # Fetch recent jobs for this company to compare
            # Optimally we should fetch ONLY jobs for this company, but we need company_id
            if company_id:
                existing_jobs = self.supabase.table("jobs").select("title").eq("company_id", company_id).order("created_at", desc=True).limit(50).execute()
                is_duplicate = False
                for existing in existing_jobs.data:
                    existing_title = existing.get("title", "").lower()
                    ratio = fuzz.token_set_ratio(title, existing_title)
                    if ratio > 85: # High similarity threshold
                        print(f"Duplicate Content: '{title}' too similar to '{existing_title}' ({ratio}%)")
                        is_duplicate = True
                        break
                
                if is_duplicate:
                    continue

            # If unique, proceed
            payload = {
                "company_id": company_id,
                "title": job.get("title"),
                "fit_category": job.get("fit_category"),
                "fit_score": 0, 
                "application_url": url,
                "source_type": "Scraped",
                "details": job 
            }
            new_jobs.append(payload)
            
            # Notify
            await self.send_telegram_alert(job)
        
        if new_jobs:
            try:
                self.supabase.table("jobs").insert(new_jobs).execute()
                print(f"Steward saved {len(new_jobs)} new jobs.")
            except Exception as e:
                print(f"Error saving jobs: {e}")
        else:
            print("No new jobs to save.")

    def run(self, analyzed_jobs: List[Dict]):
        # Async wrapper for sync run call
        asyncio.run(self.save_and_notify(analyzed_jobs))

if __name__ == "__main__":
    pass
