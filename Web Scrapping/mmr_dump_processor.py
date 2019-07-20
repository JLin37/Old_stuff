import numpy as np
from datetime import datetime
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime
from pymongo import MongoClient
from lxml import etree
from pytz import timezone
import re
import requests

def getPrice(html_tree, xpath):
    price = html_tree.xpath(xpath)[0].text.strip()
    price = price.replace('$', '').replace(',', '')
    price = int(price)
    return price


def downloadLink(link):

    #defines header information
    headers = {
        "Connetion" : "close",
        "User-Agent" : "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)"
    }
    print(link)

    # using timeouts and requests library
    #  fixes timeout problems
    html = requests.get(link, timeout = 500, headers = headers)
    html = html.content

    return html

client2 = MongoClient('localhost', 27017)
db2 = getattr(client2, 'mmr_dumps')
collection_mmr_dumps = getattr(db2, 'dumps1')

list_delta = []
list_markup = []

#for listing in collection_mmr_dumps.find({'mid_info.make': 'ACURA'}):
for listing in collection_mmr_dumps.find():
    #print('anotha 1')
    #print(listing['link'])
    html_source = listing['html']

    html_tree = etree.HTML(html_source)

    if not ('Sorry, no pricing available.' in html_source or 'is invalid' in html_source):

        #print(html_source)

        #time.sleep(10)

        name = str(html_tree.xpath('string(//*[@id="mmrFavorite"])')).strip()

        auction_above = getPrice(html_tree, """//*[@id="content"]/table[3]/tbody/tr[2]/td[1]""")
        auction_average = getPrice(html_tree, """//*[@id="content"]/table[3]/tbody/tr[2]/td[2]""")
        auction_below = getPrice(html_tree, """//*[@id="content"]/table[3]/tbody/tr[2]/td[3]""")

        est_retaill_above = getPrice(html_tree, """//*[@id="content"]/table[3]/tbody/tr[3]/td[1]""")
        est_retaill_average = getPrice(html_tree, """//*[@id="content"]/table[3]/tbody/tr[3]/td[2]""")
        est_retaill_below = getPrice(html_tree, """//*[@id="content"]/table[3]/tbody/tr[3]/td[3]""")

        odometer_average = html_tree.xpath("""//*[@id="ymms_lookup"]/div[2]/div/div/fieldset/div[5]/input[1]""")[0].get(
            'value')
        region = html_tree.xpath("""//*[@id="select"]/optgroup[1]/option[1]""")[0].get('value')

        curr_date_range = html_tree.xpath("""//*[@id="content"]/h3[2]""")
        curr_date_range = curr_date_range[0].text
        # print(curr_date_range)
        curr_date_range = curr_date_range.split()
        curr_date_range.pop(0)

        curr_year = curr_date_range.pop()
        from_date_month = curr_date_range.pop(0)
        from_date_day = curr_date_range.pop(0)
        from_dt_str = from_date_month + ' ' + from_date_day + ' ' + curr_year

        from_dt = datetime.datetime.strptime(from_dt_str, '%b %d %Y')

        curr_date_range.pop(0)

        to_date_month = curr_date_range.pop(0)
        to_date_day = curr_date_range.pop(0)

        to_dt_str = to_date_month + ' ' + to_date_day + ' ' + curr_year
        to_dt = datetime.datetime.strptime(from_dt_str, '%b %d %Y')

        #print('curr year', curr_year)
        #print('from month day', from_date_month, from_date_day)
        #print('to month day', to_date_month, to_date_day)

        #print(name)
        #print('auction prices', auction_above, auction_average, auction_below)
        #print('retail prices', est_retaill_above, est_retaill_average, est_retaill_below)
        #print('avg odometer', odometer_average)
        #print('region', region)
        #print('from dt', from_dt)
        #print('to dt', to_dt)

        if auction_above != 0 and auction_average != 0 and auction_below != 0 and est_retaill_above != 0 and est_retaill_average != 0 and est_retaill_below != 0:
            above_delta = est_retaill_above - auction_above
            avg_delta = est_retaill_average - auction_average
            below_delta = est_retaill_below - auction_below


            general_delta_avg = (avg_delta + below_delta + above_delta) / 3

            if (general_delta_avg > 0):
                list_delta.append(general_delta_avg)

            print(listing['mid_info']['year'], listing['mid_info']['make'], listing['mid_info']['model'], listing['mid_info']['style'])
            #print('above delta', above_delta)
            #print('avg delta', avg_delta)
            #print('below delta', below_delta)
            print('delta avg', general_delta_avg)

            above_markup = (above_delta / auction_above) * 100
            avg_markup = (avg_delta / auction_average) * 100
            below_markup = (below_delta / auction_below) * 100


            general_markup = (above_markup + avg_markup + below_markup) / 3

            if (general_markup > 0):
                list_markup.append(general_markup)

            #print('above markup percentage', above_markup)
            #print('avg markup percentage', avg_markup)
            #print('below markup percentage', below_markup)
            print('markup avg', general_markup)
            print('*' * 50)

a = np.array(list_delta)
b = np.array(list_markup)

print('delta mean', a.mean())
print('delta min', a.min())
print('delta max', a.max())

print('markup mean', b.mean())
print('markup min', b.min())
print('markup max', b.max())
