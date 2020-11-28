import constant
import parse_system_file
import do_expand

if __name__ == '__main__':
    (h, l, m) = parse_system_file.parse_system_file(constant.base_path + "处理-系统资产总表-二次报废.csv")
    aa = bb = 0
    for i in m:
        if m[i]['status'] == 1:
            aa = aa + 1
        else:
            bb = bb + 1

    file1 = constant.data_file_perfix + '-有实有账.csv'
    file2 = constant.data_file_perfix + '-有账无实.csv'
    outfile1 = do_expand.get_expand_file_name(file1)
    outfile2 = do_expand.get_expand_file_name(file2)

    real = do_expand.check_repeat([constant.base_path + outfile1, constant.base_path + outfile2], constant.base_path + "处理-清查情况汇总表-2020-11-24-重复.csv")
    aa = bb = cc = dd = 0
    fout1 = open(constant.base_path + '处理-' + constant.data_file_perfix + '-总账有清查无.csv', 'w')
    fout2 = open(constant.base_path + '处理-' + constant.data_file_perfix + '-清查有总账无.csv', 'w')
    for i in m:
        if i not in real:
            if m[i]['status'] == 1:
                # print(m[i]['line'])
                fout1.write(m[i]['line'])
                aa = aa + 1
            else:
                bb = bb + 1
        else:
            if m[i]['status'] == 1:
                cc = cc + 1
            else:
                dd = dd + 1

    ii = jj = 0
    for i in real:
        if i not in m:
            ii = ii + 1
            fout2.write(real[i]['line'])
        else:
            if m[i]['status'] != 1:
                jj = jj + 1
                print(m[i]['line'])
    print('总账有，清查无: {}'.format(aa))
    print('总账有，清查有: {}'.format(cc))
    print('总账无，清查有: {}'.format(ii))
    print('总账有(报废)，清查有: {}'.format(jj))
    print(aa, bb, cc, dd, ii, jj)

    fout1.close()
    fout2.close()

