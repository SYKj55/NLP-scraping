import io
import os
import pandas as pd
import re

from nltk.tokenize import word_tokenize

directory1='StopWords'
files1=os.listdir(directory1)
stop_words=[]
for file1 in files1:
    f_name1=os.path.join(directory1,file1)
    f1=open(f_name1,"r")
    words=f1.read().split('\n')
    stop_words.extend(words)


print(len(stop_words))
directory='ScrapedData'
files = os.listdir(directory)
for file in sorted(files):
    f_name = os.path.join(directory, file)
    new_name=f_name.split('.')[0]+'_cleaned.txt'
    print(new_name)
    f = open(f_name, "r",encoding='utf-8')
    lines = f.read()
    #print(lines)
    #word=lines.split()
    #print(word)
    line=lines.split()
    appendFile = open(new_name,'w',encoding='utf-8')
    for w in line:
        if w not in stop_words:
            appendFile.write(' '+w)
            #print(w)
    print(len(new_name))
    



        
    

