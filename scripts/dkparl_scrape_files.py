#!/usr/bin/env python

import os
from os.path import join
import sys

sys.path.append(os.path.join('..', 'modules'))
from dkparl_scraperfunctions import *

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
startdate = "20050101" ## format YYYYMMDD
enddate = "20071230" ## format YYYYMMDD


## Get resume links
resume_links = get_resume_links(startdate, enddate)


## Get resume
#resume_scraper(resume_links[0])


## Download files
log_name = f'resume_dl_{str(datetime.now().date())}.txt'

failed = []

for link in resume_links:
    try:
        resume_download(link, data_path = data_p)
    except (ConnectionError, AttributeError):
        failed.append(link)
    
    time.sleep(random.uniform(0.5, 1.5))

### Save log of failed urls
with open(join(log_p, log_name), 'w', encoding = 'utf-8') as f:
    for link in failed:
        f.write(link + '\n')