from pyspark.mllib.feature import ChiSqSelector
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint


def Chi_square(df):
    selector = ChiSqSelector(numTopFeatures=1)
    model = selector.fit(df)

    # temp_path = "/"
    # chiSqSelectorPath = temp_path + "/chi-sq-selector"
    # selector.save(chiSqSelectorPath)

    print model.transform(Vectors.sparse(3, {1: 9.0, 2: 6.0}))
    print model.transform(Vectors.dense([8.0, 9.0, 5.0]))

if __name__ == "__main__":
    data = [LabeledPoint(0.0, Vectors.sparse(3, {0: 8.0, 1: 7.0})),
            LabeledPoint(1.0, Vectors.sparse(3, {1: 9.0, 2: 6.0})),
            LabeledPoint(1.0, [0.0, 9.0, 8.0]),
            LabeledPoint(2.0, [8.0, 9.0, 5.0])]

    Chi_square(data)




