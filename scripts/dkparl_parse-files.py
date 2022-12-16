#!/usr/bin/env python

import os
from os.path import join
import sys
from bs4 import BeautifulSoup as bs
import json
import re

sys.path.append(join('/work', '214477', 'scraper_parlpol', 'modules'))

from dkparl_parserfunctions import get_agendaitem
from dkparl_parserfunctions import parse_parlresume

## Paths
data_p = join('/work', '214477', 'scraper_parlpol', 'data')
data_raw_p = join(data_p, 'raw')
data_out_p = join(data_p)

## List of datafiles
files = os.listdir(data_raw_p)
fileps = [join(data_raw_p, file) for file in files]

## List for parsed files
parsed_files = []

## Parse files
failed = []
for filep in fileps:

    with open(filep, 'r') as f:
        parlresume = f.read()

    try:
        resume_parsed = parse_parlresume(parlresume)
        parsed_files.append(resume_parsed)
    except:
        failed.append(filep)

file_out = 'dkparl_parsed_20221216.json'
