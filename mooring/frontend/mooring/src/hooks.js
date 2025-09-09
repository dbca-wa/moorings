// module for all third party dependencies

import $ from 'jquery'
import DataTable from 'datatables.net';
import DataTableBs from 'datatables.net-bs';
import DataTableRes from 'datatables.net-responsive-bs';
import moment from 'moment/moment.js';
import { extendMoment } from 'moment-range';
import select2 from 'select2';
import awesomplete from 'awesomplete';
import slick from 'slick-carousel-browserify';
import daterangepicker from 'bootstrap-daterangepicker';
import formValidate from './components/utils/validator.js';
var Moment = extendMoment(moment);
import swal from 'sweetalert2';
import api_endpoints from './apps/api.js';
import store from './apps/store';
import helpers from './components/utils/helpers.js';
import { bus } from './components/utils/eventBus.js';

export default {}

export {
    $,
    DataTable,
    DataTableBs,
    DataTableRes,
    Moment,
    api_endpoints,
    helpers,
    bus,
    select2,
    daterangepicker,
    awesomplete,
    formValidate,
    swal,
    store,
    slick
}
