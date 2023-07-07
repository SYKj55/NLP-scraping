import nltk
import pandas as pd
import numpy as np
import io
import os
import re
from nltk.tokenize import word_tokenize
import xlwt
import xlrd
from xlutils.copy import copy

directory1 = 'StopWords'
files1 = os.listdir(directory1)
stop_words = []
for file1 in files1:
    f_name1 = os.path.join(directory1, file1)
    f1 = open(f_name1, "r")
    words = f1.read().split('\n')
    stop_words.extend(words)

neg_words = []
pos_words = []
fn = open(r'MasterDictionary\negative-words.txt', 'r')
line1 = fn.read().split('\n')
for r in line1:
    if r not in stop_words:
        neg_words.append(r)
fn.close()
fp = open(r'MasterDictionary\positive-words.txt', 'r')
line2 = fp.read().split('\n')
for line in line2:
    if line not in stop_words:
        pos_words.append(line)
fp.close()
print(len(neg_words))
print(len(pos_words))

directory = 'CleanedData'
files = os.listdir(directory)

df = pd.read_excel('output.xlsx', index_col='URL_ID')

for file in sorted(files):
    f_name = os.path.join(directory, file)
    f = open(f_name, "r", encoding='utf-8')
    tokens = word_tokenize(f.read())
    # print(tokens)
    p_score = 0
    n_score = 0
    for word in tokens:
        if word in pos_words:
            p_score += 1
        elif word in neg_words:
            n_score += 1
    print(p_score)
    print(n_score)
    pol_score = (p_score - n_score) / ((p_score + n_score) + 0.000001)
    print(pol_score)
    sub_score = (p_score + n_score) / (len(tokens) + 0.000001)
    print(sub_score)

    #print(df)
    try:
        df.loc[int(file.split('_')[0]), 'POSITIVE SCORE'] = p_score
        df.loc[int(file.split('_')[0]), 'NEGATIVE SCORE'] = n_score
        df.loc[int(file.split('_')[0]), 'POLARITY SCORE'] = pol_score
        df.loc[int(file.split('_')[0]), 'SUBJECTIVITY SCORE'] = sub_score
        df.to_excel('output.xlsx')
    except KeyError:
        df = pd.concat([df, pd.DataFrame([[p_score, n_score, pol_score, sub_score]], 
                                         columns=['POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 'SUBJECTIVITY SCORE'], 
                                         index=[int(file.split('_')[0])])])
        df.to_excel('output.xlsx')
