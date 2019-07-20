__author__ = 'Menghao Lin'
# created on Dec 14, 2015

from random import randint
from pymongo import MongoClient
from lxml import etree
import requests, time, datetime



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


def makeListing(listinghtml):
    x = etree.HTML(listinghtml)
    i = 1
    # MongoDB connection
    connection = MongoClient('localhost', 27017)
    CMListingsdb = connection.CMCarsDB
    posts = CMListingsdb.CMCars

    while i <= 20:
        i= str(i)
        YearMakeModelTrim = x.xpath('string(//html/body/div[1]/div/div[2]/div[2]/div[13]/div['+ i +']/div[2]/a/h3)')
        Miles = x.xpath('string(//html/body/div[1]/div/div[2]/div[2]/div[13]/div['+ i +']/div[2]/dl/dd[1])')
        Drive = x.xpath('string(//html/body/div[1]/div/div[2]/div[2]/div[13]/div['+ i +']/div[2]/dl/dd[2])')
        Transmission = x.xpath('string(//html/body/div[1]/div/div[2]/div[2]/div[13]/div['+ i +']/div[2]/dl/dd[3])')
        ExtColor = x.xpath('string(//html/body/div[1]/div/div[2]/div[2]/div[13]/div['+ i +']/div[2]/dl/dd[5])')
        IntColor = x.xpath('string(//html/body/div[1]/div/div[2]/div[2]/div[13]/div['+ i +']/div[2]/dl/dd[6])')
        Price = x.xpath('string(//html/body/div[1]/div/div[2]/div[2]/div[13]/div['+ i +']/div[3]/div[1]/div[2])')
        Location = x.xpath('string(//html/body/div[1]/div/div[2]/div[2]/div[13]/div['+ i +']/div[3]/div[2]/div[1]/div[2])')
        StockNum = x.xpath('string(//html/body/div[1]/div/div[2]/div[2]/div[13]/div['+ i +']/div[2]/dl/dd[7])')
        CMhrefs = x.xpath('/html/body/div[1]/div/div[2]/div[2]/div[13]/div[1]/div[3]/a')
        for element in CMhrefs:
            CMcarlink = "http://www.carmax.com" + element.get('href')
        checkstockNum = posts.distinct("stcknum", {"stcknum": StockNum})
        if checkstockNum == []:
            post = \
            (
                {
                    "yearmakemodel" : YearMakeModelTrim,
                    "miles" : Miles,
                    "drive" : Drive,
                    "transmission" : Transmission,
                    "extcolor" : ExtColor,
                    "intcolor" : IntColor,
                    "price" : Price,
                    "stcknum" : StockNum,
                    "location" : Location,
                    "CMcarlink" : CMcarlink,
                    'date_created': str(datetime.datetime.utcnow())
                }
            )
            posts.insert(post)
        i = int(i)
        i = i+1


def lenCMlistings(html):
    x = etree.HTML(html)
    cmListings = x.xpath('string(//html/body/div[1]/div/div[2]/div[2]/div[13]/div[1]/div[2]/a/h3)')
    if len(cmListings) == 0:
        return len(cmListings)


print("Hello world\n\n\n**********************************************************************")
start = time.clock()

linkarray = ['http://www.carmax.com/search?No=FCKCM&D=90&zip=90001&N=285+4294961419+4294961243+4294961487+4294961377&Q=a23b9880-00b1-4f85-af12-107d0c10e098&Ep=search:results:results%20page',
                'http://www.carmax.com/search?No=FCKCM&D=90&zip=90001&N=285+4294961406+4294961285+4294959609+4294961469+4294961458+4294960794+4294959428+4294961321&Q=a23b9880-00b1-4f85-af12-107d0c10e098&Ep=search:results:results%20page',
                'http://www.carmax.com/search?No=FCKCM&D=90&zip=90001&N=285+4294959558+4294961382+4294961347+4294961238+4294961474+4294959638&Q=6091c8e0-647a-4bc6-91c2-e445d258515a&Ep=search:results:results%20page',
                'http://www.carmax.com/search?No=FCKCM&D=90&zip=90001&N=285+4294961459+4294959456+4294961226+4294961330+4294961478+4294961399+4294961116+4294961341+4294961219+4294961412&Q=a23b9880-00b1-4f85-af12-107d0c10e098&Ep=search:results:results%20page',
                'http://www.carmax.com/search?No=FCKCM&D=90&zip=90001&N=285+4294961388+4294961355+4294960570&Q=a23b9880-00b1-4f85-af12-107d0c10e098&Ep=search:results:results%20page',
                'http://www.carmax.com/search?No=FCKCM&D=90&zip=90001&N=285+4294961359+4294961278&Q=989b1e44-6e4c-4d94-9dbc-a6e8c53bc258&Ep=search:results:results%20page',
                'http://www.carmax.com/search?No=FCKCM&D=90&zip=90001&N=285+4294961261+4294961332+4294959246+4294960619+4294961312+4294961126+4294961203&Q=c2d71212-5702-42dc-b2ab-a631ba61c868&Ep=search:results:results%20page',
                'http://www.carmax.com/search?No=FCKCM&D=90&zip=90001&N=285+4294959378+4294959254+4294961430+4294961286+4294961266+4294961484+4294961333&Q=3853d4f6-6b73-40c6-a731-b5d99390399d&Ep=search:results:results%20page',
                'http://www.carmax.com/search?No=FCKCM&D=90&zip=90001&N=285+4294961380+4294961375+4294961253+4294961287+4294961387+4294961418+4294959334+4294961354+4294961258&Q=aa95381b-a52c-4262-b625-5474b4a60e11&Ep=search:results:results%20page',
                'http://www.carmax.com/search?No=FCKCM&D=90&zip=90001&N=285+4294961425+4294961340+4294961401&Q=2790444a-ccc1-4092-834d-6987a7f02731&Ep=search:results:results%20page',
                'http://www.carmax.com/search?No=FCKCM&D=90&zip=90001&N=285+4294961297+4294960875+4294961251&Q=27826d69-1fed-485e-94fa-3b25189531c2&Ep=search:results:results%20page',
                'http://www.carmax.com/search?No=FCKCM&D=90&zip=90001&N=285+4294961481+4294961384+4294961386+4294960687&Q=282530a6-29fd-42a9-a489-58bc3c8be779&Ep=search:results:results%20page',
                'http://www.carmax.com/search?No=FCKCM&D=90&zip=90001&N=285+4294961365+4294961392+4294961342+4294961317+4294961329+4294961336+4294961255+4294961304+4294959349&Q=0ca6c09f-1f41-4d49-9c3b-de3c04de5315&Ep=search:results:results%20page',
                'http://www.carmax.com/search?No=FCKCM&D=90&zip=90001&N=285+4294959773+4294959250+4294960383+4294961475+4294961398+4294961180+4294961294+4294961363+4294961400&Q=42550655-823e-4b1f-92a8-e8b42269cc04&Ep=search:results:results%20page',
                'http://www.carmax.com/search?No=FCKCM&D=90&zip=90001&N=285+4294961404+4294961445+4294961338+4294960700+4294961344+4294961417+4294961462&Q=e49b6087-daea-45d1-a8fd-a37ca8f0a8eb&Ep=search:results:results%20page',
                'http://www.carmax.com/search?No=FCKCM&D=90&zip=90001&N=285+4294961452+4294961199+4294961260+4294961090+4294961296&Q=e3ccb4b7-d32d-4907-b4f6-e1a101a01a21&Ep=search:results:results%20page',
                'http://www.carmax.com/search?No=FCKCM&D=90&zip=90001&N=285+4294959345+4294961201+4294961352+4294961420&Q=368b3282-5875-4acf-8b82-e5109537bcfc&Ep=search:results:results%20page',
                'http://www.carmax.com/search?No=FCKCM&D=90&zip=90001&N=285+4294961313+4294959574+4294961464+4294961415+4294960590&Q=08e0e9e9-8989-41e2-b1b9-9a0421bc59e6&Ep=search:results:results%20page',
                'http://www.carmax.com/search?No=FCKCM&D=90&zip=90001&N=285+4294960606+4294961188+4294961234+4294961249+4294961381+4294961118+4294961448+4294961476+4294961265&Q=0e093898-d881-4f07-867a-3382342e7009&Ep=search:results:results%20page',
                'http://www.carmax.com/search?No=FCKCM&D=90&zip=90001&N=285+4294961265+4294961246+4294961356+4294961374+4294961467+4294960362+4294960724+4294960784+4294959316&Q=96293c20-8a24-45f0-8288-5ab535c8c351&Ep=search:results:results%20page',
                'http://www.carmax.com/search?No=FCKCM&D=90&zip=90001&N=285+4294961450+4294961370+4294961395+4294961269+4294961324+4294961351+4294961422+4294959593+4294959406&Q=b491b10f-878e-4fd9-bea7-a9f7272f28f5&Ep=search:results:results%20page',
                'http://www.carmax.com/search?No=FCKCM&D=90&zip=90001&N=285+4294961393+4294959355+4294961396+4294961232+4294961319+4294961390+4294961361+4294961424&Q=808eff3d-2833-4ef4-8db9-cd46ac3b9c8e&Ep=search:results:results%20page']

counter = 0
for link in linkarray:
    pgNum = 0
    Numskip = str(pgNum)
    listings = 20
    while listings != 0:
        time.sleep((randint(1 , 10)/100))
        html = downloadLink(link.replace('FCKCM', Numskip))
        makeListing(html)
        pgNum = pgNum + 20
        Numskip = str(pgNum)
        listings = lenCMlistings(html)
        counter = counter + 20

print(counter)
end = time.clock()
timeTaken = end - start
print("Time taken:", timeTaken)
print("**********************************************************************\n\n\nGoodbye world")