from pyspark.mllib.util import MLUtils
from pyspark import SparkContext


if __name__ == "__main__":
    sc = SparkContext(appName="test_on_read_libsvm_data")
    # valdata_path = "/user/tmp/sample_libsvm_data.txt"
    valexamples = MLUtils.loadLibSVMFile(sc, "example_libsvm_data_file.txt").cache()

    radio_of_training_set = 0.7
    # split the samples to training samples and testing samples
    valsplits = valexamples.randomSplit([radio_of_training_set, 1-radio_of_training_set], seed=11L)
    valtraining = valsplits[0].cache()
    valtest = valsplits[1]

    valnumTraining = valtraining.count()
    valnumTest = valtest.count()
    print valnumTraining, valnumTest