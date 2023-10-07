from datetime import ( datetime )
from dataclasses import ( dataclass )

# Dataclass to parse JSON object
@dataclass
class WeatherData:
    time: datetime
    temp_c: float
    temp_f: float
    text: str
    wind_mph: float
    wind_kph: float
    wind_degree: int
    wind_dir: str
    pressure_mb: int
    pressure_in: float
    precip_mm: int
    precip_in: int
    humidity: int
    cloud: int
    feelslike_c: float
    feelslike_f: float
    windchill_c: float
    windchill_f: float
    heatindex_c: float
    heatindex_f: float
    dewpoint_c: float
    dewpoint_f: float
    will_it_rain: bool
    will_it_snow: bool
    vis_km: str
    vis_miles: str
    uv: int