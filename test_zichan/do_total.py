import os
import constant
import check
import utils
import parse_system_file

def do_total_ext(out_file):
    total_dict = {}
    total_dict['data'] = []
    key_list = []
    total_files = os.listdir(constant.total_file_path)
    for i in total_files:
        if i.find('.csv') == -1:
            continue
        target = constant.total_file_path + i
        data = parse_system_file.parse_system_file_ext(target)
        if 'header' not in total_dict:
            total_dict['header'] = data['header']
        check.check(utils.to_string(total_dict['header']) != utils.to_string(data['header']),
                    "Header missmatch in {}".format(i))
        for info in data['data']:
            key = info['卡片编号']
            check.check(key in key_list, "{} {} 卡片编号 重复".format(i, key))
            key_list.append(key)
            total_dict['data'].append(info)

    aa = 0
    bb = 0
    for i in total_dict['data']:
        if i['使用状态'] == '报废':
            aa = aa + 1
        else:
            bb = bb + 1
    print("do_total_ext {}, 总共: {}, 在用: {}, 报废: {}".format(constant.total_file_path, len(total_dict['data']), aa, bb))
    return total_dict

def do_total(out_file):
    total_dict = {}
    total_files = os.listdir(constant.total_file_path)
    should_write_header = True
    header = ''
    with open(out_file, 'w') as f:
        for i in total_files:
            if i.find('.csv') == -1:
                continue
            target = constant.total_file_path + i
            (h, l, m) = parse_system_file.parse_system_file(target)
            if should_write_header:
                f.write(h)
                header = h;
                should_write_header = False
            for line in l:
                f.write(line)
            for k in m:
                total_dict[k] = m[k]

    aa = 0
    bb = 0
    for i in total_dict:
        if total_dict[i]['status'] == 1:
            aa = aa + 1
        else:
            bb = bb + 1
    print("{}, 总共: {}, 在用: {}, 报废: {}".format(constant.total_file_path, len(total_dict), aa, bb))
    return (header, total_dict)

def do_total_discard(header, total_dict, discard_file, out_file):
    delta_dict = {}
    discard_dict = {}
    discard_header = {}
    with open(discard_file, 'r') as f:
        discard_header = f.readline()
        while True:
            line = f.readline()
            if not line:
                # print("Reach {} EOF".format(f))
                break
            info = line.split(',')
            discard_dict[info[2]] = line

    with open(out_file, 'w') as f:
        f.write(header)
        for i in total_dict:
            if i not in discard_dict:
                delta_dict[i] = total_dict[i]
                f.write(total_dict[i]['line'])
    cc = 0
    with open(constant.base_path + "处理-二次报废没有在总账.csv", 'w') as f:
        f.write(discard_header)
        for i in discard_dict:
            if i not in total_dict:
                f.write(discard_dict[i])
                cc = cc + 1
    aa = bb = 0
    for i in delta_dict:
        if total_dict[i]['status'] == 1:
            aa = aa + 1
        else:
            bb = bb + 1
    print("报废更新, 总共: {},  新增报废: {}, 剩余在用: {}, 二次报废没在总账: {}".format(len(total_dict), len(discard_dict), aa, cc))
    return delta_dict

if __name__ == '__main__':
    (h, total_dict) = do_total(constant.base_path + "处理-系统资产总表.csv")
    do_total_discard(h, total_dict, constant.total_minus_file, constant.base_path + "处理-系统资产总表-二次报废.csv")