import DS from 'ember-data';

const {attr} = DS;
const {hasMany} = DS;

export default DS.Model.extend({
  email: attr('number'),
  address: attr('string'),
  tags: hasMany('tag', {async: true})
});
