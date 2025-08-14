// module for all third party dependencies

import $ from 'jquery'
import DataTable from 'datatables.net';
import DataTableBs from 'datatables.net-bs';
import DataTableRes from 'datatables.net-responsive-bs';
// import bootstrap from 'bootstrap';
import moment from 'moment/moment.js';
import { extendMoment } from 'moment-range';
// import datetimepicker from 'eonasdan-bootstrap-datetimepicker';
import validate from 'jquery-validation';
import slick from 'slick-carousel-browserify';
import select2 from 'select2';
import awesomplete from 'awesomplete';
import daterangepicker from 'bootstrap-daterangepicker';
// var formValidate = require('./utils/validator.js';
var Moment = extendMoment(moment);
import swal from 'sweetalert2';
import api_endpoints from './api.js';
import store from './utils/store';
import helpers from './utils/helpers.js';
import {bus} from './utils/eventBus.js';

export default {}
export {
    $,
    DataTable,
    DataTableBs,
    DataTableRes,
    Moment,
    // datetimepicker,
    api_endpoints,
    helpers,
    validate,
    bus,
    slick,
    select2,
    daterangepicker,
    awesomplete,
    swal,
    store
}
