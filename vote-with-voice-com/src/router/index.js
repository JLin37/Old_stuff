import Vue from 'vue';
import Router from 'vue-router';
import LandingPage from '@/components/LandingPage';
import Privacy from '@/components/Privacy';
import PoliticalAd from '@/components/PoliticalAd';
import ActionPage from '@/components/ActionPage';
import InfoPage from '@/components/InfoPage';
import ContactPage from '@/components/ContactPage';

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'LandingPage',
      component: LandingPage,
    },
    {
      path: '/privacy',
      name: 'Privacy',
      component: Privacy,
    },
    {
      path: '/politicalad',
      name: 'PoliticalAd',
      component: PoliticalAd,
    },
    {
      path: '/action',
      name: 'ActionPage',
      component: ActionPage,
    },
    {
      path: '/info',
      name: 'InfoPage',
      component: InfoPage,
    },
    {
      path: '/contact',
      name: 'ContactPage',
      component: ContactPage,
    },
  ],
});
