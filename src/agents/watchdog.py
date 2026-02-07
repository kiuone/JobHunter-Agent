from datetime import datetime, timedelta
from typing import List, Dict, Any
from duckduckgo_search import DDGS
import time
from src.core.config import get_supabase_client

class Watchdog:
    def __init__(self):
        self.supabase = get_supabase_client()
        # Tavily removed in favor of free DDG
        self.ddgs = DDGS()

    def get_active_companies(self) -> List[Dict]:
        response = self.supabase.table("companies").select("*").eq("status", "active").execute()
        return response.data

    def search_jobs(self, company: Dict) -> List[str]:
        """
        Searches for job openings using DuckDuckGo (Free).
        """
        company_name = company["name"]
        keywords = company.get("search_keywords", ["estágio"])
        
        # Optimize: Single query with OR operator
        keywords_str = " OR ".join(keywords)
        query = f"{company_name} vagas ({keywords_str}) site:linkedin.com/jobs OR site:gupy.io OR site:vagas.com.br"
        # Note: DDG site: params are powerful. We can broaden this or keep it targeted.
        # Broader query for better recall:
        query = f'site:br.linkedin.com/jobs OR site:*.gupy.io OR site:vagas.com.br "{company_name}" ("estágio" OR "trainee" OR "dados")'

        search_results = []
        try:
            # DDGS text search
            # region="br-pt" optimizes for Brazil
            results = self.ddgs.text(query, region="br-pt", max_results=5)
            search_results.extend(results)
            time.sleep(2) # Respect rate limits
        except Exception as e:
            print(f"Error searching for {company_name}: {e}")

        # Extract URLs (DDGS returns 'href')
        urls = [result.get("href") for result in search_results if result.get("href")]
        return list(set(urls))

    def run(self):
        print("Watchdog started...")
        companies = self.get_active_companies()
        
        jobs_found = []
        for company in companies:
            print(f"Checking {company['name']}...")
            urls = self.search_jobs(company)
            for url in urls:
                jobs_found.append({
                    "company_id": company["id"],
                    "url": url,
                    "found_at": datetime.now().isoformat()
                })
        
        print(f"Watchdog finished. Found {len(jobs_found)} potential job links.")
        return jobs_found

if __name__ == "__main__":
    agent = Watchdog()
    agent.run()
