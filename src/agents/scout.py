from tavily import TavilyClient
from src.core.config import get_supabase_client, TAVILY_API_KEY

class Scout:
    def __init__(self):
        self.supabase = get_supabase_client()
        self.tavily = TavilyClient(api_key=TAVILY_API_KEY)

    def search_new_companies(self) -> list:
        queries = [
            "Top Biotech Startups Brasil 2024 2025",
            "Empresas Agritech Mato Grosso inovação",
            "Melhores empresas para trabalhar agronegócio tecnologia",
            "Startups biotecnologia supply chain data science brasil"
        ]
        
        suggestions = []
        for q in queries:
            try:
                response = self.tavily.search(query=q, search_depth="advanced")
                # Simplified: In a real scenario, we'd parse the snippets with LLM to extract company names.
                # For now, we will just return the titles/snippets as potential leads or use LLM here too.
                # Let's assume we use LLM (to be implemented fully) or just mock for now.
                # Adding raw results for now.
                for result in response.get("results", []):
                    suggestions.append({
                        "name": result["title"], # Placeholder, really needs named entity recognition
                        "reason": f"Found via query: {q}",
                        "source": result["url"],
                        "status": "pending"
                    })
            except Exception as e:
                print(f"Error in scout search: {e}")
                
        return suggestions

    def save_suggestions(self, suggestions):
        if not suggestions:
            return
            
        # Deduplication based on source/name would be good here
        try:
            self.supabase.table("company_suggestions").insert(suggestions).execute()
        except Exception as e:
            print(f"Error saving suggestions: {e}")

    def run(self):
        print("Scout checking for new companies...")
        suggestions = self.search_new_companies()
        # In a real impl, we'd filter these through an LLM to get actual company names
        # For this v1, we might just store the top results.
        self.save_suggestions(suggestions)
        print("Scout finished.")

if __name__ == "__main__":
    agent = Scout()
    agent.run()
