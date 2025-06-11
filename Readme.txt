Stock Analyser - Term Project 

Abstract
This term project created a Python application - Stock Analyser. It takes any given stock’s 3 years of historical data, provides calculated average annual excess risk return rate, predicts excess return rate  by regression analysis between excess returns of individual assets and S&P 500 index (market returns). The backend model is designed with Asset Class to organize multiple methods, and polymorphism to output results. It has applied libraries Pandas, Numpy for data manipulation, YFinance, Requests and BeautifulSoup for web scraping. The UI applied Gooey package and implemented a user friendly GUI interface. 

Here is the video demo: https://youtu.be/vx2nTbLwSok?si=u47hvw6n2lBlCxhA 
and the presentation: https://youtu.be/7cOcFgT4AcM


User Instructions

You need to install all the libraries used: 
Gooey by: https://github.com/chriskiehl/Gooey/, 
YFinance by: https://pypi.org/project/yfinance/


Then you put ‘StockAnalyser.py’, ‘UI_Gooey.py’, and ‘TB3MS.csv’ in one folder, and run from the file ‘UI_Gooey.py’. If you run into configuration issues on Spyder, it would be better to run it on VSCode. 


Note: 
The API way of downloading data is implemented in 2 ways: with both YFinance and Alpha Vantage API to meet the project’s requirements. The code is under the method ‘getMontlyData(self)’ marked with method 1 and 2 in comments. So you can comment out either method and run another method. Because the API key from Alpha Vantage may have limited usage within a period of time, I normally run the YFiance method. The extra Alpha Vantage API key is provided in the comments in case you need it. 


After the app opens, the home page is self-explanatory. You input a stock ticker, choose an INDEX, and an optional task to start. Either INDEX works the same, just the company information you get would be different. So if you get ‘none’, you should choose the other market INDEX. You can click the ‘Edit’ button on the result page to come back to the home page.
