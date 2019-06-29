import DS from 'ember-data';
import Ember from 'ember';

export default DS.JSONAPISerializer.extend({
  normalizeFindRecordResponse(store, type, payload){
    return {
      data: {
        attributes: {
          colorExt: payload['data']['attributes'].color_ext, 
          colorInt: payload['data']['attributes'].color_int,
          make: payload['data']['attributes'].make,
          priceMax: payload['data']['attributes'].price_max,
          models: payload['data']['attributes'].models,
          odometer: payload['data']['attributes'].odometer,
          trim: payload['data']['attributes'].trim,
          transmission: payload['data']['attributes'].transmission,
          bodyStyle: payload['data']['attributes'].body_style,
          yearList: payload['data']['attributes'].year_list,
          optionsList: payload['data']['attributes'].options_list,
        },
        id: payload['data'].id,
        type: type.modelName,
      }
    };
  },
  keyForAttribute: function(attr){
    return Ember.String.underscore(attr);
  },
});