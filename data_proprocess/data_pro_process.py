# This file is used to process the original data

import sys

from pyspark.sql import SQLContext
from pyspark import SparkContext, SparkConf

from pyspark.sql import HiveContext


def data_read_from_sql():

    # SQL excutor
    conf = SparkConf().setAppName("spark_sql")
    sc = SparkContext(conf=conf)
    sql_context = SQLContext(sc)

    # SQL Hive
    conf = SparkConf().setAppName("spark_sql")
    sc = SparkContext(conf=conf)
    sql_context = HiveContext(sc)




