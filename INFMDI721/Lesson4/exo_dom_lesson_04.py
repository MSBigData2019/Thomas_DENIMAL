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


def get_carinfo(url):
    root_url='https://www.lacentrale.fr/'
    r = requests.get(root_url+url)
    soup = BeautifulSoup(r.content, "html.parser")
    #headers = {'Authorization': 'token {}'.format(access_token)}
    #r = requests.get(url,headers=headers)
    #json=r.json()
    href_list=soup.find(class_="box boxOptions infosGen").find_all(class_="linkAd ann")
    all_repos=[]
    for repos in json:
        all_repos+=[repos["name"],repos["stargazers_count"]]
    return all_repos

def get_pageresults(url,pagenumber):
    url_page=url+'&page='+pagenumber
    r = requests.get(url_page)
    url_list=[]
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, "html.parser")
        href_list=soup.find(class_="resultListContainer").find_all(class_="linkAd ann")
        for href in href_list:
            url_list.append(href['href'])
        return url_list
    else:
        print("Status Code Error")


def get_carlist():
    url='https://www.lacentrale.fr/listing?makesModelsCommercialNames=RENAULT%3AZOE&regions=FR-PAC'
    r = requests.get(url)
    result_list=[]
    pageindex=1
    page_list=get_pageresults(url,str(pageindex))
    while len(page_list)!=0 :
        result_list.append(page_list)
        pageindex+=1
        page_list=get_pageresults(url,str(pageindex))
    return result_list


# Print github users ordered by stars
#def main(access_token):
def main():
    #dict_users={}
    #dict_users_mean={}

    #Get user list
    print(get_carlist())

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
