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

## List for parsed files
parsed_files = []

## Parse files
failed = []
for c, file in enumerate(files, start=1):

    filepath = join(data_raw_p, file)

    with open(filep, 'r') as f:
        parlresume = f.read()

    try:
        resume_parsed = parse_parlresume(parlresume, file)
        parsed_files.append(resume_parsed)
    except:
        failed.append(filep)
    
    progress = "|{0}| {1:.2f} %".format(("="*int(c/len(fileps) * 50)).ljust(50), c/len(fileps) * 100)
    print(progress, end = "\r")

## Store data as JSON - failed files as newline separated txt
file_out = 'dkparl_parsed_20221216.json'
failed_out = 'files_failed.txt'

file_out_p = join(data_out_p, file_out)
failed_out_p = join(data_out_p, failed_out)

with open(file_out_p, 'w', encoding='utf-8') as f:
    json.dump(parsed_files, f)

with open(failed_out_p, 'w', encoding='utf-8') as f:
    for line in failed:
        f.write(line + '\n')

