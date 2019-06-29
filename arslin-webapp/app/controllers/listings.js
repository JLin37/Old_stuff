import Ember from 'ember';

export default Ember.Controller.extend({
	filters: Ember.inject.service('filters'),

	queryParams: ['make', 
	'car_model', 
	'color_ext',
	'color_int', 
	'odometer', 
	'price',
	'transmission',
	'bodyStyle', 
	'sorting'],

	make: null,
	car_model: null,
	color_ext: null,
	color_int: null,
	year: null,
	transmission: null,
	bodyStyle: null,
	odometer: null,
	price: null,
	sorting: null,
	//the current page we are on
});
