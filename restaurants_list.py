"""
Load or download the restaurants for Restaurant Week

"""

import json
import requests


def load_restaurants():
    """
    Attempt to load from local JSON, but download if file not found

    """
    try:
        restaurants = json.load(open("restaurants_updated.json", 'r'))
    except IOError:
        restaurants = download_json()

    return restaurants


def download_json():
    """
    Downloads JSON with all restaurants

    URL was found by looking at network requests when viewing http://www.nycgo.com/restaurant-week

    """
    r = requests.get("http://www.nycgo.com/feed?vertical=restaurantWeek&entryId=179")

    restaurants_raw = r.json()

    restaurants = restaurants_raw['entries'][0]['participants']

    json.dump(restaurants, open("restaurants.json", 'w'))

    return restaurants
