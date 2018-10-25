#!/usr/bin/env python4

import requests
import pandas as pd
import sys
import os
from multiprocessing import Pool
from bs4 import BeautifulSoup
import re

#Thomas DENIMAL 2018


def compute_mean(array):
    sum_stars = 0
    for i in range(1,len(array),2):
        sum_stars += array[i]

    if len(array) != 0:
        result=sum_stars/(len(array)/2)
    else:
        result=0
    return result


def get_medocs(json):
    root_url='https://open-medicaments.fr/api/v1/medicaments?query=paracetamol'
    r = requests.get(root_url)
    df = pd.read_json(r.content)
    return df

def get_pagedf(url,pagenumber):
    url_page=url+'&page='+pagenumber
    r = requests.get(url_page)
    url_list=[]
    if r.status_code == 200:
        df = pd.read_json(r.content)
        df.take(5)
        return df
    else:
        print("Status Code Error")


def get_medlist():
    url='https://open-medicaments.fr/api/v1/medicaments?query=paracetamol'
    pageindex=1
    df_med=get_pagedf(url,str(pageindex))
    while df_med != None :
        result_df.concat(df_med)
        pageindex+=1
        df_med = get_pagedf(url,str(pageindex))
    return df_med


# Print github users ordered by stars
#def main(access_token):
def main():
    #dict_users={}
    #dict_users_mean={}

    #Get user list
    df =get_medlist()
    df.show()

    #FOr each user : retrieve stars and compute mean
    #index=1
    #for town in town_list:
    #    print(town)
        #print(f"Retrieving user {user} #{index}/{len(user_list)} ")
        #dict_users[user]=user_repolist(user,access_token)
        #dict_users_mean[user]=compute_mean(dict_users[user])
        #index+=1
    #Print users sorted by value
    #sorted_keys=sorted(dict_users_mean, key=dict_users_mean.get, reverse=True)
    #index=1
    #for user in sorted_keys:
    #    print(f"#{index} : User {user} : {dict_users_mean[user]}")
    #    index+=1

if __name__ == "__main__":
            #retrieve token from commandline
            #main(sys.argv[1])
            main()
