## Log for development of DKParl scraper

#### 2022-12-05
- Develop first version of scraper for downloading resumes/minutes from Danish Parliament (https://www.ft.dk/da/dokumenter/dokumentlister/referater)
    - `modules/dkparl_scraperfunctions.py`
- Downloading all resumes from 2007-10-02 to 2022-12-05 as HTML using script `dkparl_scrape_files.py`
- NOTE: Resumes before 2007-10-02 are stored as pdf - *need download function for pdf files*


#### 2022-12-13
- Starting development on parser for html files

#### 2022-12-16
- Parsing html files 2007-2022
- Failed added to txt file in data directory
- NOTE: *Add filename to data*