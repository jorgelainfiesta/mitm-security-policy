import Ember from 'ember';

export default Ember.Controller.extend({
  loading: false,
  actions: {
    toRecipient(id) {
      this.transitionToRoute('recipients.recipient', id);
    },
    filter(tag) {
      this.set('loading', true);
      this.store.query('recipient', {tags: tag}).then(recipients => {
        this.set('loading', false);
        this.set('model.recipients', recipients);
      });
    }
  }
});
