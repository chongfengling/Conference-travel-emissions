from typing import Dict, List, Tuple
from pytest import raises

class City:
    def __init__(self, city, country, attendees, latitude, longitude) -> None:
        if not isinstance(city, str): # type check
            raise TypeError('The type of city should be a String')
        self.city = city

        if not isinstance(country, str): # type check
            raise TypeError('The type of country should be a String')
        self.country = country

        if not isinstance(attendees, int): # type check
            raise TypeError('The type of attendees should be a Int')
        if attendees < 0: # value check
            raise ValueError('attendees should be a positive number')
        self.attendees = attendees

        if not isinstance(latitude, float): # type check
            raise TypeError('The type of latitude should be a Float')
        if latitude < -90 or latitude > 90: # value check
            raise ValueError('latitude should be restricted to the -90 to 90')
        self.latitude = latitude

        if not isinstance(longitude, float): # type check
            raise TypeError('The type of longitude should be a Float')
        if longitude < -180 or longitude > 180: # value check
            raise ValueError('longitude should be restricted to the -180 to 180')
        self.longitude = longitude
        
    def distance_to(self, other: 'City') -> float:
        raise NotImplementedError

    def co2_to(self, other: 'City') -> float:
        raise NotImplementedError

class CityCollection:
    ...

    def countries(self) -> List[str]:
        raise NotImplementedError

    def total_attendees(self) -> int:
        raise NotImplementedError

    def total_distance_travel_to(self, city: City) -> float:
        raise NotImplementedError

    def travel_by_country(self, city: City) -> Dict[str, float]:
        raise NotImplementedError

    def total_co2(self, city: City) -> float:
        raise NotImplementedError

    def co2_by_country(self, city: City) -> Dict[str, float]:
        raise NotImplementedError

    def summary(self, city: City):
        raise NotImplementedError

    def sorted_by_emissions(self) -> List[Tuple[str, float]]:
        raise NotImplementedError

    def plot_top_emitters(self, city: City, n: int, save: bool):
        raise NotImplementedError

# zurich = City(2, 'Switzerland', 52, 47.22, 8.33)