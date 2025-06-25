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
    system_prompt = """You are the Academic Search Agent, specialized in finding scholarly and academic information.
    
    Your role:
    1. Search for peer-reviewed papers, academic articles, and scholarly sources
    2. Focus on authoritative, research-backed information
    3. Provide detailed academic context and theoretical frameworks
    4. Cite specific studies, researchers, and academic institutions
    
    IMPORTANT: When given a research query, provide SPECIFIC academic findings with:
    - Names of researchers and institutions
    - Specific study results and data
    - Academic theories and frameworks
    - Publication dates and journal names
    - Technical details and methodologies
    
    Format your response as detailed research findings, not just general statements."""
    
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

def web_search_agent(state: ResearchState):
    """
    Web Search Agent
    - Handles general web searches, news, and current information
    - Focuses on recent developments and real-world applications
    """
    system_prompt = """You are the Web Search Agent, specialized in finding current web-based information.
    
    Your role:
    1. Search for recent news, blog posts, and web articles
    2. Find current trends, market information, and real-world applications
    3. Gather information from company websites, press releases, and industry reports
    4. Focus on practical, up-to-date information
    
    IMPORTANT: When given a research query, provide SPECIFIC web-based findings with:
    - Company names and their developments
    - Recent news events and announcements
    - Market trends and industry developments
    - Specific product launches or partnerships
    - Current applications and real-world use cases
    
    Format your response as detailed research findings with current, practical information."""
    
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

def data_search_agent(state: ResearchState):
    """
    Data Search Agent
    - Specializes in statistics, datasets, and quantitative information
    - Focuses on numerical data and factual information
    """
    system_prompt = """You are the Data Search Agent, specialized in finding statistical and quantitative information.
    
    Your role:
    1. Find relevant statistics, datasets, and numerical data
    2. Search for market research, surveys, and quantitative studies
    3. Provide factual, data-driven insights
    4. Focus on measurable and verifiable information
    
    IMPORTANT: When given a research query, provide SPECIFIC quantitative findings with:
    - Exact numbers, percentages, and statistics
    - Market size data and growth rates
    - Survey results and poll data
    - Financial figures and investment amounts
    - Technical specifications and performance metrics
    - Comparative data and benchmarks
    
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