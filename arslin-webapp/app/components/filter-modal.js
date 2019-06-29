import Ember from 'ember';

export default Ember.Component.extend({
	//inject the filter service to allow update
	filters: Ember.inject.service('filters'),

	add(item, type){
		this.get('filters').add(item, type);
	},
	remove(item, type){
		this.get('filters').remove(item, type);
	},

	actions: {
		//newSelection: the subset of the options that is currently selected
		//value: the corresponding value of the checkbox that was checked or unchecked
		//operation: a string describing the operation performed on the selection. 'added' or 'removed'
		updateSelection(type, newSelection, value, operation){
			// console.log(newSelection);
			// console.log(value);
			// console.log(operation);
			if(operation === 'added'){
				this.add(value, type);
			}else if(operation === 'removed'){
				this.remove(value, type);
			}
		},
		clear(type){
			this.get('filters').clear(type);
		},
		odometer(value) {
		    this.set('odometer', value);
		},
		price(value) {
		    this.set('price', value);
		},
		toggleBody() {
	        this.toggleProperty('isShowingBody');
	    },
  }
});