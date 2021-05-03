#!/usr/bin/env python3

""" reducer.py """

import sys


intermediate_result = {}
final_result = {}

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
    
    if key not in intermediate_result:
        list_of_information = []
        list_of_information.append(date)
        list_of_information.append(close_price)
        list_of_information.append(date)
        list_of_information.append(close_price)  # last date, final close_price, first date, first close_price, tx_volume
        list_of_information.append(tx_volume)
        intermediate_result[key] = list_of_information
    else:
        list_of_information = intermediate_result[key]
        if date > list_of_information[0]:
            list_of_information[0] = date
            list_of_information[1] = close_price
        
        if date < list_of_information[2]:
            list_of_information[2] = date
            list_of_information[3] = close_price
        
        volume = list_of_information[4] + tx_volume
        list_of_information[4] = volume
        intermediate_result[key] = list_of_information
    
for key, value in intermediate_result.items():
    
    key_final_result = (key[0], key[1])
    
    delta = value[1]-value[3]
    
    volume = value[4]
    
    if key_final_result not in final_result:
        list_of_prices = list()
        list_of_prices.append([value[1]])
        list_of_prices.append([value[3]])
        list_of_prices.append(delta)
        list_of_prices.append(volume)
        final_result[key_final_result] = list_of_prices
    else:
        list_of_prices = final_result[key_final_result]
        list_of_prices[0].append(value[1])
        list_of_prices[1].append(value[3])
        
        if delta > final_result[key_final_result][2]:
            list_of_prices[2] = delta
        else:
            delta = final_result[key_final_result][2]
            list_of_prices[2] = delta
        
        if volume > list_of_prices[3]:
            list_of_prices[3] = volume
        else:
            volume = final_result[key_final_result][3]
            list_of_prices[3] = volume
        
        final_result[key_final_result] = list_of_prices

for key, value in final_result.items():
    sum_of_final_prices = 0
    sum_of_initial_prices = 0
    for elem in value[0]:
        sum_of_final_prices += elem
    for e in value[1]:
        sum_of_initial_prices += e
    percentage_var = ((sum_of_final_prices / sum_of_initial_prices) * 100) - 100
    max_delta = value[2]
    max_volume = value[3]
    print("%s\t%f\t%f\t%d" % (key, percentage_var, max_delta, max_volume))
        
            
    
    
    
    
        
        
    
    
    
