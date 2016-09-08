import numpy as np


# Try to transform the "libsvm" form to the normal form, that is, label + data(features)
def trans_data_from_libsvm_to_normal(file_name, num_feature = 100):
    f = open(file_name)
    line = f.readline()
    list_label = []
    list_data = []

    while line:

        list_temp = []
        arr = line.split()
        list_label.append(float(arr[0]))

        i = 1
        k = 0
        temp_a = int(arr[1].split(":")[0])

        if temp_a > 1:
            for mm in range(temp_a - 1):
                list_temp.append(0.0)
                k = temp_a - 1

        while i < int(len(arr)):
            k += 1
            temp_a = int(arr[i].split(":")[0])

            if temp_a == k and arr[i].split(":")[1] != "nan":
                list_temp.append(float(arr[i].split(":")[1]))
            elif temp_a == k and arr[i].split(":")[1] == "nan":
                list_temp.append(np.nan)
            elif temp_a != k:
                for mmm in range(temp_a-k):
                    list_temp.append(0.0)
                k = temp_a -1

            i += 1
        if k < num_feature:
            for mm in range(num_feature-k):
                list_temp.append(0.0)
        list_data.append(list_temp)
        line = f.readline()

    f.close()
    return list_label, list_data


if __name__ == "__main__":
    list_label, list_data = trans_data_from_libsvm_to_normal("example_libsvm_data_file.txt", num_feature=64)
    print list_label
    print list_data
    list_data = np.array(list_data)
    print np.shape(list_data)
    print np.shape(list_data[0])
    print np.shape(list_data[1])
    print np.shape(list_data[2])
    print np.shape(list_data[3])
    print np.shape(list_data[4])
    print np.shape(list_data[5])
    # print list_data[0]
    # print list_data[1]
    # print list_data[2]
    # print list_data[3]
    # print list_data[4]