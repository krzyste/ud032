__author__ = 'plkstelmac'
import csv
import re
from pymongo import MongoClient
import pprint

FIELDS = {"elevation": "elevation",
          "rdf-schema#label": "name",
          "country_label": "country",
          "wgs84_pos#long": "lon",
          "wgs84_pos#lat": "lat",
          "isPartOf_label": "isPartOf",
          "timeZone_label": "timeZone",
          "populationTotal": "population"}


def make_list(v):
    if (v[0] == "{") and (v[-1] == "}"):
        v = v.lstrip("{")
        v = v.rstrip("}")
        v_array = v.split("|")
        v_array = [i.strip() for i in v_array]
        return v_array
    return [v]


def more_significant_float(lst):
    max_no_of_digits = (0, 0)
    for i, num in enumerate(lst):
        match = re.match(".*\.(?P<after_dot>.*)", num)
        if match:
            sig_len = len(match.group("after_dot"))
            if sig_len > max_no_of_digits[1]:
                max_no_of_digits = (num, sig_len)
        else:
            max_no_of_digits = (num[0], 0)
    return max_no_of_digits[0]


def update_line(dic):
    ret_dic = {}
    for key in dic.keys():
        if key in FIELDS:
            ret_dic.update({FIELDS[key]: dic[key]})
    return ret_dic


def fix_number(line_, key):
    if line_[key] in ("NULL", ""):
        line_[key] = None
    elif line_[key].startswith("{"):
        _lst = make_list(line_[key])
        line_[key] = float(more_significant_float(_lst))
    else:
        line_[key] = float(line_[key])
    return line_


def fix_name(line_):
    match = re.match("^(?P<name>.*) \(.*\)", line_["name"])
    if match:
        line_["name"] = match.group("name")
    elif line_["name"] in ("", "NULL"):
        line_["name"] = None
    return line_


def fix_country(line_):
    if line_["country"] in ("", "NULL"):
        line_["country"] = None
    elif line_["country"].startswith("{"):
        line_["country"] = make_list(line_["country"])[0]
    return line_


def put_in_list(line_, key):
    if line_[key] in ("", "NULL"):
        line_[key] = []
    else:
        line_[key] = make_list(line_[key])
    return line_


def process_file(filename):
    data = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for i in range(3):
            reader.next()
        for line in reader:
            line = update_line(line)
            line = fix_number(line, "elevation")
            line = fix_name(line)
            line = fix_country(line)
            line = fix_number(line, "lon")
            line = fix_number(line, "lat")
            line = put_in_list(line, "isPartOf")
            line = put_in_list(line, "timeZone")
            line = fix_number(line, "population")
            data.append(line)

    return data


def insert_to_db(data):
    client = MongoClient("mongodb://localhost:27017")
    db = client.examples
    db.cities.drop()
    db.cities.insert(data)
    pprint.pprint(db.cities.find_one())

if __name__ == "__main__":
    INPUT_FILE = "/tmp/cities.csv"

    cities_data = process_file(INPUT_FILE)
    insert_to_db(cities_data)

