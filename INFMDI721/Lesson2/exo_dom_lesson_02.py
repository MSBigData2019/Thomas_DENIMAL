#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re



#* les ventes au quartier à fin décembre 2018
#* le prix de l'action et son % de changement au moment du crawling
#* le % Shares Owned des investisseurs institutionels
#* le dividend yield de la company, le secteur et de l'industrie



COM = 'DANONE'
root_u = 'http://www.reuters.com'

r = requests.get(root_u+"/finance/stocks/lookup?search="+COM+"&searchType=Companies")
soup = BeautifulSoup(r.text, 'html.parser')

#print(soup.find_all('a'))
#print(soup.prettify())

if soup.find(class_="search-companies-count") is None:
    print("no results")
    exit(0)
else:
    print(soup.find(class_="search-companies-count").get_text())

#search_result=soup.find_all(class_ = "search-table-data").find_all(class_ = "stripe")
search_result=soup.find_all(class_ = "stripe")

for x in search_result:
    match=re.match(r"parent.location=\'(.*\.PA)\'.*",x['onclick'])
    if match :
        matched_u=match.group(1)
        result_u=matched_u.replace('overview','financial-highlights')


r = requests.get(root_u+result_u)

soup = BeautifulSoup(r.text, 'html.parser')


for x in soup.find_all(id = "sectionHeader"):
    for y in x.find_all(class_ = "sectionQuote nasdaqChange"):
        section = y.find('div', attrs={'class': 'sectionQuoteDetail'})
        for span in section.find_all('span', recursive=False):
                print(span.get_text())
    for z in x.find_all(class_ = "sectionQuote priceChange"):
        section = z.find('div', attrs={'class': 'sectionQuoteDetail'})
        for span in section.find_all('span', recursive=False):
                print(span.get_text())


for x in soup.find_all(class_ = "module" ):
    for y in x.find_all(class_ = "moduleHeader"):
        print(y.get_text())
    for z in x.find_all(class_ = "moduleBody"):
        table = z.find('table', attrs={'class':'dataTable'})
        if table is not None:
            table_body = table.find('tbody')

            data = []
            dath = []
            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele]) # Get rid of empty values
                colh = row.find_all('th')
                colh = [ele.text.strip() for ele in colh]
                dath.append([ele for ele in colh if ele]) # Get rid of empty values
            print(dath[0])
            for i in data:
                print(i)
            print("\n****************************************")






#print(search_result)

#Find link to company using regex - PARIS EXCHANGE only
#regex_result = re.match(r'.*onclick="parent.location=\'(.*\.PA)\'.*',search_result)
#regex_result = re.match(r'.*(.PA).*',search_result,re.MULTILINE)
#print(regex_result.group(0))



#faire un map avec lambda pour filtrer


#request post sur le site
#faire une fonction qui prend une query et
#rend une liste de liens ( utiliser map
#specific_class = "c-article-flux_title"
#map(lambda x: x.attrs['href'],soup.find_all("a",class_=specific_class)))

#FACTORISER SON CODE


#scroller sur le site avec le chrome dev tool
#chercher les class specifiques

