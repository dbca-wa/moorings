// The following line loads the standalone build of Vue instead of the runtime-only build,
// so you don't have to do: import Vue from 'vue/dist/vue'
// This is done with the browser options. For the config, see package.json
// import Vue from 'vue'
// if (process.env.VUE_APP_NODE_ENV == "development") {
//     Vue.config.devtools = true;
// }
import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import { $ } from '../hooks'
// window.$ = $;
// window.jquery = $;
// global.$ = $

import alert from '../components/utils/alert.vue';
import store from './store.js';
import { routes } from './routes.js';
import filters from "../components/utils/filters.js";
import { mapGetters } from 'vuex';
import '../hooks-css.js';
import App from './App.vue';

// Define global variables
global.debounce = function (func, wait, immediate) {
    // Returns a function, that, as long as it continues to be invoked, will not
    // be triggered. The function will be called after it stops being called for
    // N milliseconds. If `immediate` is passed, trigger the function on the
    // leading edge, instead of the trailing.
    'use strict';
    var timeout;
    return function () {
        var context = this;
        var args = arguments;
        var later = function () {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    }
};

const router = createRouter({
  history: createWebHistory(),

  routes: routes,
});

if (document.getElementById("menu")) {
  const menuApp = createApp({});
  menuApp.use(router);
  menuApp.mount("#menu");
}

// const app = createApp({
//   computed: {
//     ...mapGetters(["showAlert", "alertType", "alertMessage"]),
//   },
// });
const app = createApp(App);
app.component("alert", alert);
app.use(store);
app.use(router);

app.config.globalProperties.$filters = {
  ...filters,
};

app.mount("#app");
