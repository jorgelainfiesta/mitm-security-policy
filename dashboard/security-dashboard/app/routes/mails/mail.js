import Ember from 'ember';

export default Ember.Route.extend({
  model(params) {
    return this.store.findRecord('mail', params.mail_id);
  }
});
