from pytest import raises
from cities import City, CityCollection


def test_attributes_of_City():
    # create City instance with accepted attributes
    City('Zurich', 'Switzerland', 1, 47.22, 8.33)
    City('Zurich', 'Switzerland', 1, 90.0, 8.33)

    with raises(TypeError):
        # TypeError: The type of city should be a String
        City([], 'Switzerland', 1, 90.0, 8.33)
        City(1, 'Switzerland', 1, 90.0, 8.33)
        # TypeError: The type of country should be a String
    with raises(TypeError):
        City('Zurich', [], 1, 90.0, 8.33)
        City('Zurich', 1, 1, 90.0, 8.33)
    with raises(TypeError):
        # TypeError: The type of attendees should be a Int
        City('Zurich', 'Switzerland', [1], 90.0, 8.33)
        City('Zurich', 'Switzerland', '1', 90.0, 8.33)
    with raises(TypeError):
        # TypeError: The type of latitude should be a Float
        City('Zurich', 'Switzerland', 1, 1, 8.33)
        City('Zurich', 'Switzerland', 1, '90', 8.33)
    with raises(TypeError):
        # TypeError: The type of longitude should be a Float
        City('Zurich', 'Switzerland', 1, 90.0, 8)
        City('Zurich', 'Switzerland', 1, 90.0, [8])

    with raises(ValueError):
        # ValueError: attendees should be a non-negative number
        City('Zurich', 'Switzerland', -1, 47.22, 8.33)
    with raises(ValueError):
        # latitude should be restricted to the -90 to 90
        City('Zurich', 'Switzerland', 1, 100.0, 8.33)
        City('Zurich', 'Switzerland', 1, -100.0, 8.33)
    with raises(ValueError):
        # longitude should be restricted to the -180 to 180
        City('Zurich', 'Switzerland', 1, 47.22, 181.0)
        City('Zurich', 'Switzerland', 1, 47.22, -181.0)

city_1 = City('Zurich', 'Switzerland', 4, 47.22, 8.33)
city_2 = City('San Francisco', 'United States', 0, 37.7792808, -122.4192363)
city_collection = CityCollection([city_1, city_2])

def test_CityCollection_countries():
    # test method city_collection.countries()
    assert city_collection.countries() == ['Switzerland', 'United States']

def test_CityCollection_total_attendees():
    # test method city_collection.total_attendees()
    assert city_collection.total_attendees() == int(4)