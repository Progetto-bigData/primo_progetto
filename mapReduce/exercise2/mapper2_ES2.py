#!/usr/bin/env python3

""" mapper.py """


import sys

for line in sys.stdin:
    
    line = line.strip()
    
    ticker, close_price, tx_volume, bounded_date, sector = line.split("\t")
    
    key = (sector, bounded_date)
    
    print("%s\t%s\t%s\t%s" % (key, ticker, close_price, tx_volume))
