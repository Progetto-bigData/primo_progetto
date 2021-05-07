#!/usr/bin/env python3

"""mapper.py"""

import sys

# position first file
TICKER = 0
OPEN = 1
CLOSE = 2
LOW = 4
HIGH = 5
VOLUME = 6
DATE = 7

LOWER_DATE_LIMIT = "2017-01-01"
UPPER_DATE_LIMIT = "2017-12-31"

for line in sys.stdin:
    
    line = line.strip()
    
    words = line.split(",")

    
    if(words[0] == "ticker"):
        continue
    
    try:
        ticker = words[0]
        close_price = float(words[2])
        date = words[7]
        
        if LOWER_DATE_LIMIT <= date <= UPPER_DATE_LIMIT:
            new_date = date
        
            print("%s\t%s\t%f\t%s" % (ticker, new_date, close_price, "UNKNOWN_VALUE"))
    except ValueError:
        ticker = words[0]
        name = words[2]
        print("%s\t%s\t%s\t%s" %(ticker, "UNKNOWN_VALUE", "UNKNOWN_VALUE", name))
