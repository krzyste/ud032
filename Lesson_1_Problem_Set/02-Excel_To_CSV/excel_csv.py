# -*- coding: utf-8 -*-
# Find the time and value of max load for each of the regions
# COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
# and write the result out in a csv file, using pipe character | as the delimiter.
# An example output can be seen in the "example.csv" file.
import xlrd
import os
import csv
from zipfile import ZipFile
datafile = "2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = [["Station", "Year", "Month", "Day", "Hour", "Max Load"]]
    sheetDataInColumns = [[sheet.cell_value(r, col) for r in range(sheet.nrows)] for col in range(sheet.ncols)]
    
    for i in range(1, 9):
        _name = sheetDataInColumns[i][0]
        _maxValue = max(sheetDataInColumns[i][1:])
        _maxTime = xlrd.xldate_as_tuple(sheetDataInColumns[0][sheetDataInColumns[i].index(_maxValue)], 0)
        data.append([_name] + list(_maxTime)[:4] + [_maxValue])
    return data


def save_file(data, filename):
    with open(filename, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='|')
        for row in data:
            spamwriter.writerow(row)
       
        
def test():
    # open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    ans = {'FAR_WEST': {'Max Load': "2281.2722140000024", 'Year': "2013", "Month": "6", "Day": "26", "Hour": "17"}}
    
    fields = ["Year", "Month", "Day", "Hour", "Max Load"]
    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            s = line["Station"]
            if s == 'FAR_WEST':
                for field in fields:
                    assert ans[s][field] == line[field]

        
test()
