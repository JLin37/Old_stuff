/*jshint node:true*/
/* global require, module */
var EmberApp = require('ember-cli/lib/broccoli/ember-app');


module.exports = function(defaults) {
  var app = new EmberApp(defaults, {
    // Add options here
  });
  // Use `app.import` to add additional libraries to the generated
  // output files.
  //bootstrap
  app.import(app.bowerDirectory + '/bootstrap/dist/css/bootstrap.css');
  app.import(app.bowerDirectory + '/bootstrap/dist/js/bootstrap.js');
  app.import(app.bowerDirectory + '/bootstrap/dist/fonts/glyphicons-halflings-regular.woff', {
    destDir: 'fonts'
  });
  app.import(app.bowerDirectory + '/bootstrap/dist/css/bootstrap.css.map');
  app.import(app.bowerDirectory + '/bootstrap/js/affix.js');
  app.import(app.bowerDirectory + '/bootstrap/js/scrollspy.js');


  app.import(app.bowerDirectory + '/font-awesome/css/font-awesome.min.css');
  app.import(app.bowerDirectory + '/font-awesome/fonts/fontawesome-webfont.woff', {
    destDir: 'fonts'
  });
  app.import(app.bowerDirectory + '/font-awesome/fonts/fontawesome-webfont.woff2', {
    destDir: 'fonts'
  });

  if ((process.env.EMBER_CLI_FASTBOOT !== 'true')) {
    app.import('bower_components//jquery/dist/jquery.js');
  }

  // If you need to use different assets in different
  // environments, specify an object as the first parameter. That
  // object's keys should be the environment name and the values
  // should be the asset to use in that environment.
  //
  // If the library that you are including contains AMD or ES6
  // modules that you would like to import into your application
  // please specify an object with the list of modules as keys
  // along with the exports of each module as its value.

  return app.toTree();
};
