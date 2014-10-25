# Your task is to read the input DATAFILE line by line, and for the first 10 lines (not including the header)
# split each line on "," and then for each line, create a dictionary
# where the key is the header title of the field, and the value is the value of that field in the row.
# The function parse_file should return a list of dictionaries,
# each data line in the file being a single list entry.
# Field names and values should not contain extra whitespace, like spaces or newline characters.
# You can use the Python string method strip() to remove the extra whitespace.
# You have to parse only the first 10 data lines in this exercise,
# so the returned list should have 10 entries!
import os
import csv

DATADIR = os.getcwd()
DATAFILE = "beatles-diskography.csv"

def parse_csv(datafile):
    data = []
    with open(datafile, "r") as f:
        f_csv = csv.DictReader(f)
        for line in f_csv:
            data.append(line)
    return data

def parse_file(datafile):
    data = []
    columnNames = []
    with open(datafile, "r") as f:
        lines = f.readlines()
        columnNames = lines[0].strip().split(",")
        for line in lines[1:11]:
            line = line.rstrip().split(",")
            tmpDict = dict(zip(columnNames,line))
            data.append(tmpDict)
    return data


def test():
    # a simple test of your implemetation
    datafile = os.path.join(DATADIR, DATAFILE)
    d = parse_file(datafile)
    d1 = parse_csv(datafile)
    firstline = {'Title': 'Please Please Me', 'UK Chart Position': '1', 'Label': 'Parlophone(UK)', 'Released': '22 March 1963', 'US Chart Position': '-', 'RIAA Certification': 'Platinum', 'BPI Certification': 'Gold'}
    tenthline = {'Title': '', 'UK Chart Position': '1', 'Label': 'Parlophone(UK)', 'Released': '10 July 1964', 'US Chart Position': '-', 'RIAA Certification': '', 'BPI Certification': 'Gold'}

    assert d[0] == firstline
    assert d[9] == tenthline
    assert d1[0] == firstline
    assert d1[9] == tenthline

    
test()