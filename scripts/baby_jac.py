import yaml

from app.definitions import BuildSpec

content = open("content.txt", "r").readlines()

filepath = "../build_specs/pck/abs.yaml"
with open(filepath) as y:
    build_spec: BuildSpec = yaml.safe_load(y.read())


def strip(content: list):
    clean_content = []
    for line in content:
        line = line.rstrip()
        if line not in ["\n", "", " "]:
            clean_content.append(line)
    return clean_content


exists_already = (build_spec['template'].keys())
excel = strip(content)

excel.sort(key=lambda x: int(x))
for qcode in excel:
    if qcode not in exists_already:
        print(f'"{qcode}": "$CURRENCY_THOUSANDS"')

# for qcode in exists_already:
#     if qcode not in excel:
#         print(f'"{qcode}": "$CURRENCY_THOUSANDS"')
