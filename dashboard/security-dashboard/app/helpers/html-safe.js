import Ember from 'ember';

export function htmlSafe(params/*, hash*/) {
  return params[0].htmlSafe();
}

export default Ember.Helper.helper(htmlSafe);
