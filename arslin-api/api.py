from flask import Flask, jsonify, make_response, request
from bson import json_util
from bson.objectid import ObjectId
from pymongo import MongoClient
from flask_cache import Cache
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys, datetime, smtplib, json, requests, random, string



# Flask
application = Flask(__name__)
#WARNING: Only use 'simple' cache type in development, for production use memcached
application.config['CACHE_TYPE'] = 'simple'
application.cache = Cache(application)


@application.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  response.headers.add('Content-Type', 'application/json')
  return response

@application.errorhandler(404) 
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# MongoDB connection
connection = MongoClient('localhost', 27017)
Listingsdb = connection.activeListings
Salesdb = connection.sales
Requestdb = connection.carrequests
Freeshippingdb = connection.freeshipping

#takes a composed string (filterables), tokenizes it and returns as an array of strings
#used to split up filter params for db queries
def spliterize(string):
    items = string.split(',')
    normalized = [item for item in items]
    return normalized

def toJson(data):
    return json.dumps(data, sort_keys=True, indent=4, default=json_util.default)

def LoadUserAgents():
    uafile='user_agents.txt'
    uas = []
    with open(uafile) as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1])
    random.shuffle(uas)
    return uas

def LoadProxies():
    proxyfile='proxies.txt'
    proxystring = []
    with open(proxyfile) as proxyf:
        for someprox in proxyf.readlines():
            if someprox:
                proxystring.append(someprox.strip()[1:-1])
    random.shuffle(proxystring)
    return proxystring

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@application.route('/api/sales', methods=['POST'])
def Sale():
    if request.method == 'POST':
        req_json = request.json
        #if values not present, defaults to None
        vin =  str(req_json.get('vin'))
        make = str(req_json.get('make'))
        model = str(req_json.get('model'))
        year = str(req_json.get('year'))
        fullName = str(req_json.get('fullName'))
        email = str(req_json.get('email'))
        phone_number = str(req_json.get('tel'))
        city = str(req_json.get('city'))
        state = str(req_json.get('state'))
        zipCode = str(req_json.get('zipCode'))
        comment = str(req_json.get('comment'))

        sale = {
                "vin": vin,
                "make": make,
                "model": model,
                "year": year,
                "comment": comment,
                "fullName": fullName,
                "email": email,
                "phone_number": phone_number,
                "city": city,
                "state": state,
                "zip": zipCode,
                "date": datetime.datetime.utcnow().isoformat(' '), 
                "completed": "false",
                }

        fromaddr = "arslincars@gmail.com"
        toaddr = "contact@arslin.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Sales Contact"

        body = (fullName + " would like to buy \n" +
            " \n" +
            "A "+ ' ' + year + ' ' + make + ' ' + model +
            "\n VIN:    " + vin +
            " \n" +
            "\n They have the following comments about the purchase: " +
            "\n" +
            " \n    " + comment +
            "\n" +
            "\n Their location is: "+ city + ' ' + state + ' ' + zipCode +
            "\n" +
            "\n they can be contacted by: "+ 
            "   \n email:   " + email +
            "   \n phone:   " + phone_number
            )
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "slowmotion")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        #if successful insertion into DB
        sale_id = Salesdb['sales'].insert_one(sale).inserted_id
        return jsonify(result={"status": 200})

@application.route('/api/reportrequest', methods=['POST'])
def reportRequest():
    if request.method == 'POST':
        req_json = request.json
        #if values not present, defaults to None
        vin =  str(req_json.get('vin'))
        make = str(req_json.get('make'))
        model = str(req_json.get('model'))
        year = str(req_json.get('year'))
        fullName = str(req_json.get('fullName'))
        email = str(req_json.get('email'))
        phone_number = str(req_json.get('tel'))

        # reportrequest = {
        #         "vin": vin,
        #         "make": make,
        #         "model": model,
        #         "year": year,
        #         "fullName": fullName,
        #         "email": email,
        #         "phone_number": phone_number,
        #         }

        result = Listingsdb['Listings'].find_one({'vin': vin})

        fromaddr = "arslincars@gmail.com"
        toaddr = email
        ccaddr = "contact@arslin.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Cc'] = ccaddr
        msg['Subject'] = "Arslin: Vehicle History Report Request"

        html = """
                <html>
                  <head></head>
                  <body>
                    <p>
                        Hi """ + fullName + """,
                    </p>
                    <p>
                        Click on the VIN number for the autocheck link for <a href=https://www.arslin.com/listings/"""+ vin +"""> """ + year + ""' '"" + make + """ """ + model + """</a>.
                    </p>
                    <p>
                       VIN: <a href="""+ result['xyz']['link_ac'] +""">""" + vin + """</a>.
                    </p>
                    <p>
                        And remember we update our listings almost everyday, 
                        so check them out to see what interesting new deals are available.
                    </p>
                    <p>
                        <a href=https://www.arslin.com/listings>Click here to brower our current listings</a>
                    </p>
                    <p>
                        Kind Regards,<br> 
                        <br>
                        Arslin Team <br>
                        Phone Number: (305) 771-3717 <br>
                        Email: contact@arslin.com <br>
                    </p>
                    <p>
                        <small>
                            Subject to arslin <a href="https://www.arslin.com/terms">Terms &amp; Coditions</a> and <a href="https://www.arslin.com/privacy">Privacy Policy</a>
                        </small>
                    </p>
                  </body>
                </html>
                """

        msg.attach(MIMEText(html, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "slowmotion")
        text = msg.as_string()
        server.sendmail(fromaddr, [toaddr, ccaddr], text)
        server.quit()
        #if successful insertion into DB
        return jsonify(result={"status": 200})

@application.route('/api/freeshipping', methods=['POST'])
def freeshipping():
    if request.method == 'POST':
        req_json = request.json
        fullName = str(req_json.get('fullName'))
        email = str(req_json.get('email'))
        phone_number = str(req_json.get('tel'))
        zipCode = str(req_json.get('zipCode'))
        shippingCode = id_generator()

        freeshipping = {
                "fullName": fullName,
                "email": email,
                "phone_number": phone_number,
                "zip": zipCode,
                "shippingCode": shippingCode,
                }

        fromaddr = "arslincars@gmail.com"
        toaddr = email
        ccaddr = "contact@arslin.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Cc'] = ccaddr
        msg['Subject'] = "Arslin: Free Shipping Code"

        html = """
                <html>
                  <head></head>
                  <body>
                    <p>
                        Hi """ + fullName + """,
                    </p>
                    <p>
                        Here is your <strong>Free Shipping Code</strong>: 
                    </p>
                    <p><strong>""" + shippingCode +"""</strong></p>
                    <p>
                        Please place this code in the comment section of the forms.
                    </p>
                    <p>
                        And remember we update our listings almost everyday, 
                        so check them out to see what interesting new deals are available.
                    </p>
                    <p>
                        <a href=https://www.arslin.com/listings>Click here to brower our current listings</a>
                    </p>
                    <p>
                        Kind Regards,<br> 
                        <br>
                        Arslin Team <br>
                        Phone Number: (305) 771-3717 <br>
                        Email: contact@arslin.com <br>
                    </p>
                    <p>
                        <small>
                            Subject to arslin <a href="https://www.arslin.com/terms">Terms &amp; Coditions</a> and <a href="https://www.arslin.com/privacy">Privacy Policy</a>
                        </small>
                    </p>
                  </body>
                </html>
                """

        msg.attach(MIMEText(html, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "slowmotion")
        text = msg.as_string()
        server.sendmail(fromaddr, [toaddr, ccaddr], text)
        server.quit()

        freeshipping_id = Freeshippingdb['shippingCode'].insert_one(freeshipping).inserted_id
        #if successful insertion into DB
        return jsonify(result={"status": 200})

@application.route('/api/carrequests', methods=['POST'])
def carRequests():
    if request.method == 'POST':
        req_json = request.json
        #if values not present, defaults to None
        make = str(req_json.get('make'))
        model = str(req_json.get('carmodel'))
        year = str(req_json.get('year'))
        fullName = str(req_json.get('fullName'))
        email = str(req_json.get('email'))
        phone_number = str(req_json.get('tel'))
        city = str(req_json.get('city'))
        state = str(req_json.get('state'))
        zipCode = str(req_json.get('zipCode'))
        extColor = str(req_json.get('extColor'))
        intColor = str(req_json.get('intColor'))
        mileage = str(req_json.get('mileage'))
        price = str(req_json.get('price'))
        comment = str(req_json.get('comment'))

        carrequest = {
                "year": year,
                "make": make,
                "model": model,
                "exterior color": extColor,
                "interior color": intColor,
                "mileage range": mileage,
                "price range": price,
                "fullName": fullName,
                "email": email,
                "phone_number": phone_number,
                "city": city,
                "state": state,
                "zip": zipCode,
                "comment": comment,
                "date": datetime.datetime.utcnow().isoformat(' '), 
                "completed": "false",
                }

        fromaddr = "arslincars@gmail.com"
        toaddr = "contact@arslin.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Request Car"

        body = (fullName + " is interested in \n" +
            "\n" +
            "A "+ ' ' + year + ' ' + make + ' ' + model +
            "\n" +
            "\n With the following colors: " +
            " \n exterior color:    " + extColor +
            " \n interior color:    " + intColor +
            "\n" +
            "\n They have the following comments to add to the requst: " +
            "\n" +
            " \n " + comment +
            "\n" +
            "\n Their location is:  "+ city + ' ' + state + ' ' + zipCode +
            "\n" +
            "\n They can be contacted by:   "+ 
            " \n email:     " + email +
            " \n phone:     " + phone_number
            )
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "slowmotion")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()

        #if successful insertion into DB
        request_id = Requestdb['Requests'].insert_one(carrequest).inserted_id
        return jsonify(result={"status": 200})

        
@application.route('/api/listings/<listing_id>', methods=['GET'])
def Listing(listing_id):
    vasturl = "http://autos.vast.com/cars/api/"
    if request.method == 'GET':
        #convert the listing_id from a string back to ObjectId to query Mongo
        result = Listingsdb['Listings'].find_one({'vin': listing_id},{'xyz':0})
        return toJson({'data': {'id': result['vin'], 
            'type': 'listing', 
            'attributes': result, 
            }})

@application.route('/api/comparables', methods=['GET'])
def comparableCars():
    vasturl = "http://autos.vast.com/cars/api/"
    if request.method == 'GET':
        if request.args.get('vin'):
            listing_id = request.args.get('vin')
        result = Listingsdb['Listings'].find_one({'vin': listing_id})
        arsprice = int(result['price']['est_price']['normal'])
        if arsprice == 55555:
            arsprice = 0
        else:
            arsprice = arsprice
        arsmileage = str(result['odometer']['normal'])
        vastData = [{'name': arsmileage + ' miles' , 'y': arsprice, 'dealer': 'Arslin', 'url': 'https://www.arslin.com/listings/' + listing_id}]
        vastMileage = result['odometer']['normal'] - 1000
        if vastMileage < 0:
            vastMileagelow = "min"
        else:
            vastMileagelow = str(vastMileage)
        vastMileageHigh = str(result['odometer']['normal'] + 4000)
        
        if request.args.get('zipcode'):
            zipCode = request.args.get('zipcode')
            if result['trim']['pretty'] is None:    
                fullvasturl = (vasturl + 
                    "year-"+ str(result['year']) +"-"+ str(result['year']) +
                    "/mileage-" + vastMileagelow +"-"+ vastMileageHigh +
                    # "/price-" + str(result['price']['est_price']['normal']) + "-max" +
                    "/make-"+ result['make']['pretty'] +
                    "/model-"+ str(result['model']['pretty']) +
                    "/location-"+ zipCode +
                    "/range-150/page-1")
            else:
                fullvasturl = (vasturl + 
                    "year-"+ str(result['year']) +"-"+ str(result['year']) +
                    "/mileage-" + vastMileagelow +"-"+ vastMileageHigh +
                    # "/price-" + str(result['price']['est_price']['normal']) + "-max" +
                    "/make-"+ result['make']['pretty'] +
                    "/model-"+ str(result['model']['pretty']) +
                    "/trim-"+ str(result['trim']['pretty']) +
                    "/location-"+ zipCode +
                    "/range-150/page-1") 
            uas = LoadUserAgents()
            requestproxy = LoadProxies()
            randomproxy = str(random.choice(requestproxy))
            proxy = {"http": "http://arslincars@gmail.com:vastmine@" + randomproxy}
            ua = random.choice(uas)
            headers = {
                "Connection" : "close",  # another way to cover tracks
                "User-Agent" : ua}
            response = requests.get(fullvasturl, proxies=proxy, headers=headers)
            vast_doc = response.json()
            
            if not vast_doc['results']:
                fullvasturl = (vasturl + 
                "year-"+ str(result['year']) +"-"+ str(result['year']) +
                "/mileage-" + vastMileagelow +"-"+ vastMileageHigh +
                # "/price-" + str(result['price']['est_price']['normal']) + "-max" +
                "/make-"+ result['make']['pretty'] +
                "/model-"+ str(result['model']['pretty']) +
                "/location-"+ zipCode +
                "/range-150/page-1")
                response = requests.get(fullvasturl, proxies=proxy, headers=headers)
                vast_doc = response.json()
                if not vast_doc['results']:
                    graphresults = {'scatterContent': []}
                else:
                    for item in vast_doc['results']:
                        try:
                            price = int(item['price']['value'])
                            mileage = str(item['mileage'])
                            dealer = item['dealer']['name']
                            getdealerurl = item['url']
                            if 'details' not in getdealerurl:
                                getdealerurl = 'http://autos.vast.com' + item['url']
                            else:
                                getdealerurl =  item['url']
                            dealerurl = getdealerurl.replace("\\", "")
                            vastData.append({'name': mileage +' miles', 'y': price, 'dealer': dealer, 'url': dealerurl})
                        except:
                            continue
                    graphresults = {'scatterContent': [{'name': 'Mileage',  'colorByPoint': 'true', 'data': vastData}]}
            else:
                for item in vast_doc['results']:
                    try:
                        price = int(item['price']['value'])
                        mileage = str(item['mileage'])
                        dealer = item['dealer']['name']
                        getdealerurl = item['url']
                        if 'details' not in getdealerurl:
                            getdealerurl = 'http://autos.vast.com' + item['url']
                        else:
                            getdealerurl =  item['url']
                        dealerurl = getdealerurl.replace("\\", "")
                        vastData.append({'name': mileage +' miles', 'y': price, 'dealer': dealer, 'url': dealerurl})
                    except:
                        continue    
                    graphresults = {'scatterContent': [{'name': 'Mileage',  'colorByPoint': 'true', 'data': vastData}]}  
        else:
            graphresults = {'scatterContent': [{'name': 'Mileage',  'colorByPoint': 'true', 'data': vastData}]}
        
        return  toJson({'data': {'id': result['vin'], 
            'type': 'comparable', 
            'attributes': graphresults
            }})

@application.route('/api/similars', methods=['GET'])
def similarCars():
    if request.method == 'GET':
        if request.args.get('vin'):
            listing_id = request.args.get('vin')
        result = Listingsdb['Listings'].find_one({'vin': listing_id})
        
        highprice = int(result['price']['est_price']['normal']) + 2000
        
        if int(result['price']['est_price']['normal']) < 2000:
            lowprice = 0
        else:
            lowprice = int(result['price']['est_price']['normal']) - 2000
        
        highodometer = int(result['odometer']['normal']) + 5000
        
        if int(result['odometer']['normal']) < 5000:
            lowodometer = 0
        else:
            lowodometer = int(result['odometer']['normal']) - 5000
        
        body = result['categories']['body_style']
        
        comparableResults = Listingsdb['Listings'].find({
            '$and': [
            {'vin': {'$ne': listing_id} }, 
            {'categories.body_style': body},
            { 'price.est_price.normal': { '$gt': lowprice } }, 
            { 'price.est_price.normal': { '$lt': highprice } },
            { 'odometer.normal': { '$gt': lowodometer } }, 
            { 'odometer.normal': { '$lt': highodometer } } ]
            },{
            "_id" : 0,
            'year': 1, 
            'make': 1, 
            'model': 1, 
            'odometer': 1,
            'image_list': 1,
            'price': 1,
            'grade': 1,
            'vin': 1
            }).limit(12)
        json_results = []
        for comparable in comparableResults:
            json_results.append({'id': comparable['vin'], 'type': 'similar', 'attributes': comparable})

        return toJson({'data': json_results})


@application.route('/api/listings', methods=['GET'])
def Listings():
    if request.method == 'GET':
        #used by pagination

        #extract page number query param
        if request.args.get('page'):
            page = int(request.args.get('page')) 
        else:
            page = 0
        
        if request.args.get('per_page'):
            per_page = int(request.args.get('per_page')) 
        else:
            per_page = 12
        #**extract filter query params**
        if request.args.get('make'):
            make_params = request.args.get('make')
            rmake = {'$in': spliterize(make_params) }
        else:
            rmake = {'$exists': 'true'}

        if request.args.get('bodyStyle'):
            bodyStyle_params = request.args.get('bodyStyle')
            rbodyStyle = {'$in': spliterize(bodyStyle_params) }
        else:
            rbodyStyle = {'$exists': 'true'}

        if request.args.get('transmission'):
            transmission_params = request.args.get('transmission')
            rtransmission = {'$in': spliterize(transmission_params) }
        else:
            rtransmission = {'$exists': 'true'}

        if request.args.get('car_model'):
            model_params = request.args.get('car_model')
            rmodel = {'$in': spliterize(model_params) }
        else:
            rmodel = {'$exists': 'true'}

        if request.args.get('trim'):
            trim_params = request.args.get('trim')
            rtrim = {'$in': spliterize(trim_params) }
        else:
            rtrim = {'$exists': 'true'}
        
        if request.args.get('color_ext'):
            color_ext_params = request.args.get('color_ext')
            rcolor_ext = {'$in': spliterize(color_ext_params) }
        else:
            rcolor_ext = {'$exists': 'true'}
        
        if request.args.get('color_int'):
            color_int_params = request.args.get('color_int')
            rcolor_int = {'$in': spliterize(color_int_params) }
        else:
            rcolor_int = {'$exists': 'true'}
        
        if request.args.get('year'):
            year_params = request.args.get('year')
            vals = spliterize(year_params)
            #exact year 
            ryear = {'$in': [int(x) for x in vals]}
        else:
            ryear = {'$exists': 'true'}

        if request.args.get('odometer'):
            vals = request.args.get('odometer').split()
            rodometer = {'$lt': int(vals[0]) }
        else:
            rodometer = {'$exists': 'true'}
        
        if request.args.get('price'):
            vals = request.args.get('price').split()
            rprice = {'$lt': int(vals[0])}
        else:
            rprice = {'$exists': 'true'}    

        if request.args.get('sort') == 'yearAsc':
            sortby = 'year'
            orderby = 1
        elif request.args.get('sort') == 'yearDsc':
            sortby = 'year'
            orderby = -1
        elif request.args.get('sort') == 'priceAsc':
            sortby = 'price.est_price.normal'
            orderby = 1
        elif request.args.get('sort') == 'priceDsc':
            sortby = 'price.est_price.normal'
            orderby = -1
        elif request.args.get('sort') == 'odometerAsc':
            sortby = 'odometer.normal'
            orderby = 1
        elif request.args.get('sort') == 'odometerDsc':
            sortby = 'odometer.normal'
            orderby = -1
        else:
            sortby = '$natural'
            orderby = 1            
        #build the meta object for pagination
        #length of all car listings, used for number of pages
        #*******CACHE this data in the future *******************
        length = Listingsdb['Listings'].find({'make.normal': rmake,
            'model.normal': rmodel,
            'trim.normal': rtrim,
            'color_ext': rcolor_ext, 
            'color_int': rcolor_int, 
            'transmission': rtransmission,
            'year': ryear, 
            'odometer.normal': rodometer, 
            'price.est_price.normal': rprice,
            'categories.body_style': rbodyStyle
            }).count()
        #probably get from query params - Static??
        pageLength = per_page
        #total pages calculated from length and pagesize
        totalPages = (length/pageLength) + 1
        #use the number of values in this collection to determine which page
        skip = page*pageLength
        

        results = Listingsdb['Listings'].find({'make.normal': rmake, 
            'model.normal': rmodel, 
            'trim.normal': rtrim,
            'color_ext': rcolor_ext, 
            'color_int': rcolor_int, 
            'transmission': rtransmission,
            'year': ryear, 
            'odometer.normal': rodometer, 
            'price.est_price.normal': rprice,
            'categories.body_style': rbodyStyle
            },{
            "_id" : 0,
            'year': 1, 
            'make': 1, 
            'model': 1, 
            'odometer': 1,
            'image_list': 1,
            'price': 1,
            'grade': 1,
            'vin': 1,
            'mpg': 1,
            'expiration_dt': 1,
            'fuel_type': 1,
            'transmission': 1,
            }).sort(sortby, orderby).skip(skip).limit(pageLength)
        #extract and format data
        json_results = []
        for result in results:
            json_results.append({'id': result['vin'], 'type': 'listings', 'attributes': result})
        

        data_obj = {'data': json_results}
        data_obj['meta'] = {'currentPage' : page, 'perPage' : 12, 'totalPages' : totalPages, 'totalCars': length,}

        return toJson(data_obj)

#1 day = 24hrs * 60min/hr * 60sec/min = 5,184,000 * 1000ms
#currently set to 86.4min = 5184000ms
@application.cache.cached(timeout=5184000, key_prefix="filterables")
@application.route('/api/filterables', methods = ['GET'])
def ListingsDistinct():
    if request.method == 'GET':
        
        i = 0
        #use the same i (don't reset) in order for ids to not clash
        #in Ember Data

        if request.args.get('make'):
            make_params = request.args.get('make')
            rmake = {'$in': spliterize(make_params) }
        else:
            rmake = {'$exists': 'true'}

        if request.args.get('bodyStyle'):
            bodyStyle_params = request.args.get('bodyStyle')
            rbodyStyle = {'$in': spliterize(bodyStyle_params) }
        else:
            rbodyStyle = {'$exists': 'true'}

        if request.args.get('transmission'):
            transmission_params = request.args.get('transmission')
            rtransmission = {'$in': spliterize(transmission_params) }
        else:
            rtransmission = {'$exists': 'true'}

        if request.args.get('car_model'):
            model_params = request.args.get('car_model')
            rmodel = {'$in': spliterize(model_params) }
        else:
            rmodel = {'$exists': 'true'}

        if request.args.get('trim'):
            trim_params = request.args.get('trim')
            rtrim = {'$in': spliterize(trim_params) }
        else:
            rtrim = {'$exists': 'true'}
        
        if request.args.get('color_ext'):
            color_ext_params = request.args.get('color_ext')
            rcolor_ext = {'$in': spliterize(color_ext_params) }
        else:
            rcolor_ext = {'$exists': 'true'}
        
        if request.args.get('color_int'):
            color_int_params = request.args.get('color_int')
            rcolor_int = {'$in': spliterize(color_int_params) }
        else:
            rcolor_int = {'$exists': 'true'}
        
        if request.args.get('year'):
            year_params = request.args.get('year')
            vals = spliterize(year_params)
            #exact year 
            ryear = {'$in': [int(x) for x in vals]}
        else:
            ryear = {'$exists': 'true'}

        if request.args.get('odometer'):
            vals = request.args.get('odometer').split()
            rodometer = {'$lt': int(vals[0]) }
        else:
            rodometer = {'$exists': 'true'}
        
        if request.args.get('price'):
            vals = request.args.get('price').split()
            rprice = {'$lt': int(vals[0])}
        else:
            rprice = {'$exists': 'true'} 

        distinctMakenormal = Listingsdb['Listings'].distinct('make.normal',{'make.normal': rmake, 
            'model.normal': rmodel, 
            'trim.normal': rtrim,
            'color_ext': rcolor_ext, 
            'color_int': rcolor_int, 
            'transmission': rtransmission,
            'year': ryear, 
            'odometer.normal': rodometer, 
            'price.est_price.normal': rprice,
            'categories.body_style': rbodyStyle
            })
        distinctMakepretty = Listingsdb['Listings'].distinct('make.pretty', {'make.normal': rmake, 
            'model.normal': rmodel, 
            'trim.normal': rtrim,
            'color_ext': rcolor_ext, 
            'color_int': rcolor_int, 
            'transmission': rtransmission,
            'year': ryear, 
            'odometer.normal': rodometer, 
            'price.est_price.normal': rprice,
            'categories.body_style': rbodyStyle
            })
        unsorted_make_results = []
        for value, name in zip(distinctMakenormal,distinctMakepretty):
            unsorted_make_results.append({"id":i, "value": value, "name": name, "type": "make"})
            i=i+1
        make_results = sorted(unsorted_make_results, key=lambda k: k['name'])

        print(request.args.get('make'), request.args.get('model'))
        if request.args.get('make'):
            distinctModelnormal = Listingsdb['Listings'].distinct('model.normal',{'make.normal': rmake, 
            'model.normal': rmodel, 
            'trim.normal': rtrim,
            'color_ext': rcolor_ext, 
            'color_int': rcolor_int, 
            'transmission': rtransmission,
            'year': ryear, 
            'odometer.normal': rodometer, 
            'price.est_price.normal': rprice,
            'categories.body_style': rbodyStyle
            })
            distinctModelpretty = Listingsdb['Listings'].distinct('model.pretty',{'make.normal': rmake, 
            'model.normal': rmodel, 
            'trim.normal': rtrim,
            'color_ext': rcolor_ext, 
            'color_int': rcolor_int, 
            'transmission': rtransmission,
            'year': ryear, 
            'odometer.normal': rodometer, 
            'price.est_price.normal': rprice,
            'categories.body_style': rbodyStyle
            })
            unsorted_model_results = []
            for name, value in zip(distinctModelpretty, distinctModelnormal):
                unsorted_model_results.append({"id":i, "value": value, "name": name, "type": "model"})
                i=i+1
            model_results = sorted(unsorted_model_results, key=lambda k: k['name'])
        else:
            model_results = []
        

        if request.args.get('car_model'):
            distinctTrimnormal = Listingsdb['Listings'].distinct('trim.normal', { "trim.normal" : { "$ne" : None }, 'make.normal': rmake, 
            'model.normal': rmodel, 
            'trim.normal': rtrim,
            'color_ext': rcolor_ext, 
            'color_int': rcolor_int, 
            'transmission': rtransmission,
            'year': ryear, 
            'odometer.normal': rodometer, 
            'price.est_price.normal': rprice,
            'categories.body_style': rbodyStyle
            })
            distinctTrimpretty = Listingsdb['Listings'].distinct('trim.pretty', { "trim.normal" : { "$ne" : None }, 'make.normal': rmake, 
            'model.normal': rmodel, 
            'trim.normal': rtrim,
            'color_ext': rcolor_ext, 
            'color_int': rcolor_int, 
            'transmission': rtransmission,
            'year': ryear, 
            'odometer.normal': rodometer, 
            'price.est_price.normal': rprice,
            'categories.body_style': rbodyStyle
            })
            unsorted_trim_results = []
            for name, value in zip(distinctTrimpretty, distinctTrimnormal):
                if(name != None ) or (value != None):
                    unsorted_trim_results.append({"id":i, "value": value, "name": name, "type": "trim"})
                    i=i+1
            trim_results = sorted(unsorted_trim_results, key=lambda k: k['name'])
        else:
            trim_results = []

        distinctTransmission = Listingsdb['Listings'].distinct('transmission', {'make.normal': rmake, 
            'model.normal': rmodel, 
            'trim.normal': rtrim,
            'color_ext': rcolor_ext, 
            'color_int': rcolor_int, 
            'transmission': rtransmission,
            'year': ryear, 
            'odometer.normal': rodometer, 
            'price.est_price.normal': rprice,
            'categories.body_style': rbodyStyle
            })
        unsorted_transmission_results = []
        for result in distinctTransmission:
            if(result != None):
                unsorted_transmission_results.append({"id":i, "name":result, "type": "transmission"})
                i=i+1
        transmission_results = sorted(unsorted_transmission_results, key = lambda k: k['name'])
        

        distinctbodyStyle = Listingsdb['Listings'].distinct('categories.body_style', {'make.normal': rmake, 
            'model.normal': rmodel, 
            'trim.normal': rtrim,
            'color_ext': rcolor_ext, 
            'color_int': rcolor_int, 
            'transmission': rtransmission,
            'year': ryear, 
            'odometer.normal': rodometer, 
            'price.est_price.normal': rprice,
            'categories.body_style': rbodyStyle
            })
        unsorted_bodyStyle_results = []
        for result in distinctbodyStyle:
            if(result != None):
                unsorted_bodyStyle_results.append({"id":i, "name":result, "type": "bodyStyle"})
                i=i+1
        bodyStyle_results = sorted(unsorted_bodyStyle_results, key=lambda k: k['name'])


        distinctextColor = Listingsdb['Listings'].distinct('color_ext', {'make.normal': rmake, 
            'model.normal': rmodel, 
            'trim.normal': rtrim,
            'color_ext': rcolor_ext, 
            'color_int': rcolor_int, 
            'transmission': rtransmission,
            'year': ryear, 
            'odometer.normal': rodometer, 
            'price.est_price.normal': rprice,
            'categories.body_style': rbodyStyle
            })
        unsorted_extColor_results = []
        for result in distinctextColor:
            if(result != None):
                unsorted_extColor_results.append({"id":i, "name":result.lower(), "type": "extColor"})
                i=i+1
        extColor_results = sorted(unsorted_extColor_results, key=lambda k: k['name'])


        distinctintColor = Listingsdb['Listings'].distinct('color_int', {'make.normal': rmake, 
            'model.normal': rmodel, 
            'trim.normal': rtrim,
            'color_ext': rcolor_ext, 
            'color_int': rcolor_int, 
            'transmission': rtransmission,
            'year': ryear, 
            'odometer.normal': rodometer, 
            'price.est_price.normal': rprice,
            'categories.body_style': rbodyStyle
            })
        unsorted_intColor_results = []
        for result in distinctintColor:
            if(result != None):
                unsorted_intColor_results.append({"id":i, "name":result.lower(), "type": "intColor"})
                i=i+1
        intColor_results = sorted(unsorted_intColor_results, key=lambda k: k['name'])
        

        distinctYear = Listingsdb['Listings'].distinct('year', {'make.normal': rmake, 
            'model.normal': rmodel, 
            'trim.normal': rtrim,
            'color_ext': rcolor_ext, 
            'color_int': rcolor_int, 
            'transmission': rtransmission,
            'year': ryear, 
            'odometer.normal': rodometer, 
            'price.est_price.normal': rprice,
            'categories.body_style': rbodyStyle
            })
        unsorted_year_results = []
        for result in distinctYear:
            if(result != None):
                unsorted_year_results.append({"id":i, "value":result, "type": "year"})
                i=i+1
        yearList = sorted(unsorted_year_results, key=lambda k: k['value'])

        distinctOptions = Listingsdb['Listings'].distinct('options_list', {'make.normal': rmake, 
            'model.normal': rmodel, 
            'trim.normal': rtrim,
            'color_ext': rcolor_ext, 
            'color_int': rcolor_int, 
            'transmission': rtransmission,
            'year': ryear, 
            'odometer.normal': rodometer, 
            'price.est_price.normal': rprice,
            'categories.body_style': rbodyStyle
            })
        unsorted_options_results = []
        for result in distinctOptions:
            if(result != None):
                words = result.split(" ")
                rebuilt = "_".join(words)
                unsorted_options_results.append({"id":i, "value":rebuilt, "type": "options"})
                i=i+1
        optionsList = sorted(unsorted_options_results, key=lambda k: k['value'])

        return toJson({'data': {
            'id': 1, 
            'type': 'filterable',
            'attributes': {'make': make_results,
                'models': model_results,
                'trim': trim_results,
                'transmission': transmission_results,
                'body_style': bodyStyle_results,
                'color_ext': extColor_results,
                'color_int': intColor_results,
                'year_list': yearList,
                'options_list': optionsList,
                }}})

if __name__ == '__main__':
  application.run(debug=False)