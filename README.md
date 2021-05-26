# USStockMarketHistorical

US Stock Market Historical Data.
Fetching stock market data on daily basis from yahoo!finance.

## Technologies

**Python 3.8**
#### Required libraries
- numpy
- pandas
- bs4 (BeautifulSoup)
- yfinance
- built-in libs:
  - requests
  - time
  - datetime
  - logging

## How to use

- tickerScrape
  * This script collect the ticker names from finviz.com.
  * You can find the name of the tickers along with some additional data such as sector or industry the company is in tickers.csv file.
- collect
  * You can use this script to collect the historical data from yfinance API.
  * The data will store in stocksData folder.
  * If there is any problem during fetching historical data, you can find the ticker name in failed.txt .

> One have to bear in mind that these scripts do not fetch ETFs' historical data however we decouple the ETF's from tickers in both scripts.
## Acknowledgments

* We were using [finviz](https://finviz.com/) data to built this repo.
* These scripts were built using [yahoo!finance](https://finance.yahoo.com/) data that fetch from [yfinance](https://github.com/ranaroussi/yfinance) package.
