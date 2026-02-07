from src.core.config import get_supabase_client

supabase = get_supabase_client()

# Default keywords
ARGS_KEYWORDS = ["estágio", "trainee", "supply chain", "dados", "biotecnologia", "inteligência de mercado"]

# GROUPS 1-5: COMPANIES
companies_list = [
    # GRUPO 1: PADRÃO OURO
    {"name": "Bayer", "website_career_url": "https://jobs.bayer.com/"},
    {"name": "Illumina", "website_career_url": "https://www.illumina.com/company/careers.html"},
    {"name": "Johnson & Johnson", "website_career_url": "https://careers.jnj.com"},
    {"name": "Roche", "website_career_url": "https://careers.roche.com/"},
    {"name": "Novartis", "website_career_url": "https://www.novartis.com/careers"},
    {"name": "Pfizer", "website_career_url": "https://www.pfizer.com/careers"},
    {"name": "AstraZeneca", "website_career_url": "https://careers.astrazeneca.com/"},
    {"name": "Sanofi", "website_career_url": "https://www.sanofi.com/en/careers"},
    {"name": "GSK", "website_career_url": "https://www.gsk.com/en-gb/careers/"},
    {"name": "MSD", "website_career_url": "https://jobs.msd.com/"},
    {"name": "Takeda", "website_career_url": "https://www.takedajobs.com/"},
    {"name": "Boehringer Ingelheim", "website_career_url": "https://careers.boehringer-ingelheim.com/"},
    {"name": "Syngenta", "website_career_url": "https://www.syngenta.com.br/carreiras"},
    {"name": "Corteva", "website_career_url": "https://careers.corteva.com/"},
    {"name": "Dasa Genômica", "website_career_url": "https://dasa.gupy.io/"},
    {"name": "Mendelics", "website_career_url": "https://mendelics.gupy.io/"},
    {"name": "Grupo Fleury", "website_career_url": "https://grupofleury.gupy.io/"},
    {"name": "Hospital Israelita Albert Einstein", "website_career_url": "https://www.einstein.br/carreiras"},
    {"name": "Hospital Sírio-Libanês", "website_career_url": "https://hsl.gupy.io/"},
    {"name": "Hermes Pardini", "website_career_url": "https://hermespardini.gupy.io/"},
    {"name": "Genera", "website_career_url": "https://genera.gupy.io/"},

    # GRUPO 2: AGRO & INDÚSTRIA
    {"name": "BASF", "website_career_url": "https://www.basf.com/br/pt/careers"},
    {"name": "Yara", "website_career_url": "https://jobs.yara.com/"},
    {"name": "Mosaic Fertilizantes", "website_career_url": "https://mosaicco.com.br/Quem-Somos"},
    {"name": "Cargill", "website_career_url": "https://careers.cargill.com/pt"},
    {"name": "Bunge", "website_career_url": "https://jobs.bunge.com/"},
    {"name": "ADM", "website_career_url": "https://www.adm.com/en-us/careers/"},
    {"name": "Raízen", "website_career_url": "https://genteraizen.gupy.io/"},
    {"name": "Frimesa", "website_career_url": "https://www.frimesa.com.br/pt/trabalheconosco"},
    {"name": "Lar Cooperativa", "website_career_url": "https://www.lar.ind.br/"},
    {"name": "Coamo", "website_career_url": "https://www.coamo.com.br/"},
    {"name": "Aurora Coop", "website_career_url": "https://www.taurora.com.br/"},
    {"name": "Frísia", "website_career_url": "https://www.frisia.coop.br/trabalhe-conosco.html"},
    {"name": "Castrolanda", "website_career_url": "https://www.castrolanda.coop.br/"},
    {"name": "Copacol", "website_career_url": "https://www.copacol.com.br/trabalhe-conosco"},
    {"name": "Capal", "website_career_url": "https://www.capal.coop.br/"},
    {"name": "Coopagrícola", "website_career_url": ""}, # Check URL
    {"name": "BRF", "website_career_url": "https://talents.brf.com/"},
    {"name": "JBS", "website_career_url": "https://jbs.com.br/carreiras/"},
    {"name": "Marfrig", "website_career_url": "https://trabalheconosco.vagas.com.br/marfrig"},
    {"name": "Klabin", "website_career_url": "https://carreiras.klabin.com.br/"},
    {"name": "Suzano", "website_career_url": "https://suzano.gupy.io/"},

    # GRUPO 3: BENS DE CONSUMO & ALIMENTOS
    {"name": "Unilever", "website_career_url": "https://careers.unilever.com.br"},
    {"name": "Heineken", "website_career_url": "https://careers.theheinekencompany.com/"},
    {"name": "Kraft Heinz", "website_career_url": "https://careers.kraftheinz.com/early-careers/"},
    {"name": "Nestlé", "website_career_url": "https://www.nestle.com.br/carreiras"},
    {"name": "Danone", "website_career_url": "https://careers.danone.com"},
    {"name": "Ambev", "website_career_url": "https://ambev.gupy.io/"},
    {"name": "Coca-Cola FEMSA", "website_career_url": "https://coffe.gupy.io/"}, # Includes Monster
    {"name": "Procter & Gamble", "website_career_url": "https://www.pgcareers.com/"},
    {"name": "L'Oréal", "website_career_url": "https://careers.loreal.com/"},
    {"name": "Natura &Co", "website_career_url": "https://naturaeco.gupy.io/"},
    {"name": "Grupo Boticário", "website_career_url": "https://grupoboticario.gupy.io/"},
    {"name": "Colgate-Palmolive", "website_career_url": "https://jobs.colgate.com/"},
    {"name": "Reckitt", "website_career_url": "https://careers.reckitt.com/"},
    {"name": "Lactalis", "website_career_url": "https://www.lactalis.com.br/carreiras/"},
    {"name": "Yakult", "website_career_url": "https://www.yakult.com.br/trabalhe-conosco/"},

    # GRUPO 4: INSTITUIÇÕES DE PESQUISA
    {"name": "Embrapa", "website_career_url": "https://www.embrapa.br/estagios"},
    {"name": "Fiocruz", "website_career_url": "https://portal.fiocruz.br/"},
    {"name": "Instituto Butantan", "website_career_url": "https://butantan.gov.br/"},
    {"name": "CNPEM", "website_career_url": "https://cnpem.br/trabalhe-conosco/"},

    # GRUPO 5: TECH & CONSULTORIA
    {"name": "IQVIA", "website_career_url": "https://jobs.iqvia.com/"},
    {"name": "Accenture", "website_career_url": "https://www.accenture.com/br-pt/careers"},
    {"name": "Dr. Consulta", "website_career_url": "https://drconsulta.gupy.io/"},
    {"name": "Alice", "website_career_url": "https://alice.gupy.io/"},
    {"name": "Sami", "website_career_url": "https://sami.gupy.io/"},
    {"name": "iClinic", "website_career_url": "https://iclinic.gupy.io/"},
    {"name": "Laura", "website_career_url": "https://laura-br.gupy.io/"},
]

# GRUPO 6: FONTES DE BUSCA
sources_list = [
    # Portais (ATS)
    {"name": "Gupy", "url": "gupy.io", "type": "ATS"},
    {"name": "Workday", "url": "myworkdayjobs.com", "type": "ATS"},
    {"name": "Kenoby", "url": "jobs.kenoby.com", "type": "ATS"},
    {"name": "Indeed", "url": "indeed.com.br", "type": "Aggregator"},
    {"name": "Glassdoor", "url": "glassdoor.com.br", "type": "Aggregator"},
    {"name": "LinkedIn Jobs", "url": "linkedin.com/jobs", "type": "Aggregator"},
    
    # Agregadores & Programas
    {"name": "Cia de Talentos", "url": "ciadetalentos.com.br", "type": "Aggregator"},
    {"name": "Seja Trainee", "url": "sejatrainee.com.br", "type": "Aggregator"},
    {"name": "EstágioTrainee", "url": "estagiotrainee.com", "type": "Aggregator"},
    {"name": "Eureka", "url": "eureca.me", "type": "Aggregator"},
    {"name": "99jobs", "url": "99jobs.com", "type": "Aggregator"},
    {"name": "CIEE", "url": "ciee.org.br", "type": "Aggregator"},
    {"name": "IEL", "url": "iel.org.br", "type": "Aggregator"},
    {"name": "Estágio Online", "url": "estagioonline.com", "type": "Aggregator"},
    {"name": "Estágio Remoto", "url": "estagioremoto.com", "type": "Aggregator"},
    
    # Notícias
    {"name": "Google News", "url": "news.google.com", "type": "News"},
    {"name": "Instagram", "url": "instagram.com", "type": "Social"},
]

def seed():
    print(f"Seeding {len(companies_list)} companies...")
    for company in companies_list:
        try:
            existing = supabase.table("companies").select("id").eq("name", company["name"]).execute()
            if not existing.data:
                company["search_keywords"] = ARGS_KEYWORDS
                supabase.table("companies").insert(company).execute()
                print(f"Added Company: {company['name']}")
            else:
                print(f"Skipped Company: {company['name']} (Exists)")
        except Exception as e:
            print(f"Error seeding company {company['name']}: {e}")

    print(f"Seeding {len(sources_list)} sources...")
    for source in sources_list:
        try:
            existing = supabase.table("search_sources").select("id").eq("name", source["name"]).execute()
            if not existing.data:
                supabase.table("search_sources").insert(source).execute()
                print(f"Added Source: {source['name']}")
            else:
                print(f"Skipped Source: {source['name']} (Exists)")
        except Exception as e:
            print(f"Error seeding source {source['name']}: {e}")

if __name__ == "__main__":
    seed()
