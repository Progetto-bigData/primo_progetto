#!/usr/bin/env python3

""" reducer.py """


# position of fields:    0 -> ticker, 1 -> close_price, 2 -> tx_volume, 3 -> bounded_date, 4 -> sector



import sys
from datetime import datetime



map_2_other_attributes = {}
map_2_sector = {}

for line in sys.stdin:
    
    line = line.strip()
    
    ticker, close_price, tx_volume, bounded_date, sector = line.split("\t")
    
    if sector != "UNKNOWN_VALUE":
        map_2_sector[ticker] = sector
    else:
        if(ticker in map_2_other_attributes):
            temp = map_2_other_attributes[ticker]
            temp.append([close_price, tx_volume, bounded_date])
            map_2_other_attributes[ticker] = temp
        else:
            map_2_other_attributes[ticker] = [[close_price, tx_volume, bounded_date]]

for ticker, value in map_2_other_attributes.items():
    if ticker in map_2_sector:
        sector = map_2_sector[ticker]
        for list_attributes in value:
            print("%s\t%s\t%s\t%s\t%s" % (ticker, list_attributes[0], list_attributes[1], list_attributes[2], sector))

