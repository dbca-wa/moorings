import 'vite/modulepreload-polyfill';
// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

import $ from 'jquery';
import moment from 'moment';
import swal from 'sweetalert2';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

window.$ = $;
window.jQuery = $;
window.moment = moment;
window.swal = swal;

import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import admissions from './admissions.vue';
import costs from './costs.vue';
import App from './App.vue';
import store from './utils/store';

// CSSs
import "quill/dist/quill.snow.css";
import "datatables.net-bs/css/dataTables.bootstrap.css";
import "slick-carousel-browserify/slick/slick.css";
import "select2/dist/css/select2.min.css";
import "select2-bootstrap-theme/dist/select2-bootstrap.min.css";
import "bootstrap-daterangepicker/daterangepicker.css";
import "awesomplete/awesomplete.css";
import "sweetalert2/dist/sweetalert2.css";

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
