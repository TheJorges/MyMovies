import os
import environ
import requests


env = environ.Env()
environ.Env.read_env('.env')
print('API_KEY: ', env('API_KEY'))
print('API_TOKEN: ', env('API_TOKEN'))

'''
url --request GET \
     --url 'https://api.themoviedb.org/3/movie/76341?language=en-US' \
     --header 'Authorization: Aasdfqwer' \
     --header 'accept: application/json'
'''
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {env('API_TOKEN')}"}

movie_id = 76341
r = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?language=en-US', headers=headers) 
print(r.json())


r = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US', headers=headers) 
print(r.json())

