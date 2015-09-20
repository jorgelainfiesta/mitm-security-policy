import Ember from 'ember';
import PaperToolbar from 'ember-paper/components/paper-sidenav';

export default PaperToolbar.extend({
  classNames: ["md-sidenav-left","md-whiteframe-z2","app-navigation"],
  lockedOpen: "gt-sm",
  actions: {
    transitionTo(route) {
      this.sendAction("transitionTo", route);
    }
  }
});
