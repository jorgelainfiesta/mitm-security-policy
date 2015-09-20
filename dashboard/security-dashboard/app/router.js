import Ember from 'ember';
import config from './config/environment';

var Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.route('mails', function() {
    this.route('mail', {path: "/:mail_id"});
  });
});

export default Router;
