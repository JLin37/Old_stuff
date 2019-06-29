import DS from 'ember-data';
import Ember from 'ember';


export default DS.JSONAPISerializer.extend({  
  normalizeFindRecordResponse(store, type, payload){
    return {
      data: {
        id: payload['data'].id,
        type: type.modelName,
        attributes: {
          grade: payload['data']['attributes'].grade,
          make: payload['data']['attributes'].make,
          model: payload['data']['attributes'].model,
          odometer: payload['data']['attributes'].odometer,
          mpg: payload['data']['attributes'].mpg,
          price: payload['data']['attributes'].price,
          imageList: payload['data']['attributes'].image_list,
          expirationDt: payload['data']['attributes'].expiration_dt,
          year: payload['data']['attributes'].year,
          fuelType: payload['data']['attributes'].fuel_type,
          vin: payload['data']['attributes'].vin,
          transmission: payload['data']['attributes'].transmission,
        },
      }
    };
  },

  keyForAttribute: function(attr){
    return Ember.String.underscore(attr);
  },
});