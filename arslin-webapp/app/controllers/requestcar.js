import Ember from 'ember';

export default Ember.Controller.extend({
  showAlert: false,
  isRegistered: false,
  didValidate: false,

  actions: {
    submit(model) {
      model.validate().then(({
        model,
        validations
      }) => {
        if (validations.get('isValid')) {

          //Always explicitly resolve ajax promises.
		  var _this = this;
		  var host = this.store.adapterFor('application').get('host');
		  new Ember.RSVP.Promise(function(resolve, reject){
		    Ember.$.ajax({
		      type: "POST",
		      url: host + "/api/carrequests",
		      data: JSON.stringify(model),
		      contentType: "application/json",
		      dataType: "json",
		      success: function(data){
		        _this._super();
    			window.scrollTo(0,200);
		        //console.log("success: " + data);
		        //set route/controller property to indicate a success in template
		        //disallow any further purchase POSTs
		        resolve(data);
		        _this.setProperties({
		            showAlert: false,
		            isRegistered: true,
		        });
		      },
		      error: function(request, textStatus, error){
		        //console.log("error: " + error);
		        //set route/controller property to indicate a failure in template
            	reject(error);
            	return alert("Request Error. Please Try again later or Contact us directly.");
		      }
		    });
		  });
        } else {
          this.set('showAlert', true);
          this._super();
    	  window.scrollTo(0,200);
        }
        this.set('didValidate', true);
      }, () => {

      });
    },

    dismissAlert() {
      this.set('showAlert', false);
    },

    reset() {
      this.setProperties({
        showAlert: false,
        isRegistered: false,
        didValidate: false,
      });
    }
  }
});