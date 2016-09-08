from __future__ import with_statement

import ConfigParser
import sys
import os

import logistic_regression


if __name__ == "__main__":

    # random forest algorithm
    # config the object of ConfigParser to make the .conf to parser
    # print os.getcwd()
    # os.chdir("/home/jiangrongshen/PycharmProjects/FireAssessment/random_forest/")

    config = ConfigParser.ConfigParser()
    with open("lr_conf.conf", "rw") as conf_file:
        config.readfp(conf_file)

    section_for_rfr = "lr"
    # read the file path of data set as text
    # data_set = config.get(section=section_for_rfr, option="data_set")
    data_set = sys.argv[1]

    # try:
    #     radio_of_training_set = config.get(section=section_for_rfr, option="radio_of_training_set")
    #     list_radio_of_training_set = eval(radio_of_training_set)
    # except:
    #     list_radio_of_training_set = [0.7]
    radio_of_training_set = config.getfloat(section=section_for_rfr, option="radio_of_training_set")

    try:
        valnumIterations = config.get(section=section_for_rfr, option="valnumIterations")
        list_valnumIterations = eval(valnumIterations)
    except:
        list_valnumIterations = [1000]

    try:
        valstepSize = config.get(section=section_for_rfr, option="valstepSize")
        list_valstepSize = eval(valstepSize)
    except:
        list_valstepSize = [1]

    try:
        valminiBatchFraction = config.get(section=section_for_rfr, option="valminiBatchFraction")
        list_valminiBatchFraction = eval(valminiBatchFraction)
    except:
        list_valminiBatchFraction = [1.0]

    # model_path = config.get(section=section_for_rfr, option="model_path")

    for c_valnumIterations in list_valnumIterations:
        for c_valstepSize in list_valstepSize:
            for c_valminiBatchFraction in list_valminiBatchFraction:
                model_name = "model_of_valnumIterations_" + str(c_valnumIterations) + "_stepSize_" + str(c_valstepSize)\
                             + "_miniBatchFraction_" + \
                             str(c_valminiBatchFraction)
                model_path = sys.argv[2] + "/" + model_name
                data_path = sys.argv[3] + "/" + model_name + "_result.txt"
                # run the regressor of random forest
                # random_forest.random_forest_regressor(data_set, model_path, radio_of_training_set, c_max_depth,
                #                                       c_max_bins, c_num_trees)
                # random_forest.rdf(data_set)

                print c_valminiBatchFraction
                print "c_valminiBatchFraction is " + str(c_valminiBatchFraction) + "----------------------------------------------"

                logistic_regression.spark_1_4_logistic_regression(data_set, model_path, radio_of_training_set,
                                                                  c_valnumIterations, c_valstepSize, c_valminiBatchFraction, data_path)
                print model_path

    print data_set
    print radio_of_training_set











