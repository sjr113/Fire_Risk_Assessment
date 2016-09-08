# A feature transformer that projects vectors to a low-dimensional space using PCA.
# param k number of principal components

import numpy as np
import matplotlib.pyplot as plt


def loadDataSet(fileName, delim='\t'):
    fr = open(fileName)
    stringArr = [line.strip().split(delim) for line in fr.readlines()]
    datArr = [map(float, line) for line in stringArr]
    return np.mat(datArr)


def principle_component_analysis(data_set, top_nfeature=9999999):

    # compute the mean of the data set
    mean_val = np.mean(data_set, axis=0)
    # minus the mean of the data set to make the data set more soft
    mean_removed = data_set - mean_val

    # compute the convariance matrix
    cov_mat = np.cov(mean_removed, rowvar=0)
    # compute the eigen_value and eigen_vector of the convariance matrix
    eig_val, eig_vector = np.linalg.eig(np.mat(cov_mat))

    # sort the eigen_value of that convariance matrix
    eig_val_ind = np.argsort(eig_val)
    # get the given number (top_nfeature) eigen_values of the convariance matrix
    eig_val_sort = eig_val_ind[:-(top_nfeature + 1): -1]
    # get the given number (top_nfeature) eigen_vectors of the convariance matrix
    red_eig_vector = eig_vector[:, eig_val_sort]

    # transfer the original data set to the new feature space to get the reconstructed data set
    low_data_set = mean_removed * red_eig_vector
    recon_data = (low_data_set * red_eig_vector.transpose()) + mean_val

    return low_data_set, recon_data


def plotBestFit(dataSet1, dataSet2):
    dataArr1 = np.array(dataSet1)
    dataArr2 = np.array(dataSet2)
    n = np.shape(dataArr1)[0]
    n1 = np.shape(dataArr2)[0]
    xcord1 = []
    ycord1 = []
    xcord2 = []
    ycord2 = []
    xcord3 = []
    ycord3 = []
    j = 0
    for i in range(n):
        xcord1.append(dataArr1[i, 0])
        ycord1.append(dataArr1[i, 1])
        xcord2.append(dataArr2[i, 0])
        ycord2.append(dataArr2[i, 1])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')

    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()


import sys
import data_read_and_form_transform.trans_data_from_libsvm_to_normal as data_trans
import data_read_and_form_transform.trans_data_from_normal_to_libsvm as libsvm_trans

def test_PCA(a, b, num):

    label, data_set = data_trans.trans_data_from_libsvm_to_normal(a)
    print data_set

    num_feature = len(data_set[0])
    num_sample = len(label)

    data_set = np.array(data_set)
    print np.shape(data_set[0])
    print np.shape(data_set[1])
    print np.shape(data_set[2])
    print np.shape(data_set[3])
    print np.shape(data_set[4])
    print np.shape(data_set[5])
    print np.shape(data_set)
    print data_set
    lowDDataMat, reconMat = principle_component_analysis(data_set, num)

    plotBestFit(lowDDataMat, reconMat)

    libsvm_trans.se_trans_data_from_normal_to_libsvm(label, lowDDataMat, b)

# from pyspark.mllib.util import MLUtils
if __name__ == '__main__':
    # mata = loadDataSet('testSet.txt')
    # a, b = pca(mata, 2)
    # plotBestFit(a, b)
    #
    # sc = SparkContext(appName="LogisticRegressionWithElasticNet")
    # training = MLUtils.loadLibSVMFile(sc, sys.argv[1])

    # a = "/home/jiangrongshen/PycharmProjects/FireAssessment/data_read_and_form_transform/example_libsvm_data_file.txt"
    # b = "/home/jiangrongshen/PycharmProjects/FireAssessment/data_read_and_form_transform/test_example_libsvm_data_file.txt"

    test_PCA(sys.argv[1], sys.argv[3], int(sys.argv[2]))
    # test_PCA(a, b, 2)