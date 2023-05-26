import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
import random
import datetime as dt
import ta
from Configurations import start_date, end_date, liquidity, index, index1
#Import Benchmark Strategies (regular is absent cause it's just the index price itself)
from Benchmark_strategies.RandomStrat import randomStrat
from Benchmark_strategies.movingAvg import movingAvg
from ta_strategies.RSI_MACD_EMA9 import RSIMACDEma9
#Import Technical Analysis strategies 
from ta_strategies.RSI_MACD_NoEMA9 import RSIMACDNoEma9
from ta_strategies.RSI import RSIStrat


indexes = ["^GSPC", "^DJI", "^IXIC", "^FCHI", "^GDAXI", "^FTSE", "^N225"]
strats = [RSIMACDEma9, RSIMACDNoEma9, RSIStrat, movingAvg, randomStrat]


chosen_index = "^GSPC" #change it in one of the indexes above
chosen_strategy = RSIMACDEma9 #Change it in one of the strategies in the array above, the chosen strategy will be compared to index performance. 

#if you want to change the time window you have to do it in configurations settings. 

data, equity2, *_ = chosen_strategy(chosen_index)

fig, axs = plt.subplots(4, figsize=(10,8))
fig.suptitle('Trading Strategy returns on: ' +str(chosen_index) + " with " + str(chosen_strategy.__name__), fontweight="bold", fontsize=16)

axs[0].plot(data['Close'], label=chosen_index+ 'Close', color='red')
axs[0].text(data.index[-1], data['Close'].iloc[-1], chosen_index + ' price', ha='left', va='bottom', color='red')
axs[0].legend([chosen_index + ' Close'], loc='upper left')
axs[0].set_ylim(0, data['Close'].max()*1.3)

index_returns=[]
strategy_returns=[]

for k in range(1, len(data.index)-1, 1):

    prev = data['Close'].iloc[k-1]
    current = data['Close'].iloc[k]

    differential_percentage = ((current - prev) / prev)*100
    strat_performance = ((equity2[k]-equity2[k-1])/equity2[k-1])*100


    data.loc[data.index[k], 'strategy performance'] = strat_performance
    data.loc[data.index[k], 'Index performance'] = differential_percentage
    data.loc[data.index[k], 'Strat vs Index'] = strat_performance-differential_percentage

    index_returns.append(differential_percentage)

    average_strat_performance = data['strategy performance'].mean()


axs[2].plot(data['strategy performance'], label=index + 'Close', color='blue')
axs[2].legend(['strategy returns: '+str(chosen_strategy.__name__)], loc='upper left')
axs[2].axhline(y=0, color='black', linestyle='--')
axs[2].set_ylim(data['strategy performance'].min()*1.3, data['strategy performance'].max()*1.6)

axs[2].text(0.95, 0.95, f'Daily Avg: {average_strat_performance:.4f}%', transform=axs[2].transAxes, ha='right', va='top', fontweight="bold")


average_index_performance = data['Index performance'].mean()

axs[1].plot(data['Index performance'], label=index + 'Close', color='red')
axs[1].legend(['Index returns: ' + str(chosen_index)], loc='upper left')
axs[1].axhline(y=0, color='black', linestyle='--')
axs[1].set_ylim(data['Index performance'].min()*1.3, data['Index performance'].max()*1.6)
axs[1].text(0.95, 0.95, f'Daily Avg: {average_index_performance:.4f}%', transform=axs[1].transAxes, ha='right', va='top', fontweight="bold")



average_differential = data['Strat vs Index'].mean()
axs[3].plot(data['Strat vs Index'], label=index + 'Close', color='green')
axs[3].axhline(y=0, color='black', linestyle='--')

axs[3].legend(['Strategy returns (minus) Index returns'], loc='upper left')

axs[3].set_ylim(data['Strat vs Index'].min()*1.3, data['Strat vs Index'].max()*1.6)

axs[3].text(0.95, 0.95, f'Daily Avg: {average_differential:.4f}%', transform=axs[3].transAxes, ha='right', va='top', fontweight="bold")


plt.show()






