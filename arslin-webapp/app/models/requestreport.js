import DS from 'ember-data';
import {
  validator, buildValidations
}
from 'ember-cp-validations';

const Validations = buildValidations({
  fullName: validator('presence', true),
  email: {
    validators: [
      validator('presence', true),
      validator('format', { type: 'email' })
    ]
  },
  // tel: {
  //   validators: [
  //     validator('presence', true),
  //     validator('format', { type: 'phone' })
  //   ]
  // },
  emailConfirmation: {
    validators: [
      validator('confirmation', {
        on: 'email',
        message: 'Email addresses do not match',
        debounce: 500}),
    ]
  },
});

export default DS.Model.extend(Validations, {
  fullName: DS.attr('string'),
  email: DS.attr('string'),
  // tel: DS.attr('string'),
  comment: DS.attr('string'),
});
