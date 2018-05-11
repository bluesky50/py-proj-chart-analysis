import plotly
import pandas
import plotly.graph_objs as go
from plotly import tools
from plotly.tools import FigureFactory as FF
from analysisFunctions import formulateSMA, formulateRSI, brokenRSI, formulateEWMA, formulateHMA, formulateUltimateOscillator, formulatePPHiLo, formulateEMA, formulateSD, formulateSDev2, formulateWMA, formulatePPHiLo2, formulateSDevForPPHiLoDivergence, formulatePPHiLo3, formulateCMO
from analysisFunctionsNotes import get_pivots

# Create candlestick charts.
# Source: https://plot.ly/python/candlestick-charts/
def createCandlestickChart(df, graphTitle):
    print(">>> Function called createCandlestickChart(df, graphTitle)")
    # Setup the canvas
    main_canvas = tools.make_subplots(rows=2, cols=1, specs=[[{}], [{}]],
                              shared_xaxes=True, shared_yaxes=False,
                              vertical_spacing=0.001)


    # Adding Bars to show when the bot analysis is abov a certain level
    topLevel = 70
    bottomLevel = 30

    main_canvas['layout'].update({'shapes': [
            {
                'x0': df.index[0].date(), 'x1': df.index[-1].date(),
                'y0': topLevel, 'y1': topLevel, 'xref': 'x1', 'yref': 'y2',
                'line': {'color': 'rgb(179, 0, 134)', 'width': 0.7}
            },
            {
                'x0': df.index[0].date(), 'x1': df.index[-1].date(),
                'y0': bottomLevel, 'y1': bottomLevel, 'xref': 'x1', 'yref': 'y2',
                'line': {'color': 'rgb(179, 0, 134)', 'width': 0.7}
            }
        ]}
    )

    # Use figure factory to create a candlestick chart.
    # It also creates a canvas figure.
    fig = FF.create_candlestick(df.Open, df.High, df.Low, df.Close, dates=df.index)

    # Add the Candlestick data to the main canvas data array.
    main_canvas['data'] = fig['data']

    # Create traces based on methods.
    # topTraces = createTraces(df) # Returns an array of traces.
    # botTraces = createBotTraces(df) # returns an array of traces.

    # Section for test traces
    # get_pivots(df) #Creates a column in df that has pivots.

    ppHiLo = formulatePPHiLo(df, 7)

    pivotsTrace = go.Scatter(
        x=df.index,
        y=ppHiLo,  # The new column created by get pivots.
        mode='markers',
        line=dict(
            width=1,
            color='blue',
            # shape='hv'
        )
    )

    main_canvas.append_trace(pivotsTrace, 1, 1)
    # Add all traces to appropriate subplots on main canvas Figure.
    # appendAllTracesToTop(topTraces, main_canvas)
    # appendAllTracesToBot(botTraces, main_canvas)

    # Make final updates to the layout
    main_canvas['layout'].update(dict(title=graphTitle, yaxis=dict(domain=[0.25,1]),yaxis2=dict(domain=[0,0.2]), xaxis=dict(tickangle=-45, anchor='y2')))

    # help(plotly.graph_objs.graph_objs.Figure)
    # help(tools.make_subplots)

    # Render the Figure, main_canvas
    plotly.offline.plot(main_canvas)

def autoCreateTraces(dataArray, df):
    # TODO: Create comments and print statements

    traces = []

    for data in dataArray:
        # Create traces for analysis data.
        auto_trace = go.Scatter(
            x=df.index,
            y=data,  # insertElementsToNpArray(sma12d, 11, 'NaN'),
            line=dict(
                dash='dot',
                width=1.4)
        )
        traces.append[auto_trace]

    return traces

def createTraces(df):
    # TODO: Add comments and print functions.

    # sma12d = formulateSMA(df[u'Close'], 12)
    # sma26d = formulateSMA(df[u'Close'], 26)
    # sma50d = formulateSMA(df[u'Close'], 50)
    # wma14d = formulateWMA(df[u'Close'], 14)
    # ewma14d = formulateEWMA(df[u'Close'], 14)
    hma7d = formulateHMA(df[u'Close'], 7)
    ema3d = formulateEMA(hma7d, 3)
    ppHiLo7d = formulatePPHiLo(df, 7)
    # ppHiLo7d = formulatePPHiLo3(df, 7)

    # ppHiLo7dAll = formulatePPHiLo2(df, 7)
    # THIS DID't work for some reason, not sure why. ppWMA = formulateWMA(pandas.Series(ppHiLo7d), 1)
    ppWMA = formulateEWMA(pandas.Series(ppHiLo7d), 1)


    # The functions below are a part of the bottom plot .
    # sdev = formulateSD(pandas.Series(ppHiLo7d), 2)
    # rsi = formulateRSI(df[u'Close'])
    # uo = formulateUltimateOscillator(df, 7)

    traces = []

    # Create traces for analysis data.
    # trace_sma12d = go.Scatter(
    #     x=df.index,
    #     y=sma12d,  # insertElementsToNpArray(sma12d, 11, 'NaN'),
    #     name='SMA (12d)',
    #     line=dict(
    #         color=('blue'),
    #         width=1.4)
    # )
    #
    # trace_sma26d = go.Scatter(
    #     x=df.index,
    #     y=sma26d,  # insertElementsToNpArray(sma26d, 25, 'NaN'),
    #     name='SMA (26d)',
    #     line=dict(
    #         color=('black'),
    #         width=1.4,
    #         dash='dot'
    #     )
    # )
    # trace_sma50d = go.Scatter(
    #     x=df.index,
    #     y=sma50d,  # insertElementsToNpArray(sma26d, 25, 'NaN'),
    #     name='SMA (50d)',
    #     line=dict(
    #         color=('black'),
    #         width=1.4,
    #         dash='dot'
    #     )
    # )

    # trace_wma14d = go.Scatter(
    #     x=df.index,
    #     y=wma14d,  # insertElementsToNpArray(sma26d, 25, 'NaN'),
    #     name='WMA (14d)',
    #     line=dict(
    #         color=('black'),
    #         width=1.4,
    #         dash='dot'
    #     )
    # )

    #
    # trace_ewma14d = go.Scatter(
    #     x=df.index,
    #     y=ewma14d,  # insertElementsToNpArray(sma26d, 25, 'NaN'),
    #     name='EWMA (14d)',
    #     line=dict(
    #         color=('green'),
    #         width=1.4,
    #         dash='dot'
    #     )
    # )

    trace_hma7d = go.Scatter(
        x=df.index,
        y=hma7d,  # insertElementsToNpArray(sma26d, 25, 'NaN'),
        name='HMA (7d)',
        line=dict(
            color=('gray'),
            width=1.4,
            # dash='dot'
        )
    )

    trace_ema3d = go.Scatter(
        x=df.index,
        y=ema3d,  # insertElementsToNpArray(sma26d, 25, 'NaN'),
        name='EMA (3d, HMA7)',
        line=dict(
            color=('k'),
            width=1.4,
            # dash='dot'
        )
    )

    trace_ppHiLo7d = go.Scatter(
        x=df.index,
        y=ppHiLo7d,  # The new column created by get pivots.
        name='PPHiLow',
        mode='markers',
        line=dict(
            width=1,
            color='blue',
            shape='hv'
        )
    )

    trace_ppWMA = go.Scatter(
        x=df.index,
        y=ppWMA,  # The new column created by get pivots.
        name='WMA (PPHiLow)',
        # mode='line',
        line=dict(
            width=1,
            color='gray',

        )
    )

    # traces.append(trace_sma12d)
    # traces.append(trace_sma26d)
    # traces.append(trace_wma14d)
    # traces.append(trace_ewma14d)
    traces.append(trace_ema3d)
    # traces.append(trace_sma50d)
    traces.append(trace_hma7d)
    traces.append(trace_ppHiLo7d)
    traces.append(trace_ppWMA)

    return traces

def createBotTraces(df):
    # rsi = formulateRSI(df[u'Close'])
    # uo = formulateUltimateOscillator(df, 7)
    # hma7d = formulateHMA(df['Close'], 7)
    cmo = formulateCMO(df['Close'], 20)

    # ppHiLo7d = formulatePPHiLo(df, 7, append_value=0)
    ppHiLo7dAll = formulatePPHiLo2(df, 7)
    # ppHiLo7dAll = formulatePPHiLo3(df, 7)
    # print(ppHiLo7d)
    # ppWMA = formulateEWMA(pandas.Series(ppHiLo7d), 1)
    # ppWMA = formulateEWMA(pandas.Series(ppHiLo7dAll), 1)
    # sdev = formulateSD(pandas.Series(ppWMA), 2)
    # sdev = formulateSDev2(ppHiLo7dAll, 7)
    sdev = formulateSDev2(ppHiLo7dAll, 10)
    # sdev = formulateSDevForPPHiLoDivergence(ppHiLo7dAll, df, 2)

    traces = []

    # Plot for the RSI
    # trace_rsi = go.Scatter(
    #     x=df.index,
    #     y=rsi,
    #     fill='tozeroy',
    #     name='RSI',
    #     line=dict(
    #         color=('gray'),
    #         width=1.4,
    #         dash='dot'
    #     )
    # )

    # Create bar trace for volume data.
    trace_volume = go.Bar(
        x=df.index,
        y=df.Volume,
        name = 'Volume',
        marker=dict(
            color='rgb(193,194,184)',
            # line=dict(
                # color='rgb(8,48,107)',
                # width=1.5,
            #)
        ),
        opacity = 1
    )

    # Plot CMO Trace
    trace_cmo = go.Scatter(
        x=df.index,
        y=cmo,
        # fill='tozeroy',
        name='CMO (HMA7d)',
        line=dict(
            color=('gray'),
            width=1.4,
            # dash='dot'
        )
    )

    # Plot for the Ultimate Oscillator
    # trace_uo = go.Scatter(
    #     x=df.index,
    #     y=uo,
    #     # fill='tozeroy',
    #     name='UO',
    #     line=dict(
    #         color=('gray'),
    #         width=1.4,
    #         dash='dot'
    #     )
    # )

    # Plot for the Standard Deviation
    trace_sdev = go.Scatter(
        x=df.index,
        y=sdev,
        fill='tozeroy',
        name='SDev (PPHiLo)',
        line=dict(
            color=('gray'),
            width=1.4,
            # dash='dot'
        )
    )

    traces.append(trace_volume)
    traces.append(trace_sdev)
    # traces.append(trace_uo)
    traces.append(trace_cmo)
    # traces.append(rsi)

    return traces

def appendAllTracesToTop(traceArray, mainCanvas):
    for trace in traceArray:
        mainCanvas.append_trace(trace, 1, 1)

def appendAllTracesToBot(traceArray, mainCanvas):
    for trace in traceArray:
        mainCanvas.append_trace(trace, 2, 1)

def createHiLoChart(df):
    print(">>> Function called createCandlestickChart(df, graphTitle)")
    fig = FF.create_ohlc(df.Open, df.High, df.Low, df.Close, dates=df.index)
    plotly.offline.plot(fig, validate=False)

def createLineChart(df, graphTitle):
    print(">>> Function called createLineChart(df, graphTitle)")
    # Add data
    date = df.index
    open = df.Open
    high = df.High
    low = df.Low
    close = df.Close

    # Create and style traces
    # trace_open = go.Scatter(
    #     x=date,
    #     y=open,
    #     name='Open',
    #     line=dict(
    #         color=('rgb(51, 153, 129)'),
    #         width=1)
    # )
    trace_high = go.Scatter(
        x=date,
        y=high,
        name='High',
        line=dict(
            color=('rgb(22, 96, 167)'),
            width=3,
            dash='dot')
    )
    trace_low = go.Scatter(
        x=date,
        y=low,
        name='Low',
        line=dict(
            color=('rgb(205, 12, 24)'),
            width=3,
            dash='dot')  # dash options include 'dash', 'dot', and 'dashdot'
    )
    trace_close = go.Scatter(
        x=date,
        y=close,
        name='Close',
        line=dict(
            color=('rgb(176, 63, 191)'),
            width=1)
    )
    # trace4 = go.Scatter(
    #     x=date,
    #     y=high_2000,
    #     name='High 2000',
    #     line=dict(
    #         color=('rgb(205, 12, 24)'),
    #         width=4,
    #         dash='dot')
    # )
    # trace5 = go.Scatter(
    #     x=date,
    #     y=low_2000,
    #     name='Low 2000',
    #     line=dict(
    #         color=('rgb(22, 96, 167)'),
    #         width=4,
    #         dash='dot')
    # )

    # ppHiLo = formulatePPHiLo(df, 7)
    #
    # pivotsTrace = go.Scatter(
    #     x=df.index,
    #     y=ppHiLo,  # The new column created by get pivots.
    #     mode='markers',
    #     line=dict(
    #         width=1,
    #         color='blue',
    #         shape='hv'
    #     )
    # )
    #
    # # main_canvas.append_trace(pivotsTrace, 1, 1)
    #
    # ppWMA = formulateEWMA(pandas.Series(ppHiLo), 1)
    #
    # trace_ppWMA = go.Scatter(
    #     x=df.index,
    #     y=ppWMA,  # The new column created by get pivots.
    #     # mode='line',
    #     line=dict(
    #         width=1,
    #         color='gray',
    #
    #     )
    # )

    # data = [trace0, trace1, trace2, trace3, pivotsTrace, ppWMA] #, trace4, trace5]
    # data = [trace1, trace2, trace_ppWMA, pivotsTrace] #, trace4, trace5]
    # Create traces based on methods.


    main_canvas = tools.make_subplots(rows=2, cols=1, specs=[[{}], [{}]],
                                      shared_xaxes=True, shared_yaxes=False,
                                      vertical_spacing=0.001)


    # Adding Bars to show when the bot analysis is abov a certain level
    topLevel = 10
    bottomLevel = 5

    main_canvas['layout'].update({'shapes': [
        {
            'x0': df.index[0].date(), 'x1': df.index[-1].date(),
            'y0': topLevel, 'y1': topLevel, 'xref': 'x1', 'yref': 'y2',
            'line': {'color': 'rgb(179, 0, 134)', 'width': 0.7}
        },
        {
            'x0': df.index[0].date(), 'x1': df.index[-1].date(),
            'y0': bottomLevel, 'y1': bottomLevel, 'xref': 'x1', 'yref': 'y2',
            'line': {'color': 'rgb(179, 0, 134)', 'width': 0.7}
        }
    ]}
    )

    # Make final updates to the layout
    main_canvas['layout'].update(dict(title=graphTitle, yaxis=dict(domain=[0.25, 1]), yaxis2=dict(domain=[0, 0.2]),
                                      xaxis=dict(tickangle=-45, anchor='y2')))


    topTraces = createTraces(df) # Returns an array of traces.
    botTraces = createBotTraces(df)
    # Add all traces to appropriate subplots on main canvas Figure.
    #
    # # Edit the layout
    # layout = dict(title=graphTitle,
    #               xaxis=dict(title='Date'),
    #               yaxis=dict(title='Price'),
    #               )

    # Plot and embed in ipython notebook!
    main_canvas.append_trace(trace_high, 1, 1)
    main_canvas.append_trace(trace_low, 1, 1)
    main_canvas.append_trace(trace_close, 1, 1)
    appendAllTracesToTop(topTraces, main_canvas)
    appendAllTracesToBot(botTraces, main_canvas)
    plotly.offline.plot(main_canvas)

def createLineChart2(df, graphTitle):
    print(">>> Function called createLineChart(df, graphTitle)")


    main_canvas = tools.make_subplots(rows=4, cols=1, specs=[[{}], [{}],[{}],[{}]],
                                      shared_xaxes=True, shared_yaxes=False,
                                      vertical_spacing=0.01)


    # Adding Bars to show when the bot analysis is abov a certain level
    # topLevel = 10
    # bottomLevel = 5
    #
    # main_canvas['layout'].update({'shapes': [
    #     {
    #         'x0': df.index[0].date(), 'x1': df.index[-1].date(),
    #         'y0': topLevel, 'y1': topLevel, 'xref': 'x1', 'yref': 'y2',
    #         'line': {'color': 'rgb(179, 0, 134)', 'width': 0.7}
    #     },
    #     {
    #         'x0': df.index[0].date(), 'x1': df.index[-1].date(),
    #         'y0': bottomLevel, 'y1': bottomLevel, 'xref': 'x1', 'yref': 'y2',
    #         'line': {'color': 'rgb(179, 0, 134)', 'width': 0.7}
    #     }
    # ]}
    # )

    # Add data
    date = df.index
    open = df.Open
    high = df.High
    low = df.Low
    close = df.Close

    # Create and style traces
    # trace_open = go.Scatter(
    #     x=date,
    #     y=open,
    #     name='Open',
    #     line=dict(
    #         color=('rgb(51, 153, 129)'),
    #         width=1)
    # )
    trace_high = go.Scatter(
        x=date,
        y=high,
        name='High',
        line=dict(
            color=('rgb(22, 96, 167)'),
            width=3,
            dash='dot')
    )
    trace_low = go.Scatter(
        x=date,
        y=low,
        name='Low',
        line=dict(
            color=('rgb(205, 12, 24)'),
            width=3,
            dash='dot')  # dash options include 'dash', 'dot', and 'dashdot'
    )
    trace_close = go.Scatter(
        x=date,
        y=close,
        name='Close',
        line=dict(
            color=('rgb(176, 63, 191)'),
            width=1)
    )


    # Plot and embed in ipython notebook!
    main_canvas.append_trace(trace_high, 1, 1)
    main_canvas.append_trace(trace_low, 1, 1)
    main_canvas.append_trace(trace_close, 1, 1)

    # Create traces based on methods.
    topTraces = createTraces(df)  # Returns an array of traces.
    botTraces = createBotTraces(df)

    # Add all traces to appropriate subplots on main canvas Figure.
    appendAllTracesToTop(topTraces, main_canvas)
    # appendAllTracesToBot(botTraces, main_canvas)
    main_canvas.append_trace(botTraces[0], 2, 1)
    main_canvas.append_trace(botTraces[1], 3, 1)
    main_canvas.append_trace(botTraces[2], 4, 1)
    # botTraces[2].append_trace(main_canvas, 4, 1)
    # Make final updates to the layout
    main_canvas['layout'].update(dict(title=graphTitle,
                                      yaxis=dict(domain=[0.48, 1]),
                                      yaxis2=dict(domain=[0.32, 0.48]),
                                      yaxis3=dict(domain=[0.16, 0.32]),
                                      yaxis4=dict(domain=[0, 0.16]),
                                      xaxis=dict(tickangle=-45, anchor='y4')))

    plotly.offline.plot(main_canvas)
