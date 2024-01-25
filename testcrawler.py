# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

import pyodbc 

def crawler(start_url,max_pages=100):
   
    
   conn_str = (
       r'DRIVER={SQL Server};'
       r'SERVER=(local)\SQLEXPRESS;'
       r'DATABASE=search_data;'
       r'Trusted_Connection=yes;'
   )
   conn = pyodbc.connect(conn_str)
   
   c=conn.cursor()
   
             
   c.execute('''
              
             if not exists (select * from sysobjects where name='pages' and xtype='U')
             create table pages (
          
                     id int NOT NULL IDENTITY,
                     url TEXT,
                     content TEXT
                     )
              ''')
              
   conn.commit()
   url_frontier= [start_url]

   visited_pages= set()
   while url_frontier and len(visited_pages)<max_pages:
       
          url=url_frontier.pop(0)
       
          if url in visited_pages:
              continue
       
          print(f'Crawling {url}')
          
          response=requests.get(url)
          if response.status_code !=200:
             continue 
          print(response.content)  
          soup= BeautifulSoup(response.content,'html.parser')
    
            
          c.execute('INSERT INTO pages(url,content) VALUES (?,?)',(url,str(soup)))
          conn.commit()
       
          links=soup.find_all('a')
          
          for link in links:
              href= link.get("href")
              if href and 'http' in href and href not in visited_pages:
                  url_frontier.append(href) 
          
          visited_pages.add(url)   
   conn.close()
   print("Crawling Completed")
       
seed_urls=["http://www.bbc.co.uk/news/politics/eu-regions/E15000004"]
    
for url in seed_urls:
        crawler(url,50)
     