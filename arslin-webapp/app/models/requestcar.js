import DS from 'ember-data';
import {
  validator, buildValidations
} from 'ember-cp-validations';

const Validations = buildValidations({
  // year: {
  //   description: 'year',
  //   validators: [
  //     validator('presence', true),
  //     validator('length', {
  //       min: 2,
  //       max: 4
  //     }),
  //     validator('format', { type: 'number' })
  //   ]
  // },
  make: validator('presence', true),
  fullName: validator('presence', true),
  email: {
    validators: [
      validator('presence', true),
      validator('format', { type: 'email' })
    ]
  },
  tel: {
    validators: [
      validator('presence', true),
      validator('format', { type: 'phone' })
    ]
  },
  emailConfirmation: {
    validators: [
      validator('confirmation', {
        on: 'email',
        message: 'Email addresses do not match',
        debounce: 500}),
    ]
  },
  city: validator('presence', true),
  state: validator('presence', true),
  zipCode: {
    validators: [ 
      validator('presence', true),
      validator('length', {
        is: 5
      }),
    ]
  },

});

export default DS.Model.extend(Validations, {
  year: DS.attr('number'),
  make: DS.attr('string'),
  carmodel: DS.attr('string'),
  fullName: DS.attr('string'),
  extColor: DS.attr('string'),
  intColor: DS.attr('string'),
  mileage: DS.attr('string'),
  price: DS.attr('string'),
  email: DS.attr('string'),
  emailConfirmation: DS.attr('string'),
  tel: DS.attr('string'),
  comment: DS.attr('string'),
  city: DS.attr('string'),
  state: DS.attr('string'),
  zipCode: DS.attr('number'),
});
