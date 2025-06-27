from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Literal
from agents import (
    ResearchState,
    lead_agent,
    academic_search_agent,
    web_search_agent,
    data_search_agent,
    citations_agent,
    synthesis_agent
)

def router(state: ResearchState) -> Literal["academic_search", "web_search", "data_search"]:
    """
    Router function to determine which search agents to activate.
    For now, we'll activate all search agents in parallel.
    """
    # This could be made smarter based on the query type
    return ["academic_search", "web_search", "data_search"]

def aggregator(state: ResearchState):
    """
    Aggregation node that waits for all search agents to complete
    before proceeding to citations agent.
    """
    # This node doesn't modify the state, just acts as a collection point
    return {"messages": state["messages"]}

def create_research_workflow():
    """
    Creates the multi-agent research workflow graph with proper parallel execution.
    
    Returns:
        Compiled LangGraph workflow
    """
    # Create the workflow graph
    workflow = StateGraph(ResearchState)
    
    # Add all agent nodes
    workflow.add_node("lead_agent", lead_agent)
    workflow.add_node("academic_search", academic_search_agent)
    workflow.add_node("web_search", web_search_agent)
    workflow.add_node("data_search", data_search_agent)
    workflow.add_node("aggregator", aggregator)
    workflow.add_node("citations_agent", citations_agent)
    workflow.add_node("synthesis", synthesis_agent)
    
    # Define the workflow edges
    # Start with lead agent
    workflow.add_edge(START, "lead_agent")
    
    # Lead agent dispatches to all search agents in parallel
    workflow.add_edge("lead_agent", "academic_search")
    workflow.add_edge("lead_agent", "web_search") 
    workflow.add_edge("lead_agent", "data_search")
    
    # All search agents feed into aggregator
    workflow.add_edge("academic_search", "aggregator")
    workflow.add_edge("web_search", "aggregator")
    workflow.add_edge("data_search", "aggregator")
    
    # Aggregator feeds into citations agent
    workflow.add_edge("aggregator", "citations_agent")
    
    # Citations agent feeds into synthesis
    workflow.add_edge("citations_agent", "synthesis")
    
    # Synthesis completes the workflow
    workflow.add_edge("synthesis", END)
    
    # Compile the workflow
    return workflow.compile()

def run_research(query: str, verbose: bool = True):
    """
    Execute a research query using the multi-agent system.
    
    Args:
        query (str): The research question/topic
        verbose (bool): Whether to show detailed agent interactions
        
    Returns:
        dict: The final state containing all research results
    """
    # Create the workflow
    app = create_research_workflow()
    
    # Initialize state with user query
    initial_state = {
        "messages": [HumanMessage(content=query)],
        "user_query": query,
        "subtasks": [],
        "search_results": [],
        "citations": [],
        "final_report": ""
    }
    
    if verbose:
        print("\n🚀 Starting Multi-Agent Research Process...")
        print("=" * 60)
    
    # Execute the workflow with streaming to show progress
    result = None
    step_count = 0
    
    # Use the stream method to see each step
    for step in app.stream(initial_state):
        step_count += 1
        
        if verbose:
            # Get the node name and content
            node_name = list(step.keys())[0] if step else "unknown"
            step_data = step.get(node_name, {})
            
            # Display agent activity with nice formatting
            print(f"\n{'🎯' if node_name == 'lead_agent' else '🔍' if 'search' in node_name else '📝' if node_name == 'citations_agent' else '🧠' if node_name == 'synthesis' else '⚡'} AGENT: {node_name.upper().replace('_', ' ')}")
            print("─" * 50)
            
            # Show the latest message from this step
            if "messages" in step_data and step_data["messages"]:
                latest_message = step_data["messages"][-1]
                if hasattr(latest_message, 'content'):
                    # Truncate very long messages for readability
                    content = latest_message.content
                    if len(content) > 500:
                        content = content[:500] + "...\n[Response truncated for display]"
                    
                    print(f"💭 Response:\n{content}")
                else:
                    print("📤 Agent completed processing")
            
            print("─" * 50)
            
            # Store the final result
            result = step_data
    
    if verbose:
        print(f"\n✨ Workflow completed in {step_count} steps!")
    
    return result

# Test the workflow
if __name__ == "__main__":
    print("🔬 MULTI-AGENT RESEARCH SYSTEM")
    print("=" * 60)
    print("🤖 Powered by Azure OpenAI & LangGraph")
    print("=" * 60)
    
    # Test query
    test_query = "What are the top 3 scenarios I should model for macroeconomic events if there is geopolitical unrest in the Middle East?"
    
    print(f"\n� RESEARCH QUERY:")
    print(f"   {test_query}")
    print("\n🔄 AGENT WORKFLOW:")
    print("   Lead Agent → Search Agents (Parallel) → Citations → Synthesis")
    
    # Run the research with verbose output
    result = run_research(test_query, verbose=True)
    
    # Display final comprehensive results
    print("\n" + "=" * 60)
    print("📊 FINAL RESEARCH REPORT")
    print("=" * 60)
    
    if result and "messages" in result and result["messages"]:
        # Show all agent contributions
        print("\n🗂️  AGENT CONTRIBUTIONS:")
        print("-" * 40)
        
        agent_names = [
            "INITIAL QUERY",
            "LEAD AGENT", 
            "ACADEMIC SEARCH",
            "WEB SEARCH", 
            "DATA SEARCH",
            "AGGREGATOR",
            "CITATIONS AGENT",
            "SYNTHESIS AGENT"
        ]
        
        for i, message in enumerate(result["messages"]):
            if hasattr(message, 'content') and message.content.strip():
                agent_name = agent_names[i] if i < len(agent_names) else f"AGENT {i+1}"
                print(f"\n🏷️  {agent_name}:")
                print("   " + "─" * 35)
                
                # Format the content nicely
                content = message.content
                lines = content.split('\n')
                for line in lines[:10]:  # Show first 10 lines
                    print(f"   {line}")
                
                if len(lines) > 10:
                    print(f"   ... ({len(lines)-10} more lines)")
                print()
        
        # Highlight the final synthesis
        print("\n" + "🎯" * 20)
        print("FINAL SYNTHESIS REPORT")
        print("🎯" * 20)
        final_message = result["messages"][-1]
        if hasattr(final_message, 'content'):
            print(final_message.content)
    else:
        print("❌ No results generated.")
    
    print("\n" + "=" * 60)
    print("✅ RESEARCH COMPLETE")
    print("=" * 60)
