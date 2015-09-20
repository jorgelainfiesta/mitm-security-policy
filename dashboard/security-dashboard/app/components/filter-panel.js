import Ember from 'ember';
import PaperToolbar from 'ember-paper/components/paper-sidenav';

const {observer} = Ember;

export default PaperToolbar.extend({
  classNames: ["md-sidenav-left","md-whiteframe-z2","app-navigation"],
  lockedOpen: "gt-sm",
  _changed: observer("selectedValue", function() {
      if(this.get('selectedValue')) {
        this.sendAction('filter', this.get('selectedValue'));
      }
  }),
  actions: {
    transitionTo(route) {
      this.sendAction("transitionTo", route);
    }
  }
});
