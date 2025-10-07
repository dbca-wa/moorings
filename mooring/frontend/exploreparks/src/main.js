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

import 'ol/ol.css';
import 'awesomplete/awesomplete.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

import { createApp } from 'vue';
import ParkFinder from './parkfinder.vue';

// 1. Find the element to mount the Vue application on
const mountElement = document.querySelector('#parkfinder');

// 2. Check if the element actually exists on the page
if (mountElement) {
  // 3. Get the data from the element's `data-*` attributes.
  // The `dataset` property converts kebab-case (data-source-url) to camelCase (sourceUrl).
  const dataSourceUrl = mountElement.dataset.sourceUrl;

  // 4. Create the Vue app, passing the retrieved data as the second argument (initial props).
  const app = createApp(ParkFinder, {
    // This object will be passed as props to the ParkFinder component.
    // The key here (`dataSourceUrl`) must match the prop name defined in ParkFinder.vue.
    dataSourceUrl: dataSourceUrl
  });
  
  // 5. Mount the application
  app.mount('#parkfinder');
} else {
  // It's good practice to log an error if the mount point is not found.
  console.error('Failed to find the mount element #parkfinder for the Vue application.');
}