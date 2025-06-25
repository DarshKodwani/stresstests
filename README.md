# Multi-Agent Research System

A sophisticated multi-agent research system built with LangGraph and Azure OpenAI that coordinates specialized AI agents to conduct comprehensive research on any topic.

## 🌟 Features

- **🎯 Lead Agent**: Orchestrates research tasks and coordinates other agents
- **🔍 Parallel Search Agents**: 
  - Academic Search Agent (scholarly articles, papers)
  - Web Search Agent (current news, industry reports)
  - Data Search Agent (statistics, quantitative data)
- **📝 Citations Agent**: Verifies sources and formats citations
- **🧠 Synthesis Agent**: Creates comprehensive final reports
- **⚡ Real-time Verbose Output**: See each agent's work in beautiful terminal display

## 🏗️ Architecture

Based on Anthropic's multi-agent research architecture, this system uses LangGraph to coordinate agents in parallel execution patterns:

```
User Query → Lead Agent → [Academic, Web, Data] Search Agents (Parallel) → Citations Agent → Synthesis Agent → Final Report
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Azure OpenAI API access
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/multi-agent-research.git
cd multi-agent-research
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your Azure OpenAI credentials
```

### Usage

Run a research query:
```bash
python workflow.py
```

Or use programmatically:
```python
from workflow import run_research

result = run_research("What are the latest developments in quantum computing?")
print(result["messages"][-1].content)
```

## 📁 Project Structure

```
multi-agent-research/
├── agents.py              # Agent definitions and configurations
├── workflow.py            # LangGraph workflow orchestration
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Your actual environment variables (not tracked)
├── .gitignore           # Git ignore patterns
├── README.md            # This file
└── LICENSE              # MIT License
```

## 🔧 Configuration

Set up your `.env` file with Azure OpenAI credentials:

```env
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

## 🤖 Agents

### Lead Agent
- Breaks down research queries into subtasks
- Coordinates specialized search agents
- Manages overall research workflow

### Academic Search Agent
- Focuses on peer-reviewed papers and scholarly sources
- Provides academic context and theoretical frameworks
- Cites specific studies and researchers

### Web Search Agent
- Searches current news, industry reports, and web content
- Finds real-world applications and market trends
- Gathers recent developments and announcements

### Data Search Agent
- Specializes in statistics and quantitative information
- Finds market research and survey data
- Provides measurable insights and benchmarks

### Citations Agent
- Verifies source credibility and reliability
- Formats citations properly (APA/MLA standards)
- Flags unsubstantiated claims

### Synthesis Agent
- Combines findings from all agents
- Identifies patterns and contradictions
- Creates comprehensive final reports

## 🔄 Workflow

The system uses LangGraph for sophisticated agent coordination:

1. **User Query Processing**: Lead agent analyzes and breaks down the request
2. **Parallel Research**: Multiple search agents work simultaneously
3. **Source Verification**: Citations agent validates findings
4. **Report Synthesis**: Final agent creates comprehensive report

## 🛠️ Development

### Adding New Agents

1. Define agent function in `agents.py`:
```python
def new_agent(state: ResearchState):
    system_prompt = "Your agent's role and instructions..."
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}
```

2. Add to workflow in `workflow.py`:
```python
workflow.add_node("new_agent", new_agent)
workflow.add_edge("previous_agent", "new_agent")
```

### Extending State

Modify `ResearchState` in `agents.py` to add new data fields:
```python
class ResearchState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    # Add your new fields here
    new_field: str
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph) for agent orchestration
- Powered by [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
- Inspired by [Anthropic's multi-agent research architecture](https://www.anthropic.com/engineering/built-multi-agent-research-system)

## 📊 Roadmap

- [ ] Add real-time web search APIs
- [ ] Integrate academic database access (arXiv, PubMed)
- [ ] Implement memory and context persistence
- [ ] Add web interface
- [ ] Support for multiple research domains
- [ ] Quality control and fact-checking agents

---

⭐ If you find this project useful, please consider giving it a star!
