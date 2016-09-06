

# Try to transform the "libsvm" form to the normal form, that is, label + data(features)
def trans_data_from_libsvm_to_normal(file_name):
    f = open(file_name)
    line = f.readline()
    list_label = []
    list_data = []

    while line:

        list_temp = []
        arr = line.split()
        list_label.append(float(arr[0]))
        for i in range(len(arr)-1):
            temp_a = int(arr[i+1].split(":")[0])
            if temp_a == (i + 1) and arr[i+1].split(":")[1] != "nan":
                list_temp.append(float(arr[i+1].split(":")[1]))
            elif temp_a == (i + 1) and arr[i+1].split(":")[1] == "nan":
                list_temp.append("nan")
            elif temp_a != (i + 1):
                for m in range(i+1-temp_a):
                    list_temp.append(0.0)
        list_data.append(list_temp)
        line = f.readline()

    f.close()
    return list_label, list_data


if __name__ == "__main__":
    list_label, list_data = trans_data_from_libsvm_to_normal("example_libsvm_data_file.txt")
    print list_label
    print list_data