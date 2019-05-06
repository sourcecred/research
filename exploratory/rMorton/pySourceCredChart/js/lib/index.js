// Export widget models and views, and the npm package version number.
__webpack_public_path__ = document.querySelector('body').getAttribute('data-base-url') + 'nbextensions/pySourceCredChart/';

module.exports = require('./pySourceCredChart.js');
module.exports['version'] = require('../package.json').version;
