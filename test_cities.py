from pytest import raises
from cities import City, CityCollection


def test_City_attributes():
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

def test_City_transportation():
    # test the transportation choice
    # small error (like 1e-15) caused by computing is accepted by function round()
    c_1 = City('Zurich', 'Switzerland', 12, 0.0, 1.0)
    c_2 = City('Zurich', 'Switzerland', 20, 1.0, 0.0)
    c_3 = City('Zurich', 'Switzerland', 15, 1.0, 0.1)

    assert round(c_1.co2_to(c_2) / (c_1.attendees * c_1.distance_to(c_2)), 1) == 300.0 # c_1 to c_2: long-haul flight
    assert round(c_1.co2_to(c_3) / (c_1.attendees * c_1.distance_to(c_3)), 1) == 250.0 # c_1 to c_3: short-haul flight
    assert round(c_2.co2_to(c_3) / (c_2.attendees * c_2.distance_to(c_3)), 1) == 200.0 # c_2 to c_3: public transport


city_1 = City('Zurich', 'Switzerland', 4, 0.0, 0.0)
city_2 = City('San Francisco', 'United States', 0, 1.0, 1.0)
city_collection = CityCollection([city_1, city_2])

def test_CityCollection_countries(): # order is random
    # test method city_collection.countries()
    assert city_collection.countries() == ['Switzerland', 'United States']

def test_CityCollection_total_attendees():
    # test method city_collection.total_attendees()
    assert city_collection.total_attendees() == int(4)

# def test_CityCollection_total_distance_travel_to():
#     # test method 
#     assert CityCollection.total_distance_travel_to(city_1) == float()
