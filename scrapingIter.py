from bs4 import BeautifulSoup
import requests 
from urllib import request
import os
import pandas as pd
import re
df=pd.read_excel('input.xlsx')
mydict=df.to_dict('records')
#print(mydict)
#print(mydict[0])

directory='ScrapedData'
for i in mydict[1:]:
    url=i['URL']
    print(url)
    page=requests.get(url)
    soup=BeautifulSoup(page.content,'html.parser')
    #print(soup.prettify())
    f_name=os.path.join(directory,str(i['URL_ID'])+'.txt')
    #name=i['URL_ID']+'.txt'
    f = open(f_name, "w",encoding='utf-8')
    title=soup.find_all('h1')
    for i in title:
        f.write(i.text)
        f.write("\n")
    para=soup.find_all('div',class_='td-post-content tagdiv-type')
    #print(para)
    for i in para:
        par=i.find_all('p')
        for j in par:
            f.write(j.text)
            f.write("\n")
    f.close()


    