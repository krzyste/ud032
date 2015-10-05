#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a cleaning idea and then clean it up.

Since in the previous quiz you made a decision on which value to keep for the "areaLand" field,
you now know what has to be done.

Finish the function fix_area(). It will receive a string as an input, and it has to return a float
representing the value of the area or None.
You have to change the function fix_area. You can use extra functions if you like, but changes to process_file
will not be taken into account.
The rest of the code is just an example on how this function can be used.
"""
import codecs
import csv
import json
import pprint
import re

CITIES = 'cities.csv'


def more_significant_number(nums):
    max_no_of_digits = (0, 0)
    for i, num in enumerate(nums):
        match = re.match("^\d+\.(?P<after_dot>.*)e.*", num)
        tmp = len(match.group("after_dot"))
        if tmp > max_no_of_digits[1]:
            max_no_of_digits = (i, tmp)
    return max_no_of_digits[0]


def fix_area(area):
    is_list = re.match("^\{(?P<n1>.*)\|(?P<n2>.*)}", area)
    if is_list:
        numbers = (is_list.group("n1"), is_list.group("n2"))
        n = more_significant_number(numbers)
        area = float(numbers[n])
    elif area == "NULL":
        return None
    else:
        return float(area)

    return area


def process_file(filename):
    # CHANGES TO THIS FUNCTION WILL BE IGNORED WHEN YOU SUBMIT THE EXERCISE
    data = []

    with open(filename, "r") as f:
        reader = csv.DictReader(f)

        #skipping the extra matadata
        for i in range(3):
            l = reader.next()

        # processing file
        for line in reader:
            # calling your function to fix the area value
            if "areaLand" in line:
                line["areaLand"] = fix_area(line["areaLand"])
            data.append(line)

    return data


def test():
    data = process_file(CITIES)

    print "Printing three example results:"
    for n in range(5,8):
        pprint.pprint(data[n]["areaLand"])

    assert data[8]["areaLand"] == 55166700.0
    assert data[3]["areaLand"] == None


if __name__ == "__main__":
    test()