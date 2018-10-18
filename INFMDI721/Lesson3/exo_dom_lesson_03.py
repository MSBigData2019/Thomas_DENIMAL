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


def user_repolist(user,access_token):
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

def get_user_list():
    url='https://gist.github.com/paulmillr/2657075'
    r = requests.get(url)
    #find=soup.find_all(class_="repository-content gist-content")
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find("table").findAll("tr")[1:]
        return [row.find("td").text.split()[0] for row in table]
    else:
        print("Status Code Error")


# Print github users ordered by stars
def main(access_token):
    dict_users={}
    dict_users_mean={}

    #Get user list
    user_list=get_user_list()

    #FOr each user : retrieve stars and compute mean
    index=1
    for user in user_list:
        print(f"Retrieving user {user} #{index}/{len(user_list)} ")
        dict_users[user]=user_repolist(user,access_token)
        dict_users_mean[user]=compute_mean(dict_users[user])
        index+=1
    #Print users sorted by value
    sorted_keys=sorted(dict_users_mean, key=dict_users_mean.get, reverse=True)
    index=1
    for user in sorted_keys:
        print(f"#{index} : User {user} : {dict_users_mean[user]}")
        index+=1

if __name__ == "__main__":
            #retrieve token from commandline
            main(sys.argv[1])
