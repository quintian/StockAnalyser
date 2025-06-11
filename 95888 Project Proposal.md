# Term Project Proposal

Group 2 \- Team Wizards  
Reetu Bok \<rbok@andrew.cmu.edu\>  
Bryan Martyn \<bmartyn@andrew.cmu.edu\>,  
Quinn Tian \<kunt@andrew.cmu.edu\>

# Subject

What is the risk return rate of the stock requested during the last year?

What are the essential factors that affect the price of the stock, and how much impact is from each factor? 

# User case

The user input the stock ticker that they like to inquire about, then the application will return the risk return rate for the stock, plus the factors that would affect this stock’s price, and how much impact each factor has.

# Data Source

1. Alpha Vantage \- [https://www.alphavantage.co/](https://www.alphavantage.co/) \- for stock prices  
2. Yahoo finance for the stock’s price data in the past  
3. Treasury bonds website for return rate of risk free asset: [https://fred.stlouisfed.org/series/TB3MS](https://fred.stlouisfed.org/series/TB3MS)  
4. Google for other companies data (this might change depending on which site has API available for data downloading)

# Division of work

Quinn Tian : project proposal, model design, implementation architecture, coding for the risk return, pricing model, etc.

Reetu Bok : algorithm and implementation for top 5 companies use case. Some key steps identified:

* Review input data and data formatting, split input and test data  
* Review existing models/algorithms/approach in this space  
* Create revisions and tweaking and tuning of new algorithm  
* Check the accuracy of model from past data

Brya Martyn: Data collection, presentation, deliver comparison