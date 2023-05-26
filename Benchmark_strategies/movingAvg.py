import sys
sys.path.append('../Thesis Practical Work')

import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
from Configurations import start_date, end_date, liquidity, index, index1



def movingAvg(ticker):
    weeks_moving_avg = 2
    action = "buy"
    operations_time_day = 0
    sp500_data = yf.download(ticker, start=start_date, end=end_date)

    sp500_data['Ma_12w'] = sp500_data['Close'].rolling(window=weeks_moving_avg*5, min_periods=1).mean()  # multiplied by 5 cause trading week is 5 days. 

    current = sp500_data['Close'].iloc[0]
    equity = [current]


    # Loop through the data and apply behaviour. In this case moving average trading, when moving average crosses price and is above SELL, if it crosses price and is below BUY. 

    for k in range(1, len(sp500_data.index)-1):


        prev = sp500_data['Close'].iloc[k-1]
        current = sp500_data['Close'].iloc[k]
        differential_percentage = 1+((current - prev) / prev)

        if sp500_data.iloc[k]['Close']>sp500_data.iloc[k]['Ma_12w'] and operations_time_day>7 and action=="sell" and sp500_data.iloc[k-1]['Close']<sp500_data.iloc[k-1]['Ma_12w']:
            action = "buy"
            operations_time_day=0 
        
        if sp500_data.iloc[k]['Close']<sp500_data.iloc[k]['Ma_12w'] and operations_time_day>7 and action=="buy" and sp500_data.iloc[k-1]['Close']>sp500_data.iloc[k-1]['Ma_12w']:
            action = "sell"
            operations_time_day=0  




        if action=="buy": 
            equity.append(equity[-1]*differential_percentage)

        if action=="sell":
            equity.append(equity[-1])
        

        operations_time_day +=1 
    
    return sp500_data, equity, weeks_moving_avg




def plotting(sp500_data, equity, weeks_moving_avg):

    plot_data = pd.DataFrame({'Date': sp500_data.index[:-1], 'Equity': equity})
    plt.figure(figsize=(12, 6))
    plt.plot(plot_data['Date'], plot_data['Equity'])
    plt.plot(sp500_data['Close'], label='S&P 500 Close', color='red')
    plt.plot(sp500_data['Ma_12w'], label='S&P 500 12-Week Moving Average', color='green')
    plt.title('Equity Growth' + index + 'SP&500 with Trading Bot Technique:\n '+str(weeks_moving_avg) +' weeks moving average + price', fontweight="bold", fontsize=16)


    plt.text(sp500_data.index[-1], plot_data['Equity'].iloc[-1], 'Equity', ha='left', va='bottom')
    plt.text(sp500_data.index[-1], sp500_data['Close'].iloc[-1], index + 'Price', ha='left', va='bottom', color='red')
    plt.text(sp500_data.index[-1], sp500_data['Close'].iloc[-1]-500, 'Moving Average '+ str(weeks_moving_avg) +' weeks', ha='left', va='bottom', color='green')

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.ticklabel_format(style='plain', axis='y')


    action = "buy"
    operations_time_day = 0


    for k in range(1, len(sp500_data.index)-1):
         
    

        if sp500_data.iloc[k]['Close']>sp500_data.iloc[k]['Ma_12w'] and operations_time_day>7 and action=="sell" and sp500_data.iloc[k-1]['Close']<sp500_data.iloc[k-1]['Ma_12w']:
            action = "buy"
            operations_time_day=0

            
            plt.scatter(sp500_data.index[k], sp500_data.iloc[k]['Ma_12w'], s=200, color='green', alpha=1, linewidth=2, facecolor='none')   
          

        if sp500_data.iloc[k]['Close']<sp500_data.iloc[k]['Ma_12w'] and operations_time_day>7 and action=="buy" and sp500_data.iloc[k-1]['Close']>sp500_data.iloc[k-1]['Ma_12w']:
            action = "sell"
            operations_time_day=0

           
            plt.scatter(sp500_data.index[k], sp500_data.iloc[k]['Ma_12w'], s=200, color='red', alpha=1, linewidth=2, facecolor='none')   
          
        operations_time_day+=1
    

    plt.show()





if __name__=="__main__":
 
 sp500_data,equity, weeks_moving_avg = movingAvg(index1)

 plotting(sp500_data, equity, weeks_moving_avg)