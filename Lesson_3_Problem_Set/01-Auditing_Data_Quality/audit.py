#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a cleaning idea and then clean it up.
In the first exercise we want you to audit the datatypes that can be found in some particular fields in the dataset.
The possible types of values can be:
- 'NoneType' if the value is a string "NULL" or an empty string ""
- 'list', if the value starts with "{"
- 'int', if the value can be cast to int
- 'float', if the value can be cast to float, but is not an int
- 'str', for all other values

The audit_file function should return a dictionary containing fieldnames and the datatypes that can be found in the field.
All the data initially is a string, so you have to do some checks on the values first.

"""
import codecs
import csv
import json
import pprint
import types
import re

CITIES = 'cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label", "isPartOf_label", "areaCode",
          "populationTotal",
          "elevation", "maximumElevation", "minimumElevation", "populationDensity", "wgs84_pos#lat", "wgs84_pos#long",
          "areaLand", "areaMetro", "areaUrban"]


def is_int(x):
    try:
        if int(x) == float(x):
            return True
        else:
            return False
    except (ValueError, TypeError):
        return False


def is_float(x):
    if is_int(x):
        return False
    else:
        try:
            float(x)
            return True
        except (ValueError, TypeError):
            return False


def audit_datatype(data):
    if data in ("NULL", ""):
        return types.NoneType
    elif data.startswith("{"):
        return types.ListType
    elif is_int(data):
        return types.IntType
    elif is_float(data):
        return types.FloatType
    else:
        return types.StringType


def is_line_valid(entry):
    return re.match(".*dbpedia\.org.*", entry["URI"])


def audit_file(filename, fields):
    fieldtypes = {}
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        for line in reader:
            if is_line_valid(line):
                for key in fields:
                    type_ = audit_datatype(line[key])
                    if key in fieldtypes:
                        fieldtypes[key].add(type_)
                    else:
                        fieldtypes[key] = {type_}

    return fieldtypes


def test():
    fieldtypes = audit_file(CITIES, FIELDS)

    pprint.pprint(fieldtypes)

    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])

if __name__ == "__main__":
    test()
