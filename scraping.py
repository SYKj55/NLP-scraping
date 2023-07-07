import requests
from bs4 import BeautifulSoup
import pandas as pd
url='https://insights.blackcoffer.com/ai-in-healthcare-to-improve-patient-outcomes/'
page=requests.get(url)
soup=BeautifulSoup(page.content,'html.parser')
#print(soup.prettify())
f = open("37.txt", "w",encoding='utf-8')
title=soup.find_all('h1')
for i in title:
    f.write(i.text)
    f.write("\n")

para=soup.find_all('div',class_='tdb-block-inner td-fix-index')
#print(para)
for i in para:
    par=i.find_all('p')
    for j in par:
        f.write(j.text)
        f.write("\n")