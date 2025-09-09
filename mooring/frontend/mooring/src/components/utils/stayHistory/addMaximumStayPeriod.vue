<template>
<modal ref="modal" :large=true @ok="addMaxStay()" okText="Add">
    <template #header>
        <div class="modal-header">
            <h4 class="modal-title">{{ getTitle }}</h4>
        </div>
    </template>

    <div class="modal-body">
        <form id="addMaxStayForm" class="form-horizontal">
            <alert v-model:show="showError" type="danger">{{errorString}}</alert>

            <div class="row mb-3">
                <label for="stay_maximum" class="col-md-3 col-form-label">Maximum Stay: </label>
                <div class="col-md-4">
                    <input placeholder="Default = 28" id='stay_maximum' v-model="stay.max_days" type='text' class="form-control" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="stay-start-date" class="col-md-3 col-form-label">Period Start:</label>
                <div class="col-md-4">
                    <input
                        id="stay-start-date"
                        name="stay_start"
                        type="date"
                        class="form-control"
                        v-model="stay.range_start"
                        :max="stay.range_end"
                    />
                </div>
            </div>
            <div class="row mb-3">
                <label for="stay-end-date" class="col-md-3 col-form-label">Period End:</label>
                <div class="col-md-4">
                    <input
                        id="stay-end-date"
                        name="stay_end"
                        type="date"
                        class="form-control"
                        v-model="stay.range_end"
                        :min="stay.range_start"
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
import modal from '@/components/utils/bootstrap-modal.vue'
import reason from '@/components/utils/reasons.vue'
import {bus} from '@/components/utils/eventBus.js'
import { $, Moment } from '@/hooks'
import alert from '@/components/utils/alert.vue'
import helpers from '@/components/utils/helpers.js'

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
            my_form: '',
            reasons: [],
            isOpen: false,
            create: true,
        }
    },
    watch: {
        // Deeply watch the 'stay' prop for changes
        stay: {
            handler(newStay) {
                console.log('New stay object:', newStay);
                // Do nothing if the newStay object is null
                if (!newStay) return;

                this.stay.range_start = helpers.convertToYYYYMMDD(newStay.range_start)
                this.stay.range_end = helpers.convertToYYYYMMDD(newStay.range_end)
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
            this.stay.reason = id;
        },
        addMaxStay: function() {
            let vm = this;
            try {
                if ($(vm.my_form).valid() && vm.stay.reason) {
                    vm.stay.range_start = Moment(vm.stay.range_start).format('DD/MM/YYYY');
                    vm.stay.range_end = Moment(vm.stay.range_end).format('DD/MM/YYYY');
                    if (!vm.stay.id){
                        vm.$emit('addCgStayHistory');
                    }else {
                        vm.$emit('updateStayHistory');
                    }
                }
            } catch(e) {
                console.error(e)
            }
        },
        addFormValidations: function() {
            let vm = this;
            $(vm.my_form).validate({
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
        this.$nextTick(() => {
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
            // vm.my_form = document.forms.addMaxStayForm;
            vm.my_form = $('#addMaxStayForm');
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
        })
    }
};
</script>
