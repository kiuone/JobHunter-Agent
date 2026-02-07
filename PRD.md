# PRD: JobHunter Agent (Versão 1.0 - Full Radar)

## 1. Visão Geral
Sistema de agentes autônomos ("Agentic AI") em Python para monitoramento contínuo (72h) e descoberta de vagas de estágio em Engenharia de Bioprocessos, com foco estrito em Dados, Supply Chain e Gestão Industrial.

## 2. Objetivos de Negócio
- **Monitoramento:** O sistema deve varrer sites de carreiras a cada 3 dias.
- **Cobertura:** Deve monitorar links diretos de ATS (Gupy, Workday) e Notícias/Redes Sociais.
- **Inteligência:** Deve diferenciar vagas "de bancada" (indesejadas) de vagas de "gestão/dados" (desejadas).
- **Descoberta:** Deve sugerir ativamente novas empresas que não estão no banco de dados.

## 3. Stack Tecnológica & Infraestrutura
- **Ambiente:** Windows 11 (Execução local).
- **Linguagem:** Python 3.10+.
- **Orquestração:** LangGraph (Stateful Multi-Agent System).
- **Banco de Dados:** Supabase (PostgreSQL) - Gerenciado via MCP.
- **LLM:** Llama 3.3 (via Groq/API) para análise semântica.
- **Web Scraping:** Tavily API (Busca) + Firecrawl (Extração de conteúdo).

## 4. Arquitetura de Agentes (Nós do Grafo)

### Nó A: The Watchdog (Vigilante)
- **Input:** Tabela `companies` no Supabase.
- **Frequência:** Loop a cada 72 horas.
- **Ação:**
  1. Acessa a URL de carreiras da empresa.
  2. Busca também no Google News/LinkedIn por "Estágio [Nome da Empresa]".
  3. Prioriza encontrar o link direto de inscrição.
  4. Envia o conteúdo bruto para o Analista.

### Nó B: The Analyst (Analyst)
- **Input:** Texto bruto da vaga.
- **Processamento (LLM):**
  1. Extrai JSON estruturado com campos estendidos:
     - `application_start_date`: Data de início das inscrições
     - `application_deadline`: Data limite
     - `location`: Localização
     - `work_model`: Presencial, Híbrido, Remoto
     - `weekly_hours`: Carga horária
     - `salary`: Valor da bolsa/salário
     - `desired_profile`: Perfil buscado
     - `company_description`: Sobre a empresa
     - `area`: Área de atuação do estágio
     - `requirements`: Ferramentas, Habilidades, Idiomas
  2. Aplica Filtro Geográfico:
     - **Prioridade:** SP, MG, MT, SC, PR.
     - **Aceitável:** Resto do BR (Exceto exclusões), América do Sul, Global.
     - **Exclusão:** RJ, ES, BA, Norte do BR.
  3. Aplica Filtro de Função:
     - **Ouro:** Bioinfo, Dados, Supply Chain.
     - **Prata:** QA, Produção, Comercial Técnico.
     - **Lixo:** Laboratório (bancada), Assuntos Regulatórios.
- **Output:** `fit_score` (0-100) e classificação.

### Nó C: The Scout (Olheiro)
- **Frequência:** Semanal.
- **Ação:** Busca na web por "Top Biotech Startups Brasil", "Empresas Agritech Mato Grosso", etc.
- **Output:** Gera uma lista de *sugestões* de empresas para o usuário aprovar. NÃO insere na lista de monitoramento automaticamente.

### Nó D: The Data Steward (Arquivista)
- **Ação:** Salva/Atualiza vagas no Supabase. Evita duplicidade (deduplication via URL).

## 5. Schema do Banco de Dados (Supabase)

### Tabela: `companies`
- `id` (uuid)
- `name` (text)
- `website_career_url` (text)
- `search_keywords` (text[]) - Ex: ["estágio", "trainee", "dados"]
- `status` (active/paused)

### Tabela: `jobs`
- `id` (uuid)
- `company_id` (fk)
- `title` (text)
- `fit_category` (text) - Check: ['GOLD', 'SILVER', 'TRASH']
- `fit_score` (int)
- `details` (jsonb) - Contém: {salario, requisitos, location, deadline, skills}
- `application_url` (text) - Link direto para clicar e inscrever.
- `source_type` (text) - Ex: 'ATS', 'News', 'LinkedIn'.
- `created_at` (timestamp)
