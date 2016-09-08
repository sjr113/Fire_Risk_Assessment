import numpy as np


def read_data_of_normal_form(file_name, num_sample = 6, num_feature=64):
    f = open(file_name)
    line = f.readline()
    list1 = []
    while line:
        # print line
        arr = map(float, line.split())
        list1.append(arr)

        line = f.readline()

    f.close()

    label = np.zeros(num_sample)
    data_set = np.zeros((num_sample, num_feature))
    for i in range(num_sample):
        arr = list1[i]
        label[i] = arr[0]
        data_set[i] = arr[1:]

    return label, data_set


if __name__ == "__main__":
    label, data_set = read_data_of_normal_form("example_normal_data_file")
    print label, data_set