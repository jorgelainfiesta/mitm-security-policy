import Ember from 'ember';

export default Ember.Controller.extend({
  actions: {
    toMail(id) {
      this.transitionToRoute('mails.mail', id);
    }
  }
});
