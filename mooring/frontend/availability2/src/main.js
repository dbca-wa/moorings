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

import './foundation-min.scss';
import 'foundation-datepicker/css/foundation-datepicker.css';
import 'font-awesome/css/font-awesome.min.css'


import { createApp } from 'vue';
import availability from './availability.vue';

import 'custom-event-polyfill';

// Create and mount the Vue 3 app
const app = createApp(availability);

app.mount('#availability');
