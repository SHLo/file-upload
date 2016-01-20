var mongodb = require('mongodb');
var MongoClient = mongodb.MongoClient;
var middleware = require('./middleware');
var routes = require('./routes');
var dbConfig = require('./db-config');

MongoClient.connect(`mongodb://${dbConfig.addr}:${dbConfig.port}/${dbConfig.name}`, function (err, db) {
    if (err) {
        throw err;
    }
    
    var app = require('express')();
    var bucket = new mongodb.GridFSBucket(db, {bucketName: dbConfig.bucketName});
    app.locals.bucket = bucket;

    middleware(app);
    routes(app);

    app.listen(process.argv[2] || 3000);
});



