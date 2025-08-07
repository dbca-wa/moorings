<template id="Close">
<modal :large=true @ok="addClosure()">
    <template #header>
        <div class="modal-header">
            <h4 class="modal-title">{{ title }}</h4>
        </div>
    </template>

    <div class="modal-body">
        <form name="closeForm" class="form-horizontal">
            <alert v-model:show="showError" type="danger">{{errorString}}</alert>

            <div class="row mb-3 align-items-center">
                <!-- Closure Start Date -->
                <div class="col-md-2">
                    <label for="closure-start-date" class="col-form-label">Closure start:</label>
                </div>
                <div class="col-md-4">
                    <div class="input-group">
                        <input 
                            id="closure-start-date"
                            name="closure_start"
                            v-model="statusHistory.range_start" 
                            type="date" 
                            class="form-control" 
                        />
                    </div>
                </div>
                <!-- Start Time -->
                <div class="col-md-2">
                    <label for="closure-start-time" class="col-form-label">Start time:</label>
                </div>
                <div class="col-md-3">
                    <div class="input-group">
                        <input 
                            id="closure-start-time"
                            name="closure_start_time" 
                            v-model="statusHistory.range_start_time" 
                            type="time" 
                            class="form-control" 
                        />
                    </div>
                </div>
            </div>

            <div class="row mb-3 align-items-center">
                <!-- Reopen Date -->
                <div class="col-md-2">
                    <label for="reopen-date" class="col-form-label">Reopen:</label>
                </div>
                <div class="col-md-4">
                    <div class="input-group">
                        <input 
                            id="reopen-date"
                            name="closure_end"
                            v-model="statusHistory.range_end" 
                            type="date" 
                            class="form-control" 
                        />
                    </div>
                </div>
                <!-- End Time -->
                <div class="col-md-2">
                    <label for="reopen-end-time" class="col-form-label">End time:</label>
                </div>
                <div class="col-md-3">
                    <div class="input-group">
                        <input 
                            id="reopen-end-time"
                            name="closure_end_time" 
                            v-model="statusHistory.range_end_time" 
                            type="time" 
                            class="form-control" 
                        />
                    </div>
                </div>
            </div>

            <reason type="close" v-model="statusHistory.closure_reason"></reason>

            <div v-show="requireDetails" class="row align-items-start">
                <div class="col-md-2">
                    <label for="closure-details" class="col-form-label">Details:</label>
                </div>
                <div class="col-md-10">
                    <!-- <textarea name="closure_details" v-model="statusHistory.details" class="form-control" id="close_cg_details"></textarea> -->
                    <textarea 
                        id="closure-details"
                        name="closure_details" 
                        v-model="statusHistory.details" 
                        class="form-control"
                    ></textarea>
                </div>
            </div>
        </form>
    </div>

</modal>
</template>

<script>
import modal from '../bootstrap-modal.vue'
import { $, datetimepicker,api_endpoints, validate, helpers, bus, Moment } from '../../../hooks'
import alert from '../alert.vue'
import reason from '../reasons.vue'
    
export default {
    name: 'Close',
    props: {
        statusHistory: {
            type: Object,
            required: true
        },
        title: {
            type: String,
            required: true
        }
    },
    data: function() {
        let vm = this;
        return {
            id:'',
            current_closure: '',
            // closeStartPicker: '',
            // closeStartTimePicker: '',
            showDetails:false,
            // closeEndPicker: '',
            // closeEndTimePicker: '',
            errors: false,
            errorString: '',
            form: '',
            isOpen: false,
            reasons: [],
            close_cg_range_start: 'close_cg_range_start'+vm._uid,
            close_cg_range_start_time: 'close_cg_range_start_time'+vm.id,
            close_cg_range_end: 'close_cg_range_end'+vm._uid,
            close_cg_range_end_time: 'close_cg_range_end_time'+vm.id,
        }
    },
    watch: {
        statusHistory: {
            handler(newStatusHistory) {
                // Do nothing if the newStatusHistory object is null
                if (!newStatusHistory) return;

                // --- Handle conversion for period_start ---
                const startDate = newStatusHistory.range_start;
                if (startDate && /^\d{2}\/\d{2}\/\d{4}$/.test(startDate)) {
                    let s_date = Moment(startDate, 'DD/MM/YYYY');
                    this.statusHistory.range_start = Moment(s_date).format('YYYY-MM-DD');
                }

                // --- Handle conversion for period_end ---
                const endDate = newStatusHistory.range_end;
                if (endDate && /^\d{2}\/\d{2}\/\d{4}$/.test(endDate)) {
                    let e_date = Moment(endDate, 'DD/MM/YYYY');
                    this.statusHistory.range_end = Moment(e_date).format('YYYY-MM-DD');
                }
            },
            immediate: true, // Run the handler immediately when the component is initialized
            deep: true       // Also detect changes to nested properties of the object
        }
    },
    computed: {
        showError: function() {
            var vm = this;
            return vm.errors;
        },
        isModalOpen: function() {
            return this.isOpen;
        },
        closure_id: function() {
            return this.statusHistory.id ? this.statusHistory.id : '';
        },
        requireDetails: function() {
            let vm = this;
            var check = this.statusHistory.closure_reason
            for (var i = 0; i < vm.reasons.length; i++){
                if (vm.reasons[i].id == check){
                    return vm.reasons[i].detailRequired;
                }
            }
        },
    },
    components: {
        modal,
        alert,
        reason
    },
    methods: {
        close: function() {
            this.errors = false;
            this.errorString = '';
            this.isOpen = false;
            this.statusHistory.id = '';
            this.statusHistory.range_start= '';
            this.statusHistory.range_start_time= '';
            this.statusHistory.range_end= '';
            this.statusHistory.range_end_time= '';
            this.statusHistory.status= '1';
            this.statusHistory.details= '';
            this.statusHistory.reason = '';
            this.statusHistory.closure_reason = '';
            // var today = new Date();
            // this.closeEndPicker.data('DateTimePicker').clear();
            // this.closeStartPicker.data('DateTimePicker').clear();
        },
        addClosure: function() {
            let vm = this;
            if (vm.form.valid()){
                vm.statusHistory.range_start = Moment(vm.statusHistory.range_start).format('DD/MM/YYYY');
                vm.statusHistory.range_end = Moment(vm.statusHistory.range_end).format('DD/MM/YYYY');
                if (!vm.closure_id){
                    vm.$emit('closeRange');
                }else {
                    vm.$emit('updateRange');
                }
            }
        },
        addFormValidations: function() {
            let vm = this;
            vm.form.validate({
                rules: {
                    closure_start: "required",
                    closure_start_time: "required",
                    closure_end: "required",
                    closure_end_time: "required",
                    closure_status: "required",
                    closure_details: {
                        required: {
                            depends: function(el){
                                var check = vm.statusHistory.closure_reason
                                for (var i = 0; i < vm.reasons.length; i++){
                                    if (vm.reasons[i].id == check){
                                        return vm.reasons[i].detailRequired;
                                    }
                                }
                            }
                        }
                    }
                },
                messages: {
                    closure_start: "Enter a start date",
                    closure_start_time: "Enter a start time",
                    closure_end: "Enter a end date",
                    closure_end_time: "Enter a end time",
                    closure_status: "Select a closure reason from the options",
                    closure_details: "Details required if Other reason is selected"
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
        vm.statusHistory.status=1;
        vm.statusHistory.reason='';
        // vm.closeEndPicker = $('#'+vm.close_cg_range_end);
        // vm.closeStartPicker = $('#'+vm.close_cg_range_start).datetimepicker({
        //     format: 'DD/MM/YYYY',
        //     minDate: new Date()
        // });
        // vm.closeStartTimePicker = $('#'+vm.close_cg_range_start_time).datetimepicker({
        //     format: 'HH:mm',
        // });
        // vm.closeEndPicker.datetimepicker({
        //     format: 'DD/MM/YYYY',
        //     useCurrent: false
        // });
        // vm.closeEndTimePicker = $('#'+vm.close_cg_range_end_time).datetimepicker({
        //     format: 'HH:mm',
        // })
        // vm.closeStartPicker.on('dp.change', function(e){
        //     vm.statusHistory.range_start = vm.closeStartPicker.data('DateTimePicker').date() != null ? vm.closeStartPicker.data('DateTimePicker').date().format('DD/MM/YYYY') : '';
        //     e.date != null ? vm.closeEndPicker.data("DateTimePicker").minDate(e.date): '';
        // });
        // vm.closeStartTimePicker.on('dp.change', function(e){
        //     vm.statusHistory.range_start_time = vm.closeStartTimePicker.data('DateTimePicker').date().format('HH:mm');
        // });
        // vm.closeEndPicker.on('dp.change', function(e){
        //     vm.statusHistory.range_end = vm.closeEndPicker.data('DateTimePicker').date() != null  ? vm.closeEndPicker.data('DateTimePicker').date().format('DD/MM/YYYY') : '';
        // });
        // vm.closeEndTimePicker.on('dp.change', function(e){
        //     vm.statusHistory.range_end_time = vm.closeEndTimePicker.data('DateTimePicker').date().format('HH:mm');
        // });
        vm.form = $(document.forms.closeForm);
        vm.addFormValidations();
        // bus.$once('closeReasons',setReasons => {
        //     vm.reasons = setReasons;
        // });
        const onDataLoadedOnce = (setReasons) => {
            vm.reasons = setReasons;
            bus.off('closeReasons', onDataLoadedOnce);
        };
        bus.on('closeReasons', onDataLoadedOnce);
    },
};
</script>
