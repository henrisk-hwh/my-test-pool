import os
import constant
import parse_system_file

def do_dispatch(out_file):
    total_dict = {}
    total_files = os.listdir(constant.dispatch_file_path)
    should_write_header = True
    with open(out_file, 'w') as f:
        for i in total_files:
            if i.find('.csv') == -1:
                continue
            target = constant.dispatch_file_path + i
            (h, l, m) = parse_system_file.parse_system_file(target)
            if should_write_header:
                f.write(h)
                should_write_header = False
            for line in l:
                f.write(line)
            for k in m:
                total_dict[k] = m[k]

    return total_dict