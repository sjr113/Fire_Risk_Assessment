from pyspark import SparkContext
from pyspark.mllib.util import MLUtils
import sys
from pyspark.mllib.tree import RandomForestModel
from pyspark.mllib.tree import RandomForest
from pyspark.mllib.classification import LogisticRegressionModel
from pyspark.mllib.evaluation import MulticlassMetrics


def test_on_random_forest_model():
    sc = SparkContext(appName="Random_forest_model_Test_on_data_set_of_fire_risk_assessment")

    # Load and parse the data file into an RDD of LabeledPoint.
    test_data = MLUtils.loadLibSVMFile(sc, sys.argv[1])

    same_model = RandomForestModel.load(sc, sys.argv[2])

    predictions = same_model.predict(test_data.map(lambda x: x.features))

    # predict
    # # Evaluate model on test instances and compute test error

    # labelsAndPredictions = test_data.map(lambda lp: lp.label).zip(predictions)
    # testMSE = labelsAndPredictions.map(lambda (v, p): (v - p) * (v - p)).sum() / \
    #           float(test_data.count())
    # print('Test Mean Squared Error = ' + str(testMSE))
    # print('Learned regression forest model:')
    # print(same_model.toDebugString())

    sc.stop()


def test_on_logistic_regression_model():
    sc = SparkContext(appName="logistic_regression_model_Test_on_data_set_of_fire_risk_assessment")

    # Load and parse the data file into an RDD of LabeledPoint.
    test_data = MLUtils.loadLibSVMFile(sc, sys.argv[1])

    # note !!!

    same_model = LogisticRegressionModel.load(sc, sys.argv[2])

    valpredictionAndLabel = test_data.map(lambda lp: (float(same_model.predict(lp.features)), lp.label))
    valmetrics = MulticlassMetrics(valpredictionAndLabel)

    # Evaluate model on test instances and compute test error
    same_model.clearThreshold()
    predictions = same_model.predict(test_data.map(lambda x: x.features))

    #  Predict
    # labelsAndPredictions = test_data.map(lambda lp: lp.label).zip(predictions)
    # testMSE = labelsAndPredictions.map(lambda (v, p): (v - p) * (v - p)).sum() / \
    #           float(test_data.count())
    # print('Test Mean Squared Error = ' + str(testMSE))
    # # print('Learned regression forest model:')
    # # print(same_model.toDebugString())
    #
    # precision = valmetrics.precision()
    # recall = valmetrics.recall()
    # f1Score = valmetrics.fMeasure()
    # print("Summary Stats")
    # print("Precision = %s" % precision)
    # print("Recall = %s" % recall)
    # print("F1 Score = %s" % f1Score)
    predictions.repartition(1).saveAsTextFile(sys.argv[3])

    sc.stop()


if __name__ == "__main__":
    # test_on_random_forest_model()
    test_on_logistic_regression_model()