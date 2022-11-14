from typing import Dict, List, Tuple
from pytest import raises
import math
import matplotlib.pyplot as plt

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
        # If two cities have the same latitudes and longitudes, the distance is zero.
        R = 6371 # approximate radius of the Earth in km
        return float(2 * R * math.asin(math.sqrt((math.sin((math.radians(other.latitude) - math.radians(self.latitude))/2))**2 + math.cos(math.radians(self.latitude)) * math.cos(math.radians(other.latitude)) * (math.sin((math.radians(other.longitude) - math.radians(self.longitude))/2))**2))) # Haversine formula (km)


    def co2_to(self, other: 'City') -> float:
        distance = self.distance_to(other) # distant to other city from current city
        cost_cof = 0
        if 0 <= distance <= 1000:
            cost_cof = 200.0
        elif distance <= 8000:
            cost_cof = 250.0
        else:
            cost_cof = 300.0
        return float(cost_cof * distance * self.attendees) # total emissions (kg) for researchers from a certain City to travel to a conference held in another City - the host city

class CityCollection:

    def __init__(self, list_of_cities) -> None:
        # We accept a list of cities as different instances even their information including latitudes and longitudes are all the same.
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
        # returns the total distance traveled by all attendees
        total_distance = 0.0
        for other_city in self.cities:
            total_distance += other_city.distance_to(city) * other_city.attendees
        return total_distance

    def travel_by_country(self, city: City) -> Dict[str, float]:
        # returns a dictionary mapping the attendees' country to the distance traveled by all attendees from that country to the host city
        travel_by_country = {}
        for other_city in self.cities:
            country = other_city.country
            distance = other_city.distance_to(city) * other_city.attendees
            if country not in travel_by_country:
                travel_by_country[country] = distance
                continue
            travel_by_country[country] += distance
        return travel_by_country

    def total_co2(self, city: City) -> float:
        # returns the total CO2 emitted by all attendees if the conference were held in Zurich
        total_co2 = 0.0
        for other_city in self.cities:
            total_co2 += other_city.co2_to(city)
        return total_co2

    def co2_by_country(self, city: City) -> Dict[str, float]:
        # returns a dictionary mapping the attendees' country to the the C02 emitted by all attendees from that country to the host city
        co2_by_country = {}
        for other_city in self.cities:
            country = other_city.country
            co2 = other_city.co2_to(city)
            if country not in co2_by_country:
                co2_by_country[country] = co2
                continue
            co2_by_country[country] += co2
        return co2_by_country

    def summary(self, city: City):
        # print out the information
        print(f'Host city: {city.city} ({city.country})')

        print(f'Total CO2: {int(self.total_co2(city)/1000)} tonnes')
        num_of_cities, num_of_attendees = 0, 0
        for i in self.cities:
            if i.attendees == 0:
                continue
            num_of_cities += 1
            num_of_attendees += i.attendees
        print(f'Total attendees travelling to {city.city} from {num_of_cities} different cities: {num_of_attendees}')

    def sorted_by_emissions(self) -> List[Tuple[str, float]]:
        # returns a sorted list of city names and CO2 emissions
        # regard two cities as different instances even their information including latitudes and longitudes are all the same.
        sorted_res = []
        for host in self.cities:
            sorted_res.append((str(host.city),float(self.total_co2(host))))
        sorted_res.sort(key = lambda x:x[1])
        return sorted_res
        
    def plot_top_emitters(self, city: City, n: int = 0, save: bool = False):
        # Plot n countries with the most emissions and summed emissions for the other countries with label “All other countries”. If save is True, save the plot to a file.
        res_co2_by_country = self.co2_by_country(city)
        sorted_res = sorted(res_co2_by_country.items(), key=lambda x:x[1], reverse=True)

        countries, y, emissions_other= [], [], 0

        [[countries.append(country), y.append(emissions/1000)] for (country, emissions) in sorted_res[:n]]
        for (country, emissions) in sorted_res[n:]:
            emissions_other += emissions
        countries.append('Everywhere else')
        y.append(emissions_other/1000)

        plt.bar(countries, y)
        plt.ylabel('Total emissions (tonnes CO2)')
        plt.xticks(rotation=20, ha='right')
        plt.title(f'Total emissions from each country (top {n})')
        if save:
            host_name = city.city.replace(' ', '_')
            plt.savefig(f'./{host_name.lower()}.png')
        else:
            plt.show()


# import csv
# from pathlib import Path


# def read_attendees_file(filepath: Path) -> CityCollection:
#     list_of_cities = []
#     with open(filepath, mode ='r') as f:
#         data = csv.reader(f)
#         next(data)
#         for row in data:
#             attendees, country, city, latitude, longitude, distance = int(row[0]), str(row[1]), str(row[3]), float(row[4]), float(row[5]), row[6] # type!!!
#             city = City(city, country, attendees, latitude, longitude)
#             list_of_cities.append(city)
#     return CityCollection(list_of_cities)

# conference_city = City('Buenos Aires', 'Argentina', 0, -34.6075616, -58.437076)
# from pathlib import Path
# csv_attendees = Path('attendee_locations.csv')
# cities = read_attendees_file(csv_attendees)
# cities.plot_top_emitters(conference_city, 7)