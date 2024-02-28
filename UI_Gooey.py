#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 20:07:55 2024

@author: qt
"""

"""
CITATION: The application of Gooey is following the instructions of the creator of Gooey here:
    https://github.com/chriskiehl/Gooey/
"""

from gooey import Gooey, GooeyParser
from StockAnalyser import*



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

@Gooey(dump_build_config=True,
           program_name="Stock Analyser",
           advanced=True,
           auto_start=False,
            body_bg_color='#bfbfbf',
           
            header_bg_color='#009999',
            footer_bg_color='#009999',
   
           
           sidebar_bg_color='#262626',
           terminal_font_color="white",
           # color="grey", 
           terminal_panel_color="#d9d9d9", 
           # terminal_bg_color="white"
            font_color= 'black',
            
           )
# (program_name="Stock Analyser", navigation="SIDEBAR", show_sidebar=True, 
#        sidebar_bg_color="#f2f2f2", header_bg_color="#009999", 
#        # text_color="#cc9900", 
#        textColor="yellow", terminal_font_color="white", color="grey", terminal_panel_color="grey", 
#        # terminal_panel_color="#f2f2f2"
       
#         body_bg_color="#f2f2f2")
def main():
    
    parser = GooeyParser(description="""Welcome to Stock Analyser! 
        Plese put in a Stock Ticker and choose an index and selection, then click 'Start'.
        On the result page, click 'Edit' to come back to this page, or 'Close' to exit. """) 
    
   
    parser.add_argument('StockTicker', action="store", 
                        help="Please type the stock ticker into this box")
    
    parser.add_argument('INDEX', choices=["NASDAQ", "NYSE"], help="Choose where it's issued")
    
    # set up colors for groups
    for group in parser._action_groups:
        group.gooey_options = {'label_color': '#0099cc', 
                                'text_color': '#0099cc',
                                'description_color': 'black'
                                # 'description_color': '#363636'
                                }
    
    
    group=parser.add_mutually_exclusive_group("selection")  
   
    
    # add radio buttons  
                     
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
    
    
    
    args=parser.parse_args()
    
    print(args.StockTicker)
    
    asset1=Asset(args.StockTicker)
    
    if args.selection_1:
        avg_annual_return = asset1.averageAnnualReturn()
        print(f"\n\nThe average annual risk return rate for {args.StockTicker} is: {avg_annual_return:.2%}.\n")
    
    if args.selection_2:
        asset1.plotRegression()
        print(f"\n\nLog regression between {args.StockTicker}'s return and market return has been calculated.\n")
    
    if args.selection_3:
        projected_return = asset1.predictedAnnualReturn()
        print(f"\n\nThe projected annual risk return rate for {args.StockTicker} is {projected_return:.2%}.\n")
        
    if args.selection_4:   
        print('\n \n Company\'s information: \n')  
        asset1.companyInfo(args.INDEX)
        
    if args.selection_5:   
        print('\n Summary table: \n\n',  asset1.summaryTable())
      
  
  
  
  
if __name__ == "__main__":
    main() 
