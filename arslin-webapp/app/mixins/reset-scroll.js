import Ember from 'ember';

export default Ember.Mixin.create({
	scrollSelector: window,

	activate: function() {
    	this._super.apply(this, arguments);
    	Ember.$(this.scrollSelector).scrollTop(0);
    },

    deactivate: function() {
	    this._super.apply(this, arguments);
	    this.set('lastScroll',Ember.$(this.scrollSelector).scrollTop());  
	},

	// resetScroll: function(){
	// 	this._super();
	// 	window.scrollTo(0, 0);
	// }.on('activate'),
});
