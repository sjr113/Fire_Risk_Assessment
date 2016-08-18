from __future__ import print_function

from pyspark import SparkContext
from pyspark.sql import SQLContext
# $example on$
from pyspark.ml.feature import PCA
from pyspark.mllib.linalg import Vectors
# $example off$


def PCA(data_set, pca_k=3):
    sc = SparkContext(appName="PCAExample")
    sqlContext = SQLContext(sc)

    df = sqlContext.createDataFrame(data_set, ["features"])
    pca = PCA(k=3, inputCol="features", outputCol="pcaFeatures")
    model = pca.fit(df)
    result = model.transform(df).select("pcaFeatures")
    result.show(truncate=False)
    # $example off$

    sc.stop()

if __name__ == "__main__":
    # $example on$
    data_set = [(Vectors.sparse(5, [(1, 1.0), (3, 7.0)]),),
            (Vectors.dense([2.0, 0.0, 3.0, 4.0, 5.0]),),
            (Vectors.dense([4.0, 0.0, 0.0, 6.0, 7.0]),)]
    PCA(data_set, pca_k=3)
