#!/usr/bin/env python

import os
from os.path import join
import sys

sys.path.append(os.path.join('..', 'modules'))
from dkparl_scraperfunctions import get_minutes_links, minutes_download, minutes_scraper

from bs4 import BeautifulSoup as bs
import requests
import json
import re
import datetime
import random
import time
from urllib.parse import urljoin
import re
from datetime import datetime


## Set paths
data_p = join('..', 'data', 'raw')
log_p = join('..', 'log')


## Set dates
startdate = "20070101" ## format YYYYMMDD
enddate = "20221101" ## format YYYYMMDD


## Get minutes links
minutes_links = get_minutes_links(startdate, enddate)


## Get minutes
#minutes_scraper(minutes_links[0])


## Download files
log_name = f'minutes_dl_{str(datetime.now().date())}.txt'

failed = []

for link in minutes_links:
    try:
        minutes_download(link, data_path = data_p)
    except (ConnectionError, AttributeError):
        failed.append(link)
    
    time.sleep(random.uniform(0.5, 1.5))

### Save log of failed urls
with open(join(log_p, log_name), 'w', encoding = 'utf-8') as f:
    for link in failed:
        f.write(link + '\n')