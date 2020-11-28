import check
def to_list(str):
    res = []
    if len(str) == 0:
        return res

    i = 0

    while i < len(str):
        j = 0
        if str[i] == '"':
            j = str.find('"', i + 1)
            if j == -1:
                print("Miss match pair")
                exit(0)
            j = j + 1
        else:
            j = str.find(',', i)
            if j == -1:
                j = len(str) # The last one
            # print(j)

        if i == j:
            res.append('')
        else:
            # print(str[i:j])
            res.append(str[i:j])
        i = j + 1

    if str[len(str) - 1] == ',':
        res.append('')

    # check
    # check.check(to_string(res) != str, "Utils split str error" + str)

    return res


def to_string(l):
    s = ''
    for e in l:
        if e.find(',') != -1 and e[0] != '"':
            s = s + '"'
        s = s + e
        if e.find(',') != -1 and e[len(e) - 1] != '"':
            s = s + '"'
        s = s + ','

    return s[:len(s) - 1]

if __name__ == '__main__':
    str = '30010024,*,04130601,摩托车,报废,行政,捐赠,2005-11-01,原值,5000,5000,1,5000,仪器设备,,,已入账,交通运输设备,后勤保卫处,,后勤保卫处,,,2005-11-01,*,无,JY60T-2,建设,无,2005-11-01,96,,,*,,,,自筹经费,,学校经费,,,'
    str1 = 'S01807340,,12030110,充电手电钻,在用,生活与后勤,购置,2018-12-10,原值,1132.75,1132.75,1,0,仪器设备,9600015052$|1132.75$|^|,2019-01-15 08:30:35,未入账,低值耐耗品,后勤保卫处,曾苑龙,后勤保卫处,,,,00660771,博世,*,"GSR 14,4-2-LI",博世电动工具（中国）有限公司,2018-12-10,72,,,维修部,珠海洋明商贸有限公司,808000077,2018-08-02,自筹经费,,学校经费,,2018,201709'
    info = to_list(str1)
    str_rebuild = to_string(info)
    if str1 != str_rebuild:
        print(str1)
        print(str_rebuild)
        print("rebuild error")
        exit(0)

    info1 = str1.split(',')
    for i in range(0, len(info)):
        print(info[i], '<---->', info1[i])
    print('---', info1[42], '---')
    print(len(info), len(info1))