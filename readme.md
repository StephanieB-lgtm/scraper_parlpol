# DKParl Minutes Scraper

Scraper for collecting minutes from meeting in the Danish Parliament (Folketinget).

The scraper collects minutes from the following site: https://www.ft.dk/da/dokumenter/dokumentlister/referater

*NOTE*: This repository is in active development.

## How it works

The scraper uses the query parameters of the site to find minutes within a given time frame. All relevant links are then retireved and then downloaded as HTML to a specified data folder. 

The repo also contains function for parsing the minutes into a combined JSON records data file. 

The scraper is set up to be run from the script `dkparl_scrape_files.py` in the `scripts` folder. The relevant parameters will have to be changed directly in the script by changing the relevant variables (`startdate`, `enddate`, `data_p`, `log_p`)
- `startdate` (string): Date written as string in format YYYYMMDD marking lower bound of the date range to include. This is parsed as a query parameter to the main URL.
- `enddate` (string): Date written as string in format YYYYMMDD marking upper bound of the date range to include. This is parsed as a query parameter to the main URL.
- `data_p` (path to directory): Directory used to write HTML files to.
- `log_p` (path to directory): Directory used to dump log files. The only "log" file produced is a txt of files which for one reason or another was not possible to scrape.

### Parsing files

The script `dkparl_parse-files.py` is used for parsing the HTMLs into a JSON records file. The relevant parameters will have to be changed directly in the script by changing the relevant variables (`data_raw_p`, `data_out_p`, `file_out`, `failed_out`).
- `data_raw_p` (path to directory): Directory containing the HTML files of the minutes.
- `data_out_p` (path to directory): Directory where JSON records file is written to.
- `file_out` (string/filename): Filename used for the JSON records file.
- `failed_out` (string/filename): Filename used for txt dump of files that failed to parse (written to the the `data_out_p` directory).

## Contents

The repo is split into two main folders: `modules` and `scripts`.

### `modules`: Modules containing the scraper and parser functions
- `dkparl_parserfunctions.py`: Functions for parsing to JSON records file.
- `dkparl_scraperfunctions.py`: Functions for scraping the minutes HTML files.

### `scripts`: Scripts for running the scraper and parser functions
- `dkparl_data-explore.py`: Small code snippets for inspecting the data.
- `dkparl_parse-files.py`: Script for using the parser functions.
- `dkparl_scrape_files.py`: Script for using the scraper functinos.