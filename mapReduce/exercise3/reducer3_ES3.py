#!/usr/bin/env python3

"""reducer.py"""           

result = {}

import sys  

for line in sys.stdin:
    
    line = line.strip()
    
    key, month, delta1, delta2 = line.split("\t")  #key = (tickerA, tickerB)
    
    key = key[1:-1]
    key = key.split(",")
    tickerA = key[0][1:-1]
    tickerB = key[1][2:-1]
    
    month = int(month)
    delta1 = float(delta1)
    delta2 = float(delta2)
    
    new_key = (tickerA, tickerB)
    
    triple = [month, delta1, delta2]
    
    if new_key not in result:
        list_of_triples = []
        result = {}
    else:
        list_of_triples = result[new_key]
    
    list_of_triples.append(triple)
    if len(list_of_triples) == 12:
        list_of_triples.sort(key = lambda x : x[0])
        list_of_triples[0][0] = "GEN"
        list_of_triples[1][0] = "FEB"
        list_of_triples[2][0] = "MAR"
        list_of_triples[3][0] = "APR"
        list_of_triples[4][0] = "MAG"
        list_of_triples[5][0] = "GIU"
        list_of_triples[6][0] = "LUG"
        list_of_triples[7][0] = "AGO"
        list_of_triples[8][0] = "SET"
        list_of_triples[9][0] = "OTT"
        list_of_triples[10][0] = "NOV"
        list_of_triples[11][0] = "DEC"
        print("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" %(new_key, list_of_triples[0], list_of_triples[1], list_of_triples[2], list_of_triples[3], list_of_triples[4], list_of_triples[5], list_of_triples[6], list_of_triples[7], list_of_triples[8], list_of_triples[9], list_of_triples[10], list_of_triples[11]))
    else:
        result[new_key] = list_of_triples

    
