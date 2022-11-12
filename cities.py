from typing import Dict, List, Tuple
from pytest import raises
import math

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
            raise ValueError('attendees should be a non-negative number')
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
        R = 6371 # approximate radius of the Earth in km
        return float(2 * R * math.asin(math.sqrt((math.sin((other.latitude - self.latitude)/2))**2 + math.cos(self.latitude) * math.cos(other.latitude) * (math.sin((other.longitude - self.longitude)/2))**2))) # Haversine formula (km)


    def co2_to(self, other: 'City') -> float:
        distance = self.distance_to(other) # distant to other city from current city
        cost_cof = 0
        if 0 <= distance <= 1000:
            cost_cof = 200
        elif distance <= 8000:
            cost_cof = 250
        else:
            cost_cof = 300
        return float(cost_cof * distance * self.attendees) # total emissions (kg) for researchers from a certain City to travel to a conference held in another City - the host city

class CityCollection:

    def __init__(self, list_of_cities) -> None:
        self.cities = list_of_cities

    def countries(self) -> List[str]:
        list_of_country = []
        for city in self.cities:
            list_of_country.append(city.country)
        return list(set(list_of_country))

    def total_attendees(self) -> int:
        total_attendees = 0
        for city in self.cities:
            total_attendees += city.attendees
        return total_attendees

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