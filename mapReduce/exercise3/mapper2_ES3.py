#!/usr/bin/env python3

"""mapper.py"""           

import sys


for line in sys.stdin:
    
    line = line.strip()
    
    key, delta = line.split("\t")  #key = (A, month)   percentage_var
    
    key = key[1:-1]
    key = key.split(",")
    ticker = key[0][1:-1]
    month = key[1][1:-1]
    month = int(month[1:])
    
    delta = float(delta)
        

    print("%d\t%s\t%f" % (month, ticker, delta))  #month : ticker, delta
    
        
    
    
