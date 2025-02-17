import requests
import json
from operator import itemgetter

#https://api.nationalize.io?name=johnson    -> to guess the nationality
#https://restcountries.com/v3.1/alpha/PL    -> to select full country name
#100 requests/day


name = input('Please enter your name to gess your nationality: ')

response_nationalize = requests.get(f'https://api.nationalize.io?name={name}')

if response_nationalize.status_code == 200:
    data = response_nationalize.json().get('country', [])
    sorted_response = sorted(data, key=itemgetter('probability'), reverse=True)
    for index, item in enumerate(data):
        response_countries = requests.get(f"https://restcountries.com/v3.1/alpha/{item['country_id']}")
        if response_countries.status_code == 200:
            country_data = response_countries.json()
            country_name = country_data[0]['name']['common']
            if index == 0:
                print (f"Your nationality is {country_name}, in {int(100 * item['probability'])}%")
            else:
                print (f"The rest nationality are {country_name}, in {int(100 * item['probability'])}%")
        else:
            print(f'Error: {response_countries.status_code}')
else:
    print (f'Error: {response_nationalize.status_code}')

