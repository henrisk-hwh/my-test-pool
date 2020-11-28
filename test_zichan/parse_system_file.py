import os
import utils
import check

def parse_system_file_header(file):
    header = ''
    with open(file, 'r') as f:
        header = f.readline()
    return header

def parse_system_file_ext(file):
    data_list = []

    with open(file, 'r') as f:
        header = f.readline()
        header_list = utils.to_list(header)
        while True:
            line = f.readline()
            if not line:
                # print("Reach {} EOF".format(f))
                break
            info = utils.to_list(line)
            # info = line.split(',')

            # error check
            if len(header_list) != len(info):
                print(line, len(header_list), len(info))
                for i in range(0, min(len(info), len(header_list))):
                    print(file, header_list[i], info[i])
                    exit(0)

            info_dict = {}
            for i in range(0, len(header_list)):
                info_dict[header_list[i]] = info[i]
            data_list.append(info_dict)
    res = {'header': header_list, 'data': data_list}
    # print(file, len(data_list))
    return res





def parse_system_file(file):
    file_dict = {}
    file_list = []
    header = ''

    with open(file, 'r') as f:
        header = f.readline()
        while True:
            line = f.readline()
            if not line:
                # print("Reach {} EOF".format(f))
                break
            info = line.split(',')
            check.check(info[4] != '报废' and info[4] != '在用', '{} -> {}'.format(file, line))

            # if info[4] == '报废':
            #    continue

            check.check(len(info[0]) <= 0, '编码错误 {} -> {}'.format(file, line))
            check.check(info[0] in file_dict, '编号重复 {} -> {}'.format(file, line))
            file_dict[info[0]] = {}
            file_dict[info[0]]['line'] = line
            if info[4] == '报废':
                file_dict[info[0]]['status'] = 0
            else:
                file_dict[info[0]]['status'] = 1

            file_list.append(line)

    return (header, file_list, file_dict)

def compare_system_dict(header, dict_big, dict_small, out_file):
    delta_dict = {}
    with open(out_file, 'w') as f:
        f.write(header)
        for i in dict_big:
            if i not in dict_small:
                delta_dict[i] = dict_big[i]
                f.write((dict_big[i]))
    delta_dict1 = {}
    for i in dict_small:
        if i not in dict_big:
            delta_dict1[i] = dict_small[i]
    # for i in delta_dict1:
    #     print(delta_dict1[i])
    print("big: {}. small: {}. delta: {}".format(len(dict_big), len(dict_small), len(delta_dict)))
    return delta_dict