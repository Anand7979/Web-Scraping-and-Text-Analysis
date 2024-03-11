#Import all modules or libraries
import pandas as pd
import requests
import os
from bs4 import BeautifulSoup


#Read data from excel file
data=pd.read_excel('D:/Blackcoffer1/Input.xlsx')


#Use for loop for iterate url
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.; Win64; x64) AppleWebKit/537.6 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
for i in data.index:
    # specify the URL of the article
    url = data['URL'][i]
    
    # send a GET request to the URL
    try:
        response=requests.get(url,headers=headers)
        if response.status_code==200:
            # create a BeautifulSoup object from the HTML content
            webpage=response.text
            soup=BeautifulSoup(webpage,'lxml')
            
            # find the article title and remove any whitespace
            title=soup.find('h1').text.strip()
            
            # find the article text and remove any unwanted elements
            directory = 'D:/Blackcoffer1/articles'
            article_text = ''
            for div in soup.find_all('div',class_=['td-post-content tagdiv-type', 'tdb-block-inner td-fix-index']) :
                #if not paragraph.find('span') and not paragraph.find('a') :
                paragraph = div.find_all(['p','li','h2','h3','h4','h5'])
                for para in paragraph :
                    anchor=para.find_all('a')
                    for an in anchor:
                        an.decompose()
                    article_text += para.text + '\n' 
        
            url_id=data['URL_ID'][i]
            # save the article title and text to a text file
            filename = os.path.join(directory, f'{url_id}.txt')
            with open(filename, 'w',encoding='utf-8') as f:
                f.write(title + '\n\n')
                f.write(article_text)
                
    except requests.exceptions.RequestException:
        # If an exception occurs, skip the URL and continue to the next one
        continue           
