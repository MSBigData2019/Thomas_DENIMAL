#!/usr/bin/env python3

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


def distance_villes(ville1,ville2):
    root_url='https://api.github.com/users/'
    endpoint='/repos?page=1'
    options='&per_page=500'
    headers = {'Authorization': 'token {}'.format(access_token)}

    url=root_url+user+endpoint+options
    r = requests.get(url,headers=headers)
    json=r.json()
    all_repos=[]
    for repos in json:
        all_repos+=[repos["name"],repos["stargazers_count"]]
    return all_repos

def get_top50town_list():
    url='https://www.insee.fr/fr/statistiques/1906659?sommaire=1906743'
    r = requests.get(url)
    temp_list=[]
    town_list=[]
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find("table").findAll("th")[3:]
        index=0
        for i in table:
            temp_list.append(i.get_text())
        for i in range(1,len(temp_list),2):
            town_list.append(temp_list[i])
        return town_list
    else:
        print("Status Code Error")


# Print github users ordered by stars
#def main(access_token):
def main():
    dict_users={}
    dict_users_mean={}

    #Get user list
    town_list=get_top50town_list()

    #FOr each user : retrieve stars and compute mean
    index=1
    for town in town_list:
        print(town)
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
