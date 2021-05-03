#!/usr/bin/env python3

""" mapper.py """

import sys
from datetime import datetime

TICKER = 0
OPEN_PRICE = 1
CLOSE_PRICE = 2
LOW_PRICE = 4
HIGH_PRICE = 5
DATE = 7

for line in sys.stdin:

    # removing whitespaces
    line = line.strip()

    # separate lines into words
    words = line.split(",")
    try:
        ticker = words[TICKER]
        open_price = float(words[OPEN_PRICE])
        close_price = float(words[CLOSE_PRICE])
        low_price = float(words[LOW_PRICE])
        high_price = float(words[HIGH_PRICE])
        date = words[DATE]
    except ValueError:
        continue

    #new_date = datetime.strptime(date, "%Y-%m-%d")

    print('%s\t%f\t%f\t%f\t%f\t%s' % (ticker, open_price, close_price, low_price, high_price, date))


