import pandas as pd
import numpy as np

# Abbreviation: (PPHiLo)
# This function tries to find the pivot points in a dataset.
# Another python package to look into for doing this is "zigzag".
outputString = " function called."

def get_pivots(data, period_length = 7): # Data is a dataframe
    # data = pd.DataFrame.from_csv('tempData.txt')
    data['swings'] = np.nan # I guess this adds a column to the dataframe. I'm not sure If I want that.

    # pivot = data.iloc[0].Open # This calculates the starting point from where to calculate everything else
    # This needs to be recalculated ever so often.
    # I'm going to try doing it my own way.
    pivot = ((data.High[0] + data.Low[0] + data.Close[0])/3)
    last_pivot_id = 0
    up_down = 0 # Trend indicator
    pivot_recalc_period = period_length

    diff = 0.3 # The constant for determining how much change is allowed before a new trend is started

    for i in range(0, len(data)):
        row = data.iloc[i]

        # # Recalculate the pivot every certain number of days.
        # if (i%pivot_recalc_period ==0):
        #     pivot = ((data.High[i] + data.Low[i] + data.Close[i])/3)

        # We don't have a trend yet

        # Initial analysis of the dataswet to determine wether the trend is up or down.
        if up_down == 0:
            if row.Low < pivot - diff:
                # data.ix[i,'swings'] = row.Low - pivot
                data.ix[i,'swings'] = 'NaN'
                pivot, last_pivot_id = row.Low, i
                up_down = -1
            elif row.High > pivot + diff:
                # data.ix[i,'swings'] =row.High - pivot
                data.ix[i,'swings'] = 'Nan'
                pivot, last_pivot_id = row.High, i
                up_down = 1

        # Logic if the current trend is up.
        elif up_down == 1:
            # If got higher than last pivot, update the swing
            if row.High > pivot:
                # Remove the last pivot, as it wasn't a real one
                # OLD: data.ix[i, 'swings'] = data.ix[last_pivot_id, 'swings'] + (row.High - data.ix[last_pivot_id,'High'])
                # OLD: data.ix[i, 'swings'] = (row.High - data.ix[last_pivot_id,'High'])
                data.ix[i, 'swings'] = row.High
                data.ix[last_pivot_id, 'swings'] = 'NaN'
                pivot, last_pivot_id = row.High, i
            elif row.Low < pivot - diff:
                # data.ix[i, 'swings'] = row.Low - pivot
                data.ix[i, 'swings'] = row.Low
                pivot, last_pivot_id = row.Low, i
                # Change the rend indicator
                up_down = -1

        # Logic if the current trend is down.
        elif up_down == -1:
            # If got lower than last pivot, update the string
            if row.Low < pivot:
                # Remove the last pivot, as it wasn't a real one
                # OLD: data.ix[i,'swings']= data.ix[last_pivot_id,'swings'] + (row.Low - data.ix[last_pivot_id,'Low'])
                # OLD: data.ix[i,'swings']= (row.Low - data.ix[last_pivot_id,'Low'])
                data.ix[i,'swings']= row.Low
                data.ix[last_pivot_id,'swings']= 'NaN'
                pivot, last_pivot_id = row.Low, i
            elif row.High > pivot - diff:
                # data.ix[i, 'swings'] = row.High - pivot
                data.ix[i, 'swings'] = row.High
                pivot, last_pivot_id = row.High , i
                # Change the trend indicator
                up_down = 1

    # print data
    # print "PPHiLo" + outputString
    return data

# Abbreviation: (IC)
# This function helps define the necessary data for inchimoku charts.
# Source: http://stackoverflow.com/questions/28477222/python-pandas-calculate-ichimoku-chart-components
#
# import pandas.io.data as web
# import datetime
#
# start = datetime.datetime(2010, 1,1)
# end = datetime.datetime(2013, 1, 27)
# data=web.DataReader("F", 'yahoo', start,end)
# high_prices = data['High']
# close_prices =['Close']
# low_prices = data['low']
# dates= data.inddex
# nine_period_high = pd.rolling_max(data['High'], window = 9)
# nine_period_high = pd.rolling_min(data['low'], window = 9)
# ichimoku = (nine_period_high+ nine_period_high)/2
# ichimoku
#
# # Tenkan-sen (Conversion Line): (9-period high + 9-period low)/2))
# period9_high = pd.rolling_max(high_prices, window=9)
# period9_low = pd.rolling_min(low_prices, window=9)
# tenkan_sen = (period9_high + period9_low) / 2
#
# # Kijun-sen (Base Line): (26-period high + 26-period low) / 2))
# period26_high = pd.rolling_max(high_prices, window=26)
# period26_low = pd.rolling_min(low_prices, window=26)
# kijun_sen= (period26_high+ period26_low)/2
#
# # Senkou Span B (Leading Span A): (Conversion Line + Base Line)/2))
# senkou_span_a = ((tenkan_sen + kijun_sen)/2).shift(26)
#
# # Senkou Span B (Leading Span B): (52-period high + 52-period low)/2))
# period52_high = pd.rolling_max(high_prices, window=52)
# period52_low = pd.rolling_min(low_prices, window=52)
# senkou_span_b = ((period52_high + period52_low)/2).shift(26)
#
# # The most current closing price plotted 22 time periods behind (optional)
# chikou_span = close_prices.shift(-22) # 22 according to investopedia.
#
#
# # Abbreviation: (HMA) Hull Moving Average
# # Description: http://www.technicalindicators.net/indicators-technical-analysis/143-hma-hulls-moving-average
# # Instructions: Define your HMA time preiod first (eg. 16 days).
# # Once you have determined the period (n), here is the formula for Hull moving average:
# # Formula: HMA = WMA[integer(sqrt(n)))] of {2 * WMA[integer(n/2); Close]-WMA(n;Close)}
# # Explanation:
# # 1. Calculate WMA (weighted moving average) for half of the period(8-day) WMA in this case)
# # and multiply the result by 2.
# # 2. Calculate the WMA of the full period( 16-day WMA) and subtract it from the first result (2*WMA8).
# # 3. Calculate the square root of the full time period.
# # 4. Caclculate 4-day WMA from the result you got in step 2.
#
# # TODO: Create a function for HMA.
#
# # Abbreviation: (WMA) Weighted Moving Average
# # Description:
# # Instructions:
# # Source: http://stackoverflow.com/questions/18517722/weighted-moving-average-in-python
#
# from numpy.lib.stride_tricks import as_strided
#
# def moving_weighted_average(x, y, step_size=.1, steps_per_bin=10,
#                             weights=None):
#     # This ensures that all samples are within a bin
#     number_of_bins = int(np.ceil(np.ptp(x) / step_size))
#     bins = np.linspace(np.min(x), np.min(x) + step_size*number_of_bins,
#                        num=number_of_bins+1)
#     bins -= (bins[-1] - np.max(x)) / 2
#     bin_centers = bins[:-steps_per_bin] + step_size*steps_per_bin/2
#
#     counts, _ = np.histogram(x, bins=bins)
#     vals, _ = np.histogram(x, bins=bins, weights=y)
#     bin_avgs = vals / counts
#     n = len(bin_avgs)
#     windowed_bin_avgs = as_strided(bin_avgs,
#                                    (n-steps_per_bin+1, steps_per_bin),
#                                    bin_avgs.strides*2)
#
#     weighted_average = np.average(windowed_bin_avgs, axis=1, weights=weights)
#
#     return bin_centers, weighted_average
# #plot the moving average with triangular weights
# weights = np.concatenate((np.arange(0, 5), np.arange(0, 5)[::-1]))
# bins, average = moving_weighted_average(x, y, steps_per_bin=len(weights),
#                                         weights=weights)
# plt.plot(bins, average,label='moving average')
#
# plt.show()
#
# # Abbreviation: (SMA) Simple moving average
# # Description:
# # Instructions:
# # Source:
#
# import numpy as np
# from numpy import convolve
# import matplotlib.pyplot as plt
#
# def movingaverage (values, window):
#     weights = np.repeat(1.0, window)/window
#     sma = np.convolve(values, weights, 'valid')
#     return sma
#
# x = [1,2,3,4,5,6,7,8,9,10]
# y = [3,5,2,4,9,1,7,5,9,1]
#
# yMA = movingaverage(y,3)
# #print yMA
#
# plt.plot(x[len(x)-len(yMA):],yMA)
# plt.show()