import Ember from 'ember';

export default Ember.Controller.extend({
  loading: false,
  actions: {
    toMail(id) {
      this.transitionToRoute('mails.mail', id);
    },
    filter(tag) {
      this.set('loading', true);
      this.store.query('mail', {tags: tag}).then(mails => {
        this.set('loading', false);
        this.set('model.mails', mails);
      });
    }
  }
});
