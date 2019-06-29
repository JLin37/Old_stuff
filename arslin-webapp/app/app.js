import Ember from 'ember';
import Resolver from './resolver';
import loadInitializers from 'ember-load-initializers';
import config from './config/environment';

let App;

Ember.MODEL_FACTORY_INJECTIONS = true;

App = Ember.Application.extend({
  customEvents: {
    paste: "paste",
    cut: "cut"
  },
  modulePrefix: config.modulePrefix,
  podModulePrefix: config.podModulePrefix,
  Resolver
});

App.LoadingRoute = Ember.Route.extend({
  renderTemplate: function(){
    this.render('application-loading');
  }
});
Ember.RSVP.on('error', function(error) {
  Ember.Logger.assert(true, error);
});

loadInitializers(App, config.modulePrefix);

export default App;
