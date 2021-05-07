#!/usr/bin/env python3

"""mapper.py"""

import sys

for line in sys.stdin:
    
    line = line.strip()
    
    key, delta1, delta2, name1, name2 = line.split("\t")  # key= (A, B, month)
    
    key = key[1:-1]
    key = key.split(",")
    tickerA = key[0][1:-1]
    tickerB = key[1][2:-1]
    month = key[2]
    
    delta1 = float(delta1)
    delta2 = float(delta2)
    
    new_key = (tickerA, tickerB)
    
    print("%s\t%s\t%f\t%f\t%s\t%s" %(new_key, month, delta1, delta2, name1, name2))
