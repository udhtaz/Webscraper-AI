import requests
from bs4 import BeautifulSoup
import pandas as pd
from app.utils.prompts import LLMEventQuery

import logging
logging.basicConfig(level=logging.INFO)
    

def get_all_events_table(country, city, model):
    session = requests.Session()
    url = f"https://www.eventbrite.com/d/{country}--{city}/events/"
    
    try:
        res = session.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        res.raise_for_status()  # Raises HTTPError for bad responses

        bs = BeautifulSoup(res.text, 'html.parser')
        result_list = bs.find_all('div', {"class": "small-card-mobile eds-l-pad-all-2"})

        if not result_list:
            logging.warning("No events found for the given location.")
            return pd.DataFrame()  # Return empty DataFrame instead of a string

        gpt_query_events = LLMEventQuery(result_list, country, city, model)
        all_events = gpt_query_events.generate_events_table()

        if not isinstance(all_events, pd.DataFrame):
            logging.error("Expected a DataFrame, but got something else.")
            return pd.DataFrame()  # Prevents string error

        return all_events

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred, Please check if the country or city is spelled correctly: {http_err} ")
        return pd.DataFrame()

    except requests.exceptions.RequestException as req_err:
        logging.error(f"Please check your internet connection or the URL. Network error occurred while trying to reach the site: {req_err}")
        return pd.DataFrame()

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return pd.DataFrame()