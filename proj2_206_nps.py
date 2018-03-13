## proj_nps.py
## Skeleton for Project 2, Winter 2018
## ~~~ modify this file, but don't rename it ~~~
import json
import requests
from bs4 import BeautifulSoup

# for using class you wanna create an instance in the function and then add it
# to the dictionary of sites n shit while still in the function can prolly get
# rid of the lists n shit and just add it to the dictionaries

state_sites = {}
near_sites = {}
site_tweets = {}

CACHE_SITE = 'cache_site.json'
CACHE_NEARBY = 'cache_nearby.json'
CACHE_TWEET = 'cache_tweet.json'

# for National Sites
baseurl = 'https://www.nps.gov/index.htm'
basic_url = 'https://www.nps.gov'

try:
    fref = open(CACHE_SITE, 'r')
    data = fref.read()
    CACHE_DICT_SITE = json.loads(data)
    fref.close()
except:
    CACHE_DICT_SITE = {}

try:
    fref = open(CACHE_NEARBY, 'r')
    data = fref.read()
    CACHE_DICT_NEARBY = json.loads(data)
    fref.close()
except:
    CACHE_DICT_NEARBY = {}

try:
    fref = open(CACHE_TWEET, 'r')
    data = fref.read()
    CACHE_DICT_TWEET = json.loads(data)
    fref.close()
except:
    CACHE_DICT_TWEET = {}

## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)
class NationalSite:
    def __init__(self, type__='None', name='None', desc='None', street='None',
                 city='None', state='None', zip_='None', url='None'):
        self.type_ = type__
        self.name = name
        self.description = desc
        self.url = url

        self.address_street = street
        self.address_city = city
        self.address_state = state
        self.address_zip = zip_


    # add in thing about if no address then simply put None instead of repeating
    # it like 6 times

    def __str__(self):
        if self.address_zip is None:
            # '{} ({}): No address is available'.format(self.name, self.type_)
            #return self.name + " (" + self.type_ + "): No address is available"
            return '{} ({}): No address is available'.format(self.name, self.type_)
        else:
            # '{} ({}): {}, {}, {} {}'.format(self.name, self.type_, self.address_street, self.address_city, self.address_state, self.address_zip)
            # string = str(self.name) + " (" + str(self.type_) + "): " + str(self.address_street) + ", " + str(self.address_city) + ", " + str(self.address_state) + " " + str(self.address_zip)
            #return string
            return '{} ({}): {}, {}, {} {}'.format(self.name, self.type_, self.address_street, self.address_city, self.address_state, self.address_zip)

    # look at above note
    # please don't be a retard

## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)
class NearbyPlace():
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)
class Tweet:
    def __init__(self, tweet_dict_from_json):
        self.text = ''
        self.username = ''
        self.creation_date = ''
        self.num_retweets = 0
        self.num_favorites = 0
        self.popularity_score = self.num_favorites * 3
        self.popularity_score += self.num_retweets * 2
        self.id = ''
        self.is_retweet = True

    def __str__(self):
        string = "@" + self.username + ": " + self.text + "\n" + "[retweeted " \
                 + self.num_retweets + " times] \n" + \
                 "[favorited " + self.num_favorites + " times] \n" + \
                 "[popularity " + self.popularity_score + "] \n" + \
                 "[tweeted on " + self.creation_date + "] | [id: " + self.id \
                 + "] \n"

        return string

def convert_abbreviation(state_abbr):
    state_abbr_dict = {
        'ak': 'Alaska',
        'al': 'Alabama',
        'ar': 'Arkansas',
        'as': 'American Samoa',
        'az': 'Arizona',
        'ca': 'California',
        'co': 'Colorado',
        'ct': 'Connecticut',
        'dc': 'District of Columbia',
        'de': 'Delaware',
        'fl': 'Florida',
        'ga': 'Georgia',
        'gu': 'Guam',
        'hi': 'Hawaii',
        'ia': 'Iowa',
        'id': 'Idaho',
        'il': 'Illinois',
        'in': 'Indiana',
        'ks': 'Kansas',
        'ky': 'Kentucky',
        'la': 'Louisiana',
        'ma': 'Massachusetts',
        'md': 'Maryland',
        'me': 'Maine',
        'mi': 'Michigan',
        'mn': 'Minnesota',
        'mo': 'Missouri',
        'mp': 'Northern Mariana Islands',
        'ms': 'Mississippi',
        'mt': 'Montana',
        'na': 'National',
        'nc': 'North Carolina',
        'nd': 'North Dakota',
        'ne': 'Nebraska',
        'nh': 'New Hampshire',
        'nj': 'New Jersey',
        'nm': 'New Mexico',
        'nv': 'Nevada',
        'ny': 'New York',
        'oh': 'Ohio',
        'ok': 'Oklahoma',
        'or': 'Oregon',
        'pa': 'Pennsylvania',
        'pr': 'Puerto Rico',
        'ri': 'Rhode Island',
        'sc': 'South Carolina',
        'sd': 'South Dakota',
        'tn': 'Tennessee',
        'tx': 'Texas',
        'ut': 'Utah',
        'va': 'Virginia',
        'vi': 'Virgin Islands',
        'vt': 'Vermont',
        'wa': 'Washington',
        'wi': 'Wisconsin',
        'wv': 'West Virginia',
        'wy': 'Wyoming'
    }
    full_name = state_abbr_dict[state_abbr]
    return full_name

def scrape_some_shit():

    # totes not done but it will be for now prolly bc practice

    site = NationalSite()

    names = []
    types = []
    descriptions = []
    streets = []
    cities = []
    states = []
    states_zwei = []
    _zips_ = []
    urls = []
    individual_sites = []

    page_html = requests.get(baseurl).text
    page_soup = BeautifulSoup(page_html, 'html.parser')
    menu_links = []

    # PROBLEM: dropdown_menu is not a list so I can't iterate through it
    # FUCK ME DFJASDKL;FJKA;SDLFJKL;'ASDJF

    #dropdown_menu = page_soup.find_all(class_='dropdown-menu SearchBar-'
                                              #'keywordSearch')
    dropdown_menu = page_soup.find(class_='col-sm-12 col-md-10 col-md-push-1')
    dropdown_menu = dropdown_menu.find_all('li')
    # get paragraphs n shit by accessing a different part of the page
    # print(dropdown_menu)

    for a in dropdown_menu:
        link = a.find('a')['href']
        # print(link)
        menu_links.append(link)

    for b in menu_links:
        new_url = basic_url + str(b)
        # print(new_url)
        second_page_html = requests.get(new_url).text
        second_page_soup = BeautifulSoup(second_page_html, 'html.parser')
        paragraphs_stuff = second_page_soup.find_all(class_='col-md-9 col-sm-9 '
                                                            'col-xs-12 table-'
                                                            'cell list_left')
        # print(paragraphs_stuff)
        state = second_page_soup.find(class_='page-title').text
        states_zwei.append(state)
        # print(state)

        # find link for site specific stuff under here
        # i.e. go to page for Birmingham Civil Rights Monument
        # to get address n shit

        for c in range(len(paragraphs_stuff)):
            # LOLOLOLOLOL STUFF IS DEFINITELY FUCKED UP HERE
            names_stuff = paragraphs_stuff[c].find('h3')
            types_stuff = paragraphs_stuff[c].find('h2')
            name = names_stuff.text
            # print(name)
            names.append(name)
            type = types_stuff.text
            # print(type)
            types.append(type)
            paragraph = paragraphs_stuff[c].find('p').text
            descriptions.append(paragraph)
            next_url_stuff = paragraphs_stuff[c].find('h3')
            next_url = next_url_stuff.find('a')['href']
            site_url = basic_url + str(next_url)
            third_page_html = requests.get(site_url).text
            third_page_soup = BeautifulSoup(third_page_html, 'html.parser')
            street = third_page_soup.find(itemprop='streetAddress',
                                          class_='street-address')

            # print(names_stuff.text)
            # print(types_stuff.text)

            if street is not None:
                street = street.text
            else:
                street = 'None'
            city = third_page_soup.find(itemprop='addressLocality')
            if city is not None:
                city = city.text
            else:
                city = 'None'
            state_ = third_page_soup.find(itemprop='addressRegion',
                                          class_='region')
            if state_ is not None:
                state_ = state_.text
            else:
                state_ = 'None'
            zip_ = third_page_soup.find(itemprop='postalCode',
                                        class_='postal-code')
            if zip_ is not None:
                zip_ = zip_.text
            else:
                zip_ = 'None'
            streets.append(street)
            cities.append(city)
            states.append(state_)
            _zips_.append(zip_)
            urls.append(site_url)

        # might need to go in a loop that iterates through the drop down menu
        # so that we get info for each state

        # could also do it where the state is a param of the function as a whole
        # and then you only scrape for that state if it is not in the cache
        # (prolly the best way to do this so you don't scrape all of it each time
        # you go to scrape)

        for penis in range(len(states_zwei)):

            for s in range(len(names)):
                site.name = names[s]
                site.description = descriptions[s]
                site.type_ = types[s]
                site.address_street = streets[s]
                site.address_city = cities[s]
                site.address_state = states[s]
                site.address_zip = _zips_[s]
                site.url = urls[s]
                print(site)
                individual_sites.append(site)

            # this should take care of adding the sites to the dictionary containing
            # states and respective sites

            state_zwei = states_zwei[penis]
            CACHE_DICT_SITE[state_zwei] = individual_sites

    # print(state_zwei)

    # print(CACHE_DICT_SITE['Wyoming'])
    # print(CACHE_DICT_SITE)

        # do shit with the cache here lol

    return CACHE_DICT_SITE



## Must return the list of NationalSites for the specified state
## param: the 2-letter state abbreviation, lowercase
##        (OK to make it work for uppercase too)
## returns: all of the NationalSites
##        (e.g., National Parks, National Heritage Sites, etc.) that are listed
##        for the state at nps.gov
def get_sites_for_state(state_abbr):

    # prolly going to use requests and cache here to actually make the list n shit
    # matt confirmed we do
    state_name = convert_abbreviation(state_abbr)
    if CACHE_DICT_SITE[state_name] is None:
        # need to make scrape_some_shit take in a state name as a param
        state_sites[state_name] = scrape_some_shit()
        part1_is_cached(state_sites)
        return state_sites[state_name]

    else:
        return CACHE_DICT_SITE[state_name]

    pass

def part1_is_cached(dict):

    json_shit = json.dumps(dict)
    # cache part one using this bitch lol
    with open(CACHE_SITE, 'w') as f:
        f.write(json_shit)
        f.close()

    pass





## Must return the list of NearbyPlaces for the specified NationalSite
## param: a NationalSite object
## returns: a list of NearbyPlaces within 10km of the given site
##          if the site is not found by a Google Places search, this should
##          return an empty list
def get_nearby_places_for_site(site_object):

    # this is gonna be where the Google API is used
    # prolly gonna be complicated af
    # yay

    if CACHE_DICT_NEARBY[site_object] is None:
        near_sites[site_object] = actually_get_places(site_object)
        part2_is_cached(near_sites)
        return near_sites[site_object]

    else:
        return CACHE_DICT_NEARBY[site_object]

    pass

def actually_get_places(site_object):

    empty_list = []
    other_list = []
    if len(other_list) != 0:
        return other_list
    else:
        return empty_list
    pass

def part2_is_cached(dict):

    # cache part two here
    json_shite = json.dumps(dict)
    with open(CACHE_NEARBY, 'w') as n:
        n.write(json_shite)
        n.close()

    pass

## Must return the list of Tweets that mention the specified NationalSite
## param: a NationalSite object
## returns: a list of up to 10 Tweets, in descending order of "popularity"
def get_tweets_for_site(site_object):

    # place for Twitter API
    # will be a lot like Lecture 10 stuff
    if CACHE_DICT_TWEET[site_object] is None:
        site_tweets[site_object] = actually_get_tweets(site_object)
        part3_is_cached(site_tweets)
        return site_tweets[site_object]

    else:
        return CACHE_DICT_TWEET[site_object]

    pass

def actually_get_tweets(site_object):


    pass

def part3_is_cached(dict):

    # part three is cached here
    json_jizz = json.dumps(dict)
    with open(CACHE_TWEET, 'w') as t:
        t.write(json_jizz)
        t.close()

    pass

def part_four():
    # is gonna use a while loop for sys.arg
    # if argument isn't exit then it continues to run
    # should end up being the main
    # option is to put all of the meat in here and then use a while loop for
    # the actual main function i.e. "while some variable != 6 then call part_four
    


    pass

part_four()
