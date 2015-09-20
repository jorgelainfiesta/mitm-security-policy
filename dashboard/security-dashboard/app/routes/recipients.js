import Ember from 'ember';

export default Ember.Route.extend({
  model() {
    return Ember.RSVP.hash({
      recipients: this.store.findAll('recipient'),
      tags: this.store.query('tag', {recipient: 'True'})
    });
  }
});
