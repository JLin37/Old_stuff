import Ember from 'ember';

export default Ember.Component.extend({
	actions:{
	    loadMore: function(){
			this.sendAction('loadMore');
			//return true;
	    }
    }
});
