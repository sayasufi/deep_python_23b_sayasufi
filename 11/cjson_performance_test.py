import time
import json

import ujson

import cjson


load_c, load_u, load_j = [], [], []
dump_c, dump_u, dump_j = [], [], []

for digit in range(1, 6):
    with open(f'./test{digit}.json', 'r', encoding='UTF-8') as f:
        big_json_str = json.dumps(json.load(f))

        start = time.time()
        big_dict = cjson.loads(big_json_str)
        end = time.time()
        load_c.append(round(end - start, 10))

        start = time.time()
        big_dict = ujson.loads(big_json_str)
        end = time.time()
        load_u.append(round(end - start, 10))

        start = time.time()
        big_dict = json.loads(big_json_str)
        end = time.time()
        load_j.append(round(end - start, 10))


        start = time.time()
        cjson.dumps(big_dict)
        end = time.time()
        dump_c.append(round(end - start, 10))

        start = time.time()
        ujson.dumps(big_dict)
        end = time.time()
        dump_u.append(round(end - start, 10))

        start = time.time()
        json.dumps(big_dict)
        end = time.time()
        dump_j.append(round(end - start, 10))

        print(f'{digit} file complete')


print("=================================LOADS============================")
print(f"CJSON: {*load_c,} seconds")
print(f"UJSON: {*load_u,} seconds")
print(f"JSON:  {*load_j,} seconds")
print("=================================DUMPS============================")
print(f"CJSON: {*dump_c,} seconds")
print(f"UJSON: {*dump_u,} seconds")
print(f"JSON:  {*dump_j,} seconds")