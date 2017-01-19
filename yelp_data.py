"""
Client for using Yelp API

"""

import requests
import time


class YelpClient(object):
    def __init__(self, access_token=None):
        if access_token:
            self.access_token = access_token

            self.s = requests.Session()
            self.s.headers.update({'Authorization': 'Bearer {}'.format(self.access_token)})


    def create_access_token(self, client_id, client_secret):
        """
        Create access token

        """
        data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
        }

        r = requests.post('https://api.yelp.com/oauth2/token', data=data)

        self.access_token_raw = r.json()
        self.access_token = self.access_token_raw['access_token']

        return self.access_token


    def get_business_by_phone(self, phone_number):
        """
        Search businesses by phone number

        """
        print phone_number

        r = self.s.get('https://api.yelp.com/v3/businesses/search/phone', params={'phone': phone_number})

        time.sleep(5)

        return r.json()


    def get_business_by_location(self, name, latitude, longitude):
        """
        Search businesses by term and location

        """
        print name, latitude, longitude

        params = {
            'term': name,
            'latitude': latitude,
            'longitude': longitude,
        }

        r = self.s.get('https://api.yelp.com/v3/businesses/search', params=params)

        time.sleep(5)

        return r.json()


if __name__ == '__main__':
    main()
