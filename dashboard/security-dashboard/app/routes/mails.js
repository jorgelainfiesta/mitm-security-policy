import Ember from 'ember';

export default Ember.Route.extend({
  model() {
    return Ember.RSVP.hash({
      mails: this.store.findAll('mail'),
      tags: this.store.query('tag', {is_mail: 'True'})
    });
  }
});
