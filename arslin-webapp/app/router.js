import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.route('home');
  this.route('about');
  this.route('contact');
  this.route('faq');
  this.route('whyus');
  this.route('loading');
  this.route('listings', { path: '/'});
  this.route('listing', { path: 'listings/:listing_id' });
  this.route('payment', { path: 'payment/:listing_id' });

  this.route('protected');
  this.route('operatingRegion');
  this.route('terms');
  this.route('privacy');
  this.route('requestcar');
  this.route('underconstruction');
});

export default Router;
