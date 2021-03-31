from pyspark import SparkConf
from pyspark.sql import SparkSession
import pyspark
import os
from pyspark import SparkFiles
import os.path
import pyspark.sql.functions as F
import pyspark.sql.types as T
import json
from datetime import datetime
import  pandas as pd
from pyspark import SparkFiles

def create_struct(category, media, desvio = None):
    if desvio != None:
        return str({category:{'media': media, 'desvio': desvio}})
    return str({category:{'media': media}})

def letter(col):
    return col.replace('M', '').strip()


create_struct_udf = F.udf(create_struct, T.StringType())

spark_conf = SparkConf().setAppName('etl')
spark = SparkSession.builder.config(conf=spark_conf).getOrCreate()

url = 'https://github.com/jasonchang0/kaggle-google-apps/raw/master/google-play-store-apps/googleplaystore.csv'
spark.sparkContext.addFile(url)

df = spark.read.csv("file://"+SparkFiles.get("googleplaystore.csv"), header=True, sep=',')

##EXERCICIO 1
df_media_rating = df.select('Category', F.col('Rating').cast(T.DecimalType())).groupBy(['Category']).agg(F.mean(F.col('Rating')).alias('media_rating'))

##EXERCICIO 2
udf_letter = F.udf(letter, T.StringType())
df_desvio = df.select('Genres', udf_letter(F.col('Size')).cast(T.DecimalType()).alias('Size'))\
.groupBy(['Genres'])\
.agg(F.mean(F.col('Size')).alias('media_size'),F.stddev(F.col('Size')).alias('desvio_size'))

##EXERCICIO 3
df_media_review = df.select('Category', F.col('Reviews').cast(T.DecimalType())).groupBy(['Category']).agg((F.mean(F.col('Reviews'))*30).alias('media_review'))

#ARQUIVOS_SAIDA


df_desvio.withColumn('struct', create_struct_udf(F.col('Genres'), F.col('media_size'), F.col('desvio_size'))).select('struct')\
    .withColumn('id', F.lit(0))\
    .groupBy('id')\
    .agg(F.collect_list("struct").alias("data_list"))\
    .drop('id')\
    .repartition(1).write.mode('overwrite').format('json').save('data/desvio_padrao')

df_media_review.withColumn('struct', create_struct_udf(F.col('Category'), F.col('media_review'))).select('struct')\
    .withColumn('id', F.lit(0))\
    .groupBy('id')\
    .agg(F.collect_list("struct").alias("data_list"))\
    .drop('id')\
    .repartition(1).write.mode('overwrite').format('json').save('data/media_review')

df_media_rating.withColumn('struct', create_struct_udf(F.col('Category'), F.col('media_rating'))).select('struct')\
    .withColumn('id', F.lit(0))\
    .groupBy('id')\
    .agg(F.collect_list("struct").alias("data_list"))\
    .drop('id')\
    .repartition(1).write.mode('overwrite').format('json').save('data/media_rating')

df_media_rating.repartition(1).write.mode('overwrite').csv('data/media_rating_csv')
df_desvio.repartition(1).write.mode('overwrite').csv('data/desvio_csv')
df_media_review.repartition(1).write.mode('overwrite').csv('data/media_review_csv')

