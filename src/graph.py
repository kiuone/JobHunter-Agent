from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from src.agents.watchdog import Watchdog
from src.agents.analyst import Analyst
from src.agents.steward import Steward
from src.agents.scout import Scout

class AgentState(TypedDict):
    companies: List[Dict]
    job_urls: List[Dict] # List of {"url": str, "company_id": uuid}
    analyzed_jobs: List[Dict]

# Initialize Agents
watchdog = Watchdog()
analyst = Analyst()
steward = Steward()
scout = Scout()

def watchdog_node(state: AgentState):
    print("--- WATCHDOG NODE ---")
    # In a real app we might pass the companies from state, 
    # but Watchdog fetches them internally for now.
    # We can optimize to fetch once and pass.
    # Let's let Watchdog do its thing and return found links.
    found_links = watchdog.run() 
    # found_links is List[{"company_id", "url", "found_at"}]
    return {"job_urls": found_links}

def analyst_node(state: AgentState):
    print("--- ANALYST NODE ---")
    urls = state.get("job_urls", [])
    analyzed_results = []
    
    for item in urls:
        url = item["url"]
        company_id = item["company_id"]
        print(f"Analyzing {url}...")
        
        result = analyst.run(url)
        if result:
            result["company_id"] = company_id # Preserving ID
            result["url"] = url # Preserving original URL if needed
            analyzed_results.append(result)
            
    return {"analyzed_jobs": analyzed_results}

def steward_node(state: AgentState):
    print("--- STEWARD NODE ---")
    jobs = state.get("analyzed_jobs", [])
    steward.run(jobs)
    return {}

def scout_node(state: AgentState):
    print("--- SCOUT NODE ---")
    scout.run()
    return {}

# Define Graph
workflow = StateGraph(AgentState)

workflow.add_node("watchdog", watchdog_node)
workflow.add_node("analyst", analyst_node)
workflow.add_node("steward", steward_node)
workflow.add_node("scout", scout_node)

# Edges
workflow.set_entry_point("watchdog")
workflow.add_edge("watchdog", "analyst")
workflow.add_edge("analyst", "steward")
workflow.add_edge("steward", "scout") # Run Scout after Steward
workflow.add_edge("scout", END)

app = workflow.compile()
