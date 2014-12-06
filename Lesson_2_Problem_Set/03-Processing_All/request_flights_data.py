#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import os

datadir = "data"
HTML_ADDRESS = "http://www.transtats.bts.gov/Data_Elements.aspx?Data=2"

def extract_airports(soup):
    data = []
    _airports = soup.find(id="AirportList")
    for _option in  _airports.find_all("option"):
        _value = _option["value"]
        if not _value.startswith("All"):
            data.append(_value)
    return data

def extract_carriers(soup):
    data = []
    _carriers = soup.find(id="CarrierList")
    for _option in  _carriers.find_all("option"):
        _value = _option["value"]
        if not _value.startswith("All"):
            data.append(_value)
    return data

def extract_validation_data(soup):
    data = {"eventvalidation": "",
            "viewstate": ""}

    _eventValid = soup.find(id="__EVENTVALIDATION")
    data["eventvalidation"]=_eventValid["value"]
    _viewState = soup.find(id="__VIEWSTATE")
    data["viewstate"]=_viewState["value"]      

    return data

def get_request_data():
    s = requests.Session()
    r = s.get(HTML_ADDRESS)
    soup = BeautifulSoup(r.text)
    validation_data = extract_validation_data(soup)
    carriers = extract_carriers(soup)
    airports = extract_airports(soup)
    
    return (s, validation_data, carriers, airports)

def get_page(session, validation_data, _carrier, _airport):
         
    r = session.post(HTML_ADDRESS,
                data={'AirportList': _airport,
                      'CarrierList': _carrier,
                      'Submit': 'Submit',
                      "__EVENTTARGET": "",
                      "__EVENTARGUMENT": "",
                      "__EVENTVALIDATION": validation_data["eventvalidation"],
                      "__VIEWSTATE": validation_data["viewstate"]
                })
    return r

if __name__ == "__main__":
    session ,validation_data, carriers, airports = get_request_data()
    
    for _carrier in carriers:
        for _airport in airports:
            print _carrier, _airport
            _page = get_page(session, validation_data, _carrier, _airport)
            with open("{}/{}-{}.html".format(datadir, _carrier,_airport), "w") as f:
                f.write(_page.text)
