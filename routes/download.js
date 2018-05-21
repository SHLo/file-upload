const fs = require('fs');
var path = require('path');

module.exports = function (app) {
    app.get('/download', function (req, res, next) {
      const files = fs.readdirSync('./downloads').filter(file => path.extname(file) === '.csv').map(file => ({filename: file}));
      console.log(JSON.stringify(files));
      res.json(files);

    });
    app.get('/download/:filename', function (req, res, next) {
        var fileName = req.params.filename;

      /*
        var downloadStream = app.locals.bucket.openDownloadStream(id);
        res.setHeader('Content-disposition', `attachment; filename=${fileName}`);
        downloadStream.on('error', function (err) {
            res.setHeader('Content-disposition', '');
            next(err);
        });
        downloadStream.pipe(res);
        */
      res.download(`downloads/${fileName}`);
    });
}

