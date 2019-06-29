import Ember from 'ember';
//import ApplicationRouteMixin from 'ember-simple-auth/mixins/application-route-mixin';
export default Ember.Route.extend( {

	identifyUser: function() {
	    //check if the current user is 
	    //this.segment.identifyUser(0, {name: 'Cameron Phillips'});
	    //var sesh = this.get('session').get('session');
	    //console.log(sesh.get('content').get('authenticated'));
	    if (this.get('currentUser')) {
	      this.segment.identifyUser(this.get('currentUser.id'), this.get('currentUser'));
	    }else{
	      this.segment.identifyUser(0, { name: 'Cameron Phillips' });
	    }
	  },
	
	actions: {
		click() {
        	Ember.$('.navbar-collapse ul li a:not(.dropdown-toggle)').click(function() {
	        	Ember.$('.navbar-toggle:visible').click();
	    	});
	   	},
    },

    didInsertElement: function(){
    	this._super();
		    // Highlight the top nav as scrolling occurs
	    this.$('.body').scrollspy({
	        target: '.navbar-fixed-top',
	        offset: 51
	    });

	    // Offset for Main Navigation
	    this.$('.navbar-default').affix({
	        offset: {
	            top: 100,
	        }
	    });
	}

	// actions: {
	// 	login () {
	// 	  var lockOptions = {authParams:{scope: 'openid'}};
	// 	  this.get('session').authenticate('simple-auth-authenticator:lock', lockOptions);
	// 	},

	// 	logout () {
	// 	  this.get('session').invalidate();
	// 	}
	// },
});
