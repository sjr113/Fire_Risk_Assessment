from __future__ import with_statement

import ConfigParser
import sys

from random_forest import random_forest


def fire_risk_assessment():
    pass


if __name__ == "__main__":

    # random forest algorithm
    # config the object of ConfigParser to make the .conf to parser
    config = ConfigParser.ConfigParser()
    with open("fra_conf.conf", "rw") as conf_file:
        config.readfp(conf_file)

    section_for_rfr = "random_forest_regressions"
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
        max_depth = config.get(section=section_for_rfr, option="max_depth")
        list_max_depth = eval(max_depth)
    except:
        list_max_depth = [5]

    try:
        max_bins = config.get(section=section_for_rfr, option="max_bins")
        list_max_bins = eval(max_bins)
    except:
        list_max_bins = [20]

    try:
        num_trees = config.get(section=section_for_rfr, option="num_trees")
        list_num_trees = eval(num_trees)
    except:
        list_num_trees = [5]

    # model_path = config.get(section=section_for_rfr, option="model_path")

    for c_max_depth in list_max_depth:
        for c_max_bins in list_max_bins:
            for c_num_trees in list_num_trees:
                model_name = "model_of_max_depth_" + str(c_max_depth) + "_max_bins_" + str(c_max_bins) + "_num_trees_" + \
                             str(c_num_trees)
                model_path = sys.argv[2] + "/" + model_name
                # run the regressor of random forest
                random_forest.random_forest_regressor(data_set, model_path, radio_of_training_set, c_max_depth,
                                                      c_max_bins, c_num_trees)
                print model_path

    print data_set
    print radio_of_training_set, list_max_depth, list_max_bins, list_num_trees












