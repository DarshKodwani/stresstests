"""
Search Tools Module

This module contains search tools and utilities for the multi-agent research system.
Includes Brave Search API integration for privacy-focused web searching.
"""

import os
import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Brave Search API configuration
BRAVE_API_KEY = os.getenv("BRAVE_SEARCH_API_KEY")
BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"

# arXiv API configuration
ARXIV_API_URL = "http://export.arxiv.org/api/query"

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

def arxiv_search(query: str, max_results: int = 10) -> List[Dict]:
    """
    Search arXiv for academic papers.
    
    Args:
        query (str): Search query (can include field prefixes like 'ti:' for title, 'au:' for author)
        max_results (int): Maximum number of results to return
        
    Returns:
        List[Dict]: List of paper results with title, authors, abstract, url, published date
    """
    params = {
        'search_query': query,
        'start': 0,
        'max_results': max_results,
        'sortBy': 'relevance',
        'sortOrder': 'descending'
    }
    
    try:
        response = requests.get(ARXIV_API_URL, params=params)
        response.raise_for_status()
        
        # Parse XML response
        root = ET.fromstring(response.content)
        
        # Define namespaces
        namespaces = {
            'atom': 'http://www.w3.org/2005/Atom',
            'arxiv': 'http://arxiv.org/schemas/atom'
        }
        
        results = []
        entries = root.findall('atom:entry', namespaces)
        
        for entry in entries:
            # Extract paper information
            title = entry.find('atom:title', namespaces)
            title_text = title.text.strip().replace('\n', ' ') if title is not None else "No title"
            
            # Extract authors
            authors = []
            author_elements = entry.findall('atom:author', namespaces)
            for author in author_elements:
                name = author.find('atom:name', namespaces)
                if name is not None:
                    authors.append(name.text)
            
            # Extract abstract
            summary = entry.find('atom:summary', namespaces)
            abstract = summary.text.strip().replace('\n', ' ') if summary is not None else "No abstract"
            
            # Extract URL
            id_element = entry.find('atom:id', namespaces)
            paper_url = id_element.text if id_element is not None else ""
            
            # Extract published date
            published = entry.find('atom:published', namespaces)
            published_date = published.text[:10] if published is not None else ""  # Extract just the date part
            
            # Extract categories
            categories = []
            category_elements = entry.findall('atom:category', namespaces)
            for cat in category_elements:
                term = cat.get('term')
                if term:
                    categories.append(term)
            
            paper_info = {
                'title': title_text,
                'authors': authors,
                'abstract': abstract,
                'url': paper_url,
                'published': published_date,
                'categories': categories,
                'authors_string': ', '.join(authors) if authors else "Unknown authors"
            }
            
            results.append(paper_info)
        
        return results
        
    except requests.exceptions.RequestException as e:
        print(f"Error performing arXiv search: {e}")
        return []
    except ET.ParseError as e:
        print(f"Error parsing arXiv XML response: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error in arXiv search: {e}")
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

def format_arxiv_results(results: List[Dict]) -> str:
    """
    Format arXiv search results into a readable string for LLM consumption.
    
    Args:
        results (List[Dict]): arXiv search results
        
    Returns:
        str: Formatted academic paper results
    """
    if not results:
        return "No academic papers found on arXiv."
    
    formatted = "\n=== ARXIV ACADEMIC PAPERS ===\n\n"
    
    for i, paper in enumerate(results, 1):
        formatted += f"{i}. **{paper.get('title', 'No title')}**\n"
        formatted += f"   Authors: {paper.get('authors_string', 'Unknown authors')}\n"
        formatted += f"   Published: {paper.get('published', 'Unknown date')}\n"
        formatted += f"   Categories: {', '.join(paper.get('categories', []))}\n"
        formatted += f"   URL: {paper.get('url', 'No URL')}\n"
        formatted += f"   Abstract: {paper.get('abstract', 'No abstract')[:500]}{'...' if len(paper.get('abstract', '')) > 500 else ''}\n"
        formatted += "\n"
    
    return formatted