// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import './foundation-min.scss';
import 'foundation-datepicker/css/foundation-datepicker.css';
import 'ol/ol.css';
import 'awesomplete/awesomplete.css';

// import Vue from 'vue';
import { createApp } from 'vue';
// import VuePaginate from 'vue-paginate';
import ParkFinder from './parkfinder.vue';

// import 'bootstrap/dist/css/bootstrap.min.css'
// import 'bootstrap'

// require('custom-event-polyfill');
// require('ie-array-find-polyfill');

// Vue.use(VuePaginate);
const app = createApp(ParkFinder)
app.mount('#parkfinder')

// global.parkfinder = app
