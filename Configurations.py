from datetime import datetime, timedelta
import yfinance as yf

current_date = datetime.now()
one_day_ago = current_date - timedelta(days=1)
date_string = one_day_ago.strftime('%Y-%m-%d')

#Liquidity alaways starts with 0 as we start with full investment in the index. When we sell the value gets updated accordingly. 

liquidity = [0]

indexes = {
  "sp500": "^GSPC",
  "euro stoxx 50": "^STOXX50E",
  "ftse mib": "^FTSE",
  "cac 40": "^FCHI",
  "Sensex(Indian stock exachange index)":"^BSESN",
  "Japan Index": "^N255"
}

#Parameters you want to modify:

start_date = "2022-01-01" #DISCLAIMER: I suggest you to put at maximum 3 years if you want to run scripts in "ta_strategies" or "Benchmark_strategies" as, otherwise, the
                          #charts would become undreadable due to the amount of buy and sell signals. 
                          #These scripts should be ran just to have an idea of a strategy performance and work pattern and check if the strategy is correctly implemented. 
                          #if you plan to run "Comparison.py" or other statistics related scripts you can put any time window without any drawback. 

end_date = date_string

index = "sp500" #check indexes dictionary above

index1 = "CSV"#indexes[index]

sp500_data = yf.download(index1, start=start_date, end=end_date)

current = sp500_data['Close'].iloc[0]
equity = [current]



