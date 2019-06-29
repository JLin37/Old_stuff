import Ember from 'ember';

export default Ember.Component.extend({
  store: Ember.inject.service(),

  showAlert: false,
  isRegistered: false,
  didValidate: false,

	actions: {

    submit(freeshipping) {
      var bod = { 
            fullName: freeshipping.get('fullName'),
            email: freeshipping.get('email'),
            tel: freeshipping.get('tel'),
            zipCode: freeshipping.get('zipCode'),
      };
      freeshipping.validate().then(({
        freeshipping,
        validations
      }) => {
        if (validations.get('isValid')){
          //Always explicitly resolve ajax promises.
          var _this = this;
          var host = this.get('store').adapterFor('application').get('host');
          new Ember.RSVP.Promise(function(resolve, reject){
            Ember.$.ajax({
              type: "POST",
              url: host + "/api/freeshipping",
              data: JSON.stringify(bod),
              contentType: "application/json",
              dataType: "json",
              success: function(data){
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