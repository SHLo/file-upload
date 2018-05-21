var mongodb = require('mongodb');
var MongoClient = mongodb.MongoClient;
var middleware = require('./middleware');
var routes = require('./routes');
var dbConfig = require('./db-config');

    var app = require('express')();

    middleware(app);
    routes(app);

    app.listen(process.argv[2] || 3000);



