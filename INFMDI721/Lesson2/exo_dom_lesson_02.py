#!/usr/bin/env python3

import requests
import pandas as pd
import sys
from bs4 import BeautifulSoup
import re


#Function to cleanup string of spaces, tab, and other char
def clean_string(string):
    return string.strip().replace('\n', '').replace('\t', '').replace(u'\xa0', u' ')



#Make research on reuters for a company
#return the corresponding uri
def company_url(com):
    #parameters
    root_u = 'http://www.reuters.com'
    options_u='&comSortBy=marketcap&searchType=any'

    #make a research
    r = requests.get(root_u+"/finance/stocks/lookup?search="+com+options_u)
    soup = BeautifulSoup(r.text, 'html.parser')


    #Retrieve results if none exit
    nbr_results = soup.find(class_="search-companies-count")
    if nbr_results is None:
        print("unknow company or no results")
        sys.exit(0)


    #Parse research results
    table = nbr_results.find_parent().find('table', attrs={'class': 'search-table-data'})

    if table is not None:
        for x in table.find_all(class_="stripe"):
            match = re.match(r"parent.location=\'(.*\.PA)\'.*", x['onclick'])
            if match:
                matched_u = match.group(1)
                result_u = matched_u.replace('overview', 'financial-highlights')

    return root_u+result_u




#Fonction qui retourne un dictionnaire contenant
#l'ensemble des donnees des tables
def table_todf(table):
    tab = []
    col = []
    dico={}
    if table is not None:
        table_body = table.find('tbody')

        #Je loop sur lensemble des tr de la table sauf le premier qui a la structure

        l_tr = table_body.find_all('tr')

        for tr in l_tr:
            l_th = tr.find_all('th')
            for th in l_th:
                col.append([clean_string(th.get_text())])

        if len(col) == 0:
            for tr in l_tr:
                h = clean_string(tr.find('td',attrs={'class':None}).get_text())
                d = [clean_string(tr.find('td',attrs={'class':['data']}).get_text())]
                dico[h]=d
            return pd.DataFrame(data=dico)



        for tr in l_tr:
        #Je loop sur les data
            l_td = tr.find_all('td',attrs={'class':None})

            for td in l_td:
                elem=clean_string(td.get_text())
                if len(elem) !=0 :
                    tab.append(elem)
        dico['METADATA']=tab



        tab=[]
        for tr in l_tr:
        #Je loop sur les data
            l_td = tr.find_all('td',attrs={'class':['data']})

            for td in l_td:
                elem=clean_string(td.get_text())
                if len(elem) !=0:
                    tab.append(elem)
            if len(tab) !=0:
                for i in range(1, len(col)):
                    key = col[i][0]
                    if key in dico:
                        dico[key].append(tab[i-1])
                    else:
                        dico[key]=[tab[i-1]]
                tab=[]

    return pd.DataFrame(data=dico)



#Retrieve all dataframes in all modules
def modules_df(soup):
    for html_col in  soup.find(id="content").find_all(class_="sectionColumns"):

        #Dictionnaire de dataframe
        df_dico={}
        #On parcourt ensuite tous les modules
        for module in html_col.find_all(class_="module"):
            #Pour un module je recupere son header
            tag_header = module.find(class_="moduleHeader")
            header = clean_string(tag_header.get_text())

            #je me positionne au niveau du body
            body = module.find(class_="moduleBody")

            #Je recupere le footnote qui servira de commentaire
            footnote = body.find(class_="footnote")

            #Si elle existe Je me positionne au niveau de la table des donnees du module
            table = module.find('table', attrs={'class': 'dataTable'})


            #add dataframe to dict
            df_dico[header]=table_todf(table)
    return df_dico


#Find info on nasdaqchange & price
def get_nasdaq(soup):
    #Find info on nasdaqchange & price in header
    h_section = soup.find(id = "headerQuoteContainer")

    nasdaq=h_section.find(class_ = "sectionQuote nasdaqChange")
    price=h_section.find(class_ = "sectionQuote priceChange")


    #n_data=[]
    #p_data=[]

    #Search for info in nasdaq
    #Market place
    mkt_place = clean_string(nasdaq.find(class_= "nasdaqChangeHeader").get_text().split('on')[1])
    #Nasdaq change time
    n_time = clean_string(nasdaq.find(class_= "nasdaqChangeTime").get_text())

    #Retrieve nasdaq price
    nasdaq_price=''
    for span in nasdaq.find_all("span",class_=None):
        nasdaq_price=nasdaq_price+clean_string(span.get_text())

    #Retrieve nasdaq change %
    nasdaq_chg=clean_string(price.find(class_="valueContentPercent").get_text())
    return "Prix Action : "+nasdaq_price+" %chg :"+nasdaq_chg


def company_info(com):
    r = requests.get(company_url(com))
    soup = BeautifulSoup(r.text, 'html.parser')


    #Find info on company
    #s_cname, l_cname : short and long company name
    raw_title = clean_string(soup.find(id = "sectionTitle").get_text())
    match = re.match(r"(.*)\((.*)\)", raw_title)
    l_cname=match.group(1)
    s_cname=match.group(2)

    #Affichage nom de la compagnie
    print("NOM DE LA COMPAGNIE :"+l_cname)

    #Affichage prix action
    print(get_nasdaq(soup))

    dfs=modules_df(soup)

    #Affichage Inst Holders
    print(dfs['Institutional Holders'])

    print("\n")

    #Affichage ventes quarter
    df=dfs['Consensus Estimates Analysis']
    print(df.head(1))

    print("\n")

    #Affichage dividendes
    df=dfs['Dividends']
    print(df.head(1))

    print("\n")

# Pour Airbus,LVMH,Danone
#* les ventes au quartier à fin décembre 2018
#* le prix de l'action et son % de changement au moment du crawling
#* le % Shares Owned des investisseurs institutionels
#* le dividend yield de la company, le secteur et de l'industrie
def main():
    company_info('AIRBUS')
    company_info('LVMH')
    company_info('DANONE')

if __name__ == "__main__":
        # execute only if run as a script
            main()
