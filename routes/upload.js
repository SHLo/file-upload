var upload = require('multer')({dest: 'uploads/'});
var fs = require('fs');
const { exec } = require('child_process');

module.exports = function (app) {
    app.post('/upload', upload.single('file'), function (req, res, next) {
        if (! req.file) {
            return next(new Error('file is not found!'));
        }
      console.log(require('util').inspect(req.file));
      exec(`python preprocess.py NDAParser ${req.file.path} downloads`, (err, stdout, stderr) => {
  if (err) {
    // node couldn't execute the command
    console.log(`err: ${err}`);
    return;
  }

  // the *entire* stdout and stderr (buffered)
  console.log(`stdout: ${stdout}`);
  console.log(`stderr: ${stderr}`);
  res.redirect('/');
});

        
    });

}
