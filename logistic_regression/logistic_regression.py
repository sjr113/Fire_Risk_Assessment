from __future__ import print_function

from pyspark import SparkContext
from pyspark.sql import SQLContext
# $example on$
from pyspark.ml.classification import LogisticRegression
from pyspark.mllib.util import MLUtils
# $example off$
import sys


if __name__ == "__main__":
    sc = SparkContext(appName="LogisticRegressionWithElasticNet")
    # sqlContext = SQLContext(sc)

    # $example on$
    # Load training data
    # training = sqlContext.read.format("libsvm").load(sys.argv[1])
    training = MLUtils.loadLibSVMFile(sc, sys.argv[1])
    lr = LogisticRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8)

    # Fit the model
    lrModel = lr.fit(training)

    # Print the coefficients and intercept for logistic regression
    print("Coefficients: " + str(lrModel.coefficients))
    print("Intercept: " + str(lrModel.intercept))
    # $example off$

    sc.stop()

