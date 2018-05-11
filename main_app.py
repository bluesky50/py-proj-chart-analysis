# Main app that runs utilizing mainly Arctic for data interface and Plotly for graphing interface.
from databaseService import getArcticLibraries, getArcticLibrarySymbols, getDataFromArcticStore, getSubsetFromArcticStore
from plotlyFunctions import createCandlestickChart, createLineChart, createLineChart2
from util import isEmptyDataFrame, validate_ohlc, createArcticLibraryName, setColumns


# Input Information
stockName = 'MSFT'
exchangeName = 'NASDAQ' # This is manditory for GOOG, but is optional for YAHOO and WIKI.
quandlDatabaseCode = 'WIKI'
source = 'Quandl'

# TODO: Create a test to see if I can plot the pivot points for the highs and lows of a single column of data using the new pivot method.
# TODO: Test it on the Hull Moving average data.
# Information used to make requests from database
arcticLibraryName = createArcticLibraryName(source, quandlDatabaseCode, exchangeName)
start_date = "2014-01-15"
end_date = "2016-06-30"

# Get data and store in a variable.
# stockData = getDataFromArcticStore(stockName, market)

# Get data subset and store it in a pandas dataframe
stockData = getSubsetFromArcticStore(stockName, arcticLibraryName, start_date, end_date)

# Check if stockData is null
if (isEmptyDataFrame(stockData)):
    print("! No data was returned from database call")
else:
    # Prune the data frame of excess columns and select only certain rows for a date range.
    # OLD prune functions: columns = [u'Open', u'High', u'Low', u'Close']

    # TODO: create a check to see what type of columns exist in the data that was called back from database.
    # TODO: Right now I manually have to remember this.
    # stockData = stockData.loc[start_date:end_date, columns]

    # Temporary work around.
    # Set columns
    columns = setColumns(quandlDatabaseCode)
    # columns = [u'Open', u'High', u'Low', u'Close', u'Volume']
    # columns = [u'Adj. Open', u'Adj. High', u'Adj. Low', u'Adj. Close', u'Adj. Volume'] # Only can be used for WIKI data.
    stockData = stockData.loc[:, columns]

    # Renaming column names in dataframe is necessary if adjusted data is used.
    # This is because the code references column names.

    # Clean column names to work later in the code.
    colNames = ['Open', 'High', 'Low', 'Close', 'Volume']
    stockData.columns = colNames

    # This method will actually manipulate the data so that the graphing function will work.
    # Changes data by 0.001
    # print(stockData)
    validate_ohlc(stockData)
    # print(stockData)

    # Render Graphs
    # createCandlestickChart(stockData, stockName+" Stock Price from "+source+" "+quandlDatabaseCode)
    # createLineChart(stockData, stockName+" Stock Price from "+source+" "+quandlDatabaseCode)
    createLineChart2(stockData, stockName+" Stock Price from "+source+" "+quandlDatabaseCode)

# print(stockData.index.to_datetime())
# print(type(stockData.index.to_series()))
# createLineChart(stockData, stockName+" Stock Price")

# TESTING METHODS:
# print(stockData.columns.values.tolist())
# print(type(stockData))
# print(getArcticLibraries())
# print(type(getArcticLibraries()))
# print(unicode('NASDAQ') in getArcticLibraries())
# print(getArcticLibrarySymbols(market))
# print(u'NASDAQ'.encode('ascii', 'ignore'))
# print(type(u'NASDAQ'))
# print('FB'.decode('ascii','ignore') in getArcticLibrarySymbols(market))
# print(unicode('FB') in getArcticLibrarySymbols(market))
# print('FB' in getArcticLibrarySymbols(market))
