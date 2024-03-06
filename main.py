from cities import City
from utils import read_attendees_file

if __name__ == "__main__":
    # File path
    filepath = 'attendee_locations.csv'

    # Read city collection
    col = read_attendees_file(filepath)

    # Example usage (choose Zurich as a travel destination)
    zurich = City('Zurich', 'Switzerland', 52, 47.22, 8.33)
    col.summary(zurich)
    col.plot_top_emitters(city=zurich, n=8, save=True)