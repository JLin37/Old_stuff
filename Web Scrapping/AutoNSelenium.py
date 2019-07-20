__author__ = 'Menghao Lin'
# created on Dec 16, 2015

from lxml import etree
from selenium import webdriver
from pymongo import MongoClient
from random import randint
import math, datetime,time

connection = MongoClient('localhost', 27017)
CMListingsdb = connection.ANCarsDB
posts = CMListingsdb.ANCars


def getnumofpages():
    browser = webdriver.PhantomJS(executable_path='/home/jason/Documents/phantomjs/bin/phantomjs') # Get local session of firefox
    browser.get("https://www.autonation.com/los-angeles/cars/makes/used-+-+/90001,200/near/#/used-+-+-+-+-+-+-+-+-+-+-+-+-+-+-90001,0-+/near/1/1") # Load page
    html_source = browser.page_source
    x = etree.HTML(html_source)
    totalcarnum = x.xpath('string(/html/body/form/div[3]/div/div[3]/div/div[1]/div/div/div[1]/dl/dd[1]/div/h2[1])').replace(' Results Found', '')
    numofpages = math.ceil(int(totalcarnum)/12)
    return numofpages

def scrapthroughauton():
    numofpages = getnumofpages()
    pages = 1
    while pages <= numofpages:
        browser = webdriver.PhantomJS(executable_path='/home/jason/Documents/phantomjs/bin/phantomjs')
        page = str(pages)
        link = "https://www.autonation.com/los-angeles/cars/makes/used-+-+/90001,200/near/#/used-+-+-+-+-+-+-+-+-+-+-+-+-+-+-90001,0-+/near/72/"+ page
        print(link)
        browser.get(link)
        html_source = browser.page_source
        x = etree.HTML(html_source)
        i = 1
        while i <= 72:
            time.sleep((randint(1 , 10)/100))
            i= str(i)
            YearMakeModelTrim = x.xpath('string(/html/body/form/div[3]/div/div[3]/div/div[1]/article/div[1]/div[6]/ul/li['+ i +']/div/div[2]/a)').replace('...', '')
            Vin = x.xpath('string(/html/body/form/div[3]/div/div[3]/div/div[1]/article/div[1]/div[6]/ul/li['+ i +']/div/div[3]/span[2])')
            Price = x.xpath('string(/html/body/form/div[3]/div/div[3]/div/div[1]/article/div[1]/div[6]/ul/li['+ i +']/div/table/tbody/tr[1]/td[2]/strong)')
            ANhref = x.xpath('/html/body/form/div[3]/div/div[3]/div/div[1]/article/div[1]/div[6]/ul/li[1]/div/div[2]/a')
            for element in ANhref:
                ANcarlink = "https://www.autonation.com" + element.get('href')
            checkvin = posts.distinct('vin', {"vin": Vin})
            if checkvin == []:
                post = \
                (
                    {
                        "yearmakemodel" : YearMakeModelTrim,
                        "vin" : Vin,
                        "price" : Price,
                        "ANcarlink": ANcarlink,
                        'date_created': str(datetime.datetime.utcnow())
                    }
                )
                posts.insert(post)
            i = int(i)
            i = i+1
        pages = pages + 1

print("Hello world\n\n\n**********************************************************************")
start = time.clock()

scrapthroughauton()

end = time.clock()
timeTaken = end - start
print("Time taken:", timeTaken)
print("**********************************************************************\n\n\nGoodbye world")