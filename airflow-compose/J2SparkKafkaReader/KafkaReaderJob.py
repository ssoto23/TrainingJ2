import pyspark
from pyspark.sql import SparkSession

if __name__ == "__main__":
    config = pyspark.SparkConf()
    config.setMaster('spark://spark:7077')

    spark = SparkSession \
        .builder \
        .master('spark://spark:7077') \
        .appName("J2Test") \
        .getOrCreate()

    dataFrame = spark.parallelize(range(1, 50), 3)
    print dataFrame.count()
