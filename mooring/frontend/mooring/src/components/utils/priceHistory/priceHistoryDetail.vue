<template id="PriceHistoryDetail">
<modal :large=true @ok="addHistory()" @close="close()">
    <template #header>
        <div class="modal-header">
            <h4 class="modal-title">Add Booking Period</h4>
        </div>
    </template>

    <div class="modal-body">
        <form name="priceForm" class="form-horizontal">
            <alert v-model:show="showError" type="danger">{{errorString}}</alert>

            <div class="row mb-3">
                <label for="booking-period-select" class="col-md-3 col-form-label">Booking Period:</label>
                <div class="col-md-4">
                    <select 
                        id="booking-period-select" 
                        name="period" 
                        v-model="priceHistory.booking_period_id" 
                        class="form-select"
                    >
                        <option 
                            v-for="per in booking_periods" 
                            :value="per.id" 
                            :key="per.id"
                        >
                            {{ per.name }}
                        </option>
                    </select>
                </div>
            </div>

            <div class="row" style="display:none;">
                <div class="form-group">
                    <div class="col-md-2">
                        <label><i class="fa fa-question-circle"data-bs-toggle="tooltip" data-placement="bottom" title="Select a rate to prefill the price fields otherwise use the manual entry"></i>Select Rate: </label>
                    </div>
                    <div class="col-md-4">
                        <select name="rate" v-model="selected_rate" class="form-control">
                            <option value="">Manual Entry</option>
                            <option v-for="r in rates":value="r.id">{{r.name}}</option>
                        </select>
                    </div>
                </div>
            </div>
            <div class="row" style="display:none;">
                <div class="form-group">
                    <div class="col-md-2">
                        <label>Mooring Price: </label>
                    </div>
                    <div class="col-md-4">
                        <input :readonly="selected_rate != ''" name="mooring"  v-model="priceHistory.mooring" type='text' class="form-control" />
                    </div>
                </div>
            </div>
            <div class="row" style='display: none;'>
                <div class="form-group">
                    <div class="col-md-2">
                        <label>Adult Price: </label>
                    </div>
                    <div class="col-md-4">
                        <input :readonly="selected_rate != ''" name="adult"  v-model="priceHistory.adult" type='text' class="form-control" />
                    </div>
                </div>
            </div>
            <div class="row" style='display: none;'>
                <div class="form-group">
                    <div class="col-md-2">
                        <label>Concession Price: </label>
                    </div>
                    <div class="col-md-4">
                        <input :readonly="selected_rate != ''" name="concession"  v-model="priceHistory.concession" type='text' class="form-control" />
                    </div>
                </div>
            </div>
            <div class="row" style='display: none;'>
                <div class="form-group">
                    <div class="col-md-2">
                        <label>Child Price: </label>
                    </div>
                    <div class="col-md-4">
                        <input :readonly="selected_rate != ''" name="child"  v-model="priceHistory.child" type='text' class="form-control" />
                    </div>
                </div>
            </div>
            <div class="row" style='display: none;'>
                <div class="form-group">
                    <div class="col-md-2">
                        <label>Infant Price: </label>
                    </div>
                    <div class="col-md-4">
                        <input :readonly="selected_rate != ''" name="infant"  v-model="priceHistory.infant" type='text' class="form-control" />
                    </div>
                </div>
            </div>

            <div class="row mb-3">
                <label for="period_start" class="col-md-3 col-form-label">Period start: </label>
                <div class="col-md-4">
                    <input
                        id="period_start"
                        name="period_start"
                        type="date"
                        class="form-control"
                        v-model="priceHistory.period_start"
                    />
                </div>
            </div>

            <div class="row mb-3">
                <label for="period-end-date" class="col-md-3 col-form-label">Period end: </label>
                <div class="col-md-4">
                    <input
                        id="period-end-date"
                        name="period_end"
                        type="date"
                        class="form-control"
                        v-model="priceHistory.period_end"
                    />
                </div>
            </div>

            <reason type="price" v-model="priceHistory.reason" :threenine="true"></reason>

            <!-- Details Textarea -->
            <div v-show="requireDetails" class="row mb-3">
                <label for="price-details" class="col-md-3 col-form-label">Details: </label>
                <div class="col-md-9">
                    <textarea 
                        id="price-details" 
                        name="details" 
                        class="form-control" 
                        v-model="priceHistory.details"
                    ></textarea>
                </div>
            </div>

            <!-- Error Message Display Area -->
            <div class="row" v-if="priceHistoryError">
                <div class="offset-md-2 col-md-5">
                    <div class="text-danger fw-bold">
                        {{ priceHistoryError }}
                    </div>
                </div>
            </div>
        </form>
    </div>
</modal>
</template>

<script>
import modal from '../bootstrap-modal.vue'
import reason from '../reasons.vue'
import { $, api_endpoints, helpers, bus, Moment } from '../../../hooks'
import alert from '../alert.vue'
import { mapGetters } from 'vuex'
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

export default {
    name: 'PriceHistoryDetail',
    props: {
        priceHistory: {
            type: Object,
            required: true
        },
    },
    data: function() {
        let vm = this;
        return {
            id:'',
            booking_period_id: '',
            selected_rate: '',
            title: '',
            rates: [],
            current_closure: '',
            closeStartPicker: '',
            showDetails: false,
            closeEndPicker: '',
            errors: false,
            errorString: '',
            form: '',
            reasons: [],
            isOpen: false,
            priceHistoryError: ''
        }
    },
    computed: {
        ...mapGetters([
          'booking_periods'
        ]),
        showError: function() {
            var vm = this;
            return vm.errors;
        },
        isModalOpen: function() {
            return this.isOpen;
        },
        closure_id: function() {
            return this.priceHistory.id ? this.priceHistory.id : '';
        },
        requireDetails: function() {
            // let vm = this;
            // var check = vm.priceHistory.reason;
            // for (var i = 0; i < vm.reasons.length; i++){
            //     if (vm.reasons[i].id == check){
            //         return vm.reasons[i].detailRequired;
            //     }
            // }
            let vm = this;
            return (!vm.priceHistory.reason == '' || !vm.priceHistory.reason == null);
        },
    },
    watch: {
        selected_rate: function() {
            let vm = this;
            if (vm.selected_rate != ''){
                $.each(vm.rates, function(i, rate) {
                    if (rate.id== vm.selected_rate){
                        vm.priceHistory.rate = rate.id;
                        vm.priceHistory.mooring = rate.mooring;
                        vm.priceHistory.adult = rate.adult;
                        vm.priceHistory.concession = rate.concession;
                        vm.priceHistory.child = rate.child;
                        vm.priceHistory.infant = rate.infant;
                        $('#period_start').prop('disabled', true);
                    }
                });
            }
            else {
                delete vm.priceHistory.rate;
                vm.priceHistory.mooring = '0.00';
                vm.priceHistory.adult = '0.00';
                vm.priceHistory.concession = '0.00';
                vm.priceHistory.child = '0.00';
                vm.priceHistory.infant = '0.00';
                $('#period_start').prop('disabled', false);
            }
        },
        priceHistory: {
            handler(newPriceHistory) {
                // Do nothing if the newPriceHistory object is null
                if (!newPriceHistory) return;

                // --- Handle conversion for period_start ---
                const startDate = newPriceHistory.period_start;
                if (startDate && /^\d{2}\/\d{2}\/\d{4}$/.test(startDate)) {
                    let s_date = Moment(startDate, 'DD/MM/YYYY');
                    this.priceHistory.period_start = Moment(s_date).format('YYYY-MM-DD');
                }

                // --- Handle conversion for period_end ---
                const endDate = newPriceHistory.period_end;
                if (endDate && /^\d{2}\/\d{2}\/\d{4}$/.test(endDate)) {
                    let e_date = Moment(endDate, 'DD/MM/YYYY');
                    this.priceHistory.period_end = Moment(e_date).format('YYYY-MM-DD');
                }
            },
            immediate: true, // Run the handler immediately when the component is initialized
            deep: true       // Also detect changes to nested properties of the object
        }
    },
    components: {
        modal,
        alert,
        reason
    },
    methods: {
        close: function() {
            delete this.priceHistory.original;
            this.errors = false;
            this.selected_rate = '';
            this.priceHistory.period_start= '';
            this.priceHistory.details= '';
            this.priceHistory.booking_period_id = '';
            this.priceHistoryError = '';

            this.errorString = '';
            this.isOpen = false;
        },
        addHistory: function() {
            let vm = this;
            if ($(vm.form).valid()){
                vm.priceHistory.period_start = Moment(vm.priceHistory.period_start).format('DD/MM/YYYY');
                vm.priceHistory.period_end = Moment(vm.priceHistory.period_end).format('DD/MM/YYYY');
                if (vm.priceHistory.id || vm.priceHistory.original){
                    vm.$emit('updatePriceHistory');
                }else {
                    vm.$emit('addPriceHistory');
                }
            }
        },
        fetchRates: function() {
            let vm = this;
            $.get(api_endpoints.rates,function(data){
                vm.rates = data;
            });
        },
        addFormValidations: function() {
            let vm = this;
            $(vm.form).validate({
                rules: {
                    // adult: "required",
                    // concession: "required",
                    // child: "required",
                    // infant:"required",
                    booking_period_id:"required",
                    period_start: "required",
                    period_end: "required",
                    details: {
                        required: {
                            depends: function(el){
                                // var check = vm.priceHistory.reason;
                                // for (var i = 0; i < vm.reasons.length; i++){
                                //     if (vm.reasons[i].id == check){
                                //         return vm.reasons[i].detailRequired;
                                //     }
                                // }
                                return (!vm.priceHistory.reason == '' || !vm.priceHistory.reason == null);
                            }
                        }
                    }
                },
                messages: {
                    adult: "Enter an adult rate",
                    concession: "Enter a concession rate",
                    child: "Enter a child rate",
                    infant: "Enter a infant rate",
                    booking_period_id: "Select a booking period",
                    period_start: "Enter a start date",
                    period_end: "Enter a start end",
                    details: "Details required if other reason is selected"
                },
                showErrors: function(errorMap, errorList) {
                    const { showErrors } = helpers.useFormErrors();
                    showErrors(errorMap, errorList, this.validElements());
                }
            });
       }
    },
    mounted: function() {
        var vm = this;
        $('#pricehistory_error').html("");
        vm.$store.dispatch("fetchBookingPeriods");
        // $('[data-bs-toggle="tooltip"]').tooltip()
        [...(document.querySelectorAll('[data-bs-toggle="tooltip"]') || [])].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
        vm.form = document.forms.priceForm;
        // var picker = $(vm.form.period_start).closest('.date');
        // var picker2 = $(vm.form.period_end).closest('.date');
        var today = new Date();
        today.setDate(today.getDate()+1);
        // var tomorrow = new Date(today);

        // picker.datetimepicker({
        //     format: 'DD/MM/YYYY',
        //     useCurrent: false,
        //     minDate: tomorrow
        // });
        // picker2.datetimepicker({
        //     format: 'DD/MM/YYYY',
        //     useCurrent: false,
        //     minDate: tomorrow
        // });

        // picker.on('dp.change', function(e){
        //     vm.priceHistory.period_start = picker.data('DateTimePicker').date().format('DD/MM/YYYY');
        // });
        // picker2.on('dp.change', function(e){
        //     vm.priceHistory.period_end = picker2.data('DateTimePicker').date().format('DD/MM/YYYY');
        // });

        vm.addFormValidations();
        vm.fetchRates();
        // bus.$once('priceReasons',setReasons => {
        //     vm.reasons = setReasons;
        // });
        const onDataLoadedOnce = (setReasons) => {
            vm.reasons = setReasons;
            bus.off('priceReasons', onDataLoadedOnce);
        };
        bus.on('priceReasons', onDataLoadedOnce);
    }
};
</script>
<style lang="css" scoped>
</style>
