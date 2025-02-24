import os

import groq
from groq import Groq
import openai
from openai import OpenAI

import json
import pandas as pd
import time
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(level = logging.INFO)

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

class SmartPrompt:
    def __init__(self, country, city):
        self.delimiter = "#####"
        self.country = country
        self.city = city
        
    def get_events_details(self):

        get_events_system = """You are a web scraper and data extraction assistant.\
        Your task is to extract structured information from an HTML div containing event details from Eventbrite.\
        The input is an HTML div, and your task is to output a Python dictionary where each key corresponds to an important event attribute. 

        Follow the steps in the Instructions below:
        Step 1:##### Parse the provided HTML <div> and extract the relevant information.
        Step 2:##### Structure the extracted details into a dictionary with the following keys:
        - event_name: Extract the event title.
        - event_category: Extract the event category (e.g., film-and-media).
        - event_id: Extract the unique event identifier.
        - event_location: Extract the location (city and region).
        - venue: Extract the venue where the event is happening.
        - event_time: Extract the event date and time.
        - event_url: Extract the URL for booking tickets.
        - image_url: Extract the event main image URL.

        Step 3:##### After extracting the details into a dictionary \
        Give a brief description of the event, not longer than 50 words,\
        Ensure the descriptions are dynamic and unique \
        insert appropriate emojis and smileys in the format: event_description: Brief Description

        Step 4:#####. The final output should be a structured Python dictionary below in the json format:
        
        {
            "event_name": "Movie In The Park (February 2025)",
            "event_category": "film-and-media",
            "event_id": "1219372739689",
            "event_location": "Accra, Greater Accra Region",
            "venue": "Bako Events Center",
            "event_time": "Friday • 7:00 PM",
            "event_url": "https://www.eventbrite.com/e/movie-in-the-park-february-2025-tickets-1219372739689?aff=ebdssbcitybrowse",
            "image_url": "https://img.evbuc.com/https%3A%2F%2Fcdn.evbuc.com%2Fimages%2F958904343%2F2275683218183%2F1%2Foriginal.20250212-113350?crop=focalpoint&fit=crop&w=355&auto=format%2Ccompress&q=75&sharp=10&fp-x=5.11673151751e-05&fp-y=6.03112840467e-06&s=173afc02ecc8d6749be300b7735516de",
            "event_description": "Enjoy a magical evening under the stars with an outdoor movie at Bako Events Center in Accra. Bring your loved ones for a cozy cinematic experience. 🎬🌟"
        }
        """

        return get_events_system


class LLMEventQuery(SmartPrompt):

    def __init__(self, result_list, country, city, model, is_db=False):
        super().__init__(country, city)
        self.data = result_list
        if is_db:
            #fetch from db
            pass
        else:
            self.country = country
            self.city = city
            self.model = model

    def query_openai_chat(self, messages):
        
        temperature=0.6
        max_tokens=3000
        response_format={ "type": "json_object" }
        
        response = openai_client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature, 
            max_tokens=max_tokens,
            response_format=response_format
        )
        
        openai_response = response.choices[0].message.content
        logging
        return openai_response

    def query_groq_chat(self, message):
        
        response = groq_client.chat.completions.create(
            model=self.model,
            messages=message,
            temperature=0.6,
            max_completion_tokens=3000,
            top_p=0.95,
            stream=False,
            response_format={"type": "json_object"},
            stop=None,
        )

        groq_response = response.choices[0].message.content
        return groq_response

    def clean_llm_json(self, llm_json):
        clean_json = llm_json.replace("'", '"')    
        if "\n" in llm_json:
            clean_json = f"[{clean_json}]"
            clean_json = clean_json.replace("\n", '')
        clean_json = json.loads(clean_json)
        return clean_json

    def clean_llm_special_json(self, llm_json):
        clean_json = f"{llm_json}"
        if "\n" in llm_json:
            new_lines = ["\n\n", "\n"]
            for xter in new_lines:
                clean_json = clean_json.replace(xter,"")
            clean_json = f'[{clean_json}]'
        clean_json = json.loads(clean_json)
        return clean_json

    def generate_events_table(self):
        html_load =self.data
        model = self.model
        event_list = []
        i=0
        event_extract_system = self.get_events_details()

        for item in html_load:
            i+=1
            logging.info(f"===== extracting event data for event-item-{i} =====")

            messages =  [{'role':'system', 'content': event_extract_system},
                    {'role':'user', 'content': f"{item}"}]
            
            if model == "gpt-4o":
                event = self.query_openai_chat(messages)
            else:  
                event = self.query_groq_chat(messages)

            event_json = self.clean_llm_special_json(event)
            logging.info(f"{event_json}")
                    
            if isinstance(event_json, dict):
                event_list.append(event)
            else:
                event_list.extend(event_json)

        event_list_df = pd.DataFrame(event_list)

        return event_list_df