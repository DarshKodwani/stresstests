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
- **🎭 Interactive Web Interface**: Real-time Streamlit app with cinematic agent visualization
- **📊 Agent Workflow Visualization**: Watch agents work in real-time with progress tracking
- **📥 Report Downloads**: Generate PDF and text reports with professional formatting

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
├── streamlit_app.py             # Interactive web interface with real-time visualization
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

## 🎭 Streamlit Web Interface

The system includes a sophisticated web interface built with Streamlit that provides an engaging, cinematic experience for interacting with the multi-agent system.

### Interface Features

#### 🎬 Real-Time Agent Visualization
- **Cinematic Workflow**: Watch agents appear and activate in sequential stages
- **Agent Personalities**: Each agent has unique emojis and personality descriptions
- **Status Animations**: Active agents show pulsing animations and "thinking" indicators
- **Progress Tracking**: Real-time progress bar and status updates

#### 🎛️ Mission Control Sidebar
- **Live Mission Log**: Updates in real-time as agents complete tasks
- **Sample Queries**: Pre-loaded stress testing questions for quick start
- **Session Management**: Track current mission status and progress

#### 📊 Agent Work Display
- **Expandable Results**: Click to see what each agent discovered
- **Work Summaries**: Preview of each agent's findings with full detail options
- **Completion Metrics**: Word counts and processing statistics for each agent

#### 📥 Professional Report Generation
- **PDF Reports**: Professional, formatted documents with metadata and citations
- **Text Downloads**: Plain text versions for easy integration
- **Report Caching**: Session state management prevents re-running expensive queries

#### 🎯 User Experience Features
- **Query Suggestions**: Sample financial stress testing questions
- **Cached Results**: Smart caching to avoid re-running identical queries
- **Clean Interface**: Modern, responsive design with financial industry styling
- **Easy Navigation**: Intuitive workflow from query to final report

### Using the Web Interface

1. **Launch the app**: `streamlit run streamlit_app.py`
2. **Select a sample query** or enter your own financial stress testing question
3. **Click "Launch Research Mission"** to start the multi-agent workflow
4. **Watch agents work** in real-time with cinematic visualizations
5. **Review individual agent work** by expanding completed agent cards
6. **Download professional reports** in PDF or text format
7. **Start new research** with the reset button to clear cache and begin fresh

The web interface makes complex multi-agent AI research accessible and engaging, perfect for demonstrations, research sessions, or interactive analysis of financial stress testing scenarios.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Azure OpenAI API access
- Azure AI Search service
- Brave Search API key (optional, for web search)
- Streamlit (included in requirements.txt for web interface)

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

**Note**: The requirements include Streamlit and ReportLab for the web interface and PDF generation. If you only need the command-line version, you can install a minimal set of dependencies.

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

### Quick Start (Web Interface)

Once you've completed the setup above:

```bash
# Launch the interactive web interface
streamlit run streamlit_app.py
```

1. **Open your browser** to the displayed URL (usually `http://localhost:8501`)
2. **Try a sample query** by clicking one of the pre-loaded buttons in the sidebar
3. **Click "Launch Research Mission"** to start the multi-agent workflow
4. **Watch the agents work** in real-time with animated visualizations
5. **Download your report** when the analysis is complete

The web interface provides the most engaging way to interact with the system and is perfect for demonstrations or interactive research sessions.

## 📖 Usage

### Method 1: Interactive Web Interface (Recommended)
Launch the Streamlit web application for an engaging, visual research experience:
```bash
streamlit run streamlit_app.py
```

**Features:**
- 🎬 **Cinematic Agent Visualization**: Watch agents activate and work in real-time
- 🎛️ **Mission Control Sidebar**: Live updates and mission log tracking  
- 📋 **Sample Queries**: Pre-loaded financial stress testing questions
- 🔍 **Agent Work Review**: Expand completed agents to see their research
- 📥 **Professional Downloads**: Generate PDF reports with citations
- 🔄 **Session Management**: Cached results with easy restart functionality

The web interface provides an intuitive way to interact with the multi-agent system, complete with animated agent cards, progress tracking, and professional report generation.

### Method 2: Run Default Stress Testing Query (Command Line)
```bash
python workflow.py
```
This runs the built-in geopolitical stress testing scenario query and displays the full multi-agent workflow.

### Method 3: Programmatic Usage
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

### Method 4: Index New Documents (Optional)
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
| `streamlit_app.py` | Interactive web interface with real-time agent visualization |
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