import data_read_of_normal_form


def trans_data_from_normal_to_libsvm(file_name, save_file_name):
    label, data = data_read_of_normal_form.read_data_of_normal_form(file_name)
    num_feature = len(data[0])
    list2 = [i for i in range(num_feature)]

    # make the list to the dictionary

    # f = file("fra_data_for_rf.txt", "w+")
    # dict_1 = {}
    # for i in range(6):
    #     dict_1 = str(list1[i][0]) + "," + str(dict(zip(list2, list1[i][1:]))) + "\n"
    #     f.writelines(dict_1)
    # f.close()

    f = file(save_file_name, "w+")
    for i in range(6):
        str_1 = str(label[i])
        for j in range(64):
            if str(data[i][j]) != "nan":
                str_1 += " " + str(list2[j] + 1) + ":" + str(data[i][j])
        str_1 += "\n"
        f.writelines(str_1)
    f.close()


def se_trans_data_from_normal_to_libsvm(label, data, save_file_name):
    # label, data = data_read_of_normal_form.read_data_of_normal_form(file_name)
    num_feature = len(data[0])
    list2 = [i for i in range(num_feature)]

    # make the list to the dictionary

    # f = file("fra_data_for_rf.txt", "w+")
    # dict_1 = {}
    # for i in range(6):
    #     dict_1 = str(list1[i][0]) + "," + str(dict(zip(list2, list1[i][1:]))) + "\n"
    #     f.writelines(dict_1)
    # f.close()

    f = file(save_file_name, "w+")
    for i in range(6):
        str_1 = str(label[i])
        for j in range(64):
            if str(data[i][j]) != "nan":
                str_1 += " " + str(list2[j] + 1) + ":" + str(data[i][j])
        str_1 += "\n"
        f.writelines(str_1)
    f.close()

if __name__ == "__main__":
    trans_data_from_normal_to_libsvm("example_normal_data_file", "example_libsvm_data_file.txt")