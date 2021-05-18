#!/usr/bin/env python3

""" reducer.py """

import sys
from datetime import datetime


ticker_2_info = {}


for line in sys.stdin:
    
    line = line.strip()
    
    ticker, open_price, close_price, low_price, high_price, date = line.split("\t")     
    
    open_price = float(open_price)
    
    close_price = float(close_price)
    
    low_price = float(low_price)
    
    high_price = float(high_price)
    
  
    if ticker in ticker_2_info:
        if date < ticker_2_info[ticker][0]:
            current_first_quotation_date = date
            current_min_close_price = close_price
        else:
            current_first_quotation_date = ticker_2_info[ticker][0]
            current_min_close_price = ticker_2_info[ticker][2]
        
        if date > ticker_2_info[ticker][1]:
            current_last_quotation_date = date
            current_max_close_price = close_price
        else:
            current_last_quotation_date = ticker_2_info[ticker][1]
            current_max_close_price = ticker_2_info[ticker][3]
        
        if low_price < ticker_2_info[ticker][4]:
            current_min_low_price = low_price
        else:
            current_min_low_price = ticker_2_info[ticker][4]
        
        if high_price > ticker_2_info[ticker][5]:
            current_max_high_price = high_price
        else:
            current_max_high_price = ticker_2_info[ticker][5]
    else:
        current_first_quotation_date = date
        current_last_quotation_date = date
        current_min_close_price = close_price
        current_max_close_price = close_price
        current_min_low_price = low_price
        current_max_high_price = high_price
    #                                  0                             1                          2                      3                          4                      5
    ticker_2_info[ticker] = [current_first_quotation_date, current_last_quotation_date, current_min_close_price, current_max_close_price, current_min_low_price, current_max_high_price]

 # max gg consecutivi in cui l'azione è cresciuta
result = {}

for key, value in dict(sorted(ticker_2_info.items(), key = lambda item: item[1][1], reverse = True)).items():
    ticker = key
    first_quotation_date = value[0]
    last_quotation_date = value[1]
    percentage_var = (((value[3] / value[2])*100) - 100)
    min_low_price = value[4]
    max_high_price = value[5]
    result_value = [first_quotation_date, last_quotation_date, percentage_var, min_low_price, max_high_price]
    result[ticker] = result_value
    print("%s\t%s\t%s\t%f\t%f\t%f" % (ticker, first_quotation_date, last_quotation_date, percentage_var, min_low_price, max_high_price))

#for key,value in dict(sorted(result.items(), key=lambda item: item[1][1], reverse = True)).items():
#    print("%s\t%s\t%s\t%f\t%f\t%f" % (key, value[0], value[1], value[2], value[3], value[4]))












