import nltk
import pandas as pd
import numpy as np
import io
import os
import re
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.corpus import stopwords
import spacy
from textstat.textstat import textstatistics,legacy_round

def break_sentences(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    return list(doc.sents)

def word_count(text):
    #5
    sentences = break_sentences(text)
    words = 0
    for sentence in sentences:
        words += len([token for token in sentence])
    return words

def sentence_count(text):
    sentences = break_sentences(text)
    return len(sentences)


def avg_sentence_length(text):
    #2.1,3
    words = word_count(text)
    sentences = sentence_count(text)
    if sentences == 0:
        return 0
    else:
        average_sentence_length = float(words / sentences)
        return average_sentence_length

def syllables_count(word):
    #6
    return textstatistics().syllable_count(word)

def avg_syllables_per_word(text):
    syllable = syllables_count(text)
    words = word_count(text)
    if words == 0:
        return 0
    else:
        ASPW = float(syllable) / float(words)
        return legacy_round(ASPW, 1)

def difficult_words(text):
    #4
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    # Find all words in the text
    words = []
    sentences = break_sentences(text)
    for sentence in sentences:
        words += [str(token) for token in sentence]

    # difficult words are those with syllables >= 2
    # easy_word_set is provide by Textstat as
    # a list of common words
    diff_words_set = set()
    for word in words:
        syllable_count = syllables_count(word)
        if word not in nlp.Defaults.stop_words and syllable_count >= 2:
            diff_words_set.add(word)
    return len(diff_words_set)

def poly_syllable_count(text):
    count = 0
    words = []
    sentences = break_sentences(text)
    for sentence in sentences:
        words += [token for token in sentence]
    
    for word in words:
        syllable_count = syllables_count(word)
        if syllable_count >= 3:
            count += 1
    return count
def perc_diff_words(text):
    #2.2
    difficult_words_count = difficult_words(text)
    total_words = word_count(text)
    if total_words ==0:
        return 0
    else:
        return (difficult_words_count / total_words)*100

def gunning_fog(text):
    #2.3
    grade = 0.4 * (avg_sentence_length(text) + perc_diff_words(text))
    return grade
def personal_pronouns(text):
    #7
    pronouns=['i','me','my','mine','we','us','our','ours']
    count=0
    for word in text:
        if word in pronouns:
            count+=1
    return count
def avg_word_length(text):
    #8
    words = word_count(text)
    characters = len(text)
    if words == 0:
        return 0
    else:
        average_word_length = float(characters / words)
        return average_word_length

df = pd.read_excel('output.xlsx', index_col='URL_ID')

stop_words = set(stopwords.words('english'))
directory='ScrapedData'
files = os.listdir(directory)
for file in sorted(files):
    f_name = os.path.join(directory, file)
    new_name=f_name.split('.')[0]+'_cl.txt'
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
    appendFile.close()

    text=open(new_name,'r',encoding='utf-8')
    text=text.read()

    avg_sent_len=avg_sentence_length(text)
    per_com_words=perc_diff_words(text)
    fog_index=gunning_fog(text)
    avg_word_len=avg_word_length(text)
    com_word_count=difficult_words(text)
    wor_count=word_count(text)
    syllable_per_word=avg_syllables_per_word(text)
    pers_pronouns=personal_pronouns(text)
    avg_word_len=avg_word_length(text)

    try:
        df.loc[int(file.split('.')[0]), 'AVG SENTENCE LENGTH'] = avg_sent_len
        df.loc[int(file.split('.')[0]), 'PERCENTAGE OF COMPLEX WORDS'] = per_com_words
        df.loc[int(file.split('.')[0]), 'FOG INDEX'] = fog_index
        df.loc[int(file.split('.')[0]), 'AVG NUMBER OF WORDS PER SENTENCE'] = avg_sent_len
        df.loc[int(file.split('.')[0]), 'COMPLEX WORD COUNT'] = com_word_count
        df.loc[int(file.split('.')[0]), 'WORD COUNT'] = wor_count
        df.loc[int(file.split('.')[0]), 'SYLLABLE PER WORD'] = syllable_per_word
        df.loc[int(file.split('.')[0]), 'PERSONAL PRONOUNS'] = pers_pronouns
        df.loc[int(file.split('.')[0]), 'AVG WORD LENGTH'] = avg_word_len
        df.to_excel('output.xlsx')
    except KeyError:
        df = pd.concat([df, pd.DataFrame([[avg_sent_len, per_com_words, fog_index, avg_word_len, com_word_count, wor_count, syllable_per_word, pers_pronouns, avg_word_len]], 
                                         columns=['AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX', 'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 'WORD COUNT', 'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH'], 
                                         index=[int(file.split('_')[0])])])
        df.to_excel('output.xlsx')

    
    
