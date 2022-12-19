#!/usr/bin/env python

import os
from os.path import join
import sys
from bs4 import BeautifulSoup as bs
import json
import re

## Paths
data_p = join('/work', '214477', 'scraper_parlpol', 'data')
data_raw_p = join(data_p, 'raw')
data_out_p = join(data_p)

with open(join(data_p, 'dkparl_parsed_20221216.json'), encoding='utf-8') as f:
    dkparl = json.load(f)

dkparl_validate = []

for entry in dkparl:
    if len(entry.get('Items')) != len(entry.get('AgendaShort').split('\n')):
        dkparl_validate.append(entry)


dkparl_validate[0].keys()

len(dkparl_validate[150].get('Items')) 
len(dkparl_validate[150].get('AgendaShort').split('\n'))

dkparl_validate[150].get('Items')['1'].get('ItemTitle')