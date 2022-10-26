d = {"1": ["a","b", "c"]}

for key, value in d.items():
    new_value = []
    for item in value:
        item = "d_{}".format(item)
        new_value.append(item)
    d[key]=new_value


print(d)