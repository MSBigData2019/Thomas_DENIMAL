import requests
import unittest
from bs4 import BeautifulSoup
import pandas as pd
import json


url='http://www.omdbapi.com?apikey=8bbcd557&s=star wars&type=movie'

res = requests.get(url)

response_object = json.loads(res.text)
movies_list = response_object['Search']
df_movies = pd.DataFrame(movies_list)



