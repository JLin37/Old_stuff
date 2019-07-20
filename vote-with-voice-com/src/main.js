// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import * as VueGoogleMaps from 'vue2-google-maps';

import App from './App';
import router from './router';

Vue.config.productionTip = false;

/* eslint-disable no-new */

Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyD1pQJRJjwt7jfReAABRf2S9UJJ0tZTjes',
    libraries: 'places',
  },
});

new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
});
