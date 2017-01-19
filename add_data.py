"""
Go over restaurants and add Zagat and Yelp data

"""

import json
import pandas
import random
import time

from restaurants_list import load_restaurants
from yelp_data import YelpClient
from zagat_data import find_zagat, search_zagat, get_zagat_data


def main():
    restaurants = load_restaurants()

    with open('config_secret.json') as cred:
        creds = json.load(cred)

        # create Yelp API client
        client = YelpClient(creds['yelp']['access_token'])

        # Zagat search key
        key = creds['zagat']['key']

    data = []

    for i, restaurant in enumerate(restaurants[:]):
        print i, restaurant['title']

        if 'zagat_id' in restaurant:
            pass
        else:
            add_zagat_data(restaurant, key)

            # update restaurant info
            json.dump(restaurants, open("restaurants_updated.json", 'w'))

        if 'yelp_id' in restaurant:
            pass
        else:
            add_yelp_data(restaurant, client)

            # update restaurant info
            json.dump(restaurants, open("restaurants_updated.json", 'w'))

        if 'Dinner' in restaurant['meals']:
            data.append({
                'name': restaurant['title'],
                'zagat_id': restaurant.get('zagat_id', "NA"),
                'zagat_price': restaurant['zagat_price'],
                'zagat_food_rating': restaurant['zagat_food_rating'],
                'yelp_id': restaurant.get('yelp_id', "NA"),
                'yelp_price': restaurant.get('yelp_price', "NA"),
                'yelp_rating': restaurant.get('yelp_rating', "NA"),
                'yelp_review_count': restaurant.get('yelp_review_count', "NA")
            })

    data = pandas.DataFrame(data)
    print data.head()
    data.to_csv("restaurants.csv", index=False, encoding='utf-8')


def add_zagat_data(restaurant, key):
    """
    Add Zagat data

    """
    restaurant['zagat_food_rating'] = "NA"
    restaurant['zagat_price'] = "NA"

    time.sleep(random.randint(5,15))  # wait a random period of time before trying Zagat

    title, url = find_zagat(restaurant['title'], key)

    if url:
        try:
            business = get_zagat_data(url)
        except Exception as exc:
            print exc
            restaurant['zagat_id'] = url.split('/')[-1]
        else:
            restaurant['zagat_id'] = url.split('/')[-1]
            restaurant['zagat_food_rating'] = business['food_rating']
            restaurant['zagat_price'] = business['dollars']
    else:
        print "not found"


def add_yelp_data(restaurant, client):
    """
    Add Yelp data

    """
    restaurant['yelp_price'] = "NA"
    restaurant['yelp_rating'] = "NA"
    restaurant['yelp_review_count'] = "NA"

    # search by name / location
    response = client.get_business_by_location(restaurant['title'], restaurant['latitude'], restaurant['longitude'])

    if 'businesses' in response and response['total'] > 0:
        try:
            business = response['businesses'][0]
        except Exception as exc:
            print exc
            print response
        else:
            restaurant['yelp_id'] = business['id']
            restaurant['yelp_price'] = business['price']
            restaurant['yelp_rating'] = business['rating']
            restaurant['yelp_review_count'] = business['review_count']

    # can also search by phone number
    # convert phone number into +1DDDDDDDDDD format
    # phone_number = "+1{}".format(re.sub(r'\D', '', restaurant['phone']))
    #
    # response = client.get_business_by_phone(phone_number)
    #
    # if 'businesses' in response:
    #     if response['total'] == 1:
    #         business = response['businesses'][0]
    #
    #         restaurant['yelp_id'] = business['id']
    #         restaurant['yelp_price'] = business['price']
    #         restaurant['yelp_rating'] = business['rating']
    #         restaurant['yelp_review_count'] = business['review_count']


if __name__ == '__main__':
    main()
