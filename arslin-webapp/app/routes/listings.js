import Ember from 'ember';
import InfinityRoute from 'ember-infinity/mixins/route';
import rememberScroll from '../mixins/remember-scroll';

export default Ember.Route.extend(InfinityRoute,rememberScroll,{
  //used by ember-infinity JSON contract for pagination
  //perPageParam: "per",              // instead of "per_page"
  pageParam: "page",                  // instead of "page"
  totalPagesParam: "meta.totalPages",    // instead of "meta.total_pages"

  make: '',
  car_model: '',
  trim: '',
  color_ext: '',
  color_int: '',
  odometer: '',
  price: '',
  year: '',
  transmission: '',
  bodyStyle: '',
  sorting: '',
  category: '',

  // afterInfinityModel(model) {
  //   console.log(model.get('meta'));
  //},
  

  queryParams: {
    make:{
      refreshModel: true
    },
    color_ext: {
      refreshModel: true
    },
    color_int: {
      refreshModel: true
    },
    car_model:{
      refreshModel: true
    },
    trim:{
      refreshModel: true
    },
    odometer:{
      refreshModel: true
    },
    price: {
      refreshModel: true
    },
    year: {
      refreshModel: true
    },
    transmission: {
      refreshModel: true
    },
    bodyStyle: {
      refreshModel: true
    },
    sorting: {
      refreshModel: true
    },
    category: {
      refreshModel: true
    }
  },

  model(params){
    //extract parameters set by the listings controller, and
    //update route properties used by ember-infinity
    this.set('make', params.make);
    this.set('color_ext', params.color_ext);
    this.set('color_int', params.color_int);
    this.set('car_model', params.car_model);
    this.set('trim', params.trim);
    this.set('odometer', params.odometer);
    this.set('price', params.price);
    this.set('year', params.year);
    this.set('transmission', params.transmission);
    this.set('bodyStyle', params.bodyStyle);
    this.set('sorting', params.sorting);
    this.set('category', params.category);

    return Ember.RSVP.hash({
      filterable: this.store.queryRecord('filterable', { 
        make: params.make, 
        color_ext: params.color_ext, 
        color_int: params.color_int, 
        car_model: params.car_model,
        trim: params.trim, 
        odometer: params.odometer, 
        price: params.price, 
        year: params.year,
        transmission: params.transmission, 
        bodyStyle: params.bodyStyle,
      }),

      listings: this.infinityModel('listings', { 
        perPage: 12, 
        startingPage: 0,
        modelPath: 'controller.listings'},
       { 
        make: "make", 
        color_ext: "color_ext", 
        color_int: "color_int", 
        car_model: "car_model",
        trim: "trim", 
        odometer: "odometer", 
        price: "price", 
        year: "year",
        transmission: 'transmission', 
        bodyStyle: 'bodyStyle',
        sort: "sorting",
        category: "category"
      }),

      freeshipping: this.store.createRecord('freeshipping', { reload: true }),
    });
  },

  setupController(controller, model) {
    controller.set('listings', model.listings);
    controller.set('filterable', model.filterable);
    controller.set('totalcars', model.listings.get('meta.totalCars'));
    controller.set('freeshipping', model.freeshipping);
  },
});