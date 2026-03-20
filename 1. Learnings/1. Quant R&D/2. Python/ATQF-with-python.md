# Quant Finance & Algo developement with python


### Tools
We need to install anaconda distribution from the google, and there is no anaconda prompt in mac so we need use our system terminal iteslf.

### Create Enviornment 
Normally conda configures the base enviornment in our terminal, we use one enviornment per project & install all the dependencies in it. If we dont use enviornments multiple projects can manipulate previous dependencies and previous code can stop working.

**Create New Enviornment**
So its necessary to create new enviornment for your project with `conda create --name envName python=3.8`, python 3.8 is last LTS version.

**Activate & Deactivate New Enviornment**
TO activate newly created enviornment `conda activate | deactivate envName` & 

**List enviornments**
If we want to get info on our all envs we can get with `conda info --envs`.

**Reinstall spyder for newly create enviornment**
Now we need to install `spyder` IDE for our new enviornment, we can do that through `conda install anaconda::spyder`.

### Get Data
To start with any analysis or research we need to get data. YahooFinance is best source to get the data of stocks, If we want to get that data thorugh excel or something we can do that through `https://finance.yahoo.com/quote/SILVERBEES.NS/history/`.

But getting data everytime manually from yahoo finance is not the optimal way so we can get that data programatically or by running a script with python.

Earlier best source was pandas but due to latest api changes we are going to install `yfinance` and we can install it via `conda install -c conda-forge yfinance`.

**Download data from yfinance**
We can download the data form yfinance thorugh `yfinance.download(tickers,params)` as mentioned below.

```
import yfinance as yf

data = yf.download("MSFT",period="6mo")

print(data)
```

**Ratelimit issue & Stooq Installation**
We are having issue with yfinance data download so we will be using stooq for data from onwards.

To install stooq we need to run `conda install -c conda-forge pandas pandas-datareader -y`.

**Get data with stooq**
```
import pandas_datareader.data as web

df = web.DataReader("MSFT", "stooq")
df.sort_index(inplace=True)   # Stooq returns reverse order

print(df)
```

**Download data for multiple tickers**
We can download the data for multiple tickers as well through python lists & for loop as mentioned below.

```
import pandas_datareader.data as web

stocks = ["AMZN", "MSFT", "INTC", "GOOG", "INFY.NS", "3988.HK"]

for ticker in stocks :
    df = web.DataReader("MSFT", "stooq")
    df.sort_index(inplace=True)   # Stooq returns reverse order
    print(df)
```

**Store data for multiple tickers in dict**
In this section we will be storing whole dataframe per symbol against that ticker in the dict.

```
import pandas_datareader.data as web
import pandas as pd

stocks = ["AMZN", "MSFT", "INTC", "GOOG", "INFY.NS", "3988.HK"]
cl_price = pd.DataFrame() #Dataframe initialisation.

ohlcv_data = {}

for ticker in stocks :
    df = web.DataReader("MSFT", "stooq")
    df.sort_index(inplace=True)   # Stooq returns reverse order
    ohlcv_data[ticker] = df
```


### Pandas dataframe
Its way to store the data in 2 dimensional way like excel, normally we get pre-installed in anaconda enviornment.

**How to create dataframe & assign data to it**
```
import pandas_datareader.data as web
import pandas as pd

stocks = ["AMZN", "MSFT", "INTC", "GOOG", "INFY.NS", "3988.HK"]
cl_price = pd.DataFrame() #Dataframe initialisation.

ohlcv_data = {}

for ticker in stocks :
    df = web.DataReader("MSFT", "stooq")
    df.sort_index(inplace=True)   # Stooq returns reverse order
    cl_price[ticker] = df['Close'] #storing closing price in dataframe
```


### Web scraping for data
In the earlier method we have accessed data with help of api, but we can get data by web scraping as well.

`Note - Using web scrapping for commercial use is not ethical and attract lawsuits as well, so reconsider the fact using web scrapping.`

--- Remaining ----

### Basic Data Handelling & Data Operations

We will learn basic data handelling & data operations in this section.

**How to deal with NaN values**
We can handle NaN values by replacing with static values such as 0 or specific symbol wise with help of dict.
```
# Fill NaN with 0 in close_price data frame
cl_price.fillna(0);

# Fill NaN with dict symbol based.
cl_price.fillna({"FB" : 0, "GOOG" : 1})
```

There are different methods as well for filling nan, like if 3 rows are NaN and then we get value the cell value we will have it will fill above NaN values with that value until another value appears from bottom to top.

```
cl_price.fillna(method='bfill', axis = 0, inplace = True)

# Options
- axis = 0 : it default fill values throgh column, if we want to replace with row next cell or something we can do that through this.
- inPlace = True : By default its false means it will fill the values where we are printing but it will not fill values in dataframe, when we make it true it will update NaN values in dataframe itself.
```

We can drop or  delete the rows wihich have nan values or even we can drop the column as well which have nan values thorugh `cl_price.dropna(axis=0, how='all')` or using configurable options within it.

### Basic Statistics
we might need to derive some basic stastical values from our data like mean, standard deviation, median etc. we will cover such utilities in this section.

```
# We care about percentage change
daily_return = cl_price.pt_change()

# Dataframe stastical utilities
# Get mean values of dataframe
daily_return.mean() 

# Get standard deviation values of dataframe.
daily_return.std() 

# Get min, 25%, 50%, 75% values in dataframe
daily_return.describe() 

# Shows only first 5 rows of dataframe, argument cusotmises that no of rows.
daily_return.head(noOfRows) 

# Shows last first 5 rows of dataframe, argument cusotmises that no of rows.
daily_return.tail(noOfRows) 

# Get percentage change as compared to previous days or row closing price.
daily_return.pct_change()

#Shift rows
daily_return.shift(1) # It shifts first 2 rows down, if negative shifts last 2 rows up.
```

### Rolling Mean (Grouping)
Now as we have saw we can draw mean or average or price of column earlier, but mostly we will need to calculate the average price of certain period to derive `Moving Average` but for that we need to group the data with required period.

**Data Grouping**
```
# Rolling - groups the data with provided rows on which we can find standard deviation, or mean or etc.

# Group the data of 10 rows so 10 days & mean of it means 10 day Simple Moving average
daily_return.rolling(window=10).mean()

# Exponential Moving average (More weight to recent return)
```
## Basic Chart Visualization (Using Panda's)

We can plot chart on dataframe with builtin function `df.plot()` which plots the data for that datafrme without doing anything manually.

<img src="./assets/pd-plot.png">

**Plotting Options :-**
- `subPlots=True` - If we want to seprate charts for seprate column in dataframe we can achieve the same.
    <img src="./assets/pd-subplots.png">

- `layout=(2,2)` - When we are using multiple charts through `subPlots` we can define the layout and we need to provide values in tuple.
  <img src="./assets/pd-subplots-layouts.png">

- `sharex=True` - Shares same axis throughout subplots, by default its true as we are dealing with timeseries.
  
- `title='Title for chart'` - Provides title for chart.
  
- `grid=True` - Provides background grid.

### Commulative Growth

Before going to Commulative Growth we need to understanding about compunded returns.

**Compunded Return :-**
Lets consider we have invested $100 in stocks and we have got returns as mentioned below.
- Day 1 - 10%
- Day 2 - 5%
- Day 3 - 10%

Now what will be value of our portfolio after day 3? We might think that 25% return we got in total so it will be $125 but no, It will be `$127.5` due to compunding.

How??

```
capital = 100;
returns = [10,5,10];

for day, dr in enumerate(returns):
    capital += capital * (dr/100)
    print('Day :',day,'Daily Return:', dr, 'Capital After Daily Return = $',capital)

Day : 0 Daily Return: 10 Capital After Daily Return = $ 110.0
Day : 1 Daily Return: 5 Capital After Daily Return = $ 115.5
Day : 2 Daily Return: 10 Capital After Daily Return = $ 127.05
```

**Compunded return using pandas :-**
We can simply calculate growth factor of daily return with `1 + daily return` & then on it we can use `comprod()` built-in method for calculating compunded return in our dataframe.

`Note - We usually plot compunded return of stocks to understand how much we would have earned in certain period`
<img src="./assets/comp-return.png">

## Data visualisation using `MatPlotLib`

In panda's we can do basic data visualisation and limited options provided but if we want to do advanced data visualization and if we want complete control then we will need to use `MatPlotLib`.

**How to use MatPlotLib :-**
- Import matplotlib pyplot package with `import matplotlib.pyplot as plt`.
- Unpack figure & axis objects from matplotlib with `fig, ax = plt.subplots()` where figure is canvas and axis are the figures to be drawn on canvas.
- Configure axis through `ax.set(titl='',xlabel='',ylabel='')` through available options.
- Display charts through `plt.bar(x=daily_returns.columns,height=daily_returns.std())` where we need to provide data for x axis and y axis data is passed as height as its being bar chart.

If you want to study deep about matPlotLib then we will need to go through its documentation but as of now we have covered how to use the matplotlib fundamentally.

## Technical Indicators

Technical indicators aer mathematical calculations based on historic price volumee or open intrest information to predict asset price direction. Its primary job is analyzing trends, chart patterns etc.

Most of the technical indicators are lagging indicators and people often use combination of technical indicators to get insights from it.

Popular technical indicators are MACD, BB, RSI, ADX, Supertrend, Renko Charts etc.

In python we will need to code the technical indicators, we can refer tradingview indicators documentation for mathematical formulations behind every indicator.

**MACD (Moving Average Convergence Divergence) :-**
MACD is trend following momentum indicator which is calculated by taking the difference of two moving averages of an asset price (typically 12 period MA and 26)
