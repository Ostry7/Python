import requests
from operator import itemgetter

# https://api.nationalize.io?name=johnson    -> to guess the nationality
# https://restcountries.com/v3.1/alpha/PL    -> to select full country name
# 100 requests/day

def fullCountryName(country_id):
    response_countries = requests.get(f"https://restcountries.com/v3.1/alpha/{country_id}")
    if response_countries.status_code == 200:
        country_data = response_countries.json()
        country_name = country_data[0]['name']['common']
        return country_name
    else:
        print(f'Error: {response_countries.status_code}')
        return None

def guessNationality(name):
    response_nationalize = requests.get(f'https://api.nationalize.io?name={name}')
    if response_nationalize.status_code == 200:
        data = response_nationalize.json().get('country', [])
        sorted_response = sorted(data, key=itemgetter('probability'), reverse=True)
        return sorted_response
    else:
        print(f'Error: {response_nationalize.status_code}')
        return []

def buildResponse(data):
    for index, item in enumerate(data):   
        country_id = item['country_id']
        country_name = fullCountryName(country_id)  # Get full country name
        
        if country_name:  # Check if the country name was fetched successfully
            if index == 0:
                print(f"Your nationality is {country_name}, with {int(100 * item['probability'])}% probability")
            else:
                print(f"The other nationalities are {country_name}, with {int(100 * item['probability'])}% probability")

name = input('Please enter your name to guess your nationality: ')
nationality_data = guessNationality(name)
if nationality_data:
    buildResponse(nationality_data)
