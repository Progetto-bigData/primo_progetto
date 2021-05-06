#!/usr/bin/env python3

""" reducer.py """

import sys


result = {}


for line in sys.stdin:
    
    line = line.strip()
    
    sector_date, ticker, close_price, tx_volume = line.split("\t")
    
    close_price = float(close_price)
    
    tx_volume = int(tx_volume)
    
    sector_date = sector_date[1:-1]
    sector_date = sector_date.split(",")
    sector = sector_date[0]
    sector = sector[1:-1]
    date = sector_date[1]
    date = date[2:-1]
    year = date[0:4]   
    
    key = (sector, year, ticker)
    
    if key not in result:
        list_of_information = []
        list_of_information.append(date)
        list_of_information.append(close_price)
        list_of_information.append(date)
        list_of_information.append(close_price)  # last date, final close_price, first date, first close_price, tx_volume
        list_of_information.append(0)
        list_of_information.append(tx_volume)
        result[key] = list_of_information
    else:
        list_of_information = result[key]
        if date > list_of_information[0]:
            list_of_information[0] = date
            list_of_information[1] = close_price
        
        if date < list_of_information[2]:
            list_of_information[2] = date
            list_of_information[3] = close_price
        
        delta = ((list_of_information[1] - list_of_information[3]) / list_of_information[3])*100
        list_of_information[4] = delta
        volume = list_of_information[5] + tx_volume
        list_of_information[5] = volume
        result[key] = list_of_information
    
for key, value in result.items():
    print("%s\t%f\t%f\t%f\t%d" %(key, value[1], value[3], value[4], value[5]))

        
            
    
    
    
    
        
        
    
    
    
