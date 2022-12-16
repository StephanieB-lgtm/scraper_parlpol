#!/usr/bin/env python

from bs4 import BeautifulSoup as bs
import re

## Function for getting agenda item info
def get_agendaitem(parlsoup, itemno):

    item_dict = {}

    itemno = str(itemno)
    
    ### Getting all tags separated by <meta name="ItemNo"/>
    agendaitems = []

    item_start = soup.find('meta', attrs = {'name': 'ItemNo', 'content': itemno})
    item_tags = item_start.next_siblings # Using generator object

    current_tag = next(item_tags)
    metaname = None

    while metaname != 'ItemNo': # Continue adding tags until next agendaitem
        if str(current_tag) != '\n': # Skip newlines
            agendaitems.append(current_tag)
            
        current_tag = next(item_tags)
        try:
            metaname = current_tag.get('name')
        except AttributeError:
            metaname = None

    ### Join tags to new soup
    item_soup = bs(''.join([str(agendaitem) for agendaitem in agendaitems]))

    ### Info from soup object to dicionary
    item_dict['ItemNo'] = itemno
    item_dict['ItemTitle'] = item_soup.find('meta', attrs = {'name': 'ShortTitle'}).get('content')
    item_dict['ItemStartDateTime'] = item_soup.find('meta', attrs = {'name': 'StartDateTime'}).get('content')
    item_dict['EndDateTime'] = item_soup.find_all('meta', attrs = {'name': 'EndDateTime'})[-1].get('content')
    item_dict['ItemText'] = '\n'.join([texttag.get_text(strip = True) for texttag in item_soup.find_all('p', class_ = re.compile(r'^Tekst'))])

    return(item_dict)

## Function for parsing parlresume
def parse_parlresume(parlresume):
    ## Empty dict for all info in document/resume
    parldict = {}

    ## Convert to soup
    soup = bs(parlresume, 'html.parser')

    ## Extract title and subtitle
    parldict['Title'] = soup.find('p', class_ = 'Titel').get_text()
    parldict['SubTitle'] = soup.find('p', class_ = 'UnderTitel').get_text()

    ## Meta information in begining of document
    metas = soup.find_all('meta')

    ### Add meta information in beginning using name attribute as key
    for meta in metas:
        if meta.get('name') == 'Start MetaMeeting':
            continue

        if meta.get('name') == 'End MetaMeeting':
            break

        key = meta.get('name')
        value = meta.get('content')

        parldict[key] = value

    ## Full agenda as a string
    parldict['AgendaLong'] = '\n'.join([agendasoup.get_text(strip = True) for agendasoup in soup.find_all('p', class_ = 'DagsordenTekst')])

    ## Agenda as list 
    agendap_soup = soup.find_all('meta', attrs = {'name': 'ShortTitle'})

    agendaps = []
    for agendap in agendap_soup:
        if agendap.get('content') == 'Punkt 0': # Ignores 'meddelelser fra formanden'
            continue

        agendapoint = agendap.get('content')

        agendaps.append(agendapoint)

    parldict['AgendaShort'] = '\n'.join(agendaps) # Stored as string - separate at newline to get as list

    ## Extract item numbers
    itemnos = list(set([itemnotag.get('content') for itemnotag in soup.find_all('meta', attrs = {'name': 'ItemNo'})]))
    itemnos.sort()
    itemnos = itemnos[1:] # NOTE: Skips 0 - 'meddelelser fra formanden

    ## Add items to dictionary using function
    parldict_items = {}
    for itemno in itemnos:
        parldict_items[itemno] = get_agendaitem(soup, itemno)

    parldict['Items'] = parldict_items

    return(parldict)