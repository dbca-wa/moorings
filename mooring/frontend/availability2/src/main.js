// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import './foundation-min.scss';
import 'foundation-datepicker/css/foundation-datepicker.css';
import 'font-awesome/css/font-awesome.min.css'


import { createApp } from 'vue';
import availability from './availability';

require('custom-event-polyfill');


// Create and mount the Vue 3 app
const app = createApp(availability);


app.mount('#availability');

