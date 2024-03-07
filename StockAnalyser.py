
'''
@author: 
Quinn Tian 
Bryan Martyn
Reetu Bok
@copyright: 
    Quinn Tian owns the copyright of this model and application.
    No any distribution is permitted without her consent. 
 '''
# This file retrieves the asset's data from websites like Yahoo or Google finance,  
# does regression analysis on asset's return and markets return, and generate the predicted returns.
import pandas as pd
import numpy as np
import datetime

import matplotlib.pyplot as plt

import yfinance as yf
import requests
from bs4 import BeautifulSoup

'''CITATION: The regression code is from the link:
https://stackoverflow.com/questions/38676323/is-it-possible-to-get-monthly-historical-stock-prices-in-python
'''
# this function is to return regression coefficients of two series of numbers
def estimate_coef(x, y): 
    # number of observations/points 
    n = np.size(x) 
  
    # mean of x and y vector 
    m_x, m_y = np.mean(x), np.mean(y) 
  
    # calculating cross-deviation and deviation about x 
    SS_xy = np.sum(y*x) - n*m_y*m_x 
    SS_xx = np.sum(x*x) - n*m_x*m_x 
  
    # calculating regression coefficients 
    b_1 = SS_xy / SS_xx 
    b_0 = m_y - b_1*m_x 
  
    return(b_0, b_1)

'''treasury bill monthly rate'''
# this function is to get monthly risk free returns from the downloaded csv file
def monthlyTBReturns():
     downloadTB=pd.read_csv("TB3MS.csv")# annual return of 3-month TB file is downloaded
     dataTB=downloadTB[2:]
     
     ''' use np to calculate monthly return:'''
     dataTB['Monthly Return TB']=dataTB['TB3MS']/1200 # to get monthly return
     
    
     return dataTB
 

# riskFreeReturn is a global variable:
dataTB=monthlyTBReturns() 
# TB_returns=dataTB['Monthly Return TB'] 
TB_returns=np.array(dataTB['Monthly Return TB'] )


# this function is to get S&P monthly returns array
def monthlySPReturns():
    
     # download 3 years of S&P price from Yahoo finance
     data = yf.download('^GSPC', start="2021-01-01", end="2024-01-01") # new code
     month_end_prices = data['Adj Close'].resample('ME').last()
     
     # calculate monthly Return 
     m_returns=month_end_prices.pct_change()
     # print("\nSP montly returns: \n", m_returns)
     # exclude the first row since percentage change starts from the second row
     return np.array(m_returns[1:]) 

  
 
# Asset class is for the collection of stocks 
class Asset(object):
    # init function of any instance with stock ticker
    def __init__(self, ticker):
        self.ticker=ticker
    # download 3 years of daily stock price data from Yahoo finance
    def getData(self):
        data = yf.download(self.ticker, start="2021-01-01", end="2024-01-01") # new code
        # print("\n3 year\n", data.head())
        # print("rows of the data daily: ", len(data))
        df=pd.DataFrame(data["Adj Close"])
        # print("daily price: \n", df.head())
                
        return df 
       
    
    #  download 3 years of monthly stock prices
    # Note: 2 sets of code is provided here. The method 2 is to meet API download requirement
    # In case of the limited usage of free API key, so mothod 1 is a safer option.   
    def getMonthlyData(self):
        # method 1: use yfinance package, like an API from yahoo finance
        
        data = yf.download(self.ticker, start="2021-01-01", end="2024-01-01") # new code
        month_end_prices = data['Adj Close'].resample('ME').last()
        
        # print("\n3 year monthly\n", month_end_prices)
        # print("rows of the data montly: ", len(month_end_prices))
        df=pd.DataFrame(month_end_prices)
      
        
        # mothod 2: use API  # key='S3XLG8C4CWQCWWYY'
        
        # url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol='
        # +str(self.ticker)+'&time_from=20220410T0130&apikey=KQRUDSKQT2REFLD5'
       

        # r = requests.get(url)
        # data = r.json()
        # monthlyPrice=[]
        # for key in data: 
        #     if key=='Monthly Adjusted Time Series':
        #         for key in data['Monthly Adjusted Time Series']:
        #             if (key>'2020-12-31' and key<'2024-01-01'):
                    
        #                 # print (data['Monthly Adjusted Time Series'][key]['5. adjusted close']) 
        #                 monthlyPrice.append(float(data['Monthly Adjusted Time Series'][key]['5. adjusted close']))
        #                # print(len(monthlyPrice))
        # df=pd.DataFrame(monthlyPrice)
        
        return df
        
                        
           
    # this method is to calculate the daily returns and return as an array
    def getDailyReturns(self):
        df=self.getData()
        d_returns=df.pct_change()
        
        return np.array(d_returns[1:])

    # this method is to calculate the average monthly returns from daily returns and return as array
    def averageMonthlyReturn(self):
        d_returns=self.getDailyReturns()
        m_return=np.exp(np.sum(np.log(d_returns+1)/36))-1
        return m_return 

    # this method is to calculate the average annual return of the stock
    def averageAnnualReturn(self):
        d_returns=self.getDailyReturns()
        a_return=np.exp(np.sum(np.log(d_returns+1)/3))-1
        return a_return

    # this method is to calculate the volatility of a stock prices
    def getVolatility(self):
        d_returns=self.getDailyReturns()
        a_volatility=np.std(d_returns)*np.sqrt(251)
        return a_volatility

    # this method is to calculate the monthly returns from the monthly price data
    # and return as an array
    def monthlyReturnArray(self):
        df=self.getMonthlyData()
        m_returns=df.pct_change()
        
        return np.array(m_returns[1:])

    # this method is to calculate the excess returns on top the risk free returns
    #  for both the stock and the market, returns as a tuple of 2 arrays
    def excessReturnArray(self):
        m_returns=np.array(self.monthlyReturnArray())
        # print('m_________',np.size(m_returns))        
        # print('tb________', np.size(TB_returns))

        excess_returns=np.subtract(m_returns,TB_returns)
        m_returns_SP=monthlySPReturns()
        # print('sp________', np.size(m_returns_SP))
        excessReturns_SP=np.subtract(m_returns_SP,TB_returns)
        return excessReturns_SP, excess_returns

    # this method is to get the log reguression coefficients
    # between the market excess returns and the stock excess returns
    def logRegression(self):
        excessReturns_SP, excess_returns=self.excessReturnArray()
        x,y=np.log(excessReturns_SP+1),np.log(excess_returns+1)
        alpha, beta=estimate_coef(x, y)

        # plt.plot(x, y, 'o')
        # plt.plot(x, beta*x + alpha)
        # plt.xlabel('SP Excess Returns')
        # plt.ylabel('Asset Excess Returns')
        # plt.title(f'Regression on Excess Returns of {self.ticker} over Market')
        # plt.show()
        # plt.close()

        return alpha, beta
    
    # this method is to draw and show the regression graph based on the logRegression() method
    def plotRegression(self):
        excessReturns_SP, excess_returns=self.excessReturnArray()
        x,y=np.log(excessReturns_SP+1),np.log(excess_returns+1)
        alpha, beta=estimate_coef(x, y)
        alpha_pct=str(round(alpha*100, 2)) + '%'
        beta_pct=str(round(beta*100, 2)) + '%'
        
        # plotting and labeling
        plt.plot(x, y, 'o')
        plt.plot(x, beta*x + alpha)
        plt.xlabel('SP Excess Returns')
        plt.ylabel('Asset Excess Returns')
        plt.title(f'Regression on Excess Returns of {self.ticker} over Market')
        plt.show()
        plt.close()
        
        # print the Alpha and Beta values in console
        print(f"""The coefficients from the regression over market return:
Alpha: {alpha_pct}, 
Beta: {beta_pct}""")
        
    # This method is to calculate the projected monthly returns array
    def predictedMonthlyReturns(self):
        alpha, beta=self.logRegression()          
        excessReturn_SP, excess_returns=self.excessReturnArray()
        x,y=np.log(excessReturn_SP+1),np.log(excess_returns+1)

        predicted_log_excess=alpha+beta*x
        predicted_excess_m=np.exp(alpha+beta*x)-1  
        
        # risk_free_returns is TB_returns
        predicted_returns_m=predicted_excess_m+TB_returns
        
        return predicted_returns_m  

    # This method is to calculate the projected annual risk return rate
    def predictedAnnualReturn(self):
        predicted_returns_m=self.predictedMonthlyReturns()
        predicted_return_a=np.exp(np.sum(np.log(predicted_returns_m+1))/3)-1
        return predicted_return_a     
    
    # This method is to generate all the monthly returns table, 
    # not called in the current MVP product but kept for future use
    def monthlyTable(self):        
        returns_m=(self.monthlyReturnArray())
        average_returns_m=self.averageMonthlyReturn()
        excessReturns_SP, excess_returns=self.excessReturnArray()
        predicted_returns_m=self.predictedMonthlyReturns()

        returns_table=pd.DataFrame({"returns_m": returns_m, "average_returns_m": \
            average_returns_m, "excessReturns_SP": excessReturns_SP, \
                "excess_returns": excess_returns, \
                "predicted_returns_m":predicted_returns_m})
        
        return returns_table
    
    # This method is the print the results summary table in the console
        
    def summaryTable(self):
        a_return=self.averageAnnualReturn()
        a_predicted_return=self.predictedAnnualReturn()
        a_volatility=self.getVolatility()
        alpha, beta=self.logRegression()

        summary1=dict({"Average Anual Return": a_return, 
                         "Predicted Annual Return": a_predicted_return, 
                         "Annual Volatility": a_volatility, 
                         "Alpha": alpha, "Beta": beta  })

        a_return_pct=str(round(a_return*100, 2)) + '%'
        a_predicted_return_pct=str(round(a_predicted_return*100, 2)) + '%'
        a_volatility_pct=str(round(a_volatility*100, 2)) + '%'        
        alpha_pct=str(round(alpha*100, 2)) + '%'
        beta_pct=str(round(beta*100, 2)) + '%'

        summary=f"""Asset Ticker: {self.ticker}
Average Anual Return: {a_return_pct},
Predicted Annual Return: {a_predicted_return_pct}, 
Annual Volatility: {a_volatility_pct}, 

The coefficients from the regression over market return:
Alpha: {alpha_pct}, 
Beta: {beta_pct}"""
        return summary
    
    """
    Citation: the below code is borrowed from: 
    https://www.scrapingdog.com/blog/scrape-google-finance/    
    
    """
    # this method is to web scrape company information from Google finance
    def companyInfo(self, INDEX):
        BASE_URL = "https://www.google.com/finance"
        # INDEX = "NASDAQ"
        # INDEX = "NYSE"
        SYMBOL = str(self.ticker)
        print("Ticker: ", SYMBOL)
        LANGUAGE = "en"
        TARGET_URL = f"{BASE_URL}/quote/{SYMBOL}:{INDEX}?hl={LANGUAGE}"

        # make an HTTP request
        page = requests.get(TARGET_URL)
       
        # in case the stock is issue in NYSE, change the INDEX
        # if page.raise_for_status()!=200:
           
        #     INDEX = "NYSE"
        #     TARGET_URL = f"{BASE_URL}/quote/{SYMBOL}:{INDEX}?hl={LANGUAGE}"
 
        #     # make an HTTP request
        #     page = requests.get(TARGET_URL)           

    
        # use an HTML parser to grab the content from "page"
        soup = BeautifulSoup(page.content, "html.parser")


        # get the items that describe the stock
        items = soup.find_all("div", {"class": "gyFHrc"})


        # create a dictionary to store the stock description
        stock_description = {}


        # iterate over the items and append them to the dictionary
        for item in items:
            item_description = item.find("div", {"class": "mfs7Fc"}).text
            item_value = item.find("div", {"class": "P6K39c"}).text
            stock_description[item_description] = item_value
            
            print(item_description,": ", item_value)
        

# Test driver with a Test case here    

def main():
    # asset1=Asset(ticker)
    asset1=Asset('nvda')   

    print('\nasset1 predicted returns monthly:\n',asset1.predictedMonthlyReturns())
    print('\nmonthlyReturnArray:\n', asset1.monthlyReturnArray())
    print('\naverage annual return\n', asset1.averageAnnualReturn())
    print('\npredicted annual return\n', asset1.predictedAnnualReturn())
    print('\nvolatility:\n', asset1.getVolatility())
    print('\n Summary table: \n', asset1.summaryTable())
    
    print('\n Company info: \n')
    asset1.companyInfo("NASDAQ")

# if __name__ == "__main__":
#     main() 





