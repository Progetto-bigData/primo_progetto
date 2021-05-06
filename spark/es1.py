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
spark = SparkSession.builder.appName("Spark ES1").getOrCreate()


lines_RDD = spark.sparkContext.textFile(input_filepath)

lines_RDD = lines_RDD.map(lambda x: x.split(","))

lines_RDD = lines_RDD.map(lambda x: (x[0], [x[2], x[4], x[5], x[7]]))  # close, low, high, date

lines_RDD_grouped = lines_RDD.groupByKey()

lines_RDD_dates_prices = lines_RDD_grouped.map(lambda l: (l[0], min(l[1], key=lambda x: x[3])[3],
                                                          min(l[1], key=lambda x: x[0])[0],
                                                          max(l[1], key=lambda x: x[3])[3],
                                                          max(l[1], key=lambda x: x[0])[0],
                                                          max(l[1], key=lambda x: x[2])[2],
                                                          min(l[1], key=lambda x: x[1])[1]))


def percentage_var(x):
    try:
        return x[0], x[1], x[3], ((float(x[4]) / float(x[2])) * 100) - 100, x[5], x[6]
    except ValueError:
        pass


lines_RDD_percentage_var = lines_RDD_dates_prices.map(percentage_var)
# lines_RDD_percentage_var.collect()
sorted_lines_RDD_percentage_var = lines_RDD_percentage_var.sortBy(lambda x: x[2])
spark.sparkContext.parallelize(sorted_lines_RDD_percentage_var.collect()).saveAsTextFile(output_filepath)



