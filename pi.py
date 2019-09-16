from requests_html import HTMLSession
import requests
import re
import json
from datetime import date

sites = [
    {
        'site': 'TS',
        'fb': 'https://www.facebook.com/torontostar/',
        'tw': 'https://twitter.com/TorontoStar',
        'yt': 'https://www.youtube.com/TorontoStar',
        'ig': 'https://www.instagram.com/thetorontostar/?hl=en',
        'pi': 'https://www.pinterest.ca/torontostar/',
        # 'li': '',
    },
    {
        'site': 'HS',
        'fb': 'https://www.facebook.com/hamiltonspectator/',
        'tw': 'https://twitter.com/TheSpec',
        'yt': 'https://www.youtube.com/thespecvideo',
        'ig': 'https://www.instagram.com/hamiltonspectator/?hl=en',
        'pi': 'https://www.pinterest.ca/thespectator/',
        # 'li': 'https://ca.linkedin.com/company/the-hamilton-spectator',
    },
    {
        'site': 'WRR',
        'fb': 'https://www.facebook.com/waterlooregionrecord/',
        'tw': 'https://twitter.com/WR_Record',
        'yt': 'https://www.youtube.com/phototherecord',
        'ig': 'https://www.instagram.com/waterlooregionrecord/?hl=en',
        'pi': 'https://www.pinterest.ca/WRrecord/',
        # 'li': ''
    },
    {
        'site': 'SCS',
        'fb': 'https://www.facebook.com/stcatharinesstandard/',
        'tw': 'https://twitter.com/StCatStandard',
        'yt': 'https://www.youtube.com/channel/UCcAzUYgemMC1igVHQwyw4uA',
        'ig': 'https://www.instagram.com/stcatharinesstandard/',
        'pi': '',
        # 'li': ''
    },
    {
        'site': 'NFR',
        'fb': 'https://www.facebook.com/niagarafallsreview/',
        'tw': 'https://twitter.com/NiaFallsReview',
        'yt': '',
        'ig': '',
        'pi': '',
        # 'li': ''
    },
    {
        'site': 'WT',
        'fb': 'https://www.facebook.com/wellandtribune/',
        'tw': 'https://twitter.com/WellandTribune',
        'yt': 'https://www.youtube.com/channel/UCVClY5BoeVYaj834JOKLZUw',
        'ig': 'https://www.instagram.com/thewellandtribune/',
        'pi': '',
        # 'li': ''
    },
    {
        'site': 'PE',
        'fb': 'https://www.facebook.com/PeterboroughExaminer/',
        'tw': 'https://twitter.com/PtboExaminer',
        'yt': 'https://www.youtube.com/channel/UC9RwlcrujYFt_GRVayVt3_g',
        'ig': 'https://www.instagram.com/pboroexaminer/',
        'pi': '',
        # 'li': ''
    }
]


def pi_followers(url):
    if url:
        session = HTMLSession()
        r = session.get(url)
        r.html.render()
        results = r.html.find('span.tBJ.dyH.iFc.SMy._S5.pBj.DrD.mWe')
        followers = results[0].text
        return followers.strip()
    else:
        return ''


def main():
    for site in sites:
        print(f'''Processing {site['site']}''')
        pi = pi_followers(site['pi'])
        print('This many followers: ', pi)
    return


main()
