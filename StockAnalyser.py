# This file read asset's data from Yahoo,  does regression analysis 
# on asset's return and markets return, and generate the predicted returns.

'''CITATION: I learned how to use Matplotlib from
https://matplotlib.org/
'''

'''CITATION: 
@author: Quinn Tian 
@copyright: 
    Quinn Tian owns the copyright for everything in this model and application

 '''
import pandas as pd
import numpy as np
import datetime
# import pandas_datareader as dr
import matplotlib.pyplot as plt
# Import yfinance package
import yfinance as yf
import requests
from bs4 import BeautifulSoup

'''CITATION: The regression code is from the link:
https://stackoverflow.com/questions/38676323/is-it-possible-to-get-monthly-historical-stock-prices-in-python
'''
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
def monthlyTBReturns():
     downloadTB=pd.read_csv("TB3MS.csv")# annual return
     dataTB=downloadTB[2:]
     
     ''' use np to calculate monthly return:'''
     dataTB['Monthly Return TB']=dataTB['TB3MS']/1200 #monthly return
     
    
     return dataTB
 

# riskFreeReturn is a global variable:
dataTB=monthlyTBReturns() 
# TB_returns=dataTB['Monthly Return TB'] 
TB_returns=np.array(dataTB['Monthly Return TB'] )
# a_return_TB=np.average(dataTB['TB4WK']/100)

def monthlySPReturns():
     # df = pd.DataFrame()     
     # df=dr.get_data_yahoo('^GSPC', interval='m',
     #                            start='2017-1-1' , end='2020-1-1')['Adj Close']
     data = yf.download('^GSPC', start="2021-01-01", end="2024-01-01") # new code
     month_end_prices = data['Adj Close'].resample('ME').last()
     
     # calculate monthly Return 
     m_returns=month_end_prices.pct_change()
     # print("\nSP montly returns: \n", m_returns)
     # exclude the first row since percentage change starts from the second row
     return np.array(m_returns[1:]) 

     # # calculate monthly Return 
     # m_returns=df.pct_change()
     # # exclude the first row since percentage change starts from the second row
     # return np.array(m_returns[1:]) 
 
   
 

class Asset(object):
    def __init__(self, ticker):
        self.ticker=ticker

    def getData(self):
        data = yf.download(self.ticker, start="2021-01-01", end="2024-01-01") # new code
        # print("\n3 year\n", data.head())
        # print("rows of the data daily: ", len(data))
        df=pd.DataFrame(data["Adj Close"])
        # print("daily price: \n", df.head())
                
        return df 
       
    
        
    def getMonthlyData(self):
        # method 1: use yfinance package, like an API from yahoo finance
        
        data = yf.download(self.ticker, start="2021-01-01", end="2024-01-01") # new code
        month_end_prices = data['Adj Close'].resample('ME').last()
        
        # print("\n3 year monthly\n", month_end_prices)
        # print("rows of the data montly: ", len(month_end_prices))
        df=pd.DataFrame(month_end_prices)
      
        
        # mothod 2: use API
        # url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=AAPL&time_from=20220410T0130&apikey=S3XLG8C4CWQCWWYY'

        # r = requests.get(url)
        # data = r.json()
        # monthlyPrice=[]
        # for key in data: 
        #     if key=='Monthly Adjusted Time Series':
        #         for key in data['Monthly Adjusted Time Series']:
        #             if (key>'2020-12-31' and key<'2024-01-01'):
                    
        #                 # print (data['Monthly Adjusted Time Series'][key]['5. adjusted close']) 
        #                 monthlyPrice.append(float(data['Monthly Adjusted Time Series'][key]['5. adjusted close']))
        #                 print(len(monthlyPrice))
        # df=pd.DataFrame(monthlyPrice)
        
        return df
        
                        
           

    def getDailyReturns(self):
        df=self.getData()
        d_returns=df.pct_change()
        
        return np.array(d_returns[1:])

    def averageMonthlyReturn(self):
        d_returns=self.getDailyReturns()
        m_return=np.exp(np.sum(np.log(d_returns+1)/36))-1
        return m_return #changed to series

    def averageAnnualReturn(self):
        d_returns=self.getDailyReturns()
        a_return=np.exp(np.sum(np.log(d_returns+1)/3))-1
        return a_return

    def getVolatility(self):
        d_returns=self.getDailyReturns()
        a_volatility=np.std(d_returns)*np.sqrt(251)
        return a_volatility

    def monthlyReturnArray(self):
        df=self.getMonthlyData()
        m_returns=df.pct_change()
        
        return np.array(m_returns[1:])

    def excessReturnArray(self):
        m_returns=np.array(self.monthlyReturnArray())
        # print('m_________',np.size(m_returns))        
        # print('tb________', np.size(TB_returns))

        excess_returns=np.subtract(m_returns,TB_returns)
        m_returns_SP=monthlySPReturns()
        # print('sp________', np.size(m_returns_SP))
        excessReturns_SP=np.subtract(m_returns_SP,TB_returns)
        return excessReturns_SP, excess_returns

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
    
    def plotRegression(self):
        excessReturns_SP, excess_returns=self.excessReturnArray()
        x,y=np.log(excessReturns_SP+1),np.log(excess_returns+1)
        alpha, beta=estimate_coef(x, y)

        plt.plot(x, y, 'o')
        plt.plot(x, beta*x + alpha)
        plt.xlabel('SP Excess Returns')
        plt.ylabel('Asset Excess Returns')
        plt.title(f'Regression on Excess Returns of {self.ticker} over Market')
        plt.show()
        plt.close()
        

    def predictedMonthlyReturns(self):
        alpha, beta=self.logRegression()          
        excessReturn_SP, excess_returns=self.excessReturnArray()
        x,y=np.log(excessReturn_SP+1),np.log(excess_returns+1)

        predicted_log_excess=alpha+beta*x
        predicted_excess_m=np.exp(alpha+beta*x)-1  
        
        # risk_free_returns is TB_returns
        predicted_returns_m=predicted_excess_m+TB_returns
        
        return predicted_returns_m  

    def predictedAnnualReturn(self):
        predicted_returns_m=self.predictedMonthlyReturns()
        predicted_return_a=np.exp(np.sum(np.log(predicted_returns_m+1))/3)-1
        return predicted_return_a     
    
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
        

# Test cases:
#      

def main():
    # asset1=Asset(ticker)
    asset1=Asset('nvda')   

    # print('\nasset1 predicted returns monthly:\n',asset1.predictedMonthlyReturns())
    # print('\nmonthlyReturnArray:\n', asset1.monthlyReturnArray())
    # print('\naverage annual return\n', asset1.averageAnnualReturn())
    # print('\npredicted annual return\n', asset1.predictedAnnualReturn())
    # print('\nvolatility:\n', asset1.getVolatility())
    # print('\n Summary table: \n', asset1.summaryTable())
    
    print('\n Company info: \n')
    asset1.companyInfo("NASDAQ")

if __name__ == "__main__":
    main() 





