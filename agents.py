"""
Research Agents Definition Module

This module contains all agent definitions for the multi-agent research system.
Each agent has a specific role and set of capabilities.
"""

import os
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph.message import add_messages

# Import search tools
from tools import brave_web_search, format_search_results, arxiv_search, format_arxiv_results

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
    Data Search Agent - Enhanced with Azure Vector Search
    - Specializes in statistics, datasets, and quantitative information from indexed documents
    - Integrates with Azure AI Search for financial stress test document retrieval
    - Focuses on numerical data and factual information from authoritative sources
    """
    print("🔍 Data Search Agent: Searching financial documents and quantitative data...")
    
    # Try to use Azure vector search first for financial/regulatory queries
    user_query = state.get("user_query", "")
    vector_results = ""
    
    try:
        from vector_search_agent import create_vector_search_agent
        
        # Check if this looks like a financial/regulatory query
        financial_keywords = [
            'stress test', 'banking', 'capital', 'regulatory', 'fed', 'federal reserve',
            'bank of england', 'boe', 'basel', 'dfast', 'ccar', 'financial stability',
            'risk', 'scenario', 'crisis', 'macroeconomic', 'credit', 'market risk'
        ]
        
        is_financial_query = any(keyword in user_query.lower() for keyword in financial_keywords)
        
        if is_financial_query:
            vector_agent = create_vector_search_agent()
            if vector_agent:
                print("   🏦 Searching indexed financial stress test documents...")
                
                # Perform vector search
                search_results = vector_agent.vector_search(user_query, top_k=5)
                
                if search_results:
                    vector_results = "## 📊 Financial Document Search Results\n\n"
                    vector_results += f"Found {len(search_results)} relevant documents from our indexed financial stress test collection:\n\n"
                    
                    for i, result in enumerate(search_results, 1):
                        vector_results += f"### {i}. {result['title']}\n"
                        vector_results += f"**Source**: {result['institution']} ({result['year']})\n"
                        vector_results += f"**Document Type**: {result['document_type']}\n"
                        vector_results += f"**Relevance Score**: {result['search_score']:.3f}\n"
                        vector_results += f"**Content**: {result['content'][:500]}...\n\n"
                    
                    print(f"   ✅ Found {len(search_results)} relevant financial documents")
                else:
                    vector_results = "## 📊 Financial Document Search\n\nNo relevant documents found in the indexed financial stress test collection.\n\n"
                    print("   ⚠️ No relevant financial documents found in index")
            else:
                print("   ⚠️ Vector search not available - check Azure configuration")
        else:
            print("   ℹ️ Query not identified as financial - skipping vector search")
            
    except Exception as e:
        print(f"   ❌ Vector search error: {e}")
        vector_results = ""
    
    # Construct system prompt with vector search results
    system_prompt = f"""You are the Data Search Agent, specialized in finding statistical and quantitative information.
    
    Your role:
    1. Find relevant statistics, datasets, and numerical data
    2. Search for market research, surveys, and quantitative studies  
    3. Provide factual, data-driven insights from authoritative sources
    4. Focus on measurable and verifiable information
    5. Prioritize information from indexed financial regulatory documents when available
    
    {vector_results}
    
    IMPORTANT: When given a research query, provide SPECIFIC quantitative findings with:
    - Exact numbers, percentages, and statistics from regulatory sources
    - Market size data and growth rates
    - Stress test results and capital ratios
    - Financial figures and loss projections
    - Technical specifications and performance metrics
    - Comparative data from multiple institutions
    - Historical trends and scenario analyses
    
    Always cite your sources, especially when using information from indexed financial documents.
    Prioritize data from Federal Reserve, Bank of England, ECB, and other central bank sources.
    
    Format your response as detailed quantitative research findings with specific numbers and data points."""
    
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