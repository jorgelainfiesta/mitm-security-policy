import DS from 'ember-data';

const {attr} = DS;
const {hasMany} = DS;
const {belongsTo} = DS;

export default DS.Model.extend({
  email: belongsTo('mail', {async: true}),
  address: attr('string'),
  tags: hasMany('tag', {async: true})
});
