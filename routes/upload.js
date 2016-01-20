var upload = require('multer')({dest: 'uploads/'});

module.exports = function (app) {
    app.post('/upload', upload.single('file'), function (req, res, next) {
        if (! req.file) {
            return next(new Error('file is not found!'));
        }
        console.log(require('util').inspect(req.file));

        var uploadStream = app.locals.bucket.openUploadStream(req.file.originalname);
        var readStream = require('fs').createReadStream(req.file.path);
        uploadStream.once('finish', function () {
            res.redirect('/');
        });
        readStream.pipe(uploadStream);
        
    });

}
