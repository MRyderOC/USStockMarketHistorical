import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import requests
import datetime
import logging


def createLogger(name: str, fmt: str ='[%(name)s](%(asctime)s): %(levelname)s \t %(message)s', 
                dateformat: str ='%b/%d/%y %I:%M:%S %p', path: str ='') -> logging.getLogger:
    '''
    Create a logger for further use
    '''
    # Making log object for further use and .log file
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    SH = logging.StreamHandler() # Making a Stream Handler for shell usage
    SH.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt=fmt, datefmt=dateformat)
    SH.setFormatter(formatter) # Define the output format for Stream Handler
    logger.addHandler(SH)
    if path:
        logging.basicConfig(filename=path, level=logging.INFO,
                    format=fmt, datefmt=dateformat) # Configuration for .log file
    return logger


def now(logger: logging.getLogger = None) -> str:
    '''
    Return the current time as str
    '''
    l = str(datetime.datetime.today()).split() # get the time
    l[1] = l[1].split('.')[0] # reformat the h:m:s.ml to h:m:s
    logger.info(f"Current time is {'T'.join(l)}") if logger else None
    return 'T'.join(l)


def scrapeLastPageNumber(logger: logging.getLogger =None) -> int:
    '''
    Find the last page in stock screener to use as a dependency for scrape() function
    '''
    logger.info('scrapeLastPageNumber(): Start!')  if logger else None
    # Get the url and make a BeautifulSoup object
    url = 'https://finviz.com/screener.ashx?v=111'
    source = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}).text
    soup = bs(source, 'lxml')

    # Find the pagination
    pagination = soup.find_all('a', class_='screener-pages')
    # Return the last page number as an integer
    logger.info(f"scrapeLastPageNumber(): Last page number found: \t\t {int(pagination[-1].text)}! \t\t Let's return it.") if logger else None
    return int(pagination[-1].text)


def scrapeFinviz(data: pd.DataFrame, columnsNames: dict, firstPage: int =1, lastPage: int = 10,
            logger: logging.getLogger =None) -> pd.DataFrame:
    '''
    Scrape screener data from finviz.com from fisrtPage to lastPage
    
    data -> input DataFrame
    columnsNames -> The header row of table
    '''
    if lastPage != 10:
        lastPage = scrapeLastPageNumber(logger)
    logger.info('scrape(): Start scraping finviz.com from page {} to {}'.format(firstPage, lastPage)) if logger else None
    for i in range(firstPage, lastPage+1):
        if i % 10 == 1:
            if i+9 <= lastPage:
                logger.info('scrape(): Scraping pages {}-{}'.format(i,i+9)) if logger else None
            else:
                logger.info('scrape(): Scraping pages {}-{}'.format(i,lastPage)) if logger else None
        # Since first page url differ from the rest, we need this comparison
        if i == firstPage:
            url = 'https://finviz.com/screener.ashx?v=111'
        else:
            # Every page contains 20 tickers and 
            #   strating row number is like:[21,41,61,...] which is: 20*n + 1
            pageNumber = (20 * (i-1))+1
            url = 'https://finviz.com/screener.ashx?v=111&r='+str(pageNumber)
        
        # Get the url and make a BeautifulSoup object
        source = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}).text
        soup = bs(source, 'lxml')
        
        # Start scraping
        table = soup.find("table", attrs={'width':'100%', 'cellpadding' :"3",
                                        'cellspacing' :"1", 'border' :"0", 'bgcolor' :"#d3d3d3"})
        tableList = table.find_all('tr') # Find rows of table
        del tableList[0] # Delete the header row of the table

        # Extract data from each row and append it to DataFrame
        for row in tableList:
            dic = {}
            cells = row.find_all('td')
            for i, cell in enumerate(cells):
                dic[columnsNames[i+1]]=cell.a.text
            d = pd.Series(dic)
            data = data.append(d, ignore_index=True)
    logger.info("scrape(): Scrape ended!! Let's return the result :)") if logger else None
    return data


def scrapeWhole(logger: logging.getLogger = None):
    df = pd.DataFrame({'No.':[],
        'Ticker':[],
        'Company':[],
        'Sector':[],
        'Industry':[],
        'Country':[],
        'Market Cap':[],
        'P/E':[],
        'Price':[],
        'Change':[],
        'Volume':[],})

    columnsNames = {1:'No.',
        2:'Ticker',
        3:'Company',
        4:'Sector',
        5:'Industry',
        6:'Country',
        7:'Market Cap',
        8:'P/E',
        9:'Price',
        10:'Change',
        11:'Volume',}

    pd.set_option("display.max_columns", None)
    df = scrapeFinviz(df, columnsNames, lastPage=10, logger=logger)
    return df



if __name__ == '__main__':
    logger = createLogger('Scrape Finviz.com')
    logger.info('Prgram Starts!!')

    df = scrapeWhole(logger)

    logger.info('Write results into the disk.')
    now = now()
    # df.to_csv(f'{now}.csv', index=False)


    logger.info('End of program.\n{}'.format('-'*40))