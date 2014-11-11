# To experiment with this code freely you will have to run this code locally.
# We have provided an example json output here for you to look at,
# but you will not be able to run any queries through our UI.

import json
import requests


BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"

query_type = {  "simple": {},
                "atr": {"inc": "aliases+tags+ratings"},
                "aliases": {"inc": "aliases"},
                "releases": {"inc": "releases"}}


def query_site(url, params, uid="", fmt="json"):
    params["fmt"] = fmt
    r = requests.get(url + uid, params=params)
    print "requesting", r.url

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()
        

def query_by_name(url, params, name):
    params["query"] = "artist:" + name
    return query_site(url, params)


def pretty_print(data, indent=4):
    if type(data) == dict:
        print json.dumps(data, indent=indent, sort_keys=True)
    else:
        print data
        
        
def CountNumberOfArtists(name):
    results = query_by_name(ARTIST_URL, query_type["simple"], name)
    n = 0    
    for artist in results["artists"]:
        if artist["name"].lower() == name.lower():
            n += 1
    return n 


def GetBeginAreaOfArtist(name):
    results = query_by_name(ARTIST_URL, query_type["simple"], name)    
    for artist in results["artists"]:
        if "begin-area" in artist and artist["name"].lower() == name.lower():
            return artist["begin-area"]["name"]


def GetArtistAlias(name, locale):    
    results = query_by_name(ARTIST_URL, query_type["simple"], name) 
    for artist in results["artists"]:
        if artist["name"].lower() == name.lower():
            if "aliases" in artist:
                for alias in artist["aliases"]:
                    if alias["locale"] == locale:
                        return alias["name"]
                  
                    
def GetArtistDisambiguation(name):
    results = query_by_name(ARTIST_URL, query_type["simple"], name) 
    for artist in results["artists"]:
        if "disambiguation" in artist and artist["name"].lower() == name.lower():
            return artist["disambiguation"]
        
        
def GetArtistBeginYear(name):
    results = query_by_name(ARTIST_URL, query_type["simple"], name) 
    for artist in results["artists"]:
        if "life-span" in artist and artist["name"].lower() == name.lower():
            return artist["life-span"]["begin"]


def main():
    artist = "First Aid Kit"
    out = CountNumberOfArtists(artist)
    print "Number of bands named", artist, ":", out, "\n"
    
    artist = "Queen"
    out = GetBeginAreaOfArtist(artist)
    print "Begin area of", artist, ":", out, "\n"
    
    artist = "The Beatles"
    locale = "es"
    out = GetArtistAlias(artist, locale)
    print "Spanish alias of", artist, ":", out, "\n"

    artist = "Nirvana"
    out = GetArtistDisambiguation(artist)
    print "Disambiguation of", artist, ":", out, "\n"

    artist = "One Direction"
    out = GetArtistBeginYear(artist)
    print "Creation year of", artist, ":", out, "\n"
    

if __name__ == '__main__':
    main()
