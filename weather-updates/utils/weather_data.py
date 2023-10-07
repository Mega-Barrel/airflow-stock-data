
import os
import requests
import pandas as pd
from dotenv import ( load_dotenv )
from datetime import ( datetime, timedelta )
from weather_dataclass import ( WeatherData )

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
        data = resp.json()
        return data
    else:
        return 'Uh ooh, something went wrong while retriving data. Please check your input'

def transform_data(data):
    """
    Method to transform the data
    """
    weather_data_list = []
    json_objects_list = data["forecast"]["forecastday"][0]["hour"]

    # Iterate over the JSON data
    for json_data in json_objects_list:
        weather_data = WeatherData(
            time=str(datetime.strptime(json_data["time"], "%Y-%m-%d %H:%M")),
            temp_c=json_data["temp_c"],
            temp_f=json_data["temp_f"],
            text=json_data["condition"]["text"],
            wind_mph=json_data["wind_mph"],
            wind_kph=json_data["wind_kph"],
            wind_degree=json_data["wind_degree"],
            wind_dir=json_data["wind_dir"],
            pressure_mb=json_data["pressure_mb"],
            pressure_in=json_data["pressure_in"],
            precip_mm=json_data["precip_mm"],
            precip_in=json_data["precip_in"],
            humidity=json_data["humidity"],
            cloud=json_data["cloud"],
            feelslike_c=json_data["feelslike_c"],
            feelslike_f=json_data["feelslike_f"],
            windchill_c=json_data["windchill_c"],
            windchill_f=json_data["windchill_f"],
            heatindex_c=json_data["heatindex_c"],
            heatindex_f=json_data["heatindex_f"],
            dewpoint_c=json_data["dewpoint_c"],
            dewpoint_f=json_data["dewpoint_f"],
            will_it_rain=bool(json_data["will_it_rain"]),
            will_it_snow=bool(json_data["will_it_snow"]),
            vis_km=json_data["vis_km"],
            vis_miles=json_data["vis_miles"],
            uv=json_data["uv"]
        )
        weather_data_list.append(weather_data)
    # Return transformed data
    return weather_data_list

def load_data(data):
    """
    Method to save the data to CSV file
    """
    weather_df = pd.DataFrame(
        [weather_data.__dict__ for weather_data in data]
    )
    weather_df.to_csv(
        'data/daily_weather_data.csv',
        index=False, 
        mode='a', 
        header=not os.path.exists('data/daily_weather_data.csv')
    )
