from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Search the web for the given query and return a recent and reliable information.
       Return Title, URL,s and snippets."""
    results = tavily.search(query=query, max_results=5)

    output = []

    for r in results['results']:
        output.append(
               f"title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )

    return "\n____\n".join(output)

@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content form the given URL for deepar reading."""
    try:
        response = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup(["script", "style", "header", "footer", "nav"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True) [:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
    
