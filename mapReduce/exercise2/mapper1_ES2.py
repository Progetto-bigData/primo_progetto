#!/usr/bin/env python3

""" mapper.py """

import sys
from datetime import datetime


# position first file
TICKER = 0
OPEN = 1
CLOSE = 2
LOW = 4
HIGH = 5
VOLUME = 6
DATE = 7

# position second file
TICKER = 0
EXCHANGE = 1
NAME = 2
SECTOR = 3
INDUSTRY = 4

LOWER_BOUND_DATE = "2009-01-01"
UPPER_BOUND_DATE = "2018-12-31"

for line in sys.stdin:
    
    line = line.strip()
    
    words = line.split(",")
    
    #Vuol dire che è la riga delle intestazioni, vai avanti senza stampare niente
    if(words[0] == "ticker"):
        continue
    
    try:  # sto nel primo file
        ticker = words[0]
        close_price = float(words[2])
        tx_volume = int(words[6])
        date = words[7]
        bounded_date = ""
        if LOWER_BOUND_DATE <= date <= UPPER_BOUND_DATE:
            bounded_date = date
            print("%s\t%f\t%d\t%s\t%s" %(ticker, close_price, tx_volume, bounded_date, "UNKNOWN_VALUE"))

    except ValueError :
         ticker = words[0]
         sector = words[3]
         print("%s\t%s\t%s\t%s\t%s" %(ticker, "UNKNOWN_VALUE", "UNKNOWN_VALUE", "UNKNOWN_VALUE", sector))
         
        
        
                                      

    
    
    
 
