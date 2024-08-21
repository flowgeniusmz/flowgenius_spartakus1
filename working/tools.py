import streamlit as st
from openai import OpenAI as openai_client
from tavily import TavilyClient as tavily_client
from supabase import create_client as supabase_client
from googlemaps import places, geocoding, addressvalidation, Client as google_client
from googlesearch import search
from yelpapi import YelpAPI as yelp_client
import time
import json
import datetime
from typing import Literal
import pandas as pd
from pydantic import BaseModel



##### SET CLIENTS
oaiClient = openai_client(api_key=st.secrets.openai.api_key)
supaClient = supabase_client(supabase_key=st.secrets.supabase.api_key_admin, supabase_url=st.secrets.supabase.url)
yelpClient = yelp_client(api_key=st.secrets.yelp.api_key)
googClient = google_client(key=st.secrets.google.maps_api_key)
tavClient = tavily_client(api_key=st.secrets.tavily.api_key)

##### SET PYDANTIC
class BusinessInfo(BaseModel):
    formation_date: str
    business_address: str
    business_ownership: str
    website_url: str

def get_business_info(research: str):
    completion = oaiClient.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06", 
        messages=[
            {"role": "system", "content": "You are an expert at structured data extraction. You will be given unstructured text from a research paper and should convert it into the given structure."},
            {"role": "user", "content": f"{research}"}
        ],
        response_format=BusinessInfo
    )
    business_info = completion.choices[0].message.parsed
    return business_info

##### Functions
def internet_search(query: str):
    """
    Performs an internet search using the provided query and returns a list of search results.

    Args:
        query (str): The search query.

    Returns:
        list: A list of URLs corresponding to the search results.
    """
    new_query = f"What is the date of formation, ownership details / owners, business address, and website url for the business {query}?"
    response = search(query = new_query) 
    responselist = list(response)
    return responselist

def internet_research(query: str):
    """
    Performs advanced internet research using the provided query and returns the results.

    Args:
        query (str): The research query.

    Returns:
        dict: The research results, including answers and raw content.
    """
    new_query = f"What is the date of formation, ownership details / owners, business address, and website url for the business {query}?"
    response = tavClient.search(query=new_query, search_depth="advanced", max_results=7, include_answer=True, include_raw_content=True)
    return response
    

def google_places_search(query: str):
    """
    Searches for business information using Google Places to gather details on location, ratings, and more.
    
    Parameters:
        query (str): The search query describing the business.
    
    Returns:
        dict: The search results with detailed information about the business.
    """
    response = places.places(client=googClient, query=query, region="US")
    return response


query = "Nolasko Insurance Advisors" # business name
research = internet_research(query=query)
search = internet_search(query=query)
places = google_places_search(query=query)
results = f"Internet Research: {research} /n/nInternet Search: {search} /n/nGoogle Places: {places}"
info = get_business_info(research=results)
print(info)



#__________________________________________________________________________________________
# # 2. Tool Schemas


# internet_search_schema = {
#     "name": "internet_search",
#     "description": "Performs an internet search using the provided query and returns a list of search results.",
#     "parameters": {
#         "type": "object",
#         "properties": {
#         "query": {
#             "type": "string",
#             "description": "The search query."
#         }
#         },
#         "required": ["query"]
#     }
#     }

# internet_research_schema = {
#     "name": "internet_research",
#     "description": "Performs advanced internet research using the provided query and returns the results.",
#     "parameters": {
#         "type": "object",
#         "properties": {
#         "query": {
#             "type": "string",
#             "description": "The research query."
#         }
#         },
#         "required": ["query"]
#     }
#     }

# google_places_search_schema = {
#     "name": "google_places_search",
#     "description": "Searches for business information using Google Places to gather details on location, ratings, and more.",
#     "parameters": {
#         "type": "object",
#         "properties": {
#         "query": {
#             "type": "string",
#             "description": "The search query describing the business."
#         }
#         },
#         "required": ["query"]
#     }
#     }



# q = "What is the date of formation, address, ownership, and website url for the business Nolasko Insurance Advisors?"

# tav = internet_research(query=q)
# print(tav)

# goo = internet_search(query=q)
# print(goo)

# pla = google_places_search(query="Nolasko Insurance Advisors")
# print(pla)