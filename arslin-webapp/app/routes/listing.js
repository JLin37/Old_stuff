import Ember from 'ember';
import resetScroll from '../mixins/reset-scroll';

export default Ember.Route.extend(resetScroll,{
  setupController(controller, model){
    this._super(controller, model);
  },

  zipCode: '',

  queryParams: {
    zipCode:{
      refreshModel: true
    },
  },

  model: function(params){
    this.set('vin', params.vin);
    this.set('zipCode', params.zipCode);

    return Ember.RSVP.hash({
      listing: this.store.findRecord('listing', params.listing_id, {zipcode: params.zipCode}),
      comparable: this.store.queryRecord('comparable', {vin: params.listing_id, zipcode: params.zipCode}),
      similar: this.store.query('similar', {vin: params.listing_id}),
      requestreport: this.store.createRecord('requestreport', { reload: true }),
      zipcode: this.store.createRecord('zipcode', {reload: true}),
      freeshipping: this.store.createRecord('freeshipping', { reload: true }),
    });
  },
});