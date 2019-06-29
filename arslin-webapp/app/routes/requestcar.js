import Ember from 'ember';
import resetScroll from '../mixins/reset-scroll';


export default Ember.Route.extend(resetScroll,{
	setupController(controller, model){
	    this._super(controller, model);
	},

	model: function(){
		return this.store.createRecord('requestcar',{ reload: true });
	},
});