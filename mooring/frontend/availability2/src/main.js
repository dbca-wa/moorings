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

import 'font-awesome/css/font-awesome.min.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

import { createApp } from 'vue';
import availability from './availability.vue';

import 'custom-event-polyfill';

// Create and mount the Vue 3 app
const app = createApp(availability);

app.mount('#availability');
