#!/usr/bin/env python3

import requests
import pandas as pd
import sys
from bs4 import BeautifulSoup
import re

#Thomas DENIMAL 2018

def clean_string(string):
    return string.strip().replace('%','').replace('-','')


def get_mean_price(product):
    remises=product.find_all(class_="darty_prix_barre_remise darty_small separator_top")
    num_products=len(remises)
    mean_remise=0
    for i in remises:
        remise = clean_string(i.get_text())
        if remise != "0":
            mean_remise+=int(remise)
    if num_products==0:
        return 0
    else:
        return round(mean_remise/num_products,1)

def search_laptop(brand):
    root_url='https://www.darty.com/nav/recherche/'
    url=root_url+brand+'-portable.html'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    print("Promo sur : "+brand)
    print(get_mean_price(soup))


# Pour Airbus,LVMH,Danone
#* les ventes au quartier à fin décembre 2018
#* le prix de l'action et son % de changement au moment du crawling
#* le % Shares Owned des investisseurs institutionels
#* le dividend yield de la company, le secteur et de l'industrie
def main():
    search_laptop('acer')
    search_laptop('dell')
    search_laptop('hp')
    search_laptop('lenovo')
    search_laptop('apple')
    search_laptop('asus')
    search_laptop('sony')

if __name__ == "__main__":
        # execute only if run as a script
            main()
