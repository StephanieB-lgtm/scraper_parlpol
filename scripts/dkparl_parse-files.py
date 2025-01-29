#!/usr/bin/env python

import os
from os.path import join
import sys
from bs4 import BeautifulSoup as bs
import json
import re

module_dir = join("/work/scraper_parlpol", "modules")

sys.path.append(module_dir)

from dkparl_parserfunctions import get_agendaitems
from dkparl_parserfunctions import parse_parlminutes

## Paths
data_p = join("/work/scraper_parlpol", "data")
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

    with open(filepath, 'r', encoding='utf-8') as f:
        parlminutes = f.read()

    try:
        minutes_parsed = parse_parlminutes(parlminutes, file)
        parsed_files.append(minutes_parsed)
    except:
        failed.append(filepath)
    
    progress = "|{0}| {1:.2f} %".format(("="*int(c/len(files) * 50)).ljust(50), c/len(files) * 100)
    print(progress, end = "\r")

## Store data as JSON - failed files as newline separated txt
file_out = 'dkparl_parsed_20221216.json'
failed_out = 'files_failed.txt'

file_out_p = join(data_out_p, file_out)
failed_out_p = join(data_out_p, failed_out)

with open(file_out_p, 'w', encoding='utf-8') as f:
    json.dump(parsed_files, f, ensure_ascii=False)

with open(failed_out_p, 'w', encoding='utf-8') as f:
    for line in failed:
        f.write(line + '\n')
        
#VERIFICATION OF VERSION CONTROL