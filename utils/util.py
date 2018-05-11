import BeautifulSoup
import numpy
import urllib2
import pandas

def convertNpArrayToDf(array,columnName):
    print(">>> Function called convertNpArrayToDf(array,columnName)")
    return pandas.DataFrame(array, columns=columnName)

# Adds elements to the beginning of an array
def insertElementsToNpArray(array, elementCount, element):
    print(">>> Function called insertElementsToNpArray(array, elementCount, element)")
    supplement_array = numpy.full(elementCount, element, dtype='float64')
    new_array = numpy.concatenate((supplement_array, array), axis=0)
    return new_array

def addColumnToDf(array, dataFrame, newColumnName):
    print(">>> Function called addColumnToDf(array, dataFrame, newColumnName)")
    size_diff = len(dataFrame.index) - len(array)
    if (size_diff==0):
        print("Size diff = 0")
        dataFrame[newColumnName] = array
    elif (size_diff>0):
        print("Size diff > 0")
        new_array2 = insertElementsToNpArray(array, size_diff, 'NaN')

        dataFrame[newColumnName]= new_array2
        # You can also use the append() method to append a sequence to the dataframe.
        # There are options to ignore index of that is the case.
    else:
        print("! Error the array was not added to the data frame")

# Checks a data frame if it exists and if it has data.
def isEmptyDataFrame(dataFrame):
    print(">>> Function called isEmptyDataFrame(dataFrame)")
    if (dataFrame is None or len(dataFrame.index) == 0):
        return True
    else:
        return False

# Using the Plotly validate ohlc function for myself to modify the dataframe.
# This function will manipulate the data by adding 0.001 to highs it if is the same as a low.
# And it will subract 0.001 from the low.
def validate_ohlc(dataFrame): # (open, high, low, close, direction, **kwargs):

    """
    ohlc and candlestick specific validations

    Specifically, this checks that the high value is the greatest value and
    the low value is the lowest value in each unit.

    See FigureFactory.create_ohlc() or FigureFactory.create_candlestick()
    for params

    :raises: (PlotlyError) If the high value is not the greatest value in
        each unit.
    :raises: (PlotlyError) If the low value is not the lowest value in each
        unit.
    :raises: (PlotlyError) If direction is not 'increasing' or 'decreasing'
    """
    print(">>> Function called validate_ohlc(dataFrame)")
    open = dataFrame.Open
    low = dataFrame.Low
    close = dataFrame.Close
    high = dataFrame.High

    # open = dataFrame.iloc[:,0]
    # low = dataFrame.iloc[:,1]
    # close = dataFrame.iloc[:,2]
    # high = dataFrame.iloc[:,3]

    for lst in [open, low, close]:
        for index in range(len(high)):
            if high[index] < lst[index]:
                # print(lst[index])
                # print(high[index])
                # print("Modifying the high")

                high[index] = lst[index] + 0.01
                # print(high[index])
                # raise exceptions.PlotlyError("Oops! Looks like some of "
                #                              "your high values are less "
                #                              "the corresponding open, "
                #                              "low, or close values. "
                #                              "Double check that your data "
                #                              "is entered in O-H-L-C order")

    for lst in [open, high, close]:
        for index in range(len(low)):
            if low[index] > lst[index]:
                # print(lst[index])
                # print(low[index])
                # print("Modifying the low")
                low[index] = lst[index] - 0.01
                # print(low[index])

                # raise exceptions.PlotlyError("Oops! Looks like some of "
                #                              "your low values are greater "
                #                              "than the corresponding high"
                #                              ", open, or close values. "
                #                              "Double check that your data "
                #                              "is entered in O-H-L-C order")

    # direction_opts = ('increasing', 'decreasing', 'both')
    # if direction not in direction_opts:
    #     raise exceptions.PlotlyError("direction must be defined as "
    #                                  "'increasing', 'decreasing', or "
    #                                  "'both'")

# Method to create arctic library.
def createQuandlCode(tickerName, exchangeName, quandlDatabaseName):
    print(">>> Function called createQuandlCode("+tickerName+", "+exchangeName+", "+quandlDatabaseName+")")
    # If Quandl Database name is GOOG this is the format GOOG/EXCHANGE_TICKER
    if (quandlDatabaseName == 'GOOG'):
        quandleCode = quandlDatabaseName + "/" + exchangeName + "_" + tickerName
        print("+ Quandl code created: " + quandleCode)
        return quandleCode
    elif (quandlDatabaseName == 'WIKI'):
        # WIKI/TICKER
        quandleCode = quandlDatabaseName + "/" + tickerName
        print("+ Quandl code created: " + quandleCode)
        return quandleCode
    elif (quandlDatabaseName == 'YAHOO'):
        # YAHOO/{EXCHANGE}_{TICKER}, YAHOO/FUND_{TICKER}, YAHOO/INDEX_{TICKER}
        if (exchangeName == 'NASDAQ'):
            quandleCode = quandlDatabaseName + "/" + tickerName
            print("+ Quandl code created: " + quandleCode)
            return quandleCode
        else:
            quandleCode = quandlDatabaseName + "/" + exchangeName + "_" + tickerName # The exchange name could be a fund or index
            print("+ Quandl code created: " + quandleCode)
            return quandleCode
            return ''
    else:
        print("! No Quandl code created")
        return ''

def createArcticLibraryName(dataSource, quandlDatabaseName, exchangeName):
    print(">>> Function called createQuandlCode(" + dataSource + ", " + quandlDatabaseName + ", " + exchangeName + ")")
    arcticLibraryName = dataSource+"_"+quandlDatabaseName
    return arcticLibraryName


def isSymbolInArcticLibrary(symbolName, arcticLibrary, articStore):
    print(">>> Function called isSymbolInArcticLibrary(" + symbolName + ", arcticLibrary, articStore)")
    try:
        bool = unicode(symbolName) in arcticLibrary.list_symbols()
        return bool
    except Exception,e:
        print("! Error: "+ str(e))

    #return unicode(symbolName) in articStore.list_libraries()

def isLibraryInArcticStore(libraryName, arcticStore):
    print(">>> Function called isLibraryInArcticStore(" + libraryName + ", arcticStore)")
    try:
        bool = libraryName in arcticStore.list_libraries()
        return bool
    except Exception, e:
        print("! Error: " + str(e))

def setColumns(databaseCode):
    print(">>> Function called setColumns("+databaseCode+")")
    if (databaseCode in ['GOOG', 'YAHOO']):
        columns = [u'Open', u'High', u'Low', u'Close', u'Volume']
        return columns
    elif (databaseCode in ['WIKI']):
        columns = [u'Adj. Open', u'Adj. High', u'Adj. Low', u'Adj. Close',
                   u'Adj. Volume']  # Only can be used for WIKI data.

        # Only used for teesting.
        # columns = [u'Open', u'High', u'Low', u'Close', u'Volume']
        return columns
    else:
        print("! No valid database code was selected")


def getSymbol(url):
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page)
    return soup.findAll("div",{"class":"FL gry10"})[0].text.split("|")[1].split(":")[1]


def reviewCorpActions(url):
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page)
    cells = soup.findAll('td')

    # This function will fetch the NSE symbols from a money control company page.
    # Creating a list of list
    # Each list will be Company name, old fair value,

    rows = []
    for i in range(len(cells) / 4):
        if i == 0:
            # The first row , we can skip over that. It is the header
            continue
        else:
            currentRow=[]
            try:
                if __name__ == '__main__':
                    for j in range(4):
                        currentRow.append(cells[4*i*j].text)
                        # Now we have the first 4 elements in our row. comany name and new face value.
                        # The last element is the symbol. Get the Hyperlink from company link and use that
                        symbol=getSymbol(cells[4*i].a["href"]).strip()
                        if symbol=="": # If blank that means this company doesn't trade on the NSE
                            continue
                        currentRow.append(symbol)
                        rows.append(currentRow)
            except:
                continue
            # If there is an error in parsing, it is skipped over.
            print(currentRow)

# Now we have a list of splits
# We need to iterate through them and compute the adjusted prices.