import DS from 'ember-data';
import ENV from 'security-dashboard/config/environment';

export default DS.RESTAdapter.extend({
  host: ENV.apiUrl,
  buildURL: function(type, id, record){
      return this._super(type, id, record) + '/';
  }
});
