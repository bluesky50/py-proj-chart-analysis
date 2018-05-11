import math
import numpy as np
import pandas
from util import insertElementsToNpArray

def formulateSMA1(values, window):
    print(">>> Function called movingAverage(values,window)")
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights,'valid')
    return sma # as a numpy array

# TODO: ADD comments and print functions for these functions.

def formulateSMA(values, window_length):
    sma = values.rolling(window=window_length, win_type='boxcar', center=False).mean()
    return sma # as numpy array
# TODO: Build my own weighted moving average function

def formulateWMA(values, window_length):
    # The weighted moving average function.
    wma = values.rolling(window_length, win_type='triang').mean()
    return wma


def formulateEWMA(values, window_length):
    ewma = values.ewm(ignore_na=True, min_periods=0, adjust=True, span=window_length).mean()
    return ewma # as numpy array

def formulateEMA(values, window_length):
    weights = np.exp(np.linspace(-1.0, 0.0, window_length))
    weights /= weights.sum()

    a = np.convolve(values, weights)[:len(values)]
    a[:window_length]= a[window_length]
    return a

def formulateSD(values, window_length):
    # sd = values.ewm(ignore_na=True, adjust=True, span=window_length).std()
    # sd = pandas.rolling_std(values, window=window_length, min_periods=1)
    sd = values.rolling(min_periods=1,window=window_length,center = False).std()
    return sd  # as numpy array

def formulateHMA(values, window_length):
    sqrt_calc = math.ceil(math.sqrt(window_length))
    step1 = 2*(values.ewm(ignore_na=True, adjust=False, span=window_length/2).mean())
    step2 = step1 - values.ewm(ignore_na=True, adjust=False, span=window_length).mean()
    step3 = step2.ewm(ignore_na=True, adjust=True, span=sqrt_calc).mean()
    return step3

# The s dev function based on fidelity indicator site.
def formulateSDev2(values,  window_length):
    step1 = (values - formulateSMA(pandas.Series(values), window_length))**2
    # step1 = (values - formulateSMA1(values, window_length))**2
    # step1 = (values - pandas.Series(values).ewm(ignore_na=True, adjust=True, span=window_length).mean())**2
    # step2 = step1.rolling(window=window_length, win_type='boxcar', center=False).mean()
    step2 = np.sqrt(formulateSMA1(step1, 2))
    return step2

# Experimental function with interesting result
def formulateSDevExp(values,  window_length):
    step1 = (values - formulateEWMA(pandas.Series(values), window_length))#**2
        # print(step1)
        # step2 = step1.rolling(window=window_length, win_type='boxcar', center=False).mean()
        # step2 = step1.ewm(ignore_na=True, adjust=False, span=window_length).mean()
        # step3 = np.sqrt(step2)
    return step1

# Source Stockcharts.com/school/
def formulateUltimateOscillator(dataFrame, window_length):
    weight1=2
    weight2=4
    # Removed pandas.Series because I changed back to the older SMA function based on the web tutorial from sentex on youtube.
    average7 = formulateSMA(pandas.Series(formulateBP(dataFrame)), window_length)/formulateSMA(pandas.Series(formulateTR(dataFrame)), window_length)
    average14 = formulateSMA(pandas.Series(formulateBP(dataFrame)), window_length*weight1)/formulateSMA(pandas.Series(formulateTR(dataFrame)), window_length*weight1)
    average28 = formulateSMA(pandas.Series(formulateBP(dataFrame)), window_length*weight2)/formulateSMA(pandas.Series(formulateTR(dataFrame)), window_length*weight2)

    UO = 100 * (((4*average7)+(2*average14)+average28)/(weight2+weight1+1))
    return UO

def formulateCMO(values, window_length):
    cmo = []
    x = window_length
    # close = dataFrame['Close']
    while x < len(values):
        # Consider all up and down moves for a time frame
        considerationPrices = values[x-window_length:x]
        upSum = 0
        downSum = 0

        y = 1

        print(str(x) + " of " + str(len(values)))
        if (window_length==1):
            curPrice = values[x]
            prevPrice = values[x-1]
            if curPrice >= prevPrice:
                upSum += (curPrice - prevPrice)
            else:
                downSum += (prevPrice - curPrice)
            curCMO = ((upSum - downSum) / (upSum + float(downSum))) * 100.00
        else:
            while y < window_length:
                curPrice = considerationPrices[y]
                prevPrice = considerationPrices[y-1]
                if curPrice >= prevPrice:
                    upSum += (curPrice-prevPrice)
                    # print(upSum)
                else:
                    downSum += (prevPrice-curPrice)
                    # print(downSum)
                y+=1
            curCMO = ((upSum-downSum)/(upSum+float(downSum)))*100.00

        cmo.append(curCMO)
        x+=1

    cmo = insertElementsToNpArray(cmo, window_length, 'NaN')
    return cmo

# Source Stockcharts.com/school/
def formulateBP(dataFrame):

    result = []

    low = dataFrame.Low
    close = dataFrame.Close

    for index in range(len(close)):
        if(index == 0):
            result.append('NaN')
        else:
            result.append(close[index] - (min(low[index],close[index-1])))

    return result

# Source Stockcharts.com/school/
def formulateTR(dataFrame):
    result = []

    high = dataFrame.High
    low = dataFrame.Low
    close = dataFrame.Close

    for index in range(len(close)):
        if(index==0):
            result.append('NaN')
        else:
            result.append(max(high[index], close[index-1])-min(low[index], close[index-1]))

    return result

# Source Stockcharts.com/school/
# def forumatePP(dataFrame):
# TODO: Create a function that finds the highs and lows of just a single set of data like the close price.
def formulateSingleSetPivots(values, window_length, append_value):
    trend = 0 # 1 is up -1 is down 0 is neutral.
    index = 1
    totalLength = len(values)
    lastPivotValue = 0
    lastPivotIndex = 0
    curValue = 0
    resultSet = []

    resultSet.append(append_value)
    while index < totalLength:
        curValue = values[index]

        # Calculate the trend
        if values[index] > values[index-1]:
            tend = 1

        elif values[index] < values[index-1]:
            trend = -1
        else:
            trend = 0

        # Calculate the appropriate window size based on index location
        adjustmentDown = window_length
        adjustmentUp = window_length

        if (index < window_length):
            adjustmentDown = index
        elif (index > totalLength - window_length):
            adjustmentUp = totalLength - index

        # Establish whether the value being evaluated is a high or a low
        if (trend == 1):
            findMax = max(values[index - adjustmentDown:index + adjustmentUp].get_values())
            if curValue >= findMax:
                lastPivotIndex = index
                lastPivotValue = curValue
                resultSet.append(lastPivotValue)
            else:
                print("False max (skip)")

        elif (trend == -1):
            findMin = min(values[index - adjustmentDown:index + adjustmentUp])
            # print("Min" + str(findMin))
            # print(pivotPoint)
            if curValue <= findMin:
                lastPivotIndex = index
                lastPivotValue = curValue
                resultSet.append(lastPivotValue)
            else:
                print("False min (skip)")
        else:
            resultSet.append(append_value)

        index+=1
    return resultSet


# Source Stockcharts.com/school/
def formulatePPoint(dataFrame, window_length=7):
    result = []

    high = dataFrame.High
    low = dataFrame.Low
    close = dataFrame.Close
    pivotPointResetPeriod = window_length


    for index in range(len(close)):
        previousPivotPoint = (high[index] + low[index] + close[index]) / 3
        if (index%pivotPointResetPeriod == 0):
            previousPivotPoint = (high[index] + low[index] + close[index]) / 3
            result.append(previousPivotPoint)
        else:
            result.append(previousPivotPoint)

    return result

def formulateRSandSP(ppData, dataFrame, window_length = 7):
    result = []
    pivotPoints = formulatePPoint(dataFrame, 7)

    supportTop = (pivotPoints*2) - dataFrame.High
    supportBot = (pivotPoints) - (dataFrame.High - dataFrame.Low)

    resistanceBot = (pivotPoints*2) - dataFrame.Low
    resistanceTot = (pivotPoints) + (dataFrame.High - dataFrame.Low)

    # TODO: Still in progress.

def formulatePPHiLo(dataFrame, window_length, append_value='NaN'):
    # TODO: Possibly add something to account for when the trend changes.
    # Only when the trend changes does the result set need to be updated.
    result = []

    pivotPoint = ((dataFrame.High[0] + dataFrame.Low[0] + dataFrame.Close[0])/3)

    last_pivot_index = 0
    last_pivot_value_record = 0

    trend = 0  # Trend indicator 1 for up and -1 for down 0 for same.
    diff = 0

    # lastPivotPointTrend = 0 # Indicates whether the trend has gone from 1 to -1 and vice versa since
    # The last time that the pivotpoint was added to the result

    total_length = len(dataFrame.Close)
    for index in range(total_length):
        row = dataFrame.iloc[index]

        # If the index window threshold has been met we can
        # go into the logic for setting adding a pivot point to the result set.
        # Other wise it is not added.
        # Pivot point and trend are still being calculated.
        # if ((index - last_pivot_index) > window_length): #or index < window_length-1:

        adjustmentDown = window_length
        adjustmentUp = window_length

        if (index < window_length):
            adjustmentDown = index
        elif (index > total_length - window_length):
            adjustmentUp = total_length - index

        # We don't have a trend yet
        # Measure whether the trend is up or down.
        if (trend == 0):
            if row.Low < pivotPoint - diff:
                pivotPoint = row.Low
                # last_pivot_index = index
                # result.append(pivotPoint)
                trend = -1
                result.append(append_value)
            elif row.High > pivotPoint + diff:
                pivotPoint = row.High
                # last_pivot_index = index
                # result.append(pivotPoint)
                trend = 1
                result.append(append_value)
            else:
                result.append(append_value)
            # print(len(result))

        # Logic if the current trend is up.
        elif trend == 1:
            # If got higher than last pivot, update the pivotPoint
            if row.High > pivotPoint:
                result.append(append_value)
                # Replace the last pivot entry with NaN, as it wasn't a real one
                # result[last_pivot_index] = 'NaN'
                pivotPoint = row.High
                # last_pivot_index = index

            # This logic notices that there is a change in direction from up to down.
            elif row.Low < pivotPoint - diff:

                # if index < total_length-window_length and index >= window_length:

                findMax = max(dataFrame.High[index - adjustmentDown:index + adjustmentUp].get_values())

                # print("Max" + str(findMax))
                # print(pivotPoint)
                if pivotPoint >= findMax:
                    last_pivot_index = index - 1
                    last_pivot_value_record = pivotPoint
                    result[last_pivot_index] = last_pivot_value_record
                    # print("True Max recorded")
                    # trend = -1
                else:
                    print("False max (skip)")

                pivotPoint = row.Low
                result.append(append_value)
                trend = -1
                # lastPivotPointTrend = -1
            else:
                trend = 0
                result.append(append_value)
            # print(len(result))

        # # Logic if the current trend is down.
        # elif trend == -1 and index + window_length < total_length:
        #     findMin = min(dataFrame.High[index:index + window_length])
        #     if findMin < pivotPoint:
        #         pivotPoint = findMin

        elif trend == -1:
            # If got lower than last pivot, update the string
            if row.Low < pivotPoint:
                result.append(append_value)
                # data.ix[i, 'swings'] = row.Low
                # result[last_pivot_index] = 'NaN'
                pivotPoint = row.Low
                # last_pivot_index = index
            elif row.High > pivotPoint - diff:
                # if index < total_length-window_length and index >= window_length:
                findMin = min(dataFrame.Low[index - adjustmentDown:index + adjustmentUp])
                # print("Min" + str(findMin))
                # print(pivotPoint)
                if pivotPoint <= findMin:
                    last_pivot_index = index-1
                    last_pivot_value_record = pivotPoint
                    result[last_pivot_index] = last_pivot_value_record
                    # print("True Min recorded")
                    trend = 1
                else:
                    print("False min (skip)")

                pivotPoint = row.High
                result.append(append_value)
                # Change the trend indicator
                trend = 1
                # lastPivotPointTrend = -1
            else:
                trend = 0
                result.append(append_value)
            # print(len(result))
        else:
            result.append(append_value)

        # else:
            #This is what happens when not outside the window buffer length.
            # Write NaN to result set
            # Update pivot
            # Update Trend
            # Update Trend Change boolean


            # We don't have a trend yet
            # Measure whether the trend is up or down.
            # if (trend == 0):
            #     if row.Low < pivotPoint - diff:
            #         pivotPoint = row.Low
            #         last_pivot_index = index
            #         result.append(pivotPoint)
            #         trend = -1
            #     elif row.High > pivotPoint + diff:
            #         pivotPoint = row.High
            #         last_pivot_index = index
            #         result.append(pivotPoint)
            #         trend = 1

            # result.append('NaN')
            # if row.Low < pivotPoint - diff:
            #     pivotPoint = row.Low
            #     trend = -1
            #     advance_trend = -1
            # elif row.High > pivotPoint + diff:
            #     pivotPoint = row.High
            #     trend = 1
            #     advance_trend = 1
            # else:
            #     trend = 0
            #
            # if trend == 1 and index+window_length < total_length:
            #     findMax = max(dataFrame.High[index:index + window_length])
            #     if findMax > pivotPoint:
            #         futurePivot = findMax
            # elif trend == -1 and index+window_length < total_length:
            #     findMin = min(dataFrame.High[index:index + window_length])
            #     if findMin < pivotPoint:
            #         futurePivot = findMin

            # for plus in (range(window_length) and index+plus+1 < total_length):
            #     check_row = dataFrame.iloc[index + plus + 1]
            #     if advance_trend == 1:
            #         if check_row.High > pivotPoint:  # Is the pivot point less than the next row's high price.
            #             # If so update the pivot point.
            #             pivotPoint = check_row.High
            #             advance_trend = 1
            #         # The logic if the next day low price is lower than the current pivotprice.
            #         elif check_row.low < pivotPoint:
            #             advance_trend = -1
            #
            #     elif advance_trend == -1:
            #         if check_row.low > pivotPoint:
            #             pivotPoint = check_row.Low
            #             advance_trend = -1
            #         elif check_row.High < pivotPoint:
            #             advance_trend = -1

    # print(result)
    return result

# TODO: Create a new version of pivot points.
# TODO: creates an array of all pivot points.
# TODO: Goes back through and checks pivot points to make sure it is max or min in a rolling window at the center. if not. put NAN or 0 or close price.

# Used to calculate all pivot points.
def formulatePPHiLo2(dataFrame, window_length):
    # TODO: Possibly add something to account for when the trend changes.
    # Only when the trend changes does the result set need to be updated.
    result = []

    pivotPoint = ((dataFrame.High[0] + dataFrame.Low[0] + dataFrame.Close[0])/3)

    last_pivot_index = 0
    last_pivot_value_record = 0

    trend = 0  # Trend indicator 1 for up and -1 for down 0 for same.
    diff = 0 # Buffer amount before detecting change.

    total_length = len(dataFrame.Close)

    # Thist first section of logic calculates all the pivot points and adds them all to the result array.
    for index in range(total_length):
        row = dataFrame.iloc[index]

        # If the index window threshold has been met we can
        # go into the logic for setting adding a pivot point to the result set.
        # Other wise it is not added.
        # Pivot point and trend are still being calculated.
        # if ((index - last_pivot_index) > window_length): #or index < window_length-1:

        # We don't have a trend yet
        # Measure whether the trend is up or down.
        if (trend == 0):
            nextRow = dataFrame.iloc[index + 1]
            if nextRow.Low < row.Low - diff:
                pivotPoint = nextRow.Low

                # last_pivot_index = index
                trend = -1
            elif nextRow.High > row.High + diff:
                pivotPoint = nextRow.Low
                # last_pivot_index = index
                trend = 1
            else:
                result.append(pivotPoint)
            # print(pivotPoint)
            result.append(pivotPoint)

        # Logic if the current trend is up.
        elif trend == 1:
            # If got higher than last pivot, update the pivotPoint
            if row.High > pivotPoint:
                pivotPoint = row.High

            # This logic notices that there is a change in direction from up to down.
            elif row.Low < pivotPoint - diff:

                # last_pivot_index = index - 1
                # last_pivot_value_record = pivotPoint
                # result[last_pivot_index] = last_pivot_value_record
                # print("True Max recorded")
                pivotPoint = row.Low
                trend = -1
            else:
                trend = 0
                result.append(pivotPoint)
            result.append(pivotPoint)

        elif trend == -1:
            # If got lower than last pivot, update the string
            if row.Low < pivotPoint:
                pivotPoint = row.Low
                # data.ix[i, 'swings'] = row.Low
                # result[last_pivot_index] = 'NaN'
                # last_pivot_index = index
            elif row.High > pivotPoint - diff:
                # last_pivot_index = index-1
                # last_pivot_value_record = pivotPoint
                # result[last_pivot_index] = last_pivot_value_record
                # print("True Min recorded")

                pivotPoint = row.High
                # Change the trend indicator
                trend = 1
                # lastPivotPointTrend = -1
            else:
                trend = 0
            # print(len(result))
            result.append(pivotPoint)
        else:
            result.append(pivotPoint)

    return result

# Similar to formulatePPHiLo but does the calculation a different way.
# Should have the same result.
def formulatePPHiLo3(dataFrame, window_length):
    # TODO: Possibly add something to account for when the trend changes.
    # Only when the trend changes does the result set need to be updated.
    result = []

    pivotPoint = ((dataFrame.High[0] + dataFrame.Low[0] + dataFrame.Close[0])/3)

    last_pivot_index = 0
    last_pivot_value_record = pivotPoint

    trend = 0  # Trend indicator 1 for up and -1 for down 0 for same.
    diff = 0 # Buffer amount before detecting change.

    total_length = len(dataFrame.Close)

    # Thist first section of logic calculates all the pivot points and adds them all to the result array.
    for index in range(total_length):
        row = dataFrame.iloc[index]


        # If the index window threshold has been met we can
        # go into the logic for setting adding a pivot point to the result set.
        # Other wise it is not added.
        # Pivot point and trend are still being calculated.
        # if ((index - last_pivot_index) > window_length): #or index < window_length-1:
        adjustmentDown = window_length
        adjustmentUp = window_length

        if (index < window_length):
            adjustmentDown = index
        elif (index > total_length - window_length):
            adjustmentUp = total_length - index



        # We don't have a trend yet
        # Measure whether the trend is up or down.
        if (trend == 0):
            nextRow = dataFrame.iloc[index + 1]
            if nextRow.Low < row.Low - diff:
                pivotPoint = nextRow.Low

                # last_pivot_index = index
                trend = -1
            elif nextRow.High > row.High + diff:
                pivotPoint = nextRow.Low
                # last_pivot_index = index
                trend = 1
            else:
                result.append(last_pivot_value_record)
            # print(pivotPoint)
            result.append(last_pivot_value_record)

        # Logic if the current trend is up.
        elif trend == 1:
            # If got higher than last pivot, update the pivotPoint
            if row.High > pivotPoint:
                pivotPoint = row.High

            # This logic notices that there is a change in direction from up to down.
            elif row.Low < pivotPoint - diff:
                findMax = max(dataFrame.High[index - adjustmentDown:index + adjustmentUp].get_values())

                # print("Max" + str(findMax))
                # print(pivotPoint)
                if pivotPoint >= findMax:
                    last_pivot_index = index - 1
                    last_pivot_value_record = pivotPoint
                    result[last_pivot_index] = last_pivot_value_record
                    # print("True Max recorded")
                else:
                    print("False min (skip)")
                pivotPoint = row.Low
                trend = -1
            else:
                trend = 0
                result.append(last_pivot_value_record)
            result.append(last_pivot_value_record)

        elif trend == -1:
            # If got lower than last pivot, update the string
            if row.Low < pivotPoint:
                pivotPoint = row.Low
                # data.ix[i, 'swings'] = row.Low
                # result[last_pivot_index] = 'NaN'
                # last_pivot_index = index
            elif row.High > pivotPoint - diff:

                findMin = min(dataFrame.Low[index - adjustmentDown:index + adjustmentUp])
                # print("Min" + str(findMin))
                # print(pivotPoint)
                if pivotPoint <= findMin:
                    last_pivot_index = index-1
                    last_pivot_value_record = pivotPoint
                    result[last_pivot_index] = last_pivot_value_record
                    # print("True Min recorded")
                else:
                    print("False high (skip)")

                pivotPoint = row.High
                # Change the trend indicator
                trend = 1
                # lastPivotPointTrend = -1
            else:
                trend = 0
            # print(len(result))
            result.append(last_pivot_value_record)
        else:
            result.append(last_pivot_value_record)

    return result

def formulateSDevForPPHiLoDivergence(values, df, window_length):
    step1 = (values - formulateSMA(df['Close'], window_length))**2
    step2 = np.sqrt(formulateSMA1(step1, 2))
    return step2

# Used for momentum oscillation.
# Tries to estimate if an asset is overbought or oversold.
def formulateRSI(values, window_length=14):
    # Difference in price from previous step
    delta = values.diff()
    # Get rid of the first row, which is NaN since it did not have a previous
    # row to calculate the differences
    delta = delta[1:]

    # Make the positive gains (up) and negative gains (down) Series
    up, down = delta.copy(), delta.copy()
    up[up<0]=0
    down[down>0]=0

    # Calculate the EWMA
    rollUp1 = up.ewm(ignore_na=True,min_periods=0,adjust=True,span=window_length).mean()
    rollDown1a = down.abs().ewm(ignore_na=True, min_periods=0, adjust=True, span=window_length).mean()
    #rollDown1a = down.abs().ewm(ignore_na=True,min_periods=0,adjust=True,com=window_length).mean()
    # rollDown1 = pandas.stats.moments.ewma(down.abs(), window)

    # Calculate the RSI based on EWMA
    RS1 = rollUp1/rollDown1a
    RSI1 = 100.0-(100.0/(1.0 + RS1))

    # Calculate the SMA
    # rollUp2 = up.rolling(window=window_length, center=False).mean()
    # rollDown2 = down.abs().rolling(window=window_length, center=False).mean()
    #
    # Calculate the RSI based on SMA
    # RS2 = rollUp2 / rollDown2
    # RSI2 = 100.0 - (100.0/(1.0+RS2))

    # RSI1 = EWMA based
    # RSI2 = SMA based
    return RSI1


def brokenRSI(values, n=14):
    print(">>> Function called forumateRSI(values, n=14)")
    deltas = np.diff(values)
    seed = deltas[:n+1]
    up = seed[seed>=0].sum()/n
    down = -seed[seed<0].sum()/n
    relativeStrength=up/down
    relativeStrengthIndex = np.zeros_like(values)
    relativeStrengthIndex[:n] = 100.0 - (100.0/(1.0+relativeStrength))

    upval=0.0
    downval=0.0

    for i in range(n, len(values)):
        delta=deltas[i-1]
        if (delta > 0):
            upval = delta
            downval = 0.0
        else:
            upval = 0.0
            downnval = -delta

        up = (up*(n-1)+upval)/n
        down = (down*(n-1)+downval)/n
        relativeStrength = up/down
        relativeStrengthIndex[i] = 100.0 - (100.0/(1.0+relativeStrength))

    return relativeStrengthIndex