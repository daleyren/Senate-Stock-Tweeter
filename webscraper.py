from urllib import response
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common import keys
from selenium.webdriver.support.select import Select
from datetime import datetime
import pdb
import tweepy
import config
import time

# TWEEPY SET UP
client = tweepy.Client(consumer_key= 'API_KEY', consumer_secret= 'API_KEY_SECRET', access_token= 'ACCESS_TOKEN', access_token_secret= 'ACCESS_TOKEN_SECRET')
auth = tweepy.OAuthHandler('API_KEY', 'API_KEY_SECRET')
auth.set_access_token('ACCESS_TOKEN', 'ACCESS_TOKEN_SECRET')

api = tweepy.API(auth, retry_count= 2, timeout = 60, wait_on_rate_limit = True)


# PROCESS DATA FROM SEC.REPORT
url = 'https://sec.report/Senate-Stock-Disclosures?sort=filedhttps://sec.report/Senate-Stock-Disclosures?sort=filed'
browser = webdriver.Chrome('/Users/daler/Computer Science/Personal Projects/Tools/chromedriver')
browser.get(url)

oldID = -1
newID = 1

while 1:
    oldID = newID
    browser.get(url)
    table = browser.find_elements_by_class_name('table')[0]
    body = table.find_elements_by_tag_name('tbody')[0]
    rows = body.find_elements_by_tag_name('tr')

    newID = rows[1].text.split('\n')[1]
    print(datetime.now())
    if oldID != newID:
        # PAGE UPDATED
        print('*UPDATE*')
        sequenceID = -1
        for i in range(0, len(rows), 2):
            first = rows[i].text
            second = rows[i+1].text

            firstRow = first.split('\n')
            secondRow = second.split('\n')

            fileDate, transactionDate, stock, senator = firstRow
            transactionType, transactionID, transactionAmount, _, _ = secondRow

            cutOff = senator.find('[')
            senator = senator[0:cutOff-1]

            if i >= 2 and sequenceID != transactionID:
                break

            if i == 0:
                sequenceID = transactionID
    
            # TWEET TRADE
            out = transactionType + " of " + stock + " for " + transactionAmount + " | " + senator + " | SEC File Date: " + fileDate + " | Transaction Date: " + transactionDate
            api.update_status(status=out)
            print(out + '\n')
    else:
        # NO UPDATE
        print('*NO UPDATE*')
    time.sleep(240)
    
# pdb.set_trace()