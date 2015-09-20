import DS from 'ember-data';

const {attr} = DS;
const {hasMany} = DS;

export default DS.Model.extend({
  value: attr('string'),
  description: attr('string'),
  type: attr('string')
});
