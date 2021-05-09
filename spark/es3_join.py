#!/usr/bin/env python3
""" spark application """

import argparse

from pyspark.sql import SparkSession

# create parser and set its arguments
parser = argparse.ArgumentParser()
parser.add_argument("--input", type=str, help="Input file path")
parser.add_argument("--output", type=str, help="Output file path")

# parse arguments
args = parser.parse_args()
input_filepath, output_filepath = args.input, args.output

# initialize SparkSession
spark = SparkSession.builder.appName("Spark ES3").config("spark.driver.maxResultSize", "1000M").getOrCreate()

SOGLIA = 1

lines_RDD_primo = spark.sparkContext.textFile(input_filepath)


lines_RDD_primo = lines_RDD_primo.map(lambda x: (x.split(",")))

lines_RDD_primo = lines_RDD_primo.map(lambda x: ([x[0], x[2], x[7]]))

lines_RDD_primo = lines_RDD_primo.filter(lambda x: int(x[2][0:4]) == 2017)

lines_RDD_primo = lines_RDD_primo.map(lambda x: ([tuple([x[0], x[2][5:7]]), tuple([x[1],x[2]])]))

lines_RDD_primo_grouped = lines_RDD_primo.groupByKey()

lines_RDD_primo_min_max = lines_RDD_primo_grouped.map(lambda x : (tuple([x[0][0],x[0][1]]),
                                                      min(x[1], key = lambda k : k[1])[0], 
                                                      max(x[1], key = lambda k : k[1])[0]))

lines_RDD_diff = lines_RDD_primo_min_max.map(lambda x : (tuple([x[0][1]]), 
                                                tuple([x[0][0], ((float(x[2])- float(x[1]))/float(x[1]) * 100)])))

lines_RDD_joined = lines_RDD_diff.join(lines_RDD_diff)

lines_RDD_without_duplicates = lines_RDD_joined.filter(lambda x : x[1][0] > x[1][1])

lines_RDD_ticker_ticker = lines_RDD_without_duplicates.map(lambda x : (tuple([x[1][0][0], x[1][1][0]]),
                                                                      tuple([x[0][0], x[1][0][1], x[1][1][1]])))
lines_RDD_ticker_ticker = lines_RDD_ticker_ticker.filter(lambda x : (abs(float(x[1][1]) - float(x[1][2])) <= SOGLIA))

lines_RDD_ticker_ticker = lines_RDD_ticker_ticker.groupByKey().map(lambda x : (x[0], list(x[1])))

lines_RDD_ticker_ticker = lines_RDD_ticker_ticker.filter(lambda x : len(x[1]) == 12)

sorted_RDD_ticker_ticker = lines_RDD_ticker_ticker.sortByKey().map(lambda x : (tuple([x[0][0],x[0][1]]), sorted(x[1], key = lambda k : k[0])))

spark.sparkContext.parallelize(sorted_RDD_ticker_ticker.collect()).saveAsTextFile(output_filepath)

