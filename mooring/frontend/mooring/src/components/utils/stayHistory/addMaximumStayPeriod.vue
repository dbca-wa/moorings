<template id="addMaxStayCS">
<modal ref="modal" :large=true @ok="addMaxStay()" okText="Add">
    <template #header>
        <div class="modal-header">
            <h4 class="modal-title">{{ getTitle }}</h4>
        </div>
    </template>

    <div class="modal-body">
        <form id="addMaxStayForm" class="form-horizontal">
            <alert :show.sync="showError" type="danger">{{errorString}}</alert>

            <div class="row mb-3">
                <label for="stay_maximum" class="col-md-3 col-form-label">Maximum Stay: </label>
                <div class="col-md-4">
                    <input placeholder="Default = 28" id='stay_maximum' v-model="stay.max_days" type='text' class="form-control" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="stay-start-date" class="col-md-3 col-form-label">Period Start: </label>
                <div class="col-md-4">
                    <input
                        id="stay-start-date"
                        name="stay_start"
                        type="date"
                        class="form-control"
                        v-model="stay.range_start"
                    />
                </div>
            </div>
            <div class="row mb-3">
                <label for="stay-end-date" class="col-md-3 col-form-label">Period End: </label>
                <div class="col-md-4">
                    <input
                        id="stay-end-date"
                        name="stay_end"
                        type="date"
                        class="form-control"
                        v-model="stay.range_end"
                    />
                </div>
            </div>
            <reason type="stay" v-model="stay.reason" ref="reason" :threenine="true"></reason>
            <div v-show="requireDetails" class="row">
                <div class="form-group">
                    <div class="col-md-2">
                        <label for="stay_details">Details: </label>
                    </div>
                    <div class="col-md-5">
                        <textarea name="stay_details" v-model="stay.details" class="form-control" id="stay_details"></textarea>
                    </div>
                </div>
            </div>
        </form>
    </div>

</modal>
</template>

<script>
import modal from '../../utils/bootstrap-modal.vue'
import reason from '../../utils/reasons.vue'
import {bus} from '../../utils/eventBus.js'
import { $, datetimepicker,api_endpoints, validate, helpers } from '../../../hooks'
import alert from '../../utils/alert.vue'

export default {
    name: 'addMaxStayCS',
    props: {
        mooringarea: {
            type: Object,
            required: true
        },
        stay: {
            type: Object
        }
    },
    data: function() {
        return {
            // start_picker: '',
            // end_picker: '',
            errors: false,
            errorString: '',
            form: '',
            reasons: [],
            isOpen: false,
            create: true
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
        getTitle: function() {
            return this.create ? 'Add New Maximum Stay Period' : 'Edit Maximum Stay Period';
        },
        requireDetails: function () {
            let vm = this;
            var check = vm.stay.reason;
            for (var i = 0; i < vm.reasons.length; i++){
                if (vm.reasons[i].id == check){
                    return vm.reasons[i].detailRequired;
                }
            }
        }
    },
    components: {
        modal,
        alert,
        reason
    },
    methods: {
        // you must convert the 'YYYY-MM-DD' values before sending.
        formatToDdMmYyyy: function(isoDate){
            console.log('formatToDdMmYyyy called with:', isoDate);
            if (!isoDate || typeof isoDate !== 'string') return null;
            const parts = isoDate.split('-');
            if (parts.length !== 3) return null;
            const [year, month, day] = parts;
            return `${day}/${month}/${year}`;
        },
        close: function() {
            this.stay.max_days= '';
            this.stay.range_start = '';
            this.stay.range_end = '';
            this.stay.reason = '';
            this.stay.details = '';

            this.isOpen = false;
            this.errors = false;
            this.errorString = '';
            this.status = '';
        },
        updateReason:function (id) {
            console.log('updateReason called with id:', id);
            this.stay.reason = id;
        },
        addMaxStay: function() {
            let vm = this;
            console.log('addMaxStay called');
            if ($(this.form).valid()){
                vm.stay.range_start = vm.formatToDdMmYyyy(vm.stay.range_start);
                vm.stay.range_end = vm.formatToDdMmYyyy(vm.stay.range_end);
                console.log('Formatted Start Date:', vm.stay.range_start);
                console.log('Formatted End Date:', vm.stay.range_end);
                if (!this.stay.id){
                    console.log('Emit addCgStayHistory');
                    this.$emit('addCgStayHistory');
                }else {
                    console.log('Emit updateCgStayHistory');
                    this.$emit('updateStayHistory');
                }
            }
        },
        addFormValidations: function() {
            let vm = this;
            this.form.validate({
                rules: {
                    stay_start: "required",
                    stay_end: "required",
                    stay_reason: "required",
                    stay_details: {
                        required: {
                            depends: function(el){
                                var check = vm.stay.reason;
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
                    stay_start: "Enter a start date",
                    stay_reason: "Select an open reason from the options",
                    open_details: "Details required if Other reason is selected"
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
        if (!vm.create){
            vm.$refs.modal.title = 'Edit Maximum Stay Period';
        }
        // vm.start_picker = $('#stay_start_picker');
        // vm.end_picker = $('#stay_end_picker');
        // vm.start_picker.datetimepicker({
        //     format: 'DD/MM/YYYY'
        // });
        // vm.end_picker.datetimepicker({
        //     format: 'DD/MM/YYYY'
        // });
        // vm.start_picker.on('dp.change', function(e){
        //     vm.stay.range_start = vm.start_picker.data('DateTimePicker').date().format('DD/MM/YYYY');
        // });
        // vm.end_picker.on('dp.change', function(e){
        //     vm.stay.range_end = vm.end_picker.data('DateTimePicker').date().format('DD/MM/YYYY');
        // });
        vm.form = $('#addMaxStayForm');
        vm.addFormValidations();
        // bus.$once('maxStayReasons',setReasons => {
        //     vm.reasons = setReasons;
        // });
        const onDataLoadedOnce = (setReasons) => {
            console.log('onDataLoadedOnce called with:', setReasons);
            vm.reasons = setReasons;
            bus.off('maxStayReasons', onDataLoadedOnce);
        };
        bus.on('maxStayReasons', onDataLoadedOnce);
    }
};
</script>
