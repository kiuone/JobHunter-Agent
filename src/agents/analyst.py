import os
import json
from typing import Dict, Any
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field
from src.core.config import GROQ_API_KEY, get_supabase_client

# Define the schema for job extraction
class JobDetails(BaseModel):
    title: str = Field(description="Title of the job position")
    application_start_date: str = Field(description="Start date of applications, if available")
    application_deadline: str = Field(description="Deadline for applications, if available")
    location: str = Field(description="Location of the job (City, State, Remote, Hybrid)")
    work_model: str = Field(description="Work model: Remote, Hybrid, On-site")
    weekly_hours: str = Field(description="Weekly working hours")
    salary: str = Field(description="Salary or stipend value")
    desired_profile: str = Field(description="Desired candidate profile description")
    company_description: str = Field(description="Brief description of the company")
    area: str = Field(description="Area of the internship (e.g., Data, Supply Chain, Lab)")
    requirements: str = Field(description="List of required tools, skills, languages")
    fit_category: str = Field(description="Category: GOLD, SILVER, or TRASH based on rules")
    fit_reason: str = Field(description="Reason for the classification")

class Analyst:
    def __init__(self):
        self.supabase = get_supabase_client()
        self.firecrawl = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))
        self.llm = ChatGroq(
            temperature=0, 
            model="llama-3.3-70b-versatile", 
            api_key=GROQ_API_KEY
        )

    def scrape_job(self, url: str) -> str:
        try:
            scrape_result = self.firecrawl.scrape_url(url, params={'formats': ['markdown']})
            return scrape_result.get('markdown', '')
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return ""

    def analyze_job(self, job_content: str, url: str) -> Dict[str, Any] | None:
        if not job_content:
            return None

        system_prompt = """
        You are an expert job analyst for a Bioprocess Engineering student focused on Data Science, Bioinformatics, and Supply Chain.
        Analyze the job description and extract the following details into JSON.
        
        CLASSIFICATION RULES:
        - TRASH: "Lab Technician", "Clinical Analysis (Bench)", "Quality Control (Bench)", "Regulatory Affairs", "Pharmacovigilance".
        - SILVER: "Quality Assurance (Documental)", "Market Intelligence", "Manufacturing/Production", "Technical Sales", "Chemical/Food/Agro Industry".
        - GOLD: "Bioinformatics", "Data Science (Bio)", "Supply Chain", "Metagenomics", "R&D (Non-bench, literature/innovation)".
        
        LOCATIONS:
        - Exclude/TRASH if location is strictly: RJ, ES, BA, North Region.
        - Priority: SP, MG, MT, SC, PR.
        
        Output must be valid JSON matching the schema.
        """
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "Analyze this job: {job_content}")
        ])
        
        chain = prompt | self.llm.with_structured_output(JobDetails)
        
        try:
            # Limit content size to avoid token limits
            content_sample = job_content[:30000] if job_content else ""
            result = chain.invoke({"job_content": content_sample}) 
            return result.model_dump()
        except Exception as e:
            print(f"Error analyzing job {url}: {e}")
            return None

    def run(self, job_url: str):
        content = self.scrape_job(job_url)
        if content:
            analysis = self.analyze_job(content, job_url)
            return analysis
        return None

if __name__ == "__main__":
    # Test
    pass
