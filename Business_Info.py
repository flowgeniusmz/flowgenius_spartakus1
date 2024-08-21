import streamlit as st
from openai import OpenAI as openai_client
from tavily import TavilyClient as tavily_client
from supabase import create_client as supabase_client
from googlemaps import places, geocoding, addressvalidation, Client as google_client
from googlesearch import search
from yelpapi import YelpAPI as yelp_client
import json
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
    try:
        response = oaiClient.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06", 
            messages=[
                {"role": "system", "content": "You are an expert at structured data extraction. You will be given unstructured text from a research paper and should convert it into the given structure."},
                {"role": "user", "content": f"{research}"}
            ],
            response_format=BusinessInfo
        )
        completion = response.choices[0].message.parsed
        return completion
    except Exception as e:
        print(f"Error in get_business_info: {e}")
        return None

##### Functions
def internet_search(query: str):
    try:
        new_query = f"What is the date of formation, ownership details / owners, business address, and website url for the business {query}?"
        response = search(query=new_query) 
        responselist = list(response)
        return "\n".join(responselist)
    except Exception as e:
        print(f"Error in internet_search: {e}")
        return ""

def internet_research(query: str):
    try:
        new_query = f"What is the date of formation, ownership details / owners, business address, and website url for the business {query}?"
        response = tavClient.search(query=new_query, search_depth="advanced", max_results=7, include_answer=True, include_raw_content=True)
        return f"Answer: {response.get('answer', '')}\nRaw Content: {response.get('raw_content', '')}"
    except Exception as e:
        print(f"Error in internet_research: {e}")
        return ""

def google_places_search(query: str):
    try:
        response = places.places(client=googClient, query=query, region="US")
        results = response.get('results', [])
        return "\n".join([f"Name: {res.get('name', '')}, Address: {res.get('formatted_address', '')}" for res in results])
    except Exception as e:
        print(f"Error in google_places_search: {e}")
        return ""

def compile_results(query: str):
    try:
        search_result = internet_search(query)
        research_result = internet_research(query)
        google_result = google_places_search(query)

        compiled_result = "\n\n".join([search_result, research_result, google_result])
        return compiled_result
    except Exception as e:
        print(f"Error in compile_results: {e}")
        return ""

def business_info(query):
# Main code execution

    compiled_result = compile_results(query)

    if compiled_result:
        business_info = get_business_info(compiled_result)
        if business_info:
            print(business_info)
            return business_info
            
        else:
            print("Failed to retrieve business information.")
            return("Failed to retrieve business information")
            
    else:
        print("Failed to compile results.")
