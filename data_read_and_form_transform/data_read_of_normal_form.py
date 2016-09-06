import numpy as np


def read_data_of_normal_form(file_name):
    f = open(file_name)
    line = f.readline()
    list1 = []
    while line:
        # print line
        arr = map(float, line.split())
        list1.append(arr)

        line = f.readline()

    f.close()

    label = np.zeros(6)
    data_set = np.zeros((6, 64))
    for i in range(6):
        arr = list1[i]
        label[i] = arr[0]
        data_set[i] = arr[1:]

    return label, data_set


if __name__ == "__main__":
    label, data_set = read_data_of_normal_form("example_normal_data_file")
    print label, data_set