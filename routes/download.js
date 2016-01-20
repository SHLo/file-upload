module.exports = function (app) {
    app.get('/download', function (req, res, next) {
        app.locals.bucket.find({}).toArray(function (err, files) {
            res.json(files);
        });   
    });
    app.get('/download/:id/:filename', function (req, res, next) {
        var id = require('mongodb').ObjectID(req.params.id);

        var fileName = req.params.filename;

        var downloadStream = app.locals.bucket.openDownloadStream(id);
        res.setHeader('Content-disposition', `attachment; filename=${fileName}`);
        downloadStream.on('error', function (err) {
            res.setHeader('Content-disposition', '');
            next(err);
        });
        downloadStream.pipe(res);
    });
}

