#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 20:07:55 2024

@author: Quinn Tian
"""

"""
CITATION: The application of Gooey is following the instructions of the creator of Gooey here:
    https://github.com/chriskiehl/Gooey/
"""

from gooey import Gooey, GooeyParser
from StockAnalyser import*

# to define the default format of items on UI
item_default = {
        'error_color': '#ea7878',
        'label_color': '#ffffff',
        'help_color': '#363636',
        'full_width': False,
        'validator': {
            'type': 'local',
            'test': 'lambda x: True',
            'message': ''
        },
        'external_validator': {
            'cmd': '',
        }
    }


# This is the standard Gooey syntax to define the color and layout of this Gooey UI
@Gooey(dump_build_config=True,
           
           program_name="Stock Analyser",
           advanced=True,
           auto_start=False,
           body_bg_color='#bfbfbf',
           # body_bg_color='black',
          
           header_bg_color='#009999',
           footer_bg_color='#009999',
           
         
           
           sidebar_bg_color='#262626',
           terminal_font_color="white",
           # color="grey", 
           terminal_panel_color="#d9d9d9", 
           # terminal_bg_color="white"
            font_color= 'black',
            
           )

# This the main implementation of this UI, covering both the View and the Controller of this App
# It defines all itmes on home page and results page, 
# takes the user inputs on the home page,
# outputs the results on the result page
def main():
    
    # headings / titles of home page
    parser = GooeyParser(description="""Welcome to Stock Analyser! 
        Please put in a Stock Ticker, choose an index and an option, then click 'Start'.
        On the result page, click 'Edit' to come back to this page, or 'Close' to exit. """) 
    
    # take the user inputs for argument 'StockTicker' 
    # label the input box with help information
    parser.add_argument('StockTicker', action="store", 
                        help="Type the stock ticker into this box")
    
    # take the user inputs for argument 'INDEX'
    # label the dropdown menu for INDEX with help information
    parser.add_argument('INDEX', choices=["NASDAQ", "NYSE"], help="Choose the issue market")
    
    # set up colors for groups items
    for group in parser._action_groups:
        group.gooey_options = {'label_color': '#0099cc', 
                                'text_color': '#0099cc',
                                'description_color': 'black'
                                # 'description_color': '#363636'
                                }
    
    # set up all the radio buttons to get the user choices for what tasks to perform
    group=parser.add_mutually_exclusive_group("selection")  
   
    
    # add radio buttons with proper labeling and help information
                     
    group.add_argument("--selection_1",  action="store_true", 
                       help="1. Get the average annual risk return rate")  
    group.add_argument("--selection_2",  action="store_true", 
                       help="2. Get the graph of log regression between your stock return and market return")
    group.add_argument("--selection_3",  action="store_true", 
                       help="3. Get the projected risk return rate")
    group.add_argument("--selection_4",  action="store_true", 
                       help="4. Get company's financial information")
    group.add_argument("--selection_5",  action="store_true", 
                       help="5. Get the summary table")
    
    
    # parse the inputs of users as arguments
    args=parser.parse_args()
    
    print(args.StockTicker)
    
    # take stock ticker to initialize an Asset instance
    asset1=Asset(args.StockTicker)
    
    # for each selection, run its corresponding processes or functions
    # to present the right results to meet the user's needs
    if args.selection_1:
        avg_annual_return = asset1.averageAnnualReturn()
        print(f"\n\nThe average annual risk return rate for {args.StockTicker} is: {avg_annual_return:.2%}.\n")
    
    if args.selection_2:
        asset1.plotRegression()
        print(f"\n\nLog regression between {args.StockTicker}'s return and market return has been plotted.\n")
    
    if args.selection_3:
        projected_return = asset1.predictedAnnualReturn()
        print(f"\n\nThe projected annual risk return rate for {args.StockTicker} is {projected_return:.2%}.\n")
        
    if args.selection_4:   
        print('\n \n Company\'s information: \n')  
        asset1.companyInfo(args.INDEX)
        
    if args.selection_5:   
        print('\n Summary table: \n\n',  asset1.summaryTable())
      
  
  
  
# the app driver  
if __name__ == "__main__":
    main() 
