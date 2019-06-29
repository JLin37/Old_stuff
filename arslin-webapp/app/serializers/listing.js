import DS from 'ember-data';
import Ember from 'ember';

export default DS.JSONAPISerializer.extend({  
  normalizeFindRecordResponse(store, type, payload){
    return {
      data: {
        id: payload['data'].id,
        type: type.modelName,
        attributes: {
          colorExt: payload['data']['attributes'].color_ext, 
          colorInt: payload['data']['attributes'].color_int,
          grade: payload['data']['attributes'].grade,
          make: payload['data']['attributes'].make,
          model: payload['data']['attributes'].model,
          odometer: payload['data']['attributes'].odometer,
          optionsList: payload['data']['attributes'].options_list,
          trim: payload['data']['attributes'].trim,
          interiorList: payload['data']['attributes'].interior_list,
          categories: payload['data']['attributes'].categories,
          warrantyBasicMiles: payload['data']['attributes'].warranty_basic_miles,
          warrantyPowertrainMiles: payload['data']['attributes'].warranty_powertrain_miles,
          damagesList: payload['data']['attributes'].damages_list,
          mpg: payload['data']['attributes'].mpg,
          price: payload['data']['attributes'].price,
          warrantyBasicYears: payload['data']['attributes'].warranty_basic_years,
          interiorOdor: payload['data']['attributes'].interior_odor,
          drivenWheels: payload['data']['attributes'].driven_wheels,
          imageList: payload['data']['attributes'].image_list,
          mechanicalList: payload['data']['attributes'].mechanical_list,
          name: payload['data']['attributes'].name,
          expirationDt: payload['data']['attributes'].expiration_dt,
          warrantyPowertrainYears: payload['data']['attributes'].warranty_powertrain_years,
          numOfDoors: payload['data']['attributes'].num_of_doors,
          year: payload['data']['attributes'].year,
          fuelType: payload['data']['attributes'].fuel_type,
          vin: payload['data']['attributes'].vin,
          keyList: payload['data']['attributes'].key_list,
          engine: payload['data']['attributes'].engine,
          tireDict: payload['data']['attributes'].tire_dict,
          transmission: payload['data']['attributes'].transmission,
          edmundsReview: payload['data']['attributes'].edmundsreview,
          //scatterContent: payload['data']['scatterContent'].scatterContent,
        },
        //extract mongoid and use as ember-data id
        //oid is used for individual listing GET call
      }
    };
  },

  keyForAttribute: function(attr){
    return Ember.String.underscore(attr);
  },
});