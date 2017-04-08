#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate sample JSON input for scrapers
"""

from __future__ import print_function
import json
import sys


SAMPLE_INPUT = {
    # common restaurant samples:
    "chipotle": {
        "business_name": "Chipotle",
        "address": {
            "house_number": "723",
            "city": "Santa Barbara",
            "state": "California",
            "street": "State Street",
            "zip": "93101"
        },
        "cookiejars": {
            "foursquare-web": {
                "_default": [
                    {
                        "domain": ".foursquare.com",
                        "expires": "2018-12-02T14:25:45Z",
                        "name": "bbhive",
                        "path": "/",
                        "secure": False,
                        "value": "BWCR3JK55GQ5GLAR5OANVY2VMYGP5G%3A%3A1543760745"
                    }
                ]
            },
            "debug-cookies": {
                "_default": [
                    {
                        "domain": ".httpbin.org",
                        "name": "debugcookie",
                        "path": "/",
                        "secure": False,
                        "value": "cool, it works!"
                    }
                ]
            }
        },
        "profile_keys": {
            "googlemaps-web": "https://www.google.com/maps/place/Chipotle%20Mexican%20Grill/@34.419013,-119.69909,15z/data=!4m5!3m4!1s0x80e91478f0be39eb:0x9bd3e5b381d32936!8m2!3d34.419013!4d-119.69909",  # NOQA
        },
    },
    "cincodemayo": {
        "address": {
            "city": "Brooklyn",
            "state": "NY",
            "house_number": "1202",
            "street": "Cortelyou Rd",
            "zip": "11218"
        },
        "business_name": "Cinco de Mayo",
        "profile_keys": {
            "facebook-web": "https://www.facebook.com/pages/Cinco-De-Mayo/170258606321749",
            "foursquare-web": "https://foursquare.com/v/cinco-de-mayo/4ad123f7f964a52003dd20e3",
            "foursquare-api": "https://foursquare.com/v/cinco-de-mayo/4ad123f7f964a52003dd20e3",
            "citysearch-web": "http://www.citysearch.com/profile/7361639/brooklyn_ny/cinco_de_mayo.html",  # NOQA
            "tripadvisor-web": "https://www.tripadvisor.com/Restaurant_Review-g33045-d852971-Reviews-Mayo_s-Santa_Barbara_California.html",  # NOQA
            "yellowpages-web": "http://www.yellowpages.com/brooklyn-ny/mip/cinco-de-mayo-taqueria-22343914",  # NOQA
            "yelp-web": "https://www.yelp.com/biz/cinco-de-mayo-restaurant-brooklyn",
            "googlemaps-web": "0x89c25b3169944b6f:0x5392cfc2c56acfa|61",
            "googlemaps-api": "ChIJb0uUaTFbwokR-qxWLPwsOQU",

            # had to grab this one manually, because the site's first result
            # for query "Brooklyn, NY" is Brooklyn Connecticut
            "zomato-web": "https://www.zomato.com/new-york-city/cinco-de-mayo-restaurant-kensington-borough-park",  # NOQA
        },
    },
    "voodoo": {
        "address": {
            "city": "Portland",
            "state": "Oregon",
            "house_number": "22",
            "street": "SW 3rd Ave",
            "zip": "97204"
        },
        "business_name": "Voodoo Doughnut",
        "last_review_hashes": [
            'f144b6a8b601344214771ba0821a4777',  # tripadvisor
            '098d4d6d771fb9c85a2dd146d03fc65e',  # googlemaps
        ],
    },
    "dunkin": {
        "address": {
            "city": "Portland",
            "state": "CT",
            "house_number": "860",
            "street": "Unit #1 Corner Shops, Portland-Cobalt Rd",
            "zip": "06480"
        },
        "business_name": "Dunkin' Donuts",
    },
    "baja": {
        "address": {
            "city": "Santa Barbara",
            "state": "California",
            "house_number": "525",
            "street": "State Street",
            "zip": "93101"
        },
        "business_name": "Baja Sharkeez",
    },
    "chipotle-wrong": {
        "address": {
            "city": "Santa Barbara",
            "state": "California",
            "house_number": "525",
            "street": "State Street",   # sample with wrong address
            "zip": "93101"
        },
        "business_name": "Chipotle",
    },
    "daveandbuster": {
        "address": {
            "city": "New York",
            "state": "New York",
            "house_number": "234",
            "street": "W 42nd St",
            "zip": "10036"
        },
        "business_name": "Dave and Buster's",
    },
    "hyatt": {
        "business_name": "Hyatt Centric Santa Barbara",
        "address": {
            "city": "Santa Barbara",
            "state": "California",
            "house_number": "1111",
            "street": "East Cabrillo Boulevard",
            "zip": "93103-3701"
        },
        "last_review_hashes": [
            "12cf72c17a77899fef643937ae22b2db",  # tripadvisor
        ],
    },

    # doctor profiles
    "drbrett": {
        "business_name": "Dr. Brett S. Sanders",
        "address": {
            "city": "Chattanooga",
            "state": "TN",
            "house_number": "2415",
            "street": "McCallie Ave",
            "zip": "37404"
        },
        "id": "1icws351329oqk4jzl80"
    },
    "drbrett2": {
        "business_name": "Dr. Brett A. Gidney",
        "address": {
            "city": "Santa Barbara",
            "state": "California",
            "house_number": "504",
            "street": "W Pueblo St",
            "zip": "93101"
        },
        "profile_keys": {
            "healthgrades-web": "https://www.healthgrades.com/physician/dr-brett-gidney-294jp"
        },
        "id": "asu21s5nu0l2izh9u4qq"
    },
    "drjesse": {
        "business_name": "Dr. Jesse F. Doty",
        "address": {
            "house_number": "1075",
            "street": "N CURTIS ROAD",
            "city": "Chattanooga",
            "state": "TN",
            "zip": "37403",
        }
    },
    "drteresa": {
        "business_name": "Dr. Teresa Regan, DO",
        "address": {
            "city": "Signal Mountain",
            "state": "TN",
            "house_number": "2600",
            "street": "Taft Highway",
            "zip": "37377"
        },
    },

    "extended": {
        "business_name": "Extended Stay America - Pittsburgh - Carnegie",
        "address": {
            "house_number": "520",
            "street": "North Bell Avenue",
            "city": "Carnegie",
            "state": "PA",
            "zip": "15106"
        },
    },

    # sample for avvo and lawyers.com
    "merenbach": {
        "business_name": "Dennis Gene Merenbach",
        "address": {
            "house_number": "225",
            "street": "E. Carrillo St.",
            "city": "Santa Barbara",
            "state": "CA",
            "zip": "93101",
        },
    },

    # sample for opentable
    'finchfork': {
        "business_name": "Finch & Fork: Corner Grill Cocktails",
        "address": {
            "house_number": "31",
            "street": "West Carrillo Street",
            "city": "Santa Barbara",
            "state": "CA",
            "zip": "93101",
        },
    },

    #
    "nimmons": {
        "business_name": "Kevin R. Nimmons",
        "address": {
            "house_number": "1126",
            "street": "Santa Barbara Street",
            "city": "Santa Barbara",
            "state": "CA",
            "zip": "93102",
        }
    },

    # samples for homeadvisor
    "chavez": {
        "business_name": "Chavez Remodeling",
        "address": {
            "house_number": "14927",
            "street": "Ridgeway Avenue",
            "city": "Midlothian",
            "state": "Illinois",
            "zip": "60445",
        }
    },
    "sweatequity": {
        "business_name": "Sweat Equity Remodeling",
        "address": {
            "house_number": "700",
            "street": "East Northwest Highway",
            "city": "Arlington Heights",
            "state": "IL",
            "zip": "60004",
        }
    },

    # car dealer, for edmunds
    "perryford": {
        "business_name": "Perry Ford",
        "address": {
            "house_number": "440",
            "street": "Hitchcock Way",
            "city": "Santa Barbara",
            "state": "CA",
            "zip": "93105",
        }
    },

    # examples for angieslist
    "skyline": {
        "business_name": "Skyline Home Remodeling Ventura",
        "address": {
            "house_number": "1560",
            "street": "Eastman Avenue",
            "city": "Ventura",
            "state": "CA",
            "zip": "93003",
        },
        "persona": {
            "credentials": {
                "username": "k1613390@mvrht.com",
                "password": "botemo",
            }
        },
        # profile_key: https://member.angieslist.com/member/store/15000461
    },
    "rotorooter": {
        "business_name": "Roto-Rooter Plumbing & Drain Services",
        "address": {
            "house_number": "5180",
            "street": "Smith Road Ste F",
            "city": "Denver",
            "state": "CO",
            "zip": "80216",
        },
        "persona": {
            "credentials": {
                "username": "k1598615@mvrht.com",
                "password": "qwert1234",
            }
        },
    },
    "cunningham": {
        "business_name": "Cunningham Associates",
        "address": {
            "street": "3114 Marjan Drive",
            "city": "Atlanta",
            "state": "GA",
            "zip": "30340",
        }
    },
    "californiapizzakitchen":{
	    "business_name": "California Pizza Kitchen",
	    "address": {
            "street": "136 Boardwalk Place",
            "city": "Gaithersburg",
            "state": "MD",
            "zip": "20878",
        }
    },
    "cpksb":{
	    "business_name": "California Pizza Kitchen",
	    "address": {
            "street": "719 Paseo Nuevo",
            "city": "Santa Barbara",
            "state": "CA",
            "zip": "93101",
        }
    },
    "unitedchimney":{
	    "business_name": "United Chimney Corporation",
	    "address": {
		    "street": "487 Furrows Road",
		    "city": "Holbrook",
		    "state": "NY",
		    "zip": "11741"
	    }
    },
    "cpknatick":{
	    "business_name": "California Pizza Kitchen",
	    "address": {
		    "street": "1245 Worcester Road #1092",
		    "city": "Natick",
		    "state": "MA",
		    "zip": "01760"
	    }
    },
    "cpkfarmington":{
	    "business_name": "California Pizza Kitchen",
	    "address": {
		    "street": "3 Westfarms Mall, Sp. E-125",
		    "city": "Farmington",
		    "state": "CT",
		    "zip": "06032"
	    }
    },
    "cpkhills":{
	    "business_name": "California Pizza Kitchen",
	    "address": {
		    "street": "1200 Morris Turnpike, Unit B270",
		    "city": "Short Hills",
		    "state": "NJ",
		    "zip": "07078"
	    }
    },
    "cpknj":{
	    "business_name": "California Pizza Kitchen",
	    "address": {
		    "street": "2000 Route 38, Unit #1025",
		    "city": "Cherry Hill",
		    "state": "NJ",
		    "zip": "08002"
	    }
    },
    "cpkglendale":{
	    "business_name": "California Pizza Kitchen",
	    "address": {
		    "street": "71-03 80th Street, Suite 7101",
		    "city": "Glendale",
		    "state": "NY",
		    "zip": "11385"
	    }
    },
    "hiltonsd":{
	    "business_name": "Hilton",
	    "address": {
		    "street": "1 Park Blvd.",
		    "city": "San Diego",
		    "state": "CA",
		    "zip": "92101"
	    },
	    "profile_keys": {
            "googlemaps-web": "https://www.google.com/maps/place/Hilton%20San%20Diego%20Bayfront/@32.703245,-117.15861,15z/data=!4m5!3m4!1s0x80d95345315f460b:0xd669cb6fe6a09fd7!8m2!3d32.703245!4d-117.15861"
        },
        "persona":{
	    	"UserAgent":"Scrapy/1.2.2 (+http://scrapy.org)"  
        },
	    "last_review_hashes": [
            '22e82ef1143a56aece3ad32ace6cb1b2',  # googlemaps
            '22e82ef1143a56aece3ad32ace6cb1b2',  # googlemaps
        ]
    },
    "nordstromsf":{
	    "business_name": "Nordstrom",
	    "address": {
		    "street": "865 Market St",
		    "city": "San Francisco",
		    "state": "CA",
		    "zip": "94103"
	    },
	    "profile_keys": {
            "googlemaps-web": "https://www.google.com/maps/place/Nordstrom%20San%20Francisco%20Centre/@37.784196,-122.407446,15z/data=!4m5!3m4!1s0x80858085e669cca1:0xd929252f6c42706e!8m2!3d37.784196!4d-122.407446"
        },
        "persona":{
	    	"UserAgent":"Scrapy/1.2.2 (+http://scrapy.org)"  
        },
	    "last_review_hashes": [
            'aec0b4803213488e8297559bc774b804',  # googlemaps
            'eff6903b969f95c9625f973dbf8e5c7d',  # googlemaps
        ]
    },
    "hiltonus":{
	    "business_name": "Hilton",
	    "address": {
		    "street": "333 O'Farrell Street",
		    "city": "San Francisco",
		    "state": "CA",
		    "zip": "94102"
	    },
	    "profile_keys": {
            "yelp-web": "https://www.yelp.com/biz/hilton-san-francisco-union-square-san-francisco-5"
        },
	    "last_review_hashes": []
    },
    "gplaytest":{
	    "business_name": "Hilton",
	    "address": {
		    "street": "333 O'Farrell Street",
		    "city": "San Francisco",
		    "state": "CA",
		    "zip": "94102"
	    },
	    "profile_keys": {
		    "gplay": "com.trello"
	    },
	    "last_review_hashes": []
    },
    "gplay":{
	    "business_name": "Hilton",
	    "address": {
		    "street": "333 O'Farrell Street",
		    "city": "San Francisco",
		    "state": "CA",
		    "zip": "94102"
	    },
	    "profile_keys": {},
	    "last_review_hashes": []
    }
}


# all regions:
# CRAWLERA_PROXY = '01e01df5dd224906a2e2f9ed7f152cb6:@proxy.crawlera.com:8010'

# US-only:
CRAWLERA_PROXY = '65c0f90ccf854cb5874088f30da2d82c:@proxy.crawlera.com:8010'

PROXY_CHOICES = {
    'none': None,
    'local': 'http://localhost:8080',
    'crawlera': CRAWLERA_PROXY,
}


def error(mesg):
    print(mesg, file=sys.stderr)


def gen_sample(sample_name, spider, proxy):
    sample = dict(SAMPLE_INPUT[sample_name])

    profile_key = sample.pop('profile_keys', {}).get(spider)
    if profile_key:
        sample['profile_key'] = profile_key

    cookiejars = sample.get('cookiejars', {}).get(spider)
    if cookiejars:
        sample.setdefault('persona', {})['cookies'] = cookiejars

    proxy = PROXY_CHOICES[proxy]
    if proxy:
        sample.setdefault('persona', {})['proxy'] = proxy

    sample.setdefault('last_review_hashes', [])

    sample.pop('cookiejars', None)
    return json.dumps(sample)


def run(args):
    sample_names = SAMPLE_INPUT.keys() if args.sample_names == ['ALL'] else args.sample_names
    for name in sample_names:
        print(gen_sample(name, args.spider, args.proxy))


if '__main__' == __name__:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sample_names', nargs='+',
                        default=('chipotle',), choices=SAMPLE_INPUT.keys() + ['ALL'])
    parser.add_argument('--spider')
    parser.add_argument('--proxy', choices=PROXY_CHOICES, default='none')

    args = parser.parse_args()
    run(args)
