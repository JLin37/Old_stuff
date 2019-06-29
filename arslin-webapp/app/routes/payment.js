import Ember from 'ember';
import resetScroll from '../mixins/reset-scroll';

export default Ember.Route.extend(resetScroll,{

  model: function(params){    
    return Ember.RSVP.hash({
      listing: this.store.findRecord('listings', params.listing_id, { reload: true }),
      
      payment: this.store.createRecord('payment', { reload: true }),
      
    });
  },

  setupController: function(controller, model) {
    // all your data is in model hash
    controller.set("listing", model.listing);
    controller.set("payment", model.payment);
  },
});