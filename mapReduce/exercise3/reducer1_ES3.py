#!/usr/bin/env python3

"""reducer.py"""           

import sys 

result = {}

THRESHOLD = 1

for line in sys.stdin:
    
    line = line.strip()
    
    ticker, date, close_price = line.split("\t")  
    
    close_price = float(close_price)
    
    new_key = (ticker, date[5:7])
    
    if new_key not in result:
        list_of_information = []
        list_of_information.append(date)
        list_of_information.append(close_price)
        list_of_information.append(date)
        list_of_information.append(close_price)
        result[new_key] = list_of_information
    else:
        list_of_information = result[new_key]
        if date > result[new_key][0]:
            list_of_information[0] = date
            list_of_information[1] = close_price
        if date < result[new_key][2]:
            list_of_information[2] = date
            list_of_information[3] = close_price
        result[new_key] = list_of_information
    

for key, value in result.items():
    
    delta = ( ( value[1] / value[3] ) * 100 ) - 100
    
    print("%s\t%f" %(key, delta))

    
    
    
    
