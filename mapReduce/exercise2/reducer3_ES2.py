#!/usr/bin/env python3

""" reducer.py """

import sys

result = {}

for line in sys.stdin:
    
    line = line.strip()
    
    sector_year, last_close_price, first_close_price, delta, volume = line.split("\t")
    
    key = sector_year[1:-1]
    key = key.split(",")
    sector = key[0]
    sector = sector[1:-1]
    year = key[1]
    year = year[2:-1]
    
    key = (sector, year)
    
    last_close_price = float(last_close_price)
    first_close_price = float(first_close_price)
    delta = float(delta)
    volume = int(volume)
    
    list_of_prices = list()
    
    if key in result:
        last_close_price = result[key][0] + last_close_price
        first_close_price = result[key][1] + first_close_price
        previous_delta = result[key][2]
        previous_volume = result[key][3]
        
        if delta < previous_delta:
            delta = previous_delta
        
        if volume < previous_volume:
            volume = previous_volume

    list_of_prices.append(last_close_price)
    list_of_prices.append(first_close_price)
    list_of_prices.append(delta)
    list_of_prices.append(volume)
    result[key] = list_of_prices


for key, value in result.items():
    percentage_var = ((value[0]/value[1])*100)-100
    print("%s\t%f\t%f\t%d" %(key, percentage_var, value[2], value[3]))
        
        
        
