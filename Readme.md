Dependencies:

-Python==3.10.10
-yfinance==0.2.17
-ta==0.10.2
-matplotlib==3.7.0
-pandas==1.5.3


1. **Folder's Structure**

-Benchmark_strategies: this folder contains 3 python scripts that implement the most basic strategies: Random trading, buy and hold and moving average trading. Results are then plotted

-ta_strategies: this folder contains 3 python scripts that implement strategies using RSI, the most important technical analysis index to asses overbought/oversold market conditions. Results are then plotted

-Configurations.py: this script defines the parameters that you want to use in all the strategy implementation scripts such as the start and end date as well as the index. 

-Comparison.py: this scripts lets you chose a strategy and an index and compares the returns of the two over a time window (you have to change it in Configurations.py). 


2. **General Implementation info:**

In all the strategies implementations I have implemented the following logic:

-your amount of trades is limited (to avoid excessive commission costs in real world application, I did not implement any commition logic yet!). usually 
7 to 10 days depending on the strategy. Therefore you will find often a variable called "operations_time_day" that basically acts like a counter. 

-The implementation is Discrete. Each day is one step. This happens because i have only took the 'Close' price of the indexes (and therefore all the ta indexes are computed on this discrete price movements, therefore they are also discrete). I made this choice so that my computations were faster as well as simplifyng the process making it less error prone. 

-There is just a "buy" or "sell" status. Essentially if you have a "buy" status your equity movements copy the index movements. If index does +5% the equity will do +5%. The "Sell" status assumes that you sold everything, therefore the equity while thet status is "sell" will be flat, essentially staying the same untile a new "buy" status comes. 

-you start having all your money invested in the index, essentially you start with a "buy" status. Then the strategies start to play out. The amount you start with is equal to the start of the index, such that we can easily compare the performance of the strategy against the index. 

-when you are in a "sell" status the equity will be flat as, in that period, you should have a cash position (therefore not affected by stock indexes movements). This is very easy to see on smaller time frames. 



if you have any trouble understanding or running something contact me!