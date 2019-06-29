/* jshint node: true */

module.exports = function(environment) {
  var ENV = {
    modulePrefix: 'arslin-webapp',
    environment: environment,
    baseURL: '/',
    locationType: 'auto',
    EmberENV: {
      FEATURES: {
        // Here you can enable experimental features on an ember canary build
        // e.g. 'with-controller': true

        //necessary for the ember-infinity module to pushObjects
      }
    },

    APP: {
      // Here you can pass flags/options to your application instance
      // when it is created
      API_HOST: "https://www.arslin.com"
    }
  };

  ENV.stripe = {
    publishableKey: 'pk_test_vRYPbLFnk9R5sggXPgX2TtrZ'
  };

  //ember-cli-segment settings
  ENV['segment'] = {
    WRITE_KEY: 'yFh6pQeltilS3geT23byWyeDdz4lfFvl',
    LOG_EVENT_TRACKING: true
  };
  //configure ember-simple-auth
  ENV['ember-simple-auth'] = {
    authorizer: 'simple-auth-authorizer:jwt',
    authenticationRoute: 'listings',
    routeAfterAuthentication: 'user',
    routeIfAlreadyAuthenticated: 'listings'
  }
  //configure auth0 ember-simple-auth module
  ENV['auth0-ember-simple-auth'] = {
    clientID: "xXU62uHqHQo4huY1nqGRNbztNGXxVulK",
    domain: "arslin.auth0.com"
  }

  if (environment === 'development') {
    // ENV.APP.LOG_RESOLVER = true;
    // ENV.APP.LOG_ACTIVE_GENERATION = true;
    // ENV.APP.LOG_TRANSITIONS = true;
    // ENV.APP.LOG_TRANSITIONS_INTERNAL = true;
    // ENV.APP.LOG_VIEW_LOOKUPS = true; // override
    ENV.APP.LOG_TRANSITIONS = true;
    ENV.APP.API_HOST = 'https://www.arslin.com';
  }

  if (environment === 'test') {
    // Testem prefers this...
    ENV.baseURL = '/';
    ENV.locationType = 'none';

    // keep test console output quieter
    ENV.APP.LOG_ACTIVE_GENERATION = false;
    ENV.APP.LOG_VIEW_LOOKUPS = false;

    ENV.APP.rootElement = '#ember-testing';
  }

  if (environment === 'production') {
    ENV.APP.LOG_TRANSITIONS = true;
    ENV.APP.API_HOST = 'https://www.arslin.com';
  }

  // if (!process.env.EMBER_CLI_FASTBOOT) {
  //   var EmberApp = require('ember-cli/lib/broccoli/ember-app');
  //   module.exports = function(defaults) {
  //     var app = new EmberApp(defaults, {
  //       // Add options here
  //     });
  //     // This will only be included in the browser build
  //     app.import(app.bowerDirectory + '/jquery/dist/jquery.js');
  //     app.import(app.bowerDirectory + '/jquery/dist/jquery.min.js');
  //     app.import(app.bowerDirectory + '/jquery/dist/jquery.min.mapss');
  //     return app.toTree();
  //   };
  // }

  //updated security policy for auth0 user management
  ENV.contentSecurityPolicy = {
  'default-src': "https://www.youtube.com/embed/ https://js.stripe.com/v2/channel.html",
  'script-src': "'self' 'unsafe-eval' 'unsafe-inline' https://autos.vast.com/ http://www.google-analytics.com/analytics.js http://www.google-analytics.com/plugins/ua/linkid.js https://js.stripe.com/v2/ https://www.gstatic.com/charts/44/third_party/dygraphs/dygraph-tickers-combined.js https://www.gstatic.com/charts/44/third_party/webfontloader/webfont.js https://www.gstatic.com/charts/44/js/jsapi_compiled_bar_module.js https://www.gstatic.com/charts/44/js/jsapi_compiled_line_module.js https://www.gstatic.com/charts/44/js/jsapi_compiled_scatter_module.js https://www.gstatic.com/charts/44/js/jsapi_compiled_format_module.js https://www.gstatic.com/charts/44/js/jsapi_compiled_default_module.js https://www.gstatic.com/charts/44/js/jsapi_compiled_ui_module.js https://www.gstatic.com/charts/44/js/jsapi_compiled_corechart_module.js http://ajax.googleapis.com http://blueimp.github.io http://cdn.segment.com https://www.gstatic.com/charts/loader.js https://maxcdn.bootstrapcdn.com https://cdn.mxpnl.com  https://cdn.auth0.com arslin.auth0.com https://client.crisp.im https://ajax.googleapis.com https://checkout.stripe.com", // Allow scripts from https://cdn.mxpnl.com 
  'font-src': "'self' http://fonts.gstatic.com data: http://cdn.auth0.com https://cdn.auth0.com https://maxcdn.bootstrapcdn.com https://client.crisp.im", // Allow fonts to be loaded from http://fonts.gstatic.com 
  'connect-src': "'self' https://autos.vast.com/ https://api.mixpanel.com http://localhost:* arslin.auth0.com http://api.segment.io https://www.arslin.com wss://relay-client.crisp.im", // Allow data (ajax/websocket) from api.mixpanel.com and custom-api.local 
  'img-src': "'self' https://images.cdn.manheim.com https://placehold.it http://www.google-analytics.com/collect http://www.google-analytics.com/r/collect https://stats.g.doubleclick.net/r/collect http://services.edmunds-media.com/image-service/media-ed/ximm/ https://client.crisp.im http://blueimp.github.io https://placeholdit.imgix.net",
  'style-src': "'self' 'unsafe-inline' https://www.gstatic.com/charts/44/css/util/util.css https://www.gstatic.com/charts/44/css/core/tooltip.css  http://fonts.googleapis.com https://client.crisp.im https://maxcdn.bootstrapcdn.com http://blueimp.github.io http://ajax.googleapis.com", // Allow inline styles and loaded CSS from http://fonts.googleapis.com  
  'media-src': "'self' https://client.crisp.im"
  //'frame-src': "'self' https://js.stripe.com/v2/channel.html?stripe_xdm_e=http%3A%2F%2Flocalhost%3A4200&stripe_xdm_c=default624758&stripe_xdm_p=1#__stripe_transport__"
  }
  return ENV;
};
