#!/usr/bin/env python3

"""reducer.py"""           

import sys 

result = {}

THRESHOLD = 1

for line in sys.stdin:
    
    line = line.strip() 
    
    month, ticker, delta = line.split("\t") 
    
    month = int(month)
    delta = float(delta)
    
    key = month
    
    if key not in result:
        list_of_information = list()
    else:
        list_of_information = result[key]
    
    list_of_information.append([ticker, delta])
    result[key] = list_of_information
    
    
for key, value in result.items():
    for e1 in value:
        for e2 in value:
            if e1[0] > e2[0]:
                delta = abs(e1[1] - e2[1])
                if delta <= THRESHOLD:
                    new_key = (e1[0], e2[0], key)
                    print("%s\t%f\t%f" %(new_key, e1[1],e2[1]))   #tickerA, tickerB, month : delta1, delta2
