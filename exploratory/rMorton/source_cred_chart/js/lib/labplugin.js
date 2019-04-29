var source_cred_chart = require('./index');
var base = require('@jupyter-widgets/base');

module.exports = {
  id: 'source_cred_chart',
  requires: [base.IJupyterWidgetRegistry],
  activate: function(app, widgets) {
      widgets.registerWidget({
          name: 'source_cred_chart',
          version: source_cred_chart.version,
          exports: source_cred_chart
      });
  },
  autoStart: true
};

