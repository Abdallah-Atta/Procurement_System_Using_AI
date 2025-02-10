from crewai import Agent, LLM
from crewai.tools import tool
from tavily import TavilyClient
from scrapegraph_py import Client
from pydantic import BaseModel, Field
from typing import List
import json
import os
from dotenv import load_dotenv


load_dotenv()
llm = LLM(model=os.getenv("OLLAMA_MODEL"), base_url="http://localhost:11434")
search_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
scrape_client = Client(api_key=os.getenv("SGAI_API_KEY"))


# ----------------------------------------------Agent_1-----------------------------------------------

# Define the Search Queries Recommendation Agent
search_queries_recommendation_agent = Agent(
    role="Search Queries Recommendation Agent",
    goal="\n".join([
        "To provide a list of suggested search queries to be passed to the search engine.",
        "The queries must be varied and specific to the requested items."
    ]),
    backstory="The agent helps generate targeted search queries for product searches based on the provided context.",
    llm=llm,  # Use the Ollama model for consistency
    verbose=True,
)


# ----------------------------------------------Agent_2-----------------------------------------------

@tool
def search_engine_tool(query: str):
    """Useful for search-based queries. Use this to find current information about any query related pages using a search engine"""
    return search_client.search(query)

search_engine_agent = Agent(
    role="Search Engine Agent",
    goal="To search for products based on the suggested search query",
    backstory="The agent is designed to help in looking for products by searching for products based on the suggested search queries.",
    llm=llm,
    verbose=True,
    tools=[search_engine_tool]
)

# ----------------------------------------------Agent_3-----------------------------------------------

class ProductSpec(BaseModel):
    specification_name: str
    specification_value: str

class SingleExtractedProduct(BaseModel):
    page_url: str = Field(..., title="The original url of the product page")
    product_title: str = Field(..., title="The title of the product")
    product_image_url: str = Field(..., title="The url of the product image")
    product_url: str = Field(..., title="The url of the product")
    product_current_price: float = Field(..., title="The current price of the product")
    product_original_price: float = Field(title="The original price of the product before discount. Set to None if no discount", default=None)
    product_discount_percentage: float = Field(title="The discount percentage of the product. Set to None if no discount", default=None)

    product_specs: List[ProductSpec] = Field(..., title="The specifications of the product. Focus on the most important specs to compare.", min_items=1, max_items=5)

    agent_recommendation_rank: int = Field(..., title="The rank of the product to be considered in the final procurement report. (out of 5, Higher is Better) in the recommendation list ordering from the best to the worst")
    agent_recommendation_notes: List[str]  = Field(..., title="A set of notes why would you recommend or not recommend this product to the company, compared to other products.")

@tool
def web_scraping_tool(page_url: str):
    """
    An AI Tool to help an agent to scrape a web page

    Example:
    web_scraping_tool(
        page_url="https://www.noon.com/egypt-en/search/?q=espresso%20machine"
    )
    """
    details = scrape_client.smartscraper(
        website_url=page_url,
        user_prompt="Extract ```json\n" + SingleExtractedProduct.schema_json() + "```\n From the web page"
    )

    return {
        "page_url": page_url,
        "details": details
    }

scraping_agent = Agent(
    role="Web scraping agent",
    goal="To extract details from any website",
    backstory="The agent is designed to help in looking for required values from any website url. These details will be used to decide which best product to buy.",
    llm=llm,
    tools=[web_scraping_tool],
    verbose=True,
)

# ----------------------------------------------Agent_4-----------------------------------------------

procurement_report_author_agent = Agent(
    role="Procurement Report Author Agent",
    goal="To generate a professional HTML page for the procurement report",
    backstory="The agent is designed to assist in generating a professional HTML page for the procurement report after looking into a list of products.",
    llm=llm,
    verbose=True,
)
