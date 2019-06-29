from flask import Flask, jsonify, make_response, request
from bson import json_util
from bson.objectid import ObjectId
from pymongo import MongoClient
import json, requests
from flask.ext.cache import Cache
import sys
import datetime


# Flask
app = Flask(__name__)
#WARNING: Only use 'simple' cache type in development, for production use memcached
app.config['CACHE_TYPE'] = 'simple'
app.cache = Cache(app)


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  response.headers.add('Content-Type', 'application/json')
  return response

@app.errorhandler(404) 
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# MongoDB connection
connection = MongoClient('localhost', 27017)
Listingsdb = connection.activeListings
Salesdb = connection.sales

#takes a composed string (filterables), tokenizes it and returns as an array of strings
#used to split up filter params for db queries
def spliterize(string):
    items = string.split(',')
    normalized = [item for item in items]
    return normalized

def toJson(data):
    return json.dumps(data, sort_keys=True, indent=4, default=json_util.default)

@app.route('/api/sales', methods=['POST'])
def Sale():
    if request.method == 'POST':
        req_json = request.json
        #if values not present, defaults to None
        sale = {"user_id": req_json.get('user_id'),
                "objectid": req_json.get('id'),
                "vin": req_json.get('vin'),
                "make": req_json.get('make'),
                "model": req_json.get('model'),
                "year": req_json.get('year'),
                "link": req_json.get('link'),
                "fname": req_json.get('fname'),
                "lname": req_json.get('lname'),
                "email": req_json.get('email'),
                "phone_number": req_json.get('tel'),
                "city": req_json.get('city'),
                "state": req_json.get('state'),
                "zip": req_json.get('zip'),
                "date": datetime.datetime.utcnow().isoformat(' '), 
                "completed": "false",
                }
        #if successful insertion into DB
        sale_id = Salesdb['testsales'].insert_one(sale).inserted_id

        return toJson(sale)
        
@app.route('/api/listings/<listing_id>', methods=['GET'])
def Listing(listing_id):
    vasturl = "http://autos.vast.com/cars/api/"
    if request.method == 'GET':
        #convert the listing_id from a string back to ObjectId to query Mongo
        result = Listingsdb['Listings'].find_one({'vin': listing_id})
        if result['trim']['pretty'] is None:
            graphresults = {'scatterContent': ''}
        else:
            fullvasturl = vasturl + "year-"+ str(result['year']) +"-"+ str(result['year']) +"/make-"+ result['make']['pretty'] +"/model-"+ result['model']['pretty'] +"/trim-"+ result['trim']['pretty'] +"/location-33173/page-1"
            response = requests.get(fullvasturl)
            vast_doc = response.json()
            arsprice = int(result['price']['est_price']['normal'])
            arsmileage = str(result['odometer']['normal'])
            vastData = [['mileage','price'],['Arslin \n Odometer: ' + arsmileage + ' miles' , arsprice]]
            if not vast_doc['results']:
                vastData = []
            else:
                for item in vast_doc['results']:
                    try:
                        price = int(item['price']['value'])
                        mileage = str(item['mileage'])
                        dealer = item['dealer']['name']
                        vastData.append([dealer +'\n Odometer: '+ mileage +' miles',price])
                    except:
                        continue
            graphresults = {'scatterContent': vastData}
        return toJson({'data': {'id': result['vin'], 'type': 'listing', 'attributes': result, 'scatterContent': graphresults}})


@app.route('/api/listings', methods=['GET'])
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

        if request.args.get('car_model'):
            model_params = request.args.get('car_model')
            rmodel = {'$in': spliterize(model_params) }
        else:
            rmodel = {'$exists': 'true'}
        
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
            ryear = int(vals[0])
        else:
            ryear = {'$exists': 'true'}
        
        if request.args.get('odometer'):
            vals = request.args.get('odometer').split()
            rodometer = {'$lt': int(vals[0]) }
        else:
            rodometer = {'$exists': 'true'}
        
        if request.args.get('price'):
            vals = request.args.get('price').split()
            rprice = {'$lt': vals[0]}
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
            
        if request.args.get('category'):
            if request.args.get('category') == 'uberx':
                rmodel = {'$in': ['prius', 
                    'accord', 
                    '3', 
                    '6', 
                    'camry', 
                    'corolla', 
                    'focus', 
                    'altima', 
                    'civic', 
                    'cruze']}
                ryear = {'$gt': 2008 }
                rodometer = {'$lt': 65000 }
            elif request.args.get('category') == 'uberxl':
                rmodel = {'$in': ['acadia', 
                    'caravan', 
                    'odyssey', 
                    'expedition', 
                    'explorer', 
                    'pilot', 
                    'durango', 
                    'suburban', 
                    'pathfinder', 
                    'highlander',
                    'quest']}
                ryear = {'$gt': 2008 }
                rodometer = {'$lt': 65000 }
            elif request.args.get('category') == 'uberselect':
                rmodel = {'$in': ['a3', 
                    'a4', 'a5',
                    '3-series', 
                    '3-series-gran-turismo', 
                    '4-series', 
                    '4-series-gran-coupe', 
                    'm3', 'x3', 'x4', 'x5',
                    'mark-lt',
                    'mkc', 'mks', 'mkt', 'mkx', 'mkz',
                    'navigator', 
                    'c-class', 
                    'cla-class',
                    'e-class',
                    'clk-class',
                    'ilx', 'mdx', 'rdx', 'rlx', 'tl', 'tlx', 'tsx'
                    'ats', 'cts', 'dts', 'escalade',
                    'deville', 'escalade-esv', 'srx', 'xts',
                    'genesis',
                    'fx', 'fx35', 'fx50', 'g-sedan', 'g35', 'g37',
                    'jx', 'm', 'm35', 'q50', 'q70', 'qx', 'qx56', 
                    'qx60', 'qx70', 'qx80',
                    ]}
                ryear = {'$gt': 2010 }
                rodometer = {'$lt': 50000 }
            elif request.args.get('category') == 'uberblack':
                rmodel = {'$in': ['a6', 
                    'a7', 'a8',
                    '5-series', 
                    '5-series-gran-turismo', 
                    '6-series', 
                    '6-series-gran-coupe',
                    '7-series', 'x6', 
                    'navigator', 
                    's-class', 
                    'e-class',
                    'gl-class',
                    'maybach',
                    'glk-class'
                    'escalade',
                    'panamera',
                    'escalade-esv',
                    'model-s',
                    'xts',
                    'xf', 'xj',
                    'lx', 'qx80', 
                    'yukon-xl',
                    'suburban',
                    ]}
                rcolor_ext = 'black'
                rcolor_int = 'black'
                ryear = {'$gt': 2010 }
                rodometer = {'$lt': 50000 }

        print( rmodel, rmake, rodometer, ryear)
        #build the meta object for pagination
        #length of all car listings, used for number of pages
        #*******CACHE this data in the future *******************
        length = Listingsdb['Listings'].find({'make.normal': rmake,
            'model.normal': rmodel,
            'color_ext': rcolor_ext, 
            'color_int': rcolor_int, 
            'year': ryear, 
            'odometer.normal': rodometer, 
            'price.est_price.normal': rprice
            }).count()
        #probably get from query params - Static??
        pageLength = per_page
        #total pages calculated from length and pagesize
        totalPages = (length/pageLength) + 1
        #use the number of values in this collection to determine which page
        skip = page*pageLength
        

        results = Listingsdb['Listings'].find({'make.normal': rmake, 
            'model.normal': rmodel, 
            'color_ext': rcolor_ext, 
            'color_int': rcolor_int, 
            'year': ryear, 
            'odometer.normal': rodometer, 
            'price.est_price.normal': rprice
            },{'edmundsreview': 0, 'edmunds_review': 0, 'damages_list': 0, 'name': 0, 'tire_dict': 0}).sort(sortby, orderby).skip(skip).limit(pageLength)
        #extract and format data
        json_results = []
        for result in results:
            json_results.append({'id': result['vin'], 'type': 'listing', 'attributes': result})
        

        data_obj = {'data': json_results}
        data_obj['meta'] = {'currentPage' : page, 'perPage' : 12, 'totalPages' : totalPages}

        return toJson(data_obj)


@app.cache.cached(timeout=1000, key_prefix="filterables")
@app.route('/api/filterables/<filter_id>', methods = ['GET'])
def ListingsDistinct(filter_id):
    if request.method == 'GET':
        distinctMake = Listingsdb['Listings'].distinct('make.normal')
        distinctModel = Listingsdb['Listings'].distinct('model.normal')
        distinctTrim = Listingsdb['Listings'].distinct('trim')
        distinctextColor = Listingsdb['Listings'].distinct('color_ext')
        distinctintColor = Listingsdb['Listings'].distinct('color_int')
        maxYear = Listingsdb['Listings'].find({},{'_id': 0, 'year': 1}).sort('year', -1).limit(1)
        minYear = Listingsdb['Listings'].find({},{'_id': 0, 'year': 1}).sort('year', 1).limit(1)
        maxOdometer = Listingsdb['Listings'].find({},{'_id': 0, 'odometer.normal': 1}).sort('odometer.normal', -1).limit(1)
        minOdometer = Listingsdb['Listings'].find({},{'_id': 0, 'odometer.normal': 1}).sort('odometer.normal', 1).limit(1)
        maxPrice = Listingsdb['Listings'].find({},{'_id': 0, 'price.est_price.normal': 1}).sort('price.est_price.normal', -1).limit(1)
        minPrice = Listingsdb['Listings'].find({},{'_id': 0, 'price.est_price.normal': 1}).sort('price.est_price.normal', 1).limit(1)
        maxGrade = Listingsdb['Listings'].find({},{'_id': 0, 'grade': 1}).sort('grade', -1).limit(1)
        minGrade = Listingsdb['Listings'].find({},{'_id': 0, 'grade': 1}).sort('grade', 1).limit(1)

        make_model_links = []
        unsorted_make_results = []
        i = 0
        for result in distinctMake:
            unsorted_make_results.append({"id":i, "name":result.lower(), "type": "make"})
            i=i+1

            models_for_make = Listingsdb['Listings'].distinct('model.normal', {'make.normal': result})
            makes_list = []            
            for model in models_for_make:
                makes_list.append({"id":i, "name":model.lower(), "type": "model"})
                i=i+1
            sorted_makes_list = sorted(makes_list, key=lambda k: k['name'])
            make_model_links.append({'make': result.lower(), 'models' : sorted_makes_list})
        
        make_model_links_results = sorted(make_model_links, key=lambda k: k['make'])
        make_results = sorted(unsorted_make_results, key=lambda k: k['name'])
        
        #use the same i (don't reset) in order for ids to not clash
        #in Ember Data
        unsorted_model_results = []
        for result in distinctModel:
            unsorted_model_results.append({"id":i, "name":result.lower(), "type": "model.normal"})
            i=i+1
        model_results = sorted(unsorted_model_results, key=lambda k: k['name'])
        
        trim_results = []
        for result in distinctTrim:
            trim_results.append(result)
        
        unsorted_extColor_results = []
        for result in distinctextColor:
            if(result != None):
                unsorted_extColor_results.append({"id":i, "name":result.lower(), "type": "extColor"})
                i=i+1
        extColor_results = sorted(unsorted_extColor_results, key=lambda k: k['name'])
        
        intColor_results = []
        for result in distinctintColor:
            intColor_results.append(result)
        
        maxYear_result = []
        for result in maxYear:
            maxYear_result.append(result)
        minYear_result = []
        for result in minYear:
            minYear_result.append(result)
        #generate the yearList from the min and max year values
        yearList = []
        

        minVal = minYear_result[0]['year']
        j = 0
        for i in range(minVal, maxYear_result[0]['year'] + 1):
            yearList.append({'id': j,'value': minVal})
            j = j + 1
            minVal = minVal + 1

        return toJson({'data': {'id': 1, 'type': 'filterable',
                                'attributes': {'make': make_results,
                                               'model': model_results,
                                               'trim': trim_results,
                                               'color_ext': extColor_results,
                                               'color_int': intColor_results,
                                               'year_list': yearList,
                                               'make_model_links': make_model_links_results
                                               }}})

@app.route('/api/ubers', methods=['GET'])
def uberx():
    if request.method == 'GET':
        if request.args.get('page'):
            page = int(request.args.get('page')) 
        else:
            page = 0
        
        if request.args.get('per_page'):
            per_page = int(request.args.get('per_page')) 
        else:
            per_page = 12

        rmake = {'$in':['toyota', 'honda', 'mazda', 'ford', 'nissan', 'chevrolet']}
        rmodel = {'$in': ['prius', 'accord', '3', '6', 'camry', 'corolla', 'focus', 'altima', 'civic', 'cruze']}
        ryear = {'$gt': 2007 }
        rodometer = {'$lt': 80000 }

        length = Listingsdb['Listings'].find({
            'make.normal': rmake,
            'model.normal': rmodel,
            'year': ryear, 
            'odometer.normal': rodometer, 
            }).count()
        print(length)
        #probably get from query params - Static??
        pageLength = per_page
        #total pages calculated from length and pagesize
        totalPages = (length/pageLength) + 1
        #use the number of values in this collection to determine which page
        skip = page*pageLength

        results = Listingsdb['Listings'].find({
            'make.normal': rmake, 
            'model.normal': rmodel,
            'year': ryear, 
            'odometer.normal': rodometer, 
            },{'edmundsreview': 0, 'edmunds_review': 0, 'damages_list': 0, 'name': 0, 'tire_dict': 0}).skip(skip).limit(pageLength)
        #extract and format data
        json_results = []
        for result in results:
            json_results.append({'id': result['vin'], 'type': 'uber', 'attributes': result})
        

        data_obj = {'data': json_results}
        data_obj['meta'] = {'currentPage' : page, 'perPage' : 12, 'totalPages' : totalPages}

        return toJson(data_obj)

if __name__ == '__main__':
  app.run()