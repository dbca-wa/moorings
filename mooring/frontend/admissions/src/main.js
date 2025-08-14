import 'vite/modulepreload-polyfill';
// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

import $ from 'jquery';
import moment from 'moment';
import swal from 'sweetalert2';

window.$ = $;
window.jQuery = $;
window.moment = moment;
window.swal = swal;

import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import admissions from './admissions.vue';
import costs from './costs.vue';
import App from './App.vue';
import alert from './utils/alert.vue';
import store from './utils/store';
import { mapGetters } from 'vuex';
import './hooks-css.js';
console.log('main loaded');
console.log(costs);
const routes = [
    {
        path: '/admissions/:loc/',
        component: admissions, 
    },
    {
        path: '/admissions-cost/',
        component: costs,
    }
];

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});


if (document.getElementById("menu")) {
  const menuApp = createApp({});
  menuApp.use(router);
  menuApp.mount("#menu");
}

const app = createApp(App);
app.use(store);
app.use(router);

app.mount('#appdiv');
