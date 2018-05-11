# Creates higher level request functions for accesing data stored by Arctic in a Mongo DB.

from arctic import Arctic
from util import isEmptyDataFrame

# TODO: Function to get data, columns, etc.

# TODO: Function to get Tickers.

# TODO: Function to get metadata.

# TODO: Function to get entire dataset.
# Arguments tickerSymbol, storeName (the namer of the arctic library)
# Returns Pandas DataFrame
from arctic.date import DateRange


def getDataFromArcticStore(tickerName, storeName):
    print(">>> Function called getDataFromArcticStore("+tickerName+", "+storeName+")")
    # Connect to local MONGODB
    source = 'localhost'
    store = Arctic(source)
    print "+ Arctic connected to MongoDB at "+ source

    # Access the library
    library = store[storeName]

    # base = datetime.datetime.today()
    # date_list = [base - datetime.timedelta(days=x) for x in range(0, 365)]

    # Reading the data
    item = library.read(tickerName)
    print "+ Arctic reading "+tickerName+" from "+storeName
    # aapl = item.data
    # metadata = item.metadata

    # print aapl
    # print metadata
    return item.data

def getSubsetFromArcticStore(tickerName, arcticLibraryName, start_date, end_date):
    print(">>> Function called getSubsetFromArcticStore("+tickerName+", "+arcticLibraryName+")")
    # Connect to local MONGODB
    source = 'localhost'
    store = Arctic(source)
    print "+ Arctic connected to MongoDB at "+source

    # Access the library
    library = store[arcticLibraryName]

    # base = datetime.datetime.today()
    # date_list = [base - datetime.timedelta(days=x) for x in range(0, 365)]

    # Reading the data

    try:
        print "+ Arctic reading " + tickerName + " from " + arcticLibraryName
        item = library.read(tickerName, date_range=DateRange(start_date, end_date))
        if (isEmptyDataFrame(item.data)):
            print("! Error no data returned for " + tickerName)
        else:
            return item.data
    except Exception, e:
        print("! Error "+tickerName+" not found in "+arcticLibraryName+": " + str(e) )

    # Old test:
    # if (unicode(tickerName) in getArcticLibrarySymbols(storeName)):
    #     item = library.read(tickerName, date_range=DateRange(start_date, end_date))
    #     print "+ Arctic reading "+tickerName+" from "+storeName
    #     return item.data
    # else:
    #     print("! "+tickerName+" not found in "+storeName)


def getArcticLibraries():
    print(">>> Function called getArcticLibraries()")
    # Connect to local MONGODB
    store = Arctic('localhost')
    print "+ Arctic connected to MongoDB at localhost"
    print("+ Requesting libraries from Arctic store")
    return store.list_libraries()

def getArcticLibrarySymbols(libraryName):
    print(">>> Function called getArcticLibrarySymbols("+libraryName+ ")")
    # Connect to local MONGODB
    store = Arctic('localhost')
    print "+ Arctic connected to MongoDB at localhost"

    # Access the library
    library = store[libraryName]
    print("+ Requesting symbols from "+libraryName)
    return library.list_symbols()


# TODO: create append data function

#Arctic.initialize_library("something")
# stocks = Arctic["something"]
# aapl = get_stock_history('aapl', '2015-02-01', '2015-03-01')
# stocks.append('aapl', aapl)