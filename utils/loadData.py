from dataInterfaceService import saveQuandlDataToArctic
from databaseService import getArcticLibrarySymbols, getArcticLibraries
from util import createArcticLibraryName

# Request information
tickerSymbol = 'AAPL'
exchangeName = 'NASDAQ' # This can be a fund or index name for YAHOO,
quandlDatabaseName = 'WIKI' # YAHOO, GOOG, WIKI are the only ones programmed to work.

# Save location information
# arcticStoreName = 'NASDAQ' Not used any more.
host = 'localhost'

# saveQuandlDataToArctic(quandlDatabaseName, exchangeName, tickerSymbol, host)

libName = createArcticLibraryName('Quandl',quandlDatabaseName, exchangeName)
print(getArcticLibraries())
print(getArcticLibrarySymbols(libName))

# TODO: Create a method that will load data when given a quandl code.