import datetime as dt

import pandas as pd
from noaa_sdk import NOAA


# Get today's high temperature
def getTodaysHigh():
    n = NOAA()
    res = n.get_forecasts('78207', 'US', type='forecastGridData')
    maxTemp = res['maxTemperature']['values'][0]['value']
    fahrenheit = round((maxTemp * 9/5) + 32)
    return fahrenheit

# Get today's low temperature
def getTodaysLow():
    n = NOAA()
    res = n.get_forecasts('78207', 'US', type='forecastGridData')
    maxTemp = res['minTemperature']['values'][0]['value']
    fahrenheit = round((maxTemp * 9/5) + 32)
    return fahrenheit

# Get today's normal high temperature
def getNormalHigh(today):
    df = pd.read_csv('data/dailyMax.csv', index_col=0)
    return round(df.loc[today, 'DLY-TMAX-NORMAL'])

# Get today's normal low temperature
def getNormalLow(today):
    df = pd.read_csv('data/dailyMax.csv', index_col=0)
    return round(df.loc[today, 'DLY-TMIN-NORMAL'])

# Get today's date in this format 1/1/2022
def getToday():
    today = dt.datetime.today()
    return today.strftime('%-m/%-d/%y')

def getPositiveNegative(diff):
    if diff > 0:
        return '+' + str(diff) + '°'
    elif diff == 0:
        return str(diff) + '°'
    else:
        return '-' + str(diff) + '°'

todaysDate = getToday()
normalHigh = getNormalHigh(todaysDate)
normalLow = getNormalLow(todaysDate)
todaysHigh = getTodaysHigh()
todaysLow = getTodaysLow()
highDiff = getPositiveNegative(todaysHigh - normalHigh)
lowDiff = getPositiveNegative(todaysLow - normalLow)

df = pd.DataFrame()
df[''] = ['High', 'Low']
df['Today'] = [f'{todaysHigh}ºF', f'{todaysLow}ºF']
df['Normal'] = [f'{normalHigh}ºF', f'{normalLow}ºF']
df['Gap'] = [highDiff, lowDiff]

# print(df)

df.to_csv('data/table.csv', index=False)
