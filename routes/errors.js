module.exports = function (app) {
    app.use(function (req, res, next) {
        res.status(404);
        res.send('Page is not found!');
    });
    app.use(function (err, req, res, next) {
        console.log(`err at ${req.url} ${err.stack}`);
        res.send('Server error!');
    });
}
