#!/usr/bin/env python3

""" mapper.py """

import sys

for line in sys.stdin:
    
    line = line.strip()
    
    key, last_close_price, first_close_price, delta, volume = line.split("\t")     # key = (sector, year, ticker)  last date, last close_price, first date, first close_price, delta, volume
    
    last_close_price = float(last_close_price)
    first_close_price = float(first_close_price)
    delta = float(delta)
    volume = int(volume)
    
    key = key[1:-1]
    key = key.split(",")
    sector = key[0]
    year = key[1]
    ticker = key[2]
    
    new_key = (sector, year)
    
    print("%s\t%f\t%f\t%f\t%d" % (new_key, last_close_price, first_close_price, delta, volume))
