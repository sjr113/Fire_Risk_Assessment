from __future__ import print_function

from pyspark import SparkContext
from pyspark.sql import SQLContext
# $example on$
from pyspark.ml.classification import LogisticRegression
from pyspark.mllib.classification import LogisticRegressionWithSGD
from pyspark.mllib.util import MLUtils
from pyspark.mllib.evaluation import MulticlassMetrics
# $example off$
import sys


def lr_ml():
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


def spark_1_4_logistic_regression(data_set, model_path, radio_of_training_set, c_valnumIterations, c_valstepSize,
                                  c_valminiBatchFraction):
    sc = SparkContext(appName="LogisticRegressionWithElasticNet" + "c_valnumIterations" + str(c_valnumIterations))
    # valdata_path = "/user/tmp/sample_libsvm_data.txt"
    valexamples = MLUtils.loadLibSVMFile(sc, data_set).cache()

    # split the samples to training samples and testing samples
    valsplits = valexamples.randomSplit([radio_of_training_set, 1-radio_of_training_set], seed=11L)
    valtraining = valsplits[0].cache()
    valtest = valsplits[1]
    valnumTraining = valtraining.count()
    valnumTest = valtest.count()
    # print(s"Training: $numTraining, test: $numTest.")
    print("miao-miao-miao-miao-miao-miao-miao-miao-miao-miao-miao-miao-miao-miao-miao")
    print("Training" + str(valnumTraining) + "  Testing" + str(valnumTest))

    valnumIterations = c_valnumIterations
    valstepSize = c_valstepSize
    valminiBatchFraction = c_valminiBatchFraction
    valmodel = LogisticRegressionWithSGD.train(valtraining, valnumIterations, valstepSize, valminiBatchFraction)

    # valprediction = valmodel.predict(valtest.map(lambda x: x.features))
    # valpredictionAndLabel = valprediction.zip(valtest.map(lambda x: x.label) * 1.0)
    valpredictionAndLabel = valtest.map(lambda lp: (float(valmodel.predict(lp.features)), lp.label))
    valmetrics = MulticlassMetrics(valpredictionAndLabel)

    # # Save and load model
    valmodel.save(sc, model_path)
    print("miao--miao--miao--miao--miao--miao--miao--miao--miao--miao--miao--miao--miao")

    precision = valmetrics.precision()
    recall = valmetrics.recall()
    f1Score = valmetrics.fMeasure()
    print("Summary Stats")
    print("Precision = %s" % precision)
    print("Recall = %s" % recall)
    print("F1 Score = %s" % f1Score)

    sc.stop()

    # result
    # Summary Stats
    # Precision = 1.0
    # Recall = 1.0
    # F1
    # Score = 1.0
