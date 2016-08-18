import numpy as np


def trans_data():
    f = open("fra_data")
    line = f.readline()
    list1 = []
    while line:
        # print line
        arr = map(float, line.split())
        list1.append(arr)
        print arr
        line = f.readline()

    f.close()
    return list1


if __name__ == "__main__":
    list1 = trans_data()

    print np.size(list1)
    # print list1[0]
    # print list1[1]
    # print list1[2]
    # print list1[3]
    label = np.zeros(6)
    data_set = np.zeros((6, 64))
    for i in range(6):
        arr = list1[i]
        label[i] = arr[0]
        data_set[i] = arr[1:]

    print np.shape(data_set)

    list2 = [i for i in range(64)]
    print list2

    # make the list to the dictionary

    # f = file("fra_data_for_rf.txt", "w+")
    # dict_1 = {}
    # for i in range(6):
    #     dict_1 = str(list1[i][0]) + "," + str(dict(zip(list2, list1[i][1:]))) + "\n"
    #     f.writelines(dict_1)
    # f.close()

    f = file("fra_data_for_rf.txt", "w+")
    dict_1 = {}
    for i in range(6):
        str_1 = str(list1[i][0])
        for j in range(64):
            if str(list1[i][j+1]) != "nan":
                str_1 += " " + str(list2[j]) + ":" + str(list1[i][j+1])
        str_1 += "\n"
        f.writelines(str_1)
    f.close()


