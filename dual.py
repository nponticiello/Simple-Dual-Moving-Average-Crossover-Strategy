import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

data = pd.read_csv('AAPL.csv')

#visualize the data

plt.figure(figsize = (12.5 , 4.5))
plt.plot(data['Adj Close'], label = 'AAPL')
plt.title('Apple Adj. Close Price History')
plt.xlabel('June. 11, 2008 - Oct. 14, 2008')
plt.ylabel('Adj Close Price US($)')
plt.legend(loc = 'upper left')

#create simple moving average with 15 day window

SMA15 = pd.DataFrame()
SMA15['Adj Close'] = data['Adj Close'].rolling(window = 15).mean()
SMA30 = pd.DataFrame()
SMA30['Adj Close'] = data['Adj Close'].rolling(window = 30).mean()

#visualize the Data
plt.figure(figsize = (12.5 , 4.5))
plt.plot(data['Adj Close'], label = 'AAPL')
plt.plot(SMA15['Adj Close'], label = 'SMA15')
plt.plot(SMA30['Adj Close'], label = 'SMA30')
plt.title('Apple Adj. Close Price History')
plt.xlabel('June. 11, 2008 - Oct. 14, 2008')
plt.ylabel('Adj Close Price US($)')
plt.legend(loc = 'upper left')

#Create a new data frame to store all the Data
new_data = pd.DataFrame()
new_data['data'] = data['Adj Close']
new_data['SMA30'] = SMA30['Adj Close']
new_data['SMA15'] = SMA15['Adj Close']


#create a function to signal when to buy and seel the asset/stocks
def buy_sell(new_data):
    sigPriceBuy = []
    sigPriceSell = []
    flag = -1

    for i in range(len(data)):
        if new_data['SMA15'][i] > new_data['SMA30'][i]:
            if flag != 1:
                sigPriceBuy.append(new_data['data'][i])
                sigPriceSell.append(np.NaN)
                flag = 1
            else:
                sigPriceBuy.append(np.NaN)
                sigPriceSell.append(np.NaN)
        elif new_data['SMA15'][i] < new_data['SMA30'][i]:
                    if flag != 0:
                        sigPriceBuy.append(np.NaN)
                        sigPriceSell.append(new_data['data'][i])
                        flag = 0
                    else:
                        sigPriceBuy.append(np.NaN)
                        sigPriceSell.append(np.NaN)
        else:
                    sigPriceBuy.append(np.NaN)
                    sigPriceSell.append(np.NaN)
    return(sigPriceBuy,sigPriceSell)


#Store the buy and sell data into a variable

buy_sell = buy_sell(new_data)
new_data['Buy_Signal_Price'] = buy_sell[0]
new_data['Sell_Signal_Price'] = buy_sell[1]


#visualize the data and the strategy to buy and sell the stock

plt.figure(figsize = (12.5, 4.5))
plt.plot(new_data['data'],label = 'AAPL',alpha = 0.35)
plt.plot(new_data['SMA15'], label = 'SMA15',alpha = 0.35)
plt.plot(new_data['SMA30'], label = 'SMA30',alpha = 0.35)
plt.scatter(new_data.index,new_data['Buy_Signal_Price'], label = 'Buy' , marker = '^' , color = 'green')
plt.scatter(new_data.index, new_data['Sell_Signal_Price'], label = 'Sell', marker = 'v', color = 'red')
plt.title('AAPl Adj Close Price History Buy & Sell Signals')
plt.xlabel('June. 11, 2008 - Oct. 14, 2008')
plt.ylabel('Adj Close Price US($)')
plt.legend(loc = 'upper left')
plt.show()
