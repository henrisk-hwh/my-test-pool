import constant
def get_expand_file_name(file):
    info = file.split('.')
    name = '处理-' + info[0] + '-展开.csv'
    return name

def getKeyRange(key):
    key_range = []
    if key.find('-') == -1:
        key_range.append(key)
        return key_range

    rangs = key.split('-')
    if len(rangs) != 2:
        print("Key Range error:".format(rangs))
        exit(0)
    key_idx = 0
    if len(rangs[0]) != len(rangs[1]):
        print("rangs missmatch", rangs, len(rangs[0]), len(rangs[1]))
        exit(0)
    for i in range(0, len(rangs[0])):
        if rangs[0][i] != rangs[1][i]:
            key_idx = i
            break
    rangs_start = rangs[0][:key_idx]
    rangs_end1 = int(rangs[0][key_idx:])
    rangs_end2 = int(rangs[1][key_idx:])
    # print(key, rangs_start, rangs_end1, rangs_end2, rangs_end2 - rangs_end1 + 1)
    for i in range(rangs_end1, rangs_end2 + 1):
        delta = len(str(rangs_end2)) - len(str(i))
        delta_str = ''
        for ii in range(0, delta):
            delta_str = delta_str + '0'
        new_key = rangs_start + delta_str + str(i)
        if len(new_key) != len(rangs[1]) or len(new_key) != len(rangs[0]):
            print(" ***** ", new_key, key)
            exit(0)
        key_range.append(new_key)

    return key_range

def do_expand(infile, outfile):
    aa = 0
    with open(outfile, 'w') as fout:
        with open(infile, 'r') as fin:
            header = fin.readline()
            fout.write(header)
            while True:
                line = fin.readline()
                if not line:
                    print("Read {} EOF".format(fin))
                    break

                idx = line.find(',')
                if idx == -1:
                    print("{} line {} --- idx error".format(fin, line))
                    exit(0)
                key = line[:idx]
                info = line.split(',')
                num = info[3]
                should_write_line = True
                keys = getKeyRange(key)
                # if num != '' and len(keys) != int(num):
                #     print("{} line {} --- Num error {} {}".format(fin, line, len(keys), num))
                #     print(keys)
                    # exit(0)
                for k in keys:
                    aa = aa + 1
                    write_line = k + line[idx:]
                    if should_write_line:
                        fout.write(write_line)
                        should_write_line = False
                    else:
                        fout.write(k)
                        fout.write('\n')
    print("{}, 共: {}".format(infile, aa))

def check_repeat(files, outfile):
    aa = 0
    total = {}
    repeat = {}
    frepeat = open(outfile, 'w')
    should_write_header = True
    for f in files:
        repeat[f] = 0
        with open(f, 'r') as fin:
            header = fin.readline()
            if should_write_header:
                frepeat.write(header)
                should_write_header = False
            while True:
                line = fin.readline()
                if not line:
                    print("Read {} EOF".format(fin))
                    break
                idx = line.find(',')
                key = line[:idx]
                if key not in total:
                    total[key] = {}
                    total[key]['line'] = line
                    total[key]['file'] = f
                else:
                    if f == total[key]['file']:
                        repeat[f] = repeat[f] + 1
                    frepeat.write(line)
                    # print("重复: {}".format(line), end='')
                    aa = aa + 1
    print("重复: {}, 剩余: {}".format(aa, len(total)))
    print(repeat)
    return total

if __name__ == '__main__':

    file1 = constant.data_file_perfix + '-有实有账.csv'
    outfile1 = get_expand_file_name(file1)
    do_expand(constant.data_file_path + file1, constant.base_path + outfile1)

    file2 = constant.data_file_perfix + '-有账无实.csv'
    outfile2 = get_expand_file_name(file2)
    do_expand(constant.data_file_path + file2, constant.base_path + outfile2)

    check_repeat([constant.base_path + outfile1, constant.base_path + outfile2], constant.base_path + "处理-" + constant.data_file_perfix + "-重复.csv")
    # file3 = '新清查明细表-汇总.csv'
    # outfile3 = get_expand_file_name(file3)
    # do_expand(constant.data_file_path + file3, constant.base_path + outfile3)
