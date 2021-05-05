import time
import logging
import numpy as np
import pandas as pd


import yfinance as yf

import tickerScrape as tickersData

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


def getTickerData(logger: logging.getLogger = None) -> (pd.DataFrame, pd.DataFrame):
    logger.info('getTickerData(): Start of a function') if logger else None
    df = tickersData.scrapeWhole(logger)
    # Drop unnecessary columns
    df.drop(['No.', 'Price', 'Change', 'Volume', 'P/E', 'Market Cap'], axis=1, inplace=True)
    # Decouple ETFs from Stocks
    stocks = df[df['Industry'] != 'Exchange Traded Fund']
    stocks = stocks.reset_index().drop(['index'], axis=1) # Reset index
    ETFs = df[df.Industry == 'Exchange Traded Fund'].reset_index().drop(['index', 'Sector', 'Industry', 'Country'], axis=1)
    return stocks, ETFs


def collectData(data: pd.DataFrame, logger: logging.getLogger = None):
    startTime = time.time()
    l = len(data)
    for i in range(l):
        try:
            tmp = yf.Ticker(data.iloc[i].Ticker).history(period='max')
            tmp.to_csv('/stocksData/'+data.iloc[i].Ticker+'.csv')
            if i % 100 == 0: logger.info(f'SO FAR, SO GOOD: \t #{i}')
        except:
            with open('failed.txt', 'a') as file:
                file.write(data.iloc[i].Ticker+'\n')
                logger.info(f'FAILED: {data.iloc[i].Ticker}') if logger else None
    print(f'\n\n\nTime is: {time.time() - startTime}')



if __name__ == '__main__':
    logger = createLogger('Failed')

    stocks, ETFs = getTickerData(logger)
    collectData(stocks, logger)