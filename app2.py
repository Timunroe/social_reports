import tweepy
import facebook
# import requests
import time
import datetime
import json

# KEYS AND TOKENS

# need to log in to facebook and get new access token
# to run API: https://developers.facebook.com/tools/explorer/145634995501895/

config = {
    "twitter_keys": {
        'tco_consumer_key': 'f2strQdTzGpeWRMRPWh45dAjk',
        'tco_consumer_secret': '2zamRSvKlmzppqJzAhoHn5sd0BTEK00kxev3yFPcKofWLYha3x',
        'tco_access_token': '17861972-dtMOdAhtPTsmAc1XURGY097CPzRlXV0KejablU0Dd',
        'tco_access_token_secret': 'xQYmBpwPH8kxEQDtbheohHLYs1HX6HElAelojelAfswcw'
    },
    "fb_access_token": 'EAAAAXOqreEUBAMGp2bAIWYiYHF7pDoQSeVWl41EPlnBCkqB3e5GDq0Hp1iPUqc7WYOKiJUY0sxtwNDZChhcIpOXf2pHQYza7u3SU6z5BOIv2Ai8m2C42EivC3QeZB9mO7S3ieXe5kZCy4hgonxCPqZCtBgPXqmsZD',
    "accounts": [
        ('TheSpec', 'thespec', '374180572246'),
        ('TheRecord', 'wr_record', '164238703606271'),
        ('MercTribune', 'mercurytribune', '18273611274'),
        ('STC Standard', 'stcatstandard', '311195955727'),
        ('Ptbo Examiner', 'ptboexaminer', '155638667834280'),
        ('NF Review', 'niafallsreview', '169828741647'),
        ('W Tribune', 'wellandtribune', '304679263870')
    ]
}


# account tuple is (paper, twitter handle, FB page id)

# tco_users = ['thespec', 'wr_record', 'mercurytribune', 'stcatstandard', 'wellandtribune', 'niafallsreview', 'ptboexaminer']

def get_fb_stats(s_token, s_page_id):
    graph = facebook.GraphAPI(access_token=s_token, version=3.1)
    page = graph.get_object(s_page_id, fields='name,fan_count')
    return page['fan_count']


def get_tco_stats(d_keys, s_user):
    auth = tweepy.OAuthHandler(d_keys['tco_consumer_key'], d_keys['tco_consumer_secret'])
    auth.set_access_token(d_keys['tco_access_token'], d_keys['tco_access_token_secret'])
    api = tweepy.API(auth)
    this_user = api.get_user(s_user)
    return this_user.followers_count


def loop(d_config):
    # adds objects to list l_stats
    l_list = []
    for item in d_config['accounts']:
        d_obj = {}
        d_obj["site"] = item[0]
        d_obj["fb"] = get_fb_stats(d_config['fb_access_token'], item[2])
        time.sleep(2)
        d_obj["tco"] = get_tco_stats(d_config['twitter_keys'], item[1])
        l_list.append(d_obj)
        time.sleep(2)
    return l_list


# MAIN

this_record = {}
this_record['date'] = str(datetime.date.today())
this_record['stats'] = loop(config)

# db = [
# { "date": "2018-04-02", "stats": [{"site": "xx", "fb": 123, "tco": 123}] }
# ]

with open('db.json', 'a+') as outfile:
    json.dump(this_record, outfile, ensure_ascii=False, sort_keys=True, indent=4)
