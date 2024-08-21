import googlemaps.addressvalidation
import googlemaps.geocoding
import streamlit as st
from openai import OpenAI
from simple_salesforce import Salesforce
from tavily import TavilyClient
import pandas as pd
import json
import time
import requests
from googlemaps import Client as gClient, addressvalidation, places, geocoding, geolocation

class Tools:
    def __init__(self):
        self.salesforce_client = Salesforce(username=st.secrets.salesforce.username, password=st.secrets.salesforce.password, security_token=st.secrets.salesforce.security_token)
        self.tavily_client = TavilyClient(api_key=st.secrets.tavily.api_key)
        self.google_client = gClient(key=st.secrets.googleconfig.maps_api_key)
        self.salesforce_client = Salesforce(username=st.secrets.salesforce.username, password=st.secrets.salesforce.password, security_token=st.secrets.salesforce.security_token)
        self.tavily_client = TavilyClient(api_key=st.secrets.tavily.api_key)
        self.google_client = gClient(key=st.secrets.googleconfig.maps_api_key)
        self.headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        self.yelp_base_url = st.secrets.urlconfig.yelp_search_url


def internet_search(query: str):
    client = TavilyClient(api_key=st.secrets.tavily.api_key)
    results = client.search(query=query, search_depth="advanced", max_results=10, include_answer=True, include_raw_content=True)
    return results


# q = "What is the date of formation, address, ownership, and website url for the business Nolasko Insurance Advisors?"

# r = internet_search(query=q)
# print(r)


def places_search(query: str):
    client = gClient(key=st.secrets.google.maps_api_key)
    places_search_response = places.places(client=client, query=query, region="US")