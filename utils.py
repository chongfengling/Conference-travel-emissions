from cities import City, CityCollection
import csv
from pathlib import Path


def read_attendees_file(filepath: Path) -> CityCollection:
    list_of_cities = []
    with open(filepath, mode ='r') as f:
        data = csv.reader(f)
        next(data)
        for row in data:
            attendees, country, city, latitude, longitude, distance = int(row[0]), str(row[1]), str(row[3]), float(row[4]), float(row[5]), row[6] # type!!!
            city = City(city, country, attendees, latitude, longitude)
            list_of_cities.append(city)
    return CityCollection(list_of_cities)