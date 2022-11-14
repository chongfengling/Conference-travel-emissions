from pytest import raises, approx
import pytest
from cities import City, CityCollection

def test_City_attributes():
    # create City instance with accepted attributes
    # could reduce repetition with @pytest.mark.parametrize. We will use this method later to show different ways to construct test functions and easy understanding.
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
    c_1 = City('Zurich', 'Switzerland', 12, 0.0, 0.0)
    c_2 = City('Zurich', 'Switzerland', 20, 0.0, 75.0)
    c_3 = City('Zurich', 'Switzerland', 15, 0.0, 70.0)

    assert c_1.co2_to(c_2) / (c_1.attendees * c_1.distance_to(c_2)), 1 == approx(300.0) # c_1 to c_2: long-haul flight
    assert c_1.co2_to(c_3) / (c_1.attendees * c_1.distance_to(c_3)), 1 == approx(250.0) # c_1 to c_3: short-haul flight
    assert c_2.co2_to(c_3) / (c_2.attendees * c_2.distance_to(c_3)), 1 == approx(200.0) # c_2 to c_3: public transport

# test about method CityCollection.countries()
@pytest.mark.parametrize(
    'city_1, city_2',
    [
        (
            City('Zurich', 'Switzerland', 4, 0.0, 0.0), City('San Francisco', 'United States', 1, 1.0, 1.0)
        )
    ]
)
def test_CityCollection_countries(city_1, city_2):
    assert CityCollection([city_1, city_2]).countries().sort() == ['United States', 'Switzerland'].sort()

# test about method CityCollection.cities()
@pytest.mark.parametrize(
    'city_1, city_2',
    [
        (
            City('Zurich', 'Switzerland', 4, 0.0, 0.0), City('San Francisco', 'United States', 1, 1.0, 1.0)
        ),
        (
            City('a', 'A', 4, 0.0, 0.0), City('b', 'A', 1, 50.0, 0.0)
        )
    ]
)
def test_CityCollection_creation(city_1, city_2):
    assert CityCollection([city_1, city_2]).cities == [city_1, city_2]

# test about method CityCollection.total_attendees()
@pytest.mark.parametrize(
    'collection, expected',
    [
        (
            CityCollection([City('Zurich', 'Switzerland', 4, 0.0, 0.0), City('San Francisco', 'United States', 1, 1.0, 1.0)]), 5
        ),
        (
            CityCollection([City('a', 'a1', 4, 0.0, 0.0), City('b', 'b1', 1, 50.0, 0.0), City('c', 'c1', 10, 30.0, 0.0)]), 15
        )
    ]
)
def test_CityCollection_total_attendees(collection, expected):
    assert collection.total_attendees() == expected

# test about method CityCollection.total_distance_travel_to()
@pytest.mark.parametrize(
    'collection, host, expected',
    [
        (
            CityCollection([City('a', 'a1', 4, 0.0, 0.0), City('b', 'b1', 1, 50.0, 0.0)]), City('c', 'c1', 10, 30.0, 0.0), 15558
        ),
        (
            CityCollection([City('a', 'a1', 4, 0.0, 0.0), City('c', 'c1', 10, 50.0, 0.0)]), City('a', 'a1', 4, 0.0, 0.0), 5556*10
        )
    ]
)
def test_CityCollection_total_distance_travel_to(collection, host, expected):
    assert collection.total_distance_travel_to(host) == approx(expected,rel=1e-3)

# test about method CityCollection.travel_by_country()
@pytest.mark.parametrize(
    'collection, host, expected',
    [
        (
            CityCollection(
                [
                    City('a', 'A', 2, 0.0, 10.0),
                    City('b', 'B', 10, 0.0, 30.0)
                ]
            ),
            City('c', 'C', 3, 0.0, 40.0),
            {
                'A': approx(3334 * 2, rel=1e-3),
                'B': approx(1111 * 10, rel=1e-3)
            }
        ),
        (
            CityCollection(
                [
                    City('a1', 'A', 2, 0.0, 10.0),
                    City('a2', 'A', 10, 0.0, 30.0)
                ]
            ),
            City('c', 'C', 3, 0.0, 40.0),
            {
                "A": approx(3334 * 2 + 1111 * 10, rel=1e-3)
            }
        )
    ]
)
def test_CityCollection_travel_by_country(collection, host, expected):
    assert collection.travel_by_country(host) == expected

# test about method CityCollection.total_co2()
@pytest.mark.parametrize(
    # we do not choose various transportation as it is tested before
    'collection, host, expected',
    [
        (
            CityCollection(
                [
                    City('a', 'A', 2, 0.0, 0.0),
                    City('b', 'B', 10, 0.0, 30.0)
                ]
            ),
            City('c', 'C', 3, 0.0, 40.0),
        approx(4445 * 2 * 250 + 1111 * 10 * 250, rel=1e-3)
        ),
        (
            CityCollection(
                [
                    City('a3', 'A', 2, 0.0, 20.0),
                    City('a2', 'A', 10, 0.0, 30.0)
                ]
            ),
            City('c', 'C', 3, 0.0, 40.0),
            approx(2222 * 2 * 250 + 1111 * 10 * 250, rel=1e-3)
        )
    ]
)
def test_CityCollection_total_co2(collection, host, expected):
    assert collection.total_co2(host) == expected

# test about method CityCollection.co2_by_country()
@pytest.mark.parametrize(
    'collection, host, expected',
    [
        (
            CityCollection(
                [
                    City('a1', 'A', 2, 0.0, 0.0),
                    City('a2', 'A', 3, 0.0, 10.0),
                    City('b', 'B', 10, 0.0, 30.0)
                ]
            ),
            City('c', 'C', 3, 0.0, 40.0),
            {
                'A': approx(4445 * 2 * 250 + 3334 * 3 * 250, rel=1e-3),
                'B': approx(1111 * 10 * 250, rel=1e-3)
            }
        ),
        (
            CityCollection(
                [
                    City('a', 'A', 2, 0.0, 10.0),
                    City('b', 'B', 10, 0.0, 30.0)
                ]
            ),
            City('c', 'A', 3, 0.0, 40.0),
            {
                "A": approx(3334 * 2 * 250, rel=1e-3),
                "B": approx(1111 * 10 * 250, rel=1e-3)
            }
        )
    ]
)
def test_CityCollection_co2_by_country(collection, host, expected):
    assert collection.co2_by_country(host) == expected

# test about method CityCollection.sorted_by_emissions()
@pytest.mark.parametrize(
    'collection, expected',
    [
        (
            CityCollection(
                [
                    City('a1', 'A', 2, 0.0, 0.0),
                    City('a2', 'A', 3, 0.0, 10.0),
                    City('b', 'B', 10, 0.0, 30.0),
                    City('c', 'C', 23, 0.0, -20.0)
                ]
            ),
            [
                ('c', approx(17501500, rel=1e-3)),
                ('a1', approx(21944750, rel=1e-3)),
                ('a2', approx(25281000, rel=1e-3)),
                ('b', approx(35280500, rel=1e-3))
            ]
        )
    ]
)
def test_CityCollection_sorted_by_emissions(collection, expected):
    assert collection.sorted_by_emissions() == expected