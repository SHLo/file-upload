# File-upload
A file server using mongodb gridfs

## Installation
```sh
$ git clone https://github.com/SHLo/file-upload.git
$ cd file-upload
$ npm install
```

## Usage
```sh
$ node index.js [server port]
```
If 'server port' parameter is missed, default server port will be 3000.

0. Edit and check the db config in db-config.js
1. Use browser to access http://localhost:server port
2. Upload local file to server by the form on web page
3. Uploaded files will be keep on the web page which are downloadable by clicking the 'download' links



