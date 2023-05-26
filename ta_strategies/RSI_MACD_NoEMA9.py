import sys
sys.path.append('../Thesis Practical Work')

import yfinance as yf 
import datetime as dt 
import matplotlib.pyplot as plt 
import pandas as pd 
import matplotlib.ticker as ticker 
import random 
import datetime as dt 
import ta 
from Configurations import start_date, end_date, liquidity, index, index1




def RSIMACDNoEma9(ticker):

    sp500_data = yf.download(ticker, start=start_date, end=end_date)
    current = sp500_data['Close'].iloc[0]
    equity = [current]
    action = "buy"
    operations_time_day=0

    buy_signal = 30
    sell_signal = 70

    # Compute the RSI index
    rsi = ta.momentum.RSIIndicator(sp500_data['Close'], window=14)
    sp500_data['RSI'] = rsi.rsi()

    #compute the MACD indicator
    macd = ta.trend.MACD(sp500_data['Close'])
    sp500_data['MACD'] = macd.macd()

 

   

    # Loop through the data and simulate the bot's behavior. in this case we have RSI with 30,50,70 configuration + MACD 0 cross configuration. 
    for k in range(1, len(sp500_data.index)-1):


        prev = sp500_data['Close'].iloc[k-1]
        current = sp500_data['Close'].iloc[k]
        differential_percentage = 1+((current - prev) / prev)

        #RSI RULES
        rsi30crossbuy = sp500_data.iloc[k-1]['RSI']<buy_signal and sp500_data.iloc[k]['RSI']>buy_signal and operations_time_day>10 and action=="sell"
        rsi70crossell = sp500_data.iloc[k-1]['RSI']>sell_signal and sp500_data.iloc[k]['RSI']<sell_signal and operations_time_day>10 and action=="buy"
        rsi50crossbuy = sp500_data.iloc[k-1]['RSI']<50 and sp500_data.iloc[k]['RSI']>50 and operations_time_day>10 and action=="sell"
        rsi50crosssell= sp500_data.iloc[k-1]['RSI']>50 and sp500_data.iloc[k]['RSI']<50 and operations_time_day>10 and action=="buy"

        #MACD RULES
        macd0crossbuy = sp500_data.iloc[k-1]['MACD']<0 and sp500_data.iloc[k]['MACD']>0 and operations_time_day>10 and action=="sell"
        macd0crosssell = sp500_data.iloc[k-1]['MACD']>0 and sp500_data.iloc[k]['MACD']<0 and operations_time_day>10 and action=="buy"

        if rsi30crossbuy:
            action = "buy"
            operations_time_day=0
        

        if rsi70crossell:
            action = "sell"
            operations_time_day=0
        

        if macd0crossbuy:
            action = "buy"
            operations_time_day=0
        

        if macd0crosssell:
            action = "sell"
            operations_time_day=0


        if rsi50crossbuy:
            action = "buy"
            operations_time_day=0
        

        if rsi50crosssell:
            action = "sell"
            operations_time_day=0


        if action=="buy": 
            equity.append(equity[-1]*differential_percentage)

        if action=="sell":
            equity.append(equity[-1])
        

        operations_time_day +=1 
    
    return sp500_data, equity, buy_signal, sell_signal




def plotting(sp500_data, equity, buy_signal, sell_signal): 

    fig, axs = plt.subplots(3)
    fig.suptitle('Equity Growth ' + index + ' with Trading Bot Technique:\n RSI with ('+str(buy_signal)+","+str(sell_signal)+') configuration + MACD', fontweight="bold", fontsize=16)

    axs[0].plot(plot_data['Date'], plot_data['Equity'])
    axs[0].plot(sp500_data['Close'], label=index + 'Close', color='red')

    axs[0].text(sp500_data.index[-1], plot_data['Equity'].iloc[-1], 'Equity', ha='left', va='bottom')
    axs[0].text(sp500_data.index[-1], sp500_data['Close'].iloc[-1], index + ' price', ha='left', va='bottom', color='red')

    axs[0].legend(['Equity', index + ' Close'], loc='upper left')
    axs[0].set_ylim(0, max(sp500_data['Close'].max(), plot_data['Equity'].max())*1.2)

    axs[1].plot(sp500_data.index, sp500_data['RSI'], color='purple')
    axs[1].plot(sp500_data.index,[sell_signal]*len(sp500_data['RSI']), color="red", linewidth=0.7)
    axs[1].plot(sp500_data.index,[buy_signal]*len(sp500_data['RSI']), color="green", linewidth=0.7)
    axs[1].plot(sp500_data.index,[50]*len(sp500_data['RSI']), color="black", linewidth=0.7)
    axs[1].legend(['RSI'], loc='upper left')
    axs[1].set_ylim(0, sp500_data['RSI'].max()*1.2)

    axs[2].plot(sp500_data.index, sp500_data['MACD'], color='orange')
    axs[2].plot(sp500_data.index,[0]*len(sp500_data['RSI']), color="black", linewidth=0.7)
    axs[2].legend(['MACD'], loc='upper left')
    axs[2].set_ylim(sp500_data['MACD'].min()*1.7, sp500_data['MACD'].max()*1.7)

    for i in range(0, 3):
     axs[i].spines['top'].set_visible(False)
     axs[i].spines['right'].set_visible(False)

    action = "buy"
    operations_time_day = 0


    for k in range(1, len(sp500_data.index)-1):

        #Rules repetition 
        rsi30crossbuy = sp500_data.iloc[k-1]['RSI']<buy_signal and sp500_data.iloc[k]['RSI']>buy_signal and operations_time_day>10 and action=="sell"
        rsi70crossell = sp500_data.iloc[k-1]['RSI']>sell_signal and sp500_data.iloc[k]['RSI']<sell_signal and operations_time_day>10 and action=="buy"
        rsi50crossbuy = sp500_data.iloc[k-1]['RSI']<50 and sp500_data.iloc[k]['RSI']>50 and operations_time_day>10 and action=="sell"
        rsi50crosssell= sp500_data.iloc[k-1]['RSI']>50 and sp500_data.iloc[k]['RSI']<50 and operations_time_day>10 and action=="buy"
        macd0crossbuy = sp500_data.iloc[k-1]['MACD']<0 and sp500_data.iloc[k]['MACD']>0 and operations_time_day>10 and action=="sell"
        macd0crosssell = sp500_data.iloc[k-1]['MACD']>0 and sp500_data.iloc[k]['MACD']<0 and operations_time_day>10 and action=="buy"
       

        if rsi30crossbuy:
            action = "buy"
            operations_time_day=0
            
            axs[0].axvline(x=sp500_data.index[k], color='green', alpha=1, ymin=0, ymax=1)
       
            axs[1].scatter(sp500_data.index[k], 30, s=250, color='green', alpha=1, linewidth=2, facecolor='none')


        if rsi70crossell:
            action = "sell"
            operations_time_day=0

            axs[0].axvline(x=sp500_data.index[k], color='red', alpha=1, ymin=0, ymax=1)
          
            axs[1].scatter(sp500_data.index[k], 70, s=250, color='red', alpha=1, linewidth=2, facecolor='none')
        
        if macd0crossbuy:
            action = "buy"
            operations_time_day=0

            axs[0].axvline(x=sp500_data.index[k], color='green', alpha=1, ymin=0, ymax=1)
         
            axs[2].scatter(sp500_data.index[k], 0, s=250, color='green', alpha=1, linewidth=2, facecolor='none')

        if macd0crosssell:
            action = "sell"
            operations_time_day=0

            axs[0].axvline(x=sp500_data.index[k], color='red', alpha=1, ymin=0, ymax=1)
          
            axs[2].scatter(sp500_data.index[k], 0, s=250, color='red', alpha=1, linewidth=2, facecolor='none')


        if rsi50crossbuy:
            action = "buy"
            operations_time_day=0

            axs[0].axvline(x=sp500_data.index[k], color='green', alpha=1, ymin=0, ymax=1)
        
            axs[1].scatter(sp500_data.index[k], 50, s=250, color='green', alpha=1, linewidth=2, facecolor='none')


        if rsi50crosssell:
            action = "sell"
            operations_time_day=0

            axs[0].axvline(x=sp500_data.index[k], color='red', alpha=1, ymin=0, ymax=1)

            axs[1].scatter(sp500_data.index[k], 50, s=250, color='red', alpha=1, linewidth=2, facecolor='none')


          

        operations_time_day+=1
    
    
    plt.ticklabel_format(style='plain', axis='y')
    plt.show()




if __name__=="__main__":
 
 sp500_data, equity, buy_signal, sell_signal = RSIMACDNoEma9(index1)
 sp500_data.index = pd.to_datetime(sp500_data.index)
 plot_data = pd.DataFrame({'Date': sp500_data.index[:-1], 'Equity': equity})
 plotting(sp500_data, equity, buy_signal, sell_signal)