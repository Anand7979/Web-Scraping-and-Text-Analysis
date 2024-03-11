#Import different modules
import pandas as pd
import numpy as np
import nltk
from textblob import TextBlob
import re
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os
import json
import math



#Create empty list for store the values
dict_list=[]
score_list=[]
readability_list=[]
avg_words_and_complex_words_list=[]
word_and_syllable_count_list=[]
pronouns_and_word_length_list=[]

#Read data from excel file
data=pd.read_excel('D:/Blackcoffer1/Input.xlsx')


for i in data.index:
    # specify the URL ID of the article
    url_id = data['URL_ID'][i]  
    
    try:
        filename = os.path.join('D:/Blackcoffer1/articles/', f'{url_id}.txt')
        with open(filename, 'r',encoding='utf-8') as f:
            lines = f.readlines()
            content = ''.join(lines[1:])  # join all lines except the first one (title)
        
        #use regex for clean the text    
        content1=re.sub(r'\[\d+\]',"",content)  
        content2=re.sub(r'\[\w+\]',"",content1)
        content3=re.sub('[0-9]+',"",content2)

        with open('D:/Blackcoffer1/stopword_merged_file.txt', 'r') as file:
        # Read the contents of the file
            stopwords= file.read()
        #Tokenize the stopwords
        stopwords1=word_tokenize(stopwords)
        #Take only alphanum words
        stopwords2=[word for word in stopwords1 if word.isalnum()]

        with open('D:/Blackcoffer1/positive-words.txt', 'r') as file:
        # Read the contents of the file
            positivewords= file.read()
        positivewords1=word_tokenize(positivewords)
        positivewords2=[word for word in positivewords1 if word.isalnum()]

        with open('D:/Blackcoffer1/negative-words.txt', 'r') as file:
        # Read the contents of the file
            negativewords= file.read()
        negativewords1=word_tokenize(negativewords)
        negativewords2=[word for word in negativewords1 if word.isalnum()]

        #Store positive and negative words in dictionary
        word_dict={'positive':[],'negative':[]}
        for word in positivewords2:
            if word not in stopwords2:
                word_dict['positive'].append(word)        

        for word in negativewords2:
            if word not in stopwords2:
                word_dict['negative'].append(word)  
        dict_list.append(word_dict)  

        #Tokenize the sentences
        sentences=sent_tokenize(content3)
        total_sentences=len(sentences)
        words=word_tokenize(content3)
        words1=[w1 for w1 in words if w1.isalnum()]
        words2=[w2 for w2 in words1 if w2 not in stopwords2]
        total_words=len(words2)

        #Find positive score
        positive_score=0
        for wp in words2:
            if wp in word_dict['positive']:
                positive_score +=1 
        
        #Find negative score
        negative_score=0
        for wn in words2:
            if wn in word_dict['negative']:
                negative_score -=1
        negative_score=negative_score*(-1)

        #Find polarity score
        polarity_score=(positive_score - negative_score)/((positive_score + negative_score) + 0.000001)

        #Find subjectivity score
        subjectivity_score = (positive_score + negative_score)/ ((total_words) + 0.000001)
        
        #Store values in json format
        score = {'url_id':url_id, 'positive_score':positive_score , 'negative_score':negative_score, 'polarity_score': polarity_score,'subjectivity_score': subjectivity_score}

        score_list.append(score)  
        
        #Analysis of Readability
        average_sentence_length=math.ceil(total_words/total_sentences)

        #count complex word
        def count_syllables(word):
            vowels=['A','a','E','e','I','i','O','o','U','u']
            count=0
            for w in word:
                if w in vowels:
                    count +=1
            return count         

        # Count the number of syllables in each word
        syllables = [count_syllables(word) for word in words2]
        
        complex_words = sum(1 for syllable in syllables if syllable >2)

        #Percentage of Complex words 
        percentage_complex_words=complex_words/total_words

        #Fog Index 
        fog_index =0.4 * (average_sentence_length + percentage_complex_words )
        
        #Store values in json format
        readability = {'url_id':url_id, 'avg_sent_length': average_sentence_length,'percent_of_complex_words': percentage_complex_words,'fog_index': fog_index}

        readability_list.append(readability)  
        
        #Average Number of Words Per Sentence
        average_number_of_words_per_sentence = math.ceil(total_words / total_sentences)
        
        #Store values in json format
        avg_words_and_complex_words = {'url_id': url_id, 'avg_no_words_per_sent':average_number_of_words_per_sentence,'complex_word_count':complex_words }
        avg_words_and_complex_words_list.append(avg_words_and_complex_words)

        #Word Count
        #1.removing stopwords
        #2.remove punctuations
        words3=[word for word in words1 if word not in stopwords]
        total_words3=len(words3)
        

        #Syllable Count Per Word
        vowels=['A','a','E','e','I','i','O','o','U','u']
        syllables={}
        for word in words2:
            count=0
            syllables[word]=[]
            v=str.lower(word[:-3:-1])
            if v=='es'or v=='ed':
                pass
            else:
                for w in word:
                    if w in vowels:
                        count +=1
                syllables[word].append(count) 
        

        word_and_syllable_count = {'url_id': url_id, 'word_count': total_words3, 'syllable_count':syllables }
        word_and_syllable_count_list.append(word_and_syllable_count)  
            
        #Personal Pronouns
        def count_personal_pronouns(text):
            pronoun_count = re.compile(r'\b(I|we|my|ours|us)\b(?<!\bUS\b)')
            pronouns = pronoun_count.findall(text)
            return len(pronouns)

        text=content
        # Regular expression to match personal pronouns
        pronoun_regex = r'\b(I|we|my|ours|us)\b(?<!\bUS\b)'


        # Count the number of matches
        count =count_personal_pronouns(text)
        

        #Average Word Length
        sum_of_total_char=0
        for word in words2:
            l=len(word)
            sum_of_total_char +=l
            

        avg_word_len=math.ceil(sum_of_total_char/total_words)
        pronouns_and_word_length = {'url_id': url_id, 'personal_pronouns':count ,'word_avg_length': avg_word_len}

        pronouns_and_word_length_list.append(pronouns_and_word_length)
        print(i)
    except Exception as e:
        print('File Not Found')

#Convert list in dataframe
data1=pd.DataFrame(dict_list)

data2=pd.DataFrame(score_list)

data3=pd.DataFrame(readability_list)

data4=pd.DataFrame(avg_words_and_complex_words_list)

data5=pd.DataFrame(word_and_syllable_count_list)

data6=pd.DataFrame(pronouns_and_word_length_list)


#Merge all dataframes and make one dataframe
df_merge1=pd.merge(data2, data3, on = 'url_id', how = 'outer')

df_merge2=pd.merge(df_merge1, data4, on = 'url_id', how = 'outer')

df_merge3=pd.merge(df_merge2, data5, on = 'url_id', how = 'outer')

df_merge4=pd.merge(df_merge3, data6, on = 'url_id', how = 'outer')


#Convert dataframe into excel file 
df_merge4.to_excel('D:/Blackcoffer1/Output_Data_Structure.xlsx', index=False)
