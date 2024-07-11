from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import requests
import pprint


BASE_URL = 'https://api.edamam.com/api/recipes/v2'
APP_ID = 'd3661e3f'
APP_KEY = '1c75873f67d56f2a5c48a2b82f53cc56'

params = {
    'type': 'public',
    'q': ['fish', 'fruit'],
    'app_id': APP_ID,
    'app_key': APP_KEY,
}

response = requests.get(BASE_URL, params=params)
dict_format = response.json()

print(dict_format['hits'][0]['recipe']
      ['ingredientLines'])  # list of ingredients
print(dict_format['hits'][0]['recipe']['label'])  # recipe name
print(dict_format['hits'][0]['recipe']['shareAs'])  # edamam recipe url
print(dict_format['hits'][0]['recipe']['url'])  # original recipe url
