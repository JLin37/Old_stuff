from flask import Flask, jsonify, make_response, request
from bson import json_util
from bson.objectid import ObjectId
from pymongo import MongoClient
import json
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
    if request.method == 'GET':
        #convert the listing_id from a string back to ObjectId to query Mongo
        result = Listingsdb['oldListings'].find_one({'_id': ObjectId(listing_id)})

        json_results = []
        json_results.append({'id': str(result['_id']), 'type': 'listing', 'attributes': result})
        return toJson({'data': json_results})


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
            rmake = {'$in': request.args.get('make').capitalize().split() }
        else:
            rmake = {'$exists': 'true'}
        
        if request.args.get('car_model'):
            rmodel = {'$in': request.args.get('car_model').upper().split() }
        else:
            rmodel = {'$exists': 'true'}
        
        if request.args.get('color_ext'):
            rcolor_ext = {'$in': request.args.get('color_ext').capitalize().split() }
        else:
            rcolor_ext = {'$exists': 'true'}
        
        if request.args.get('color_int'):
            rcolor_int = {'$in': request.args.get('color_int').split() }
        else:
            rcolor_int = {'$exists': 'true'}
        
        if request.args.get('year'):
            vals = request.args.get('year').split()\
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
            rprice_ws_avg = {'$lt': int(vals[0]) }
        else:
            rprice_ws_avg = {'$exists': 'true'}    

        if request.args.get('sort') == 'yearAsc':
            sortby = 'year'
            orderby = 1
        elif request.args.get('sort') == 'yearDsc':
            sortby = 'year'
            orderby = -1
        elif request.args.get('sort') == 'priceAsc':
            sortby = 'price_ws_avg'
            orderby = 1
        elif request.args.get('sort') == 'priceDsc':
            sortby = 'price_ws_avg'
            orderby = -1
        elif request.args.get('sort') == 'odometerAsc':
            sortby = 'odometer'
            orderby = 1
        elif request.args.get('sort') == 'odometerDsc':
            sortby = 'odometer'
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
            
        #build the meta object for pagination
        #length of all car listings, used for number of pages
        #*******CACHE this data in the future *******************
        length = Listingsdb['oldListings'].find({'make': rmake,
            'model': rmodel,
            'color_ext': rcolor_ext, 
            'color_int': rcolor_int, 
            'year': ryear, 
            'odometer': rodometer, 
            'price_ws_avg': rprice_ws_avg
            }).count()
        #probably get from query params - Static??
        pageLength = per_page
        #total pages calculated from length and pagesize
        totalPages = (length/pageLength) + 1
        #use the number of values in this collection to determine which page
        skip = page*pageLength
        

        results = Listingsdb['oldListings'].find({'make': rmake, 
            'model': rmodel, 
            'color_ext': rcolor_ext, 
            'color_int': rcolor_int, 
            'year': ryear, 
            'odometer': rodometer, 
            'price_ws_avg': rprice_ws_avg
            }).sort(sortby, orderby).skip(skip).limit(pageLength)
        #extract and format data
        json_results = []
        for result in results:
            json_results.append({'id': str(result['_id']), 'type': 'listing', 'attributes': result})
        

        data_obj = {'data': json_results}
        data_obj['meta'] = {'currentPage' : page, 'perPage' : 12, 'totalPages' : totalPages}

        return toJson(data_obj)


@app.cache.cached(timeout=10, key_prefix="filterables")
@app.route('/api/filterables/<filter_id>', methods = ['GET'])
def ListingsDistinct(filter_id):
    if request.method == 'GET':
        distinctMake = Listingsdb['oldListings'].distinct('make')
        distinctModel = Listingsdb['oldListings'].distinct('model')
        distinctTrim = Listingsdb['oldListings'].distinct('trim')
        distinctextColor = Listingsdb['oldListings'].distinct('color_ext')
        distinctintColor = Listingsdb['oldListings'].distinct('color_int')
        maxYear = Listingsdb['oldListings'].find({},{'_id': 0, 'year': 1}).sort('year', -1).limit(1)
        minYear = Listingsdb['oldListings'].find({},{'_id': 0, 'year': 1}).sort('year', 1).limit(1)
        maxOdometer = Listingsdb['oldListings'].find({},{'_id': 0, 'odometer': 1}).sort('odometer', -1).limit(1)
        minOdometer = Listingsdb['Listings'].find({},{'_id': 0, 'odometer': 1}).sort('odometer', 1).limit(1)
        maxPrice = Listingsdb['oldListings'].find({},{'_id': 0, 'price_ws_avg': 1}).sort('price_ws_avg', -1).limit(1)
        minPrice = Listingsdb['oldListings'].find({},{'_id': 0, 'price_ws_avg': 1}).sort('price_ws_avg', 1).limit(1)
        maxGrade = Listingsdb['oldListings'].find({},{'_id': 0, 'grade': 1}).sort('grade', -1).limit(1)
        minGrade = Listingsdb['oldListings'].find({},{'_id': 0, 'grade': 1}).sort('grade', 1).limit(1)

        unsorted_make_results = []
        i = 0
        for result in distinctMake:
            unsorted_make_results.append({"id":i, "name":result.lower(), "type": "make"})
            i=i+1
        make_results = sorted(unsorted_make_results, key=lambda k: k['name'])
        
        #use the same i (don't reset) in order for ids to not clash
        #in Ember Data
        unsorted_model_results = []
        for result in distinctModel:
            unsorted_model_results.append({"id":i, "name":result.lower(), "type": "model"})
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
                                               'year_list': yearList
                                               }}})


@app.route('/api/listings/filters', methods=['POST'])
def listingsFilter():
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':

            Make = request.json['Make']
            if Make == 'null':
                CarMake = {'$exists': 'true'}
            else:
                CarMake = {'$in': Make }

            Model = request.json['Model']
            if Model == 'null':
                CarModel = {'$exists': 'true'}
            else:
                CarModel = {'$in': Model }

            ExtColor = request.json['ExtColor']
            if ExtColor == 'null':
                CarExtColor = {'$exists': 'true'}
            else:
                CarExtColor = {'$in': ExtColor }

            IntColor = request.json['IntColor']
            if IntColor == 'null':
                CarIntColor = {'$exists': 'true'}
            else:
                CarIntColor = {'$in': IntColor }

            yearLow = request.json['yearLow']
            yearHigh = request.json['yearHigh']

            gradeLow = request.json['gradeLow']
            gradeHigh = request.json['gradeHigh']

            priceLow = request.json['priceLow']
            priceHigh = request.json['priceHigh']

            odoLow = int(request.json['odoLow'])
            odoHigh = int(request.json['odoHigh'])

            lim = request.json['limit']
            off = request.json['offset']

            sorts = request.json['sort']
            if sorts == 'year1':
                sortby = 'year'
                orderby = 1
            elif sorts == 'year-1':
                sortby = 'year'
                orderby = -1
            elif sorts == 'make1':
                sortby = 'make'
                orderby = 1
            elif sorts == 'make-1':
                sortby = 'make'
                orderby = -1
            elif sorts == 'price1':
                sortby = 'price_ws_avg'
                orderby = 1
            elif sorts == 'price-1':
                sortby = 'price_ws_avg'
                orderby = -1
            elif sorts == 'odometer1':
                sortby = 'odometer'
                orderby = 1
            elif sorts == 'odometer-1':
                sortby = 'odometer'
                orderby = -1
            else:
                sortby = '$natural'
                orderby = 1

            filter_query = {'$and': [{'make': CarMake},
                            {'model': CarModel},
                            {'color_ext': CarExtColor},
                            {'color_int': CarIntColor},
                            {'year': {'$gte': yearLow}},{'year':{'$lte': yearHigh}},
                            {'grade': {'$gte': gradeLow}},{'grade':{'$lte': gradeHigh}},
                            {'price_ws_avg': {'$gte': priceLow}},{'price_ws_avg':{'$lte': priceHigh}},
                            {'odometer': {'$gte': odoLow}},{'odometer':{'$lte': odoHigh}}
                            ]}

            distinctMake = Listingsdb['Listings'].distinct('make', filter_query)
            distinctModel = Listingsdb['Listings'].distinct('model', filter_query)
            distinctTrim = Listingsdb['Listings'].distinct('trim', filter_query)
            distinctextColor = Listingsdb['Listings'].distinct('color_ext', filter_query)
            distinctintColor = Listingsdb['Listings'].distinct('color_int', filter_query)
            maxYear = Listingsdb['Listings'].find(filter_query,{'_id': 0, 'year': 1}).sort('year', -1).limit(1)
            minYear = Listingsdb['Listings'].find(filter_query,{'_id': 0, 'year': 1}).sort('year', 1).limit(1)
            maxOdometer = Listingsdb['Listings'].find(filter_query,{'_id': 0, 'odometer': 1}).sort('odometer', -1).limit(1)
            minOdometer = Listingsdb['Listings'].find(filter_query,{'_id': 0, 'odometer': 1}).sort('odometer', 1).limit(1)
            maxPrice = Listingsdb['Listings'].find(filter_query,{'_id': 0, 'price_ws_avg': 1}).sort('price_ws_avg', -1).limit(1)
            minPrice = Listingsdb['Listings'].find(filter_query,{'_id': 0, 'price_ws_avg': 1}).sort('price_ws_avg', 1).limit(1)
            maxGrade = Listingsdb['Listings'].find(filter_query,{'_id': 0, 'grade': 1}).sort('grade', -1).limit(1)
            minGrade = Listingsdb['Listings'].find(filter_query,{'_id': 0, 'grade': 1}).sort('grade', 1).limit(1)
            filteredlistings = Listingsdb['Listings'].find(filter_query,{'_id': 1, 'year': 1, 'make': 1, 'model': 1,
                                    'trim': 1, 'dt_sale': 1, 'odometer': 1, 'color_ext': 1,
                                    'color_int': 1, 'price_ws_avg': 1, 'grade': 1,
                                    'transmission': 1}).sort(sortby, orderby).skip(off).limit(lim)
            json_results = []
            make_results = []
            minGrade_result = []
            model_results = []
            trim_results = []
            extColor_results = []
            intColor_results = []
            maxYear_results = []
            minYear_result = []
            maxOdometer_results = []
            minOdometer_result = []
            maxPrice_results = []
            minPrice_result = []
            maxGrade_results = []

            i = 1
            for result in filteredlistings:
                json_results.append({'id': i, 'type': 'listing', 'attributes' : result})
                i=i+1
            for make in distinctMake:
                make_results.append(make)
            for result in distinctModel:
                model_results.append(result)
            for result in distinctTrim:
                trim_results.append(result)
            for result in distinctextColor:
                extColor_results.append(result)
            for result in distinctintColor:
                intColor_results.append(result)
            for result in maxYear:
                maxYear_results.append(result)
            for result in minYear:
                minYear_result.append(result)
            for result in maxOdometer:
                maxOdometer_results.append(result)
            for result in minOdometer:
                minOdometer_result.append(result)
            for result in maxPrice:
                maxPrice_results.append(result)
            for result in minPrice:
                minPrice_result.append(result)
            for result in maxGrade:
                maxGrade_results.append(result)
            for result in minGrade:
                minGrade_result.append(result)

            return toJson({'data': json_results, 'Distinct Values': {'Available Makes': make_results,
                                               'Available Models': model_results,
                                               'Available Trim': trim_results,
                                               'Available Ext Color': extColor_results,
                                               'Available Int Color': intColor_results,
                                               'Max Year': maxYear_results,
                                               'Min Year': minYear_result,
                                               'Max Odometer': maxOdometer_results,
                                               'Min Odometer': minOdometer_result,
                                               'Max Price': maxPrice_results,
                                               'Min Price': minPrice_result,
                                               'Max Grade': maxGrade_results,
                                               'Min Grade': minGrade_result}})


if __name__ == '__main__':
  app.run(debug=True)