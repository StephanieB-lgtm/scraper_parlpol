#!/usr/bin/env python

import os
from os.path import join
from bs4 import BeautifulSoup as bs
import requests
import json
import re
import datetime
import random
import time
from urllib.parse import urljoin
import re


## Search url formats
SEARCH_URL_FORMAT = 'https://www.ft.dk/da/dokumenter/dokumentlister/referater?startDate={}&endDate={}&pageSize=200'
PAGE_URL_FORMAT = '{}&pageNumber={}'


## Function for getting resume links based on start and end date
def get_resume_links(startdate, enddate, SEARCH_URL_FORMAT = SEARCH_URL_FORMAT, PAGE_URL_FORMAT = PAGE_URL_FORMAT):

    ### Set search url
    search_url = SEARCH_URL_FORMAT.format(startdate, enddate)

    ### Results
    r = requests.get(search_url, verify = False) # disabling SSL check
    soup = bs(r.text, 'html.parser')

    ### Number of pages
    pagination_soup = soup.find('ul', class_ = 'pagination pagination-centered text-center')

    ### Check for more than one page
    if pagination_soup is not None:
        pagination = pagination_soup.get_text()
        numbers = [int(number) for number in re.findall(r'\d{1,2}', pagination)]
        no_pages = max(numbers)
    else:
        no_pages = None

    if no_pages is None:
        more_pages = False
    else:
        more_pages = True
        no_pages = int(no_pages)
    
    ### Create pagenumbers (how many pages of results)
    if more_pages:
        pagenumbers = list(range(2, no_pages+1)) # Excuding first page as it corresponds to search_url


    ### Get resume links
    resume_rows = soup.find('div', class_ = 'row search-result-container').find('table').find_all('tr')[1:]
    resume_links = [col.find('td').find('a')['href'] for col in resume_rows if col.find('td').find('a') is not None]
    #resume_links = [link.find('a')['href'] for link in soup.find_all('td', attrs = {'data-title': 'Mødedato, -tid og samling'})]

    


    if more_pages:
        for pagenumber in pagenumbers:
            
            page_url = PAGE_URL_FORMAT.format(search_url, str(pagenumber))
            r = requests.get(page_url, verify = False)
            soup = bs(r.text, 'html.parser')
            
            try:
                page_rows = soup.find('div', class_ = 'row search-result-container').find('table').find_all('tr')[1:]
                page_links = [col.find('td').find('a')['href'] for col in resume_rows if col.find('td').find('a') is not None]
            except TypeError:
                raise TypeError(f'Could not reach page {pagenumber}.')
            #page_links = [link.find('a')['href'] for link in soup.find_all('td', attrs = {'data-title': 'Mødedato, -tid og samling'})]
            
            resume_links = resume_links + page_links

            time.sleep(random.uniform(0.5, 1.5))
            
    resume_links = [urljoin(search_url, resume_link) for resume_link in resume_links]


    ### Return links
    return(resume_links)


## Resume download
def resume_download(url, data_path):

    ### check for file in data path
    filename = re.search('(?s:.*)((?<=\/).*\.htm)', url).group(1)

    if filename in os.listdir(data_path):
        return

    ### send request - 5 retries
    i = 5

    while i > 0:
        try:
            r = requests.get(url, verify = False)
            r.encoding = r.apparent_encoding

            break
        except:
            i = i - 1
            time.sleep(random.uniform(0.5, 1.5))
    
    if i == 0:
        raise ConnectionError(f'Could not reach {url}. Max retries exceeded.')
        return

    ### save to data path
    content = r.text

    with open(join(data_path, filename), 'w', encoding = 'utf-8') as f:
        f.write(content)


## Resume scraper
def resume_scraper(url):
    
    ### regexes
    agendaregex = re.compile('Dagsorden.*')
    
    ### send request and create soup object
    r = requests.get(url, verify = False)
    r.encoding = r.apparent_encoding
    soup = bs(r.text, 'html.parser')
    
    ### look for title (based on html class)
    try:
        title = soup.find('p', class_ = 'Titel').get_text()
    except AttributeError:
        title = ''

    ### look for subtitle (based on html class)        
    try:
        subtitle = soup.find('p', class_ = 'UnderTitel').get_text()
    except AttributeError:
        subtitle = ''
    
    ### look for agenda (based on regex)
    try:
        agenda = '\n'.join([tag.get_text() for tag in soup.find_all("p", class_ = agendaregex)])
    except AttributeError:
        agenda = ''    
    
    ### create dictionary for resume
    resume_dict = {}
    resume_dict['url'] = url
    resume_dict['title'] = title
    resume_dict['subtitle'] = subtitle
    resume_dict['agenda'] = agenda
    resume_dict['text'] = soup.get_text()
    
    ### return dictionary
    return(resume_dict)