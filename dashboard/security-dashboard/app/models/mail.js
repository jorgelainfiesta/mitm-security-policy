import DS from 'ember-data';

const {attr} = DS;
const {hasMany} = DS;

export default DS.Model.extend({
  datetime: attr("string"),
  sender: attr('string'),
  subject: attr('string'),
  body: attr('string'),
  recipients: hasMany('recipients', {async: true}),
  tags: hasMany('tag', {async: true})
});
