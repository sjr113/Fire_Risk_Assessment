"""
Random Forest regression for fire risk assessment
"""

from __future__ import print_function


from pyspark import SparkContext, SQLContext
from pyspark.ml import Pipeline
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.feature import VectorIndexer
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.mllib.util import MLUtils

import sys
from pyspark.mllib.tree import RandomForest, RandomForestModel
from pyspark.mllib.util import MLUtils


def random_forest_regressor(data_set, model_path, radio_of_training_set=0.7, max_depth=5, max_bins = 32, num_trees=20):
    sc = SparkContext(appName="random_forest_regressor_example")
    # sqlContext = SQLContext(sc)

    # $example on$
    # Load and parse the data file, converting it to a DataFrame.
    # data = sqlContext.read.format("libsvm").load("data/mllib/sample_libsvm_data.txt")
    # data = sqlContext.read.format("libsvm").load(data_set)
    data = MLUtils.loadLibSVMFile(sc, data_set)
    # Automatically identify categorical features, and index them.
    # Set maxCategories so features with > 4 distinct values are treated as continuous.
    featureIndexer = VectorIndexer(inputCol="features", outputCol="indexedFeatures").fit(data)

    # Split the data into training and test sets (30% held out for testing)
    # (trainingData, testData) = data.randomSplit([0.7, 0.3])
    (trainingData, testData) = data.randomSplit([radio_of_training_set, 1-radio_of_training_set])

    # Train a RandomForest model.
    rf = RandomForestRegressor(featuresCol="indexedFeatures", maxDepth=max_depth, maxBins=max_bins, numTrees=num_trees)

    # Chain indexer and forest in a Pipeline
    pipeline = Pipeline(stages=[featureIndexer, rf])

    # Train model.  This also runs the indexer.
    model = pipeline.fit(trainingData)

    # Make predictions.
    predictions = model.transform(testData)

    # Select example rows to display.
    predictions.select("prediction", "label", "features").show(5)

    # Select (prediction, true label) and compute test error
    evaluator = RegressionEvaluator(
        labelCol="label", predictionCol="prediction", metricName="rmse")
    rmse = evaluator.evaluate(predictions)

    print("Root Mean Squared Error (RMSE) on test data = %g" % rmse)

    rfModel = model.stages[1]
    print(rfModel)  # summary only
    # $example off$

    # save the model
    model.save(sc, model_path)

    sc.stop()


def rdf(data_set):
    sc = SparkContext(appName="PythonRandomForestRegressionExample")
    # $example on$
    # Load and parse the data file into an RDD of LabeledPoint.
    data = MLUtils.loadLibSVMFile(sc, data_set)
    # Split the data into training and test sets (30% held out for testing)
    (trainingData, testData) = data.randomSplit([0.7, 0.3])

    # Train a RandomForest model.
    #  Empty categoricalFeaturesInfo indicates all features are continuous.
    #  Note: Use larger numTrees in practice.
    #  Setting featureSubsetStrategy="auto" lets the algorithm choose.
    model = RandomForest.trainRegressor(trainingData, categoricalFeaturesInfo={},
                                        numTrees=3, featureSubsetStrategy="auto",
                                        impurity='variance', maxDepth=4, maxBins=32)

    # Evaluate model on test instances and compute test error
    predictions = model.predict(testData.map(lambda x: x.features))
    labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
    testMSE = labelsAndPredictions.map(lambda (v, p): (v - p) * (v - p)).sum() / \
              float(testData.count())
    print('Test Mean Squared Error = ' + str(testMSE))
    print('Learned regression forest model:')
    print(model.toDebugString())

    # # Save and load model
    # model.save(sc, "target/tmp/myRandomForestRegressionModel")
    # sameModel = RandomForestModel.load(sc, "target/tmp/myRandomForestRegressionModel")
    # # $example off$

    # result:
    # Test Mean Squared Error = 0.00358422939068
    # Learned regression forest model:
    # TreeEnsembleModel regressor with 3 trees
    #
    #   Tree 0:
    #     If (feature 462 <= 0.0)
    #      Predict: 0.0
    #     Else (feature 462 > 0.0)
    #      Predict: 1.0
    #   Tree 1:
    #     If (feature 406 <= 0.0)
    #      Predict: 0.0
    #     Else (feature 406 > 0.0)
    #      Predict: 1.0
    #   Tree 2:
    #     If (feature 490 <= 31.0)
    #      If (feature 464 <= 84.0)
    #       Predict: 0.0
    #      Else (feature 464 > 84.0)
    #       Predict: 1.0
    #     Else (feature 490 > 31.0)
    #      Predict: 1.0

if __name__ == "__main__":
    data_set = "data/mllib/sample_libsvm_data.txt"
    model_path = "data/main/myrandomforestmodel"
    random_forest_regressor(data_set, model_path)