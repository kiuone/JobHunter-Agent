# JobHunter Agent

Autonomous multi-agent system for monitoring and discovering job opportunities in Biotech/Agro sectors.

## Architecture

- **Watchdog**: Monitors career pages and search engines for new job openings.
- **Analyst**: Scrapes job details and classifies them (Gold/Silver/Trash) using LLM.
- **Scout**: Discovers new potential companies to add to the monitoring list.
- **Steward**: Saves valid jobs to Supabase and handles deduplication.

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**:
   Copy `.env.example` to `.env` and fill in your API keys:
   - `SUPABASE_URL` & `SUPABASE_KEY`: From your Supabase project.
   - `TAVILY_API_KEY`: For search.
   - `GROQ_API_KEY`: For LLM (Llama 3.3).
   - `FIRECRAWL_API_KEY`: For web scraping.

3. **Database**:
   Ensure Supabase tables (`companies`, `jobs`, `company_suggestions`) are created.

## Usage

Run the agent:
```bash
python -m src.main
```

## Agents Logic

- **Watchdog** runs every cycle.
- **Analyst** filters jobs based on location and role.
- **Scout** runs periodically to find new targets.
