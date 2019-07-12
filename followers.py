from requests_html import HTMLSession
import requests
import re
import json
from datetime import date
import utils

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


def li_followers(url):
    '''
body > main > div > div > div > div > section.top-card.module.card > div > div.top-card__details > div > div.top-card__information > span:nth-child(3)
    '''
    r = requests.get('https://www.linkedin.com/uas/login', auth=('tmunroe@thespec.com', 'WCr4EA6qmkkH'))
    print(r.status_code)
    print(r.text)
    return


def ig_followers(url):
    print('Starting IG section')
    '''
    follower count found in script json in head
    '''
    if url:
        session = HTMLSession()
        r = session.get(url)
        results = r.html.find('script')
        for result in results:
            if 'userInteractionCount' in result.text:
                d = json.loads(result.text)
                followers = d['mainEntityofPage']['interactionStatistic']['userInteractionCount']
                return followers.strip()
        results = r.html.find('meta')
        result = results[13].attrs['content']
        x = re.search(r"\d{1,3}(,\d{3})*(\.\d+)? Followers", result)
        if x:
            followers = x.group().replace(' Followers', '').replace(',', '')
            return followers.strip()
        else:
            return ''
    else:
        return ''


def yt_followers(url):
    print('Starting YT section')
    '''
    Data is added dynamically via script.
    Find script with desired phrase, regex out subscribers
    '''
    if url:
        session = HTMLSession()
        r = session.get(url)
        results = r.html.find('script')
        for result in results:
            if 'subscriber' in result.text:
                x = re.search(r"\d{1,3}(,\d{3})*(\.\d+)? subscribers", result.text)
                if x:
                    followers = x.group().replace(' subscribers', '').replace(',', '')
        return followers.strip()
    else:
        return ''


def tw_followers(url):
    print('Starting TW section')
    '''
    #page-container > div.ProfileCanopy.ProfileCanopy--withNav.ProfileCanopy--large.js-variableHeightTopBar > div > div.ProfileCanopy-navBar.u-boxShadow > div > div > div.Grid-cell.u-size2of3.u-lg-size3of4 > div > div > ul > li.ProfileNav-item.ProfileNav-item--followers > a > span.ProfileNav-value
    '''
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    result = r.html.find('#page-container > div.ProfileCanopy.ProfileCanopy--withNav.ProfileCanopy--large.js-variableHeightTopBar > div > div.ProfileCanopy-navBar.u-boxShadow > div > div > div.Grid-cell.u-size2of3.u-lg-size3of4 > div > div > ul > li.ProfileNav-item.ProfileNav-item--followers > a > span.ProfileNav-value', first=True)
    followers = result.attrs['data-count']
    return followers.strip()


def fb_followers(url):
    '''
    #PagesProfileHomeSecondaryColumnPagelet > div > div:nth-child(1) > div > div._4-u2._6590._3xaf._4-u8 > div:nth-child(4) > div > div._4bl9 > div
    <div>21,582 people follow this</div>
    '''
    session = HTMLSession()
    r = session.get(url)
    results = r.html.find('div._4bl9 > div')
    for result in results:
        if 'follow' in result.text:
            followers = result.text.replace('people follow this', '').replace(',', '')
    return followers.strip()


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
    report = f'''SOCIAL MEDIA FOLLOWERS
Week No. {date.today().isocalendar()[1]}, {date.today().isocalendar()[0]}
=========================================
SITE     FB      TW    YT     IG    PI
'''
    for site in sites:
        print(f'''Processing {site['site']}''')
        fb = fb_followers(site['fb'].replace(',', ''))
        tw = tw_followers(site['tw'].replace(',', ''))
        yt = yt_followers(site['yt'].replace(',', ''))
        ig = ig_followers(site['ig'].replace(',', ''))
        pi = pi_followers(site['pi'].replace(',', ''))
        # li = li_followers(site['li'])
        report += f'''\
-----------------------------------------
{site['site'].ljust(3)}  \
{(utils.humanize(fb)).rjust(6)} \
{(utils.humanize(tw)).rjust(7)} \
{(utils.humanize(yt)).rjust(5)} \
{(utils.humanize(ig)).rjust(6)} \
{(utils.humanize(pi)).rjust(6)}
'''
    print(report)


main()
