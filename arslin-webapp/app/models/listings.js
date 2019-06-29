import DS from 'ember-data';

export default DS.Model.extend({
	grade: DS.attr('number'),
	make: DS.attr(),
	model: DS.attr(),
	odometer: DS.attr(),
	mpg: DS.attr(),
	price: DS.attr(),
	imageList: DS.attr(),
	expirationDt: DS.attr(),
	year: DS.attr('number'),
	fuelType: DS.attr('string'),
	vin: DS.attr('string'),
	transmission: DS.attr('string'),
});

