"""
Search Tools Module

This module contains search tools and utilities for the multi-agent research system.
Includes Brave Search API integration for privacy-focused web searching.
"""

import os
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Brave Search API configuration
BRAVE_API_KEY = os.getenv("BRAVE_SEARCH_API_KEY")
BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"

def brave_web_search(query: str, count: int = 10) -> List[Dict]:
    """
    Perform a web search using Brave Search API.
    
    Args:
        query (str): The search query
        count (int): Number of results to return (max 20)
        
    Returns:
        List[Dict]: List of search results with title, url, snippet
    """
    if not BRAVE_API_KEY:
        raise ValueError("BRAVE_SEARCH_API_KEY not found in environment variables")
    
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": BRAVE_API_KEY
    }
    
    params = {
        "q": query,
        "count": min(count, 20),  # Brave API max is 20
        "search_lang": "en",
        "country": "US",
        "safesearch": "moderate",
        "freshness": "pd",  # Past day for recent results
    }
    
    try:
        response = requests.get(BRAVE_SEARCH_URL, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        results = []
        
        # Extract web results
        web_results = data.get("web", {}).get("results", [])
        
        for result in web_results:
            formatted_result = {
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "snippet": result.get("description", ""),
                "published": result.get("age", ""),
            }
            results.append(formatted_result)
        
        return results
        
    except requests.exceptions.RequestException as e:
        print(f"Error performing Brave search: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error in Brave search: {e}")
        return []

def brave_news_search(query: str, count: int = 10) -> List[Dict]:
    """
    Perform a news search using Brave Search API.
    
    Args:
        query (str): The search query
        count (int): Number of results to return
        
    Returns:
        List[Dict]: List of news results with title, url, snippet, date
    """
    if not BRAVE_API_KEY:
        raise ValueError("BRAVE_SEARCH_API_KEY not found in environment variables")
    
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": BRAVE_API_KEY
    }
    
    params = {
        "q": query,
        "count": min(count, 20),
        "search_lang": "en",
        "country": "US",
        "safesearch": "moderate",
        "freshness": "pw",  # Past week for recent news
    }
    
    try:
        response = requests.get(BRAVE_SEARCH_URL, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        results = []
        
        # Extract news results (often in web results but can filter by recent dates)
        web_results = data.get("web", {}).get("results", [])
        
        for result in web_results:
            # Filter for news-like sources
            url = result.get("url", "").lower()
            if any(news_domain in url for news_domain in ["news", "reuters", "bloomberg", "techcrunch", "wired", "bbc", "cnn"]):
                formatted_result = {
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "snippet": result.get("description", ""),
                    "published": result.get("age", ""),
                    "source": result.get("url", "").split("//")[1].split("/")[0] if "//" in result.get("url", "") else ""
                }
                results.append(formatted_result)
        
        return results[:count]  # Return requested number of results
        
    except requests.exceptions.RequestException as e:
        print(f"Error performing Brave news search: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error in Brave news search: {e}")
        return []

def format_search_results(results: List[Dict], result_type: str = "web") -> str:
    """
    Format search results into a readable string for LLM consumption.
    
    Args:
        results (List[Dict]): Search results from Brave API
        result_type (str): Type of results ("web" or "news")
        
    Returns:
        str: Formatted search results
    """
    if not results:
        return f"No {result_type} search results found."
    
    formatted = f"\n=== {result_type.upper()} SEARCH RESULTS ===\n\n"
    
    for i, result in enumerate(results, 1):
        formatted += f"{i}. **{result.get('title', 'No title')}**\n"
        formatted += f"   URL: {result.get('url', 'No URL')}\n"
        formatted += f"   Summary: {result.get('snippet', 'No description')}\n"
        
        if result.get('published'):
            formatted += f"   Published: {result.get('published')}\n"
        if result.get('source'):
            formatted += f"   Source: {result.get('source')}\n"
            
        formatted += "\n"
    
    return formatted