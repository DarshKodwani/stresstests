# Financial Stress Test Research System

[![Azure](https://img.shields.io/badge/Azure-OpenAI-blue)](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-green)](https://github.com/langchain-ai/langgraph)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-red)](LICENSE)

A sophisticated multi-agent research system specifically designed for financial stress testing analysis. Built with LangGraph and Azure OpenAI, it coordinates specialized AI agents to conduct comprehensive research on stress testing scenarios, regulatory frameworks, and macroeconomic risk modeling.

## � Purpose & Overview

This system enables financial risk professionals, regulators, and researchers to:

- **Analyze stress testing scenarios** from major central banks (Fed, BOE, ECB)
- **Research regulatory frameworks** and capital adequacy requirements
- **Model macroeconomic stress scenarios** with geopolitical risk factors
- **Access real financial documents** through Azure AI Search vector indexing
- **Generate comprehensive reports** combining academic research, current market data, and regulatory guidance

The system leverages a curated collection of real stress testing documents from the Federal Reserve, Bank of England, Basel Committee, and other regulatory bodies, all indexed and searchable through Azure AI Search.

## 🌟 Key Features

- **🏦 Financial Document Vector Search**: Search through indexed PDFs, Excel files, and CSV data from regulatory institutions
- **🔍 Multi-Source Research**: Combines academic papers (arXiv), web search (Brave API), and indexed financial documents
- **📊 Stress Testing Focus**: Specialized prompts and workflows for financial risk scenarios
- **⚡ Real-time Analysis**: Parallel agent execution for comprehensive research
- **🎯 Regulatory Intelligence**: Direct access to Fed DFAST, BOE stress tests, Basel frameworks
- **📝 Professional Reports**: Citation-backed synthesis with quantitative findings

## 🏗️ Architecture & Structure

### System Architecture
```
User Query → Lead Agent → [Academic Search | Web Search | Data Search] → Citations → Synthesis
                                                           ↓
                                                   Azure AI Search Index
                                                   (Financial Documents)
```

### Project Structure
```
stresstests/
├── agents.py                    # Multi-agent definitions and configurations
├── workflow.py                  # LangGraph orchestration (main entry point)
├── tools.py                     # Search utilities (arXiv, Brave, Azure)
├── add_documents_to_index.py    # Document ingestion pipeline
├── requirements.txt             # Python dependencies
├── financial_data/              # Indexed regulatory documents
│   ├── fed-2023-dfast-*.pdf    # Federal Reserve stress test results
│   ├── boe-stress-test-*.pdf   # Bank of England scenarios
│   ├── basel-*.pdf             # Basel Committee frameworks
│   └── *.xlsx, *.csv          # Economic data and spreadsheets
├── .env.example                # Environment template
├── firstTimeSetup.sh           # Initial setup script
└── README.md                   # This documentation
```

## 🤖 Multi-Agent System

### Lead Agent (Orchestrator)
- **Role**: Coordinates the entire research process
- **Function**: Breaks down stress testing queries into specific research subtasks
- **Output**: Research coordination and task distribution

### Academic Search Agent
- **Role**: Finds scholarly research on financial risk and stress testing
- **Data Source**: arXiv API for academic papers
- **Focus**: Peer-reviewed research, methodologies, theoretical frameworks
- **Output**: Academic citations with specific research findings

### Web Search Agent  
- **Role**: Discovers current market developments and news
- **Data Source**: Brave Search API for privacy-focused web search
- **Focus**: Recent regulatory announcements, market trends, industry reports
- **Output**: Current market intelligence and real-world applications

### Data Search Agent (Azure AI Search)
- **Role**: Searches indexed financial stress test documents
- **Data Source**: Azure AI Search vector index with 1000+ financial documents
- **Focus**: Fed DFAST results, BOE scenarios, Basel requirements, ECB guidance
- **Output**: Quantitative data, regulatory findings, and institutional analysis

### Citations Agent
- **Role**: Verifies sources and ensures proper attribution
- **Function**: Validates credibility of financial sources and regulatory documents
- **Output**: Properly formatted citations and source verification

### Synthesis Agent
- **Role**: Creates comprehensive final reports
- **Function**: Combines findings from all agents into coherent analysis
- **Output**: Professional stress testing research reports with actionable insights

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Azure OpenAI API access
- Azure AI Search service
- Brave Search API key (optional, for web search)

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/DarshKodwani/stresstests.git
cd stresstests
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

### Configuration

4. **Set up environment variables**:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
# Azure OpenAI (Required)
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_API_VERSION=2024-02-01

# Azure AI Search (Required for Data Search Agent)
AZURE_SEARCH_ENDPOINT=https://your-search.search.windows.net
AZURE_SEARCH_KEY=your-admin-key

# Azure OpenAI Embeddings (Required for vector search)
AZURE_OPENAI_EMBEDDINGS_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_EMBEDDINGS_API_KEY=your-api-key
AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME=text-embedding-3-large

# Brave Search API (Optional, for web search)
BRAVE_SEARCH_API_KEY=your-brave-api-key
```

5. **Index financial documents** (if not already done):
```bash
python add_documents_to_index.py
```

## 📖 Usage

### Method 1: Run Default Stress Testing Query
```bash
python workflow.py
```
This runs the built-in geopolitical stress testing scenario query and displays the full multi-agent workflow.

### Method 2: Programmatic Usage
```python
from workflow import run_research

# Run stress testing research
result = run_research(
    "What are the top 3 scenarios for modeling geopolitical risk in stress tests?",
    verbose=True
)

# Access final synthesis
final_report = result["messages"][-1].content
print(final_report)
```

### Method 3: Index New Documents (Optional)
If you want to add new financial documents to the search index:
```bash
python add_documents_to_index.py
```

## 💡 Examples

### Sample Queries
- `"What were the key findings from the 2023 Federal Reserve DFAST stress test results?"`
- `"How do Bank of England climate stress test scenarios compare to Fed approaches?"`
- `"What are the Basel III capital requirements for systemic risk buffers?"`
- `"Compare stress testing methodologies between major central banks"`
- `"What macroeconomic scenarios should I model for Middle East geopolitical risk?"`

### Expected Output Structure
Each query produces:
1. **Academic Research**: Scholarly papers on stress testing methodologies
2. **Current Intelligence**: Recent regulatory announcements and market developments  
3. **Regulatory Data**: Specific findings from indexed Fed/BOE/ECB documents
4. **Citations**: Properly attributed sources with institutional backing
5. **Synthesis**: Comprehensive analysis combining all research streams

## 📁 File Structure Reference

| File | Purpose |
|------|---------|
| `workflow.py` | Main entry point - runs the multi-agent workflow |
| `agents.py` | Agent definitions and AI model configurations |
| `tools.py` | Search utilities for arXiv, Brave, and Azure AI Search |
| `add_documents_to_index.py` | Ingestion pipeline for financial documents |
| `financial_data/` | Directory containing indexed regulatory documents |
| `firstTimeSetup.sh` | Initial environment setup script |
| `requirements.txt` | Python package dependencies |
| `.env.example` | Template for environment variables |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/risk-modeling`)
3. Commit your changes (`git commit -m 'Add new risk scenario modeling'`)
4. Push to the branch (`git push origin feature/risk-modeling`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

⭐ **Built for Financial Risk Professionals** - If you find this useful for stress testing research, please star the repository!