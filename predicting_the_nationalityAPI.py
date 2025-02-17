import requests
import json
from operator import itemgetter

#https://api.nationalize.io?name=johnson
#100 requests/day


name = input('Please enter your name to gess your nationality: ')

response = requests.get(f'https://api.nationalize.io?name={name}')

if response.status_code == 200:
    data = response.json().get('country', [])
    sorted_response = sorted(data, key=itemgetter('probability'), reverse=True)
    for index, item in enumerate(data):
        if index == 0:
            print (f"Your nationality is {item['country_id']}, in {int(100 * item['probability'])}%")
        else:
            print (f"The rest nationality are {item['country_id']}, in {int(100 * item['probability'])}%")

else:
    print (f'Error: {response.status_code}')

