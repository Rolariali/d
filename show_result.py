import csv
import json
import pprint
from statistics import mean, median

path = "logs/results-2.csv"

d_results = {}

filter_file = ""



with open(path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        i = 0
        name = row[i]

        if not name.startswith(filter_file):
            continue
        i += 1
        rle = row[i]
        i += 1
        delta = row[i]
        i += 1
        m2delta = row[i]
        i += 1
        bp = row[i]
        i += 1
        size = row[i]
        i += 1
        bytes = row[i]
        i += 1
        result = row[i]
        # print(size)

        cases = {}
        case = f"{rle}/{delta}/{bp}/{size}"

        if name not in d_results:
            d_results[name] = {}

        if case not in d_results[name]:
            d_results[name][case] = {}

        _M2_MODE =  "m2delta mode"
        _COMMON = "commom delta mode"
        _PROC = "rate"

        mode = _M2_MODE if m2delta == "True" else _COMMON

        d_results[name][case][mode] = result



max_proc = 0
all_avarage_proc = []

for name, cases in d_results.items():
    min_result = -100
    avarege = []
    max_result = 100
    for case, result in cases.items():
        M2 = result[_M2_MODE]
        old = result[_COMMON]
        proc = (1 - int(old) / int(M2)) * 100
        result[_PROC] = proc

        if min_result < proc:
            min_result = proc

        if max_result > proc:
            max_result = proc

        avarege.append(proc)
        all_avarage_proc.append(proc)

        if abs(max_proc) < abs(proc):
            max_proc = proc

    avarege = mean(avarege)

    d_results[name] = {
        'min_result': min_result,
             'avarege': avarege,
        'max_result': max_result
                     }

    if name.startswith("Perf") or name.startswith("Acq"):
        continue

    # print(name)
    # print(max_result, avarege, min_result)


# pprint.pp(d_results)

sort_result = sorted(d_results.items(), key=lambda x: x[1]['max_result'])

for result in sort_result:
    name = result[0]
    min_result = result[1]['min_result']
    avarege = result[1]['avarege']
    max_result = result[1]['max_result']
    print(f"{name}, {avarege:.2f}%, {max_result:.2f}%")


# pprint.pprint(d_results)
print(max_proc)
print(mean(all_avarage_proc))
# print(median(all_avarage_proc))

path_json = path + ".json"
with open(path_json, "w") as outfile:
    json.dump(sort_result, outfile, indent=4, sort_keys=False)