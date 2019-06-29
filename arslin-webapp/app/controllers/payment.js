import Ember from 'ember';

export default Ember.Controller.extend({
  showAlert: false,
  isRegistered: false,
  didValidate: false,

  actions: {
    submit(payment, listing) {
      var bod = { 
            vin: listing.get('vin'), 
            make: listing.get('make.pretty'), 
            model: listing.get('model.pretty'), 
            year: listing.get('year'), 
            fullName: payment.get('fullName'),
            email: payment.get('email'),
            tel: payment.get('tel'),
            comment: payment.get('comment'),
            city: payment.get('city'),
            state: payment.get('state'),
            zipCode: payment.get('zipCode'),
      };
      payment.validate().then(({
        payment,
        validations
      }) => {
        if (validations.get('isValid')){
          
          //Always explicitly resolve ajax promises.
          var _this = this;
          var host = this.store.adapterFor('application').get('host');
          new Ember.RSVP.Promise(function(resolve, reject){
            Ember.$.ajax({
              type: "POST",
              url: host + "/api/sales",
              data: JSON.stringify(bod),
              contentType: "application/json",
              dataType: "json",
              success: function(data){
                _this._super();
                if (Ember.$(window).width() < 756) {
                  window.scrollTo(0,1000);
                } else {
                  window.scrollTo(0,200);
                }
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
          if (Ember.$(window).width() < 756) {
            window.scrollTo(0,1000);
          } else {
            window.scrollTo(0,200);
          }
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
