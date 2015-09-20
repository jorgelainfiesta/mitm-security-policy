import Ember from 'ember';

export default Ember.Controller.extend({
  actions: {
    toMail(id) {
      this.transitionToRoute('mails.mail', id);
    },
    filter(tag) {
      this.store.query('mail', {tag: tag}).then(mails => {
        this.set('model.mail', mails);
      });
    }
  }
});
