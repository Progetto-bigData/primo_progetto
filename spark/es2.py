#!/usr/bin/env python3
""" spark application """

import argparse

from pyspark.sql import SparkSession

THRESHOLD_DATA_MIN = '2008-12-31'
THRESHOLD_DATA_MAX = '2019-01-01'

# create parser and set its arguments
parser = argparse.ArgumentParser()
parser.add_argument("--input1", type=str, help="Input file path")
parser.add_argument("--input2", type=str, help="Input file path")
parser.add_argument("--output", type=str, help="Output file path")

# parse arguments
args = parser.parse_args()
input_filepath1, input_filepath2, output_filepath = args.input1, args.input2, args.output

# initialize SparkSession
spark = SparkSession.builder.appName("Spark ES2").getOrCreate()

lines_RDD_primo = spark.sparkContext.textFile(input_filepath1)

lines_RDD_secondo = spark.sparkContext.textFile(input_filepath2)

lines_RDD_primo = lines_RDD_primo.map(lambda x: tuple(x.split(",")))
lines_RDD_secondo = lines_RDD_secondo.map(lambda x: tuple(x.split(",")))

lines_RDD_primo = lines_RDD_primo.map(lambda x: tuple([x[0], x[2], x[6], x[7]]))
lines_RDD_secondo = lines_RDD_secondo.map(lambda x: tuple([x[0], x[3]]))

lines_RDD_primo = lines_RDD_primo.filter(lambda x: THRESHOLD_DATA_MIN < x[3] < THRESHOLD_DATA_MAX)

lines_RDD_primo = lines_RDD_primo.map(lambda x: tuple([x[0], (x[1], x[2], x[3])]))

lines_RDD_joined = lines_RDD_primo.join(lines_RDD_secondo)

lines_RDD_joined = lines_RDD_joined.map(lambda x: (x[0], x[1][0][0], x[1][0][1], x[1][0][2], x[1][1]))

key_sector_year_ticker = lines_RDD_joined.map(lambda x: ((x[4], x[3][0:4], x[0]), (x[1], x[2], x[3])))

key_sector_year_ticker_grouped = key_sector_year_ticker.groupByKey()

key_sector_year_ticker_grouped.collect()


def get_minPrice_maxPrice_sumVolume(x):
    key = (x[0][0],x[0][1],x[0][2])
    minimo = min(x[1], key = lambda k: k[2])[0]
    massimo = max(x[1], key = lambda k: k[2])[0]
    delta = ((float(massimo) / float(minimo))*100) -100
    somma = 0
    for value in x[1]:
        somma += int(value[1])
    return (key, minimo, massimo, somma, delta)


key_sector_year_min_max_sum = key_sector_year_ticker_grouped.map(get_minPrice_maxPrice_sumVolume)

key_sector_year_min_max_sum.collect()

key_sector_year_min_max_sum = key_sector_year_min_max_sum.map(lambda x : ((x[0][0], x[0][1]),
                                                                          (x[0][2], x[1], x[2], x[3], x[4])))

key_sector_year_min_max_sum = key_sector_year_min_max_sum.groupByKey()


def get_percentageVar_maxVolume(x):
    prezzo_massimo = 0
    prezzo_minimo = 0
    max_delta = 0
    for value in x[1]:
        if float(value[4]) > max_delta:
            max_delta = float(value[4])
        prezzo_massimo += float(value[2])
        prezzo_minimo += float(value[1])
    maxVolume = max(x[1], key = lambda k : k[3])[3]
    percentageVar = ((prezzo_massimo / prezzo_minimo) -1)*100
    return tuple([x[0][0], x[0][1]]), tuple([percentageVar, max_delta, maxVolume])


key_sector_year_min_max_sum = key_sector_year_min_max_sum.map(get_percentageVar_maxVolume)
sorted_key_sector_year_min_max_sum = key_sector_year_min_max_sum.sortByKey()

spark.sparkContext.parallelize(sorted_key_sector_year_min_max_sum.collect()).saveAsTextFile("./output/folder/prova2")
