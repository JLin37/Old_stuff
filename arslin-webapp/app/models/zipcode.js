import DS from 'ember-data';
import {
  validator, buildValidations
} from 'ember-cp-validations';

const Validations = buildValidations({
  zipcode: {
    validators: [ 
      validator('presence', true),
      validator('length', {
        is: 5
      }),
    ]
  },

});

export default DS.Model.extend(Validations, {
  zipcode: DS.attr('number'),
});
