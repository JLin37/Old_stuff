import DS from 'ember-data';

export default DS.Model.extend({
	make: DS.attr(),
	models: DS.attr(),
	trim: DS.attr(),
	transmission: DS.attr(),
	bodyStyle: DS.attr(),
	colorExt: DS.attr(),
	colorInt: DS.attr(),
	yearList: DS.attr(),
	optionsList: DS.attr(),
});
