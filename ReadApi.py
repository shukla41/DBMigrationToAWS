import sys
import urllib3
import json
from pyspark.sql import SparkSession,Row
from collections import OrderedDict
from pyspark.sql import SQLContext


http = urllib3.PoolManager()
url='http://127.0.0.1:5000/Metadata/tgt/mobile'
rawJson=http.request("GET",url)
parseData = json.loads(rawJson.data.decode('UTF-8'))

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

sc=spark.sparkContext
df = sc.parallelize(parseData).map(lambda x: json.dumps(x))
df = spark.read.json(df)
df.show()



