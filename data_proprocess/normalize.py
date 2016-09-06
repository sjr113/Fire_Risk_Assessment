from pyspark.mllib.feature import Normalizer
from pyspark.mllib.util import MLUtils
from pyspark import SparkContext
import sys


def normalize():
    sc = SparkContext(appName="Normalize")
    data = MLUtils.loadLibSVMFile(sc, sys.argv[1])
    labels = data.map(lambda x: x.label)
    features = data.map(lambda x: x.features)

    normalizer1 = Normalizer()
    normalizer2 = Normalizer(p=float("inf"))

    # Each sample in data1 will be normalized using $L^2$ norm.
    data1 = labels.zip(normalizer1.transform(features))

    # Each sample in data2 will be normalized using $L^\infty$ norm.
    data2 = labels.zip(normalizer2.transform(features))

    data1.saveAsLibSVMFile(sc, sys.argv[2])
    print "_______________________________________"
    print "///////////////////////////////////////"

    sc.stop()


if __name__ == "__main__":
    normalize()