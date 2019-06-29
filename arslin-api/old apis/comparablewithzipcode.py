@application.route('/api/comparables', methods=['GET'])
def comparableCars():
    vasturl = "http://autos.vast.com/cars/api/"
    if request.method == 'GET':
        if request.args.get('vin'):
            listing_id = request.args.get('vin')
        result = Listingsdb['Listings'].find_one({'vin': listing_id})
        arsprice = int(result['price']['est_price']['normal'])
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
            print(fullvasturl)      
        else:
            graphresults = {'scatterContent': [{'name': 'Mileage',  'colorByPoint': 'true', 'data': vastData}]}
        
        return  toJson({'data': {'id': result['vin'], 
            'type': 'comparable', 
            'scatterContent': graphresults
            }})