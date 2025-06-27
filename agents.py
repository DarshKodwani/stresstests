import os
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph.message import add_messages

# Import search tools
from tools import (
    brave_web_search, format_search_results, 
    arxiv_search, format_arxiv_results,
    azure_vector_search, format_azure_search_results
)

# Load environment variables
load_dotenv()

# Azure OpenAI Configuration
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# Setup Azure OpenAI client
llm = AzureChatOpenAI(
    openai_api_version=api_version,
    azure_deployment=deployment_name,
    azure_endpoint=endpoint,
    api_key=api_key,
    temperature=0.7
)

# State definition (will move to separate file later)
class ResearchState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    user_query: str
    subtasks: list[str]
    search_results: list[dict]
    citations: list[dict]
    final_report: str

# =============================================================================
# AGENT DEFINITIONS
# =============================================================================

def lead_agent(state: ResearchState):
    """
    Lead Agent (Orchestrator)
    - Coordinates the entire research process
    - Breaks down user queries into subtasks
    - Synthesizes results from other agents
    """
    system_prompt = """You are the Lead Research Agent and orchestrator of a multi-agent research system.
    
    Your responsibilities:
    1. Analyze user research queries and break them into specific subtasks
    2. Coordinate other specialized agents (search agents, citation agent)
    3. Synthesize findings from multiple agents into comprehensive reports
    4. Ensure research quality and completeness
    
    When you receive a user query, first break it down into 2-3 specific research subtasks.
    Format your response as a clear breakdown of what needs to be researched."""
    
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

def academic_search_agent(state: ResearchState):
    """
    Academic Search Agent
    - Specializes in scholarly articles, papers, and academic sources
    - Focuses on peer-reviewed and authoritative content
    """
    
    # Extract the user query from messages
    user_query = ""
    if state["messages"]:
        # Get the original user query (first message)
        user_query = state["messages"][0].content
    
    # Perform real academic search using arXiv API
    print(f"🎓 Academic Search Agent searching arXiv for: {user_query}")
    arxiv_results = arxiv_search(user_query, max_results=6)
    formatted_arxiv = format_arxiv_results(arxiv_results)
    
    system_prompt = f"""You are the Academic Search Agent, specialized in finding scholarly and academic information.
    
    Your role:
    1. Analyze real academic papers from arXiv
    2. Extract key theoretical frameworks, methodologies, and research findings
    3. Focus on peer-reviewed, research-backed information
    4. Identify leading researchers and academic institutions in the field
    
    ARXIV SEARCH RESULTS TO ANALYZE:
    {formatted_arxiv}
    
    IMPORTANT: Base your response ONLY on the academic papers provided above from arXiv.
    Provide specific academic findings with:
    - Names of researchers and their affiliations
    - Specific methodologies and theoretical frameworks
    - Key research findings and conclusions
    - Technical details and experimental results
    - Research gaps and future directions mentioned
    - Mathematical formulations or algorithms (if relevant)
    
    Format your response as detailed academic research findings based on the papers found."""
    
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

def web_search_agent(state: ResearchState):
    """
    Web Search Agent
    - Handles general web searches, news, and current information
    - Focuses on recent developments and real-world applications
    """
    
    # Extract the user query from messages
    user_query = ""
    if state["messages"]:
        # Get the original user query (first message)
        user_query = state["messages"][0].content
    
    # Perform real web search using Brave Search API
    print(f"🔍 Web Search Agent searching for: {user_query}")
    search_results = brave_web_search(user_query, count=8)
    formatted_results = format_search_results(search_results, "web")
    
    system_prompt = f"""You are the Web Search Agent, specialized in finding current web-based information.
    
    Your role:
    1. Analyze real search results from Brave Search API
    2. Extract key findings about recent developments and real-world applications
    3. Focus on practical, up-to-date information from the search results
    4. Identify trends, company developments, and market information
    
    SEARCH RESULTS TO ANALYZE:
    {formatted_results}
    
    IMPORTANT: Base your response ONLY on the search results provided above. 
    Provide specific findings with:
    - Company names and their recent developments
    - Recent news events and announcements  
    - Market trends and industry developments
    - Specific product launches or partnerships
    - Current applications and real-world use cases
    
    Format your response as detailed research findings with current, practical information from the search results."""
    
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

def data_search_agent(state: ResearchState):
    """
    Data Search Agent - Azure AI Search Integration
    - Specializes in financial stress test documents using Azure vector search
    - Searches through indexed PDFs, Excel, and CSV files from regulatory institutions
    - Provides quantitative data and regulatory findings from authoritative sources
    """
    print("� Data Search Agent: Searching indexed financial documents...")
    
    # Extract the user query from messages
    user_query = ""
    if state["messages"]:
        # Get the original user query (first message)
        user_query = state["messages"][0].content
    
    # Perform Azure vector search on financial documents
    print(f"🏦 Searching Azure AI Search index for: {user_query}")
    search_results = azure_vector_search(user_query, top_k=5, use_hybrid=True)
    formatted_results = format_azure_search_results(search_results)
    
    if search_results:
        print(f"✅ Found {len(search_results)} relevant financial documents")
    else:
        print("⚠️ No relevant documents found in the financial stress test index")
    
    system_prompt = f"""You are the Data Search Agent, specialized in finding quantitative information from financial stress test documents.
    
    Your role:
    1. Analyze real financial documents from our indexed collection
    2. Extract specific statistics, stress test results, and regulatory findings
    3. Focus on quantitative data from Federal Reserve, Bank of England, ECB, and other central bank sources
    4. Provide detailed numerical data and factual information from authoritative regulatory documents
    
    INDEXED FINANCIAL DOCUMENT SEARCH RESULTS:
    {formatted_results}
    
    IMPORTANT: Base your response ONLY on the financial documents provided above from our Azure AI Search index.
    
    Provide specific quantitative findings with:
    - Exact capital ratios, stress test results, and regulatory metrics
    - Specific bank names, institution data, and comparative analyses
    - Numerical projections, loss estimates, and scenario outcomes
    - Regulatory requirements, thresholds, and compliance data
    - Historical trends and year-over-year comparisons
    - Technical specifications from stress testing methodologies
    - Market risk measures, credit losses, and operational risk data
    
    Always cite the specific institution and document year when referencing data.
    Focus on measurable, verifiable information from the indexed regulatory sources.
    
    Format your response as detailed quantitative research findings with specific numbers and institutional sources."""
    
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

def citations_agent(state: ResearchState):
    """
    Citations Agent
    - Manages source verification and citation formatting
    - Ensures all claims are properly attributed
    """
    system_prompt = """You are the Citations Agent, responsible for source verification and proper attribution.
    
    Your role:
    1. Review findings from other agents and identify claims that need citations
    2. Verify the credibility and reliability of sources
    3. Format citations properly (APA, MLA, or academic standard)
    4. Flag any unsubstantiated claims or questionable sources
    
    When reviewing research findings, focus on ensuring every claim is properly sourced and citations are correctly formatted."""
    
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

def synthesis_agent(state: ResearchState):
    """
    Synthesis Agent
    - Combines findings from all agents into coherent reports
    - Identifies patterns, contradictions, and gaps
    """
    system_prompt = """You are the Synthesis Agent, responsible for combining research findings into comprehensive reports.
    
    Your role:
    1. Analyze findings from all search agents
    2. Identify common themes, patterns, and insights
    3. Note any contradictions or conflicting information
    4. Create well-structured, comprehensive reports
    5. Highlight areas where more research might be needed
    
    When synthesizing findings, create a clear, well-organized report that presents the information logically and highlights key insights."""
    
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}