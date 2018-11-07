#!/usr/bin/env python3


# A Reddit bot that posts explanation of xkcd comic strips posted in comments
# The explanation is extracted from http://explainxkcd.com
# License: MIT License

from bs4 import BeautifulSoup
import os
import praw
import time
import re
import requests
import bs4
from datetime import datetime


commented_path = 'commented.txt'
comment_id_set = set()
# Location of file where id's of already visited comments are maintained


def authenticate():

    print('Authenticating...\n')
    reddit = praw.Reddit(user_agent='churningScraper', \
            username = 'yourUserNameHere', \
            password = 'yourPasswordHere', \
            client_id= 'yourClientIdHere' , \
            client_secret = 'yourClientSecretIdHere')
    return reddit


def fetchdata(url):

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    tag = soup.find('p')
    data = ''
    while True:
        if isinstance(tag, bs4.element.Tag):
            if tag.name == 'h2':
                break
            if tag.name == 'h3':
                tag = tag.nextSibling
            else:
                data = data + '\n' + tag.text
                tag = tag.nextSibling
        else:
            tag = tag.nextSibling

    return data

def credit_card_link(link):
    if link == "[referrals] Chase Sapphire Preferred":
        return "referyourchasecard.com/m/6/6L5/FRGP/1542434286"
    elif link == "[referrals] Chase Freedom Unlimited":
        return "referyourchasecard.com/18/QET9YZKYD5"
    elif link == "[referrals] Chase Ink Preferred":
        return "referyourchasecard.com/21/QB6ZTFEXXC"
    elif link == "[referrals] Chase Freedom":
        return "referyourchasecard.com/2/KJTU7JXRI7"
    elif link == "[referrals] Discover It":
        return "refer.discover.com/s/plolp"
    elif link == "[referrals] Chase Southwest Airlines Rapid Rewards Plus":
        return "referyourchasecard.com/m/223/6L5/FQX8/1543514181"
    elif link == "[referrals] Chase Southwest Airlines Rapid Rewards Premier":
        return "referyourchasecard.com/m/224/6L5/FQWQ/1543511070"
    elif link == "[referrals] Chase Marriott Rewards Premier Plus":
        return "referyourchasecard.com/252/SROPECSY4L"
    elif link == "[referrals] Chase United Explorer":
        return "referyourchasecard.com/217/EXOB38RT39"
    elif link == "[referrals] American Express Starwood Preferred Guest Business":
        return "americanexpress.com/us/credit-cards/card-application/apply/starwood-preferred-guest-business-credit-card/54649-9-0-B51931CE59D999C7A58DE2541A02EC9D-201279-43B1B04F1CDF826F246E05451786FE00-GrQamgdfP4FTGbSoX0TWNpjkzJI=?mgmtrackingParam=US-mgm-inav-copypaste-474-201279-GBAB:0001-474-GBAB:0001&intlink=US-mgm-inav-copypaste-474-201279-GBAB:0001-474-GBAB:0001#/"
    else:
        return 0




def run_explainbot(reddit):
    for thread in reddit.get_subreddit('churningreferrals').new(limit=2):
        reply = credit_card_link(thread.title)
        if reply !=0:
            print(thread.title  + thread.id)
            thread.reply(reply)
            print("Posted to thread " + thread.title + " with link " + reply)
        #comment_id_set.add(thread.id)


def main():
    reddit = authenticate()
    run_explainbot(reddit)


if __name__ == '__main__':
    main()
