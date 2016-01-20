var upload = require('./upload');
var download = require('./download');
var errors = require('./errors');

module.exports = function (app) {
    upload(app);
    download(app);
    errors(app);
};
