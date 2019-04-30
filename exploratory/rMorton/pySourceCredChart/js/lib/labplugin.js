var pySourceCredChart = require('./index');
var base = require('@jupyter-widgets/base');

module.exports = {
  id: 'pySourceCredChart',
  requires: [base.IJupyterWidgetRegistry],
  activate: function(app, widgets) {
      widgets.registerWidget({
          name: 'pySourceCredChart',
          version: pySourceCredChart.version,
          exports: pySourceCredChart
      });
  },
  autoStart: true
};

