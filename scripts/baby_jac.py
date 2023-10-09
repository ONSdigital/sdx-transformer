import re

import yaml

from app.definitions import BuildSpec


build_spec_path = "../build_specs/pck/abs.yaml"
with open(build_spec_path) as y:
    build_spec: BuildSpec = yaml.safe_load(y.read())


def strip(content: list):
    """
    Clean our list of lines, remove
    new lines and blank spaces etc
    """
    clean_content = []
    for line in content:
        line = line.rstrip()
        if line not in ["\n", "", " "]:
            clean_content.append(remove_spaces_and_special_chars(line))
    return clean_content


def remove_spaces_and_special_chars(s: str) -> str:
    """Remove all spaces and special characters from a string."""
    return re.sub(r'[^a-zA-Z0-9]', '', s)


def print_new_qcodes():
    """
    Print all the new qcodes found
    in the content.txt file, compared with
    the template in the abs build spec
    """

    content = open("content.txt", "r").readlines()
    exists_already = (build_spec['template'].keys())
    excel = strip(content)

    # Print all the qcodes in the spreadsheet which are NOT in the build spec
    excel.sort(key=lambda x: int(x))
    for qcode in excel:
        if qcode not in exists_already:
            print(f'"{qcode}": "$CURRENCY_THOUSANDS"')


def convert_str_to_list(content: str, seperator="+") -> list[str]:
    """
    Convert a string from an excel spreadsheet to
    a list of values
    """
    split = content.split(seperator)
    return [remove_spaces_and_special_chars(s) for s in split]


def compare_values(transform_name: str, new_values: list[str]):
    """
    Compare the list of values in an existing transform with
    some potential new values, to quickly identify new ones

    e.g
        "499_TOTAL_LONG_FORM":
        "name": "TOTAL"
        "args":
            "value": "0"
            "values": [ "&402", "&405",  "&406", "&407", "&408", "&409", "&410", "&411", "&421", "&427", "&428", "&433"]

    and we want to add: ["402", "405", "555"]

     the function will find the new qcodes to add (555)
    """

    values = build_spec['transforms'][transform_name]['args']['values']

    # Remove the symbol from the front
    clean_values = [val[1:] for val in values]

    new_codes = []

    for qcode in new_values:
        if qcode not in clean_values:
            new_codes.append(qcode)

    # If new qcodes are found, create a new values array and print
    if len(new_codes) > 0:
        print("New values found: ",new_codes)
        mega_list = clean_values + new_codes
        print([f"&{v}" for v in mega_list])
    else:
        print("No new values found")


while True:
    print("\n\nOptions:")
    print("1: Generate and print new QCodes found in content.txt")
    print("2: Compare string input with values for a particular transform")
    print("q: Quit the program")
    choice = input("Choose an option (1 or 2), or 'q' to quit: ")

    if choice == 'q':
        break

    if choice == '1':
        print_new_qcodes()
    elif choice == '2':
        user_input1 = input("Enter the name of the transform: ")
        user_input2 = input("Enter the values from the spreadsheet (seperated by '+'): ")
        list2 = convert_str_to_list(user_input2)
        compare_values(user_input1, list2)
    else:
        print("Invalid choice. Please enter 1, 2, or 'q'.")



