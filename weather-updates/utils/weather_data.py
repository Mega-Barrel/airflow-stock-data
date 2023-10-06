
import os
import requests
import pandas as pd
from dotenv import ( load_dotenv )
from datetime import ( datetime, timedelta )
load_dotenv()

def get_api_key():
    """
    Returns the API key from environment variable.
    """
    API_KEY = os.environ.get('weather_api')
    if not API_KEY:
        raise ValueError('API key is not available.')
    else:
        return API_KEY

def get_previous_hour_weather_data():
    """
    Method to Make a call to weather API, and get previous day data
    """
    # Common
    query = 'Mumbai'
    dt = datetime.today() - timedelta(1)
    _key = get_api_key()
    api_url = "http://api.weatherapi.com/v1/"
    query_key = f"key={_key}&q={query}"

    # API Endooint
    url = f"{api_url}history.json?{query_key}&dt={dt}"
    resp = requests.get(url=url)

    # Return the JSON data if status code is 200
    if resp.status_code == 200:
        data = resp.json()["forecast"]["forecastday"]

        weather_obj = {
            'Date': data[0]['date'],
            'Date Epoch': data[0]['date_epoch'],
            'Avg temp C': data[0]['day']['avgtemp_c'],
            'Avg temp F': data[0]['day']['avgtemp_f'],
            'Max temp C': data[0]['day']['maxtemp_c'],
            'Max temp F': data[0]['day']['maxtemp_f'],
            'Max wind kph': data[0]['day']['maxwind_kph'],
            'Max wind mph': data[0]['day']['maxwind_mph'],
            'Min temp C': data[0]['day']['mintemp_c'],
            'Min temp F': data[0]['day']['mintemp_f'],
            'Total precip': data[0]['day']['totalprecip_mm'],
            'Weather condition': data[0]['day']['condition']['text']
        }

        df = pd.DataFrame(weather_obj, index=[0])
        df.to_csv(
            'data/weather_data.csv', 
            index=False, 
            mode='a', 
            header=not os.path.exists('data/weather_data.csv')
        )
    else:
        return 'Uh ooh, something went wrong while retriving data. Please check your input'
