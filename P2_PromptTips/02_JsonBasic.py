import json

# dictionary->python data type
d = {
    "name": "周杰轮",
    "age": 11,
    "gender": "男"
}

# convert dictionary into json
s = json.dumps(d, ensure_ascii=False)
print(s)

l = [
    {
        "name": "周杰轮",
        "age": 11,
        "gender": "男"
    },
    {
        "name": "蔡依临",
        "age": 12,
        "gender": "女"
    },
    {
        "name": "小明",
        "age": 16,
        "gender": "男"
    }
]

# also can convert list
print(json.dumps(l, ensure_ascii=False))

json_str = '{"name": "周杰轮", "age": 11, "gender": "男"}'
json_array_str = '[{"name": "周杰轮", "age": 11, "gender": "男"}, {"name": "蔡依临", "age": 12, "gender": "女"}, {"name": "小明", "age": 16, "gender": "男"}]'

res_dct = json.loads(json_str)
print(res_dct, type(res_dct))

res_list = json.loads(json_array_str)
print(res_list, type(res_list))



