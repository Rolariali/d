import csv

def _try_parse(value: str)-> int:
    if value.isdigit():
        r = int(value)
        return r

    try:
        r = float(value)
        r = round(r)
        return r
    except:
        return None

delimiter = None

def _parse_file(path: str)-> dict:
    global delimiter
    d_arr = {}
    with open(path) as csv_file:
        try:
            csv_reader = csv.reader(csv_file, delimiter=delimiter)
            for row in csv_reader:
                for pos, value in enumerate(row):
                    ret = _try_parse(value)
                    if ret is None:
                        continue
                    if pos in d_arr:
                        d_arr[pos].append(ret)
                    else:
                        d_arr[pos] = [ret]
        except Exception as e:
            print("can't parse:")
            print(repr(e))
    return d_arr


def _get_best_values(path: str)-> dict:
    d_arr = _parse_file(path)
    d_ret = {}
    for pos, arr in d_arr.items():
        mi = min(arr)
        ma = max(arr)
        lenght = len(arr)
        if lenght < 9999:
            continue
        if mi == ma:
            continue
        if ma/2 < mi:
            continue
        if ma - mi < 100:
            continue

        d_ret[pos] = arr
        # print(pos, lenght, mi, ma)
    return d_ret



def _write_file(out_arr: str, out_file_name: str):
    with open(out_file_name, 'w') as f:
        f.write(out_arr)
    print("written file", out_file_name)


def _calc_str_arr(arr: list):
    out_arr = 'data=[' + ','.join(str(x) for x in arr) + ']'
    size = len(out_arr)
    return size, out_arr


def _pack_best_value(path: str, out_file: str)-> None:
    d_arr = _get_best_values(path)
    out_file = out_file.replace(".", "_")
    for pos, arr in d_arr.items():
        out_file_name = out_file + f'_{pos}.py'
        size, out_arr = _calc_str_arr(arr)
        _MAX = 1024*1024
        if size < _MAX:
            _write_file(out_arr, out_file_name)
            return
        print("batch ", path)
        count = size / _MAX
        count = int(count)
        if count == 1:
            _write_file(out_arr, out_file_name)
            return
        size = len(arr)
        new_size = size/count
        new_size = int(new_size)
        from math import ceil
        chunks = [arr[i * new_size:(i * new_size) + new_size] for i in range(ceil(len(arr) / new_size))]
        print("batch more for path", path, "count", count, "new_size", new_size, "chunks", len(chunks))
        for i, chunk in enumerate(chunks):
            out_file_name = out_file + f'_{pos}_add_{i}.py'
            size, out_arr = _calc_str_arr(chunk)
            _write_file(out_arr, out_file_name)



def _packing_to_file(path: str, out_dir: str)-> None:
    import os
    file_name = os.path.basename(path)
    out_file_template = out_dir + file_name
    _pack_best_value(path, out_file_template)

def parse_all_files(path: str, out_dir: str)-> None:
    import glob
    for filenames in glob.glob(path):
        _packing_to_file(filenames, out_dir)
        print(filenames, out_dir)


delimiter = '|'
# parse_all_files('/Users/a1/gpu/dataset/mortgage_2000-2001/acq/*', '/Users/a1/gpu/dataset/out/')
# parse_all_files('/Users/a1/gpu/dataset/mortgage_2000-2001/perf/*', '/Users/a1/gpu/dataset/out/')

delimiter = ','
# parse_all_files('/Users/a1/gpu/dataset/Walmart/*', '/Users/a1/gpu/dataset/out/')

parse_all_files('/Users/a1/gpu/dataset/covid19/*', '/Users/a1/gpu/dataset/out/')
parse_all_files('/Users/a1/gpu/dataset/india/*', '/Users/a1/gpu/dataset/out/')
parse_all_files('/Users/a1/gpu/dataset/car/*', '/Users/a1/gpu/dataset/out/')
parse_all_files('/Users/a1/gpu/dataset/brazil/*', '/Users/a1/gpu/dataset/out/')

