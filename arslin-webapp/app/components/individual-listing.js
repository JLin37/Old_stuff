import Ember from 'ember';

export default Ember.Component.extend({
  store: Ember.inject.service(),

  showAlert: false,
  isRegistered: false,
  didValidate: false,

	actions: {
	  mainGallery: function() {
	    this.get('mainGallery').init();
	  },

    damageGallery: function() {
      this.get('damageGallery').init();
    },

    submit(listing) {
      var requestreport = this.get('requestreport');
      var bod = { 
            vin: listing.get('vin'), 
            make: listing.get('make.pretty'), 
            model: listing.get('model.pretty'), 
            year: listing.get('year'), 
            fullName: requestreport.get('fullName'),
            email: requestreport.get('email'),
            tel: requestreport.get('tel'),
      };
      requestreport.validate().then(({
        requestreport,
        validations
      }) => {
        if (validations.get('isValid')){
          //Always explicitly resolve ajax promises.
          var _this = this;
          var host = this.get('store').adapterFor('application').get('host');
          new Ember.RSVP.Promise(function(resolve, reject){
            Ember.$.ajax({
              type: "POST",
              url: host + "/api/reportrequest",
              data: JSON.stringify(bod),
              contentType: "application/json",
              dataType: "json",
              success: function(data){
                _this._super();
                if (Ember.$(window).width() < 756) {
                  window.scrollTo(0,650);
                } else {
                  window.scrollTo(0,900);
                }
                resolve(data);
                _this.setProperties({
                    showAlert: false,
                    isRegistered: true,
                });
              },
              error: function(request, textStatus, error){
                reject(error);
                return alert("Request Error. Please Try again later or Contact us directly.");
              }
            });
          });
        } else {
          this.set('showAlert', true);
          this._super();
          window.scrollTo(0,900);
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
    },
  }
});