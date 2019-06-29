import DS from 'ember-data';
import Ember from 'ember';


export default DS.JSONAPISerializer.extend({  
  normalizeQueryRecordResponse(store, type, payload){
    return {
      data: {
        id: payload['data'].id,
        type: type.modelName,
        attributes: {
          scatterContent: payload['data']['attributes'].scatterContent,
        },
      }
    };
  },

  keyForAttribute: function(attr){
    return Ember.String.underscore(attr);
  },
});