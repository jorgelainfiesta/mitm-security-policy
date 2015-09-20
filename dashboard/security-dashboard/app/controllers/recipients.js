import Ember from 'ember';

export default Ember.Controller.extend({
  actions: {
    toRecipient(id) {
      this.transitionToRoute('recipients.recipient', id);
    },
    filter(tag) {
      this.store.query('recipient', {tag: tag}).then(recipients => {
        this.set('model.recipients', recipients);
      });
    }
  }
});
