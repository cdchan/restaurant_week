# coding=utf-8
"""
Simple PoC for scraping Zagat ratings given a restaurant name search string

"""

import json
import re
import requests

from lxml import etree


def find_zagat(name, key):
    """
    Initially try the full name of the restaurant, but then try simpler strings.

    """
    title, url = search_zagat(name, key)

    if not url:
        truncated_name = re.split(ur'-|—', name)[0]  # many restaurant names have a dash for neighborhood in them

        if truncated_name != name:
            print u"trying truncated: {}".format(truncated_name)

            title, url = search_zagat(truncated_name, key)

    if not url:
        restaurant_stripped_name = re.sub(ur'Restaurant.*|Ristorante.*', ur'', truncated_name)

        if restaurant_stripped_name != truncated_name:
            print u"trying stripping restaurant: {}".format(restaurant_stripped_name)

            title, url = search_zagat(restaurant_stripped_name, key)

    return title, url


def search_zagat(name, key):
    """
    Uses the Zagat search endpoint to find restaurants by name. This is less comprehensive than a true search on Zagat.

    """
    # Do a search on zagat.com web and find your 32 character key from the search's GET request
    params = {
        'key': key,
        'query': name,
    }

    search_response = requests.get(u"https://www.zagat.com/proxy/v1.4?m=search-suggest&city=1020", params=params)

    result = search_response.json()

    # Assume it's the first search result we want, but grab the title to
    # compare later and be "sure".
    try:
        title = result["data"]["results"][0]["title"]
        url = result["data"]["results"][0]["url"]
    except (KeyError, IndexError):
        title = None
        url = None

    return title, url


def get_zagat_data(url):
    """
    Scrape Zagat restaurant page for ratings / dollars.

    """
    rating = "NA"
    dollars = "NA"

    place_response = requests.get(url)
    tree = etree.HTML(place_response.content)

    rating_match = tree.xpath('//*[@id="content"]/div[1]/div/div[1]/div/div/div[1]/div[1]')

    try:
        rating = rating_match[0].text
    except IndexError as exc:
        pass
    except Exception as exc:
        print exc

    dollars_match = tree.xpath('//*[@id="container"]/div[2]/span/span[3]')

    try:
        dollars = dollars_match[0].text
    except IndexError as exc:
        pass
    except Exception as exc:
        print exc

    return {
        'food_rating': rating,
        'dollars': dollars
    }
