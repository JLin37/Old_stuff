import Ember from 'ember';

export default Ember.Service.extend({
  //arrays, store raw filter query values
  make: null,
  car_model: null,
  trim: null,
  color_ext: null,
  color_int: null,
  year: null,
  transmission: null,
  bodyStyle: null,
  odometer: null,
  price: null,
  sorting: null,
  search_param: null,

  init(){
    this._super(...arguments);
    this.set('make', []);
    this.set('car_model', []);
    this.set('trim', []);
    this.set('color_ext', []);
    this.set('color_int', []);
    this.set('year', []);
    this.set('transmission', []);
    this.set('bodyStyle', []);
    this.set('odometer', []);
    this.set('price', []);
    this.set('sorting', []);
  },

  //computed query parameters 
  query_make: Ember.computed('make.@each', function(){
    let params =  this.get('make');
    if (params.length === 0){
      return "";
    }
    return params.reduce(function(previousValue, currentValue){
      return currentValue + ',' + previousValue;
    });
  }),
  query_model: Ember.computed('car_model.@each', function(){
    let params =  this.get('car_model');
    if (params.length === 0){
      return "";
    }
    return params.reduce(function(previousValue, currentValue){
      return currentValue + ',' + previousValue;
    });
  }),
  query_trim: Ember.computed('trim.@each', function(){
    let params =  this.get('trim');
    if (params.length === 0){
      return "";
    }
    return params.reduce(function(previousValue, currentValue){
      return currentValue + ',' + previousValue;
    });
  }),
  query_color_ext: Ember.computed('color_ext.@each', function(){
    let params =  this.get('color_ext');
    if (params.length === 0){
      return "";
    }
    return params.reduce(function(previousValue, currentValue){
      return currentValue + ',' + previousValue;
    });
  }),
  query_color_int: Ember.computed('color_int.@each', function(){
    let params =  this.get('color_int');
    if (params.length === 0){
      return "";
    }
    return params.reduce(function(previousValue, currentValue){
      return currentValue + ',' + previousValue;
    });
  }),
  query_year: Ember.computed('year.@each', function(){

    let params =  this.get('year');
    if (params.length === 0){
      return "";
    }
    return params.reduce(function(previousValue, currentValue){
      return currentValue + ',' + previousValue;
    });
  }),
  query_transmission: Ember.computed('transmission.@each', function(){
    let params =  this.get('transmission');
    if (params.length === 0){
      return "";
    }
    return params.reduce(function(previousValue, currentValue){
      return currentValue + ',' + previousValue;
    });
  }),
  query_bodyStyle: Ember.computed('bodyStyle.@each', function(){
    let params =  this.get('bodyStyle');
    if (params.length === 0){
      return "";
    }
    return params.reduce(function(previousValue, currentValue){
      return currentValue + ',' + previousValue;
    });
  }),
  query_odometer: Ember.computed('odometer', function(){

    let params =  this.get('odometer');
    if (params.length === 0){
      return "";
    }
    return params;
  }),
  query_price: Ember.computed('price', function(){

    let params =  this.get('price');
    if (params.length === 0){
      return "";
    }
    return params;
  }),

  add(item, type){
    if(type === "make"){
      this.get('make').pushObject(item);
      console.log(this.get('make'));
    }
    else if(type === "model"){
      this.get('car_model').pushObject(item);
      console.log(this.get('car_model'));
    }
    else if(type === "trim"){
      this.get('trim').pushObject(item);
      console.log(this.get('trim'));
    }
    else if(type === "extColor"){
      this.get('color_ext').pushObject(item);    
      console.log(this.get('color_ext'));        
    }
    else if(type === "intColor"){
      this.get('color_int').pushObject(item);    
      console.log(this.get('color_int'));        
    }
    else if(type === "year"){
      this.get('year').pushObject(item);      
      console.log(this.get('year'));
    }
    else if(type === "odometer"){
      this.get('odometer').pushObject(item);   
      console.log(this.get('odometer'));         
    }
    else if(type === "price"){
      this.get('price').pushObject(item);   
      console.log(this.get('price'));         
    }
    else if(type === "transmission"){
      this.get('transmission').pushObject(item);
      console.log(this.get('transmission'));
    }
    else if(type === "bodyStyle"){
      this.get('bodyStyle').pushObject(item);
      console.log(this.get('bodyStyle'));
    }
  },
  remove(item, type){
    if(type === "make"){
      this.get('make').removeObject(item);
    }
    else if(type === "model"){
      this.get('car_model').removeObject(item);
    }
    else if(type === "trim"){
      this.get('trim').removeObject(item);
    }
    else if(type === "extColor"){
      this.get('color_ext').removeObject(item);      
    }
    else if(type === "intColor"){
      this.get('color_int').removeObject(item);      
    }
    else if(type === "year"){
      this.get('year').removeObject(item);      
    }
    else if(type === "odometer"){
      this.get('odometer').removeObject(item);      
    }
    else if(type === "price"){
      this.get('price').removeObject(item);      
    }
    else if(type === "transmission"){
      this.get('transmission').removeObject(item);      
    }
    else if(type === "bodyStyle"){
      this.get('bodyStyle').removeObject(item);      
    }
  },
  clear(type){
    if(type === "make"){
      this.get('make').setObjects([]);
    }
    else if(type === "model"){
      this.get('car_model').setObjects([]);
    }
    else if(type === "trim"){
      this.get('trim').setObjects([]);
    }
    else if(type === "extColor"){
      this.get('color_ext').setObjects([]);
    }
    else if(type === "intColor"){
      this.get('color_int').setObjects([]);
    }
    else if(type === "year"){
      this.get('year').setObjects([]);
    }
    else if(type === "odometer"){
      this.get('odometer').setObjects([]);
    }
    else if(type === "price"){
      this.get('price').setObjects([]);
    }
    else if(type === "transmission"){
      this.get('transmission').setObjects([]);
    }
    else if(type === "bodyStyle"){
      this.get('bodyStyle').setObjects([]);
    }
    //if no type is defined, clear all
    else if(type === "" || type === null){
      this.get('make').setObjects([]);
      this.get('car_model').setObjects([]);
      this.get('trim').setObjects([]);
      this.get('color_ext').setObjects([]);
      this.get('color_int').setObjects([]);
      this.get('year').setObjects([]);
      this.get('odometer').setObjects([]);
      this.get('price').setObjects([]);
      this.get('transmission').setObjects([]);
      this.get('bodyStyle').setObjects([]);
    }

  }

});
