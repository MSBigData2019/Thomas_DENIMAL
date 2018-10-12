#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

r = requests.get('http://www.yahoo.fr')

soup = BeautifulSoup(r.text, 'html.parser')

print(soup.find_all('a'))


#faire un map avec lambda pour filtrer


#request post sur le site
#faire une fonction qui prend une query et rend une liste de liens ( utiliser map
#specific_class = "c-article-flux_title"
#map(lambda x: x.attrs['href'],soup.find_all("a",class_=specific_class)))

#FACTORISER SON CODE


#scroller sur le site avec le chrome dev tool
#chercher les class specifiques
