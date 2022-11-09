from pytest import raises
from cities import City, CityCollection


def test_attributes_of_City():
    with raises(TypeError):
        City('2', 'Switzerland', 1, 47.22, 8.33)
        City('2', 'Switzerland', 1, 90, 8.33)