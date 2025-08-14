<template id="ParkPriceHistoryDetail">
<bootstrapModal :large=true @ok="addHistory()" @cancel="close()" @close="close()">
    <template #header>
        <div class="modal-header">
            <h4 class="modal-title">Add Price History</h4>
        </div>
    </template>

    <div class="modal-body" style="overflow:visible;">
        <form name="priceForm" class="form-horizontal" style="overflow:visible;">
			<alert v-model:show="showError" type="danger">{{errorString}}</alert>
            <!-- <div class="row" style="overflow:visible;">
                <div class="form-group" style="overflow:visible;">
                    <div class="col-md-2">
                        <label for="period_start">Period start: </label>
                    </div>
                    <div class="col-md-4">
                        <input type="date" 
                            id="period_start" 
                            class="form-control" 
                            v-model="priceHistory.period_start">
                    </div>
                    <div class="col-md-2" style="display:none;">
                        <label for="period_end">Period end: </label>
                    </div>
                    <div class="col-md-4" style="display:none;">
                        <input type="date" 
                            id="period_end"
                            name="period_end"
                            class="form-control" 
                            v-model="priceHistory.period_end">
                    </div>
                </div>
            </div> -->
            <div class="row">
                <!-- Period start -->
                <div class="col-md-6 mb-3">
                    <label for="period_start" class="form-label">Period start:</label>
                    <input 
                        type="date" 
                        id="period_start" 
                        class="form-control" 
                        v-model="priceHistory.period_start"
                    >
                </div>
                <!-- Period end (hidden) -->
                <div class="col-md-6 mb-3 d-none">
                    <label for="period_end" class="form-label">Period end:</label>
                    <input 
                        type="date" 
                        id="period_end"
                        name="period_end"
                        class="form-control" 
                        v-model="priceHistory.period_end"
                    >
                </div>
            </div>
            <!-- <div class="row">
                <div class="form-group">
                    <div class="col-md-2">
                        <label>Adult Cost Day: </label>
                    </div>
                    <div class="col-md-4">
                        <input name="adult_cost"  v-model="priceHistory.adult_cost" type='number' class="form-control" />
                    </div>
                    <div class="col-md-2">
                        <label>Adult Cost Overnight: </label>
                    </div>
                    <div class="col-md-4">
                        <input name="adult_overnight_cost"  v-model="priceHistory.adult_overnight_cost" type='number' class="form-control" />
                    </div>
                </div>
            </div> -->
            <div class="row">
                <!-- Adult Cost Day -->
                <div class="col-md-6 mb-3">
                    <label for="adultCostDay" class="form-label">Adult Cost Day:</label>
                    <input 
                        id="adultCostDay"
                        name="adult_cost"
                        v-model="priceHistory.adult_cost"
                        type="number" 
                        class="form-control" 
                    />
                </div>
                <!-- Adult Cost Overnight -->
                <div class="col-md-6 mb-3">
                    <label for="adultCostOvernight" class="form-label">Adult Cost Overnight:</label>
                    <input 
                        id="adultCostOvernight"
                        name="adult_overnight_cost"
                        v-model="priceHistory.adult_overnight_cost"
                        type="number" 
                        class="form-control"
                    />
                </div>
            </div>

            <!-- <div class="row">
                <div class="form-group">
                    <div class="col-md-2">
                        <label>Child Cost Day: </label>
                    </div>
                    <div class="col-md-4">
                        <input name="child_cost"  v-model="priceHistory.children_cost" type='number' class="form-control" />
                    </div>
                    <div class="col-md-2">
                        <label>Child Cost Overnight: </label>
                    </div>
                    <div class="col-md-4">
                        <input name="child_overnight_cost"  v-model="priceHistory.children_overnight_cost" type='number' class="form-control" />
                    </div>
                </div>
            </div> -->

            <div class="row">
                <!-- Child Cost Day -->
                <div class="col-md-6 mb-3">
                    <label for="childCostDay" class="form-label">Child Cost Day:</label>
                    <input 
                        id="childCostDay"
                        name="child_cost"
                        v-model="priceHistory.children_cost"
                        type="number"
                        class="form-control" 
                    />
                </div>
                <!-- Child Cost Overnight -->
                <div class="col-md-6 mb-3">
                    <label for="childCostOvernight" class="form-label">Child Cost Overnight:</label>
                    <input 
                        id="childCostOvernight"
                        name="child_overnight_cost"
                        v-model="priceHistory.children_overnight_cost"
                        type="number"
                        class="form-control"
                    />
                </div>
            </div>

            <!-- <div class="row">
                <div class="form-group">
                    <div class="col-md-2">
                        <label>Infant Cost Day: </label>
                    </div>
                    <div class="col-md-4">
                        <input name="infant_cost"  v-model="priceHistory.infant_cost" type='number' class="form-control" />
                    </div>
                    <div class="col-md-2">
                        <label>Infant Cost Overnight: </label>
                    </div>
                    <div class="col-md-4">
                        <input name="infant_overnight_cost"  v-model="priceHistory.infant_overnight_cost" type='number' class="form-control" />
                    </div>
                </div>
            </div> -->
            <div class="row">
                <!-- Infant Cost Day -->
                <div class="col-md-6 mb-3">
                    <label for="infantCostDay" class="form-label">Infant Cost Day:</label>
                    <input 
                        id="infantCostDay"
                        name="infant_cost"
                        v-model="priceHistory.infant_cost"
                        type="number"
                        class="form-control" 
                    />
                </div>

                <!-- Infant Cost Overnight -->
                <div class="col-md-6 mb-3">
                    <label for="infantCostOvernight" class="form-label">Infant Cost Overnight:</label>
                    <input 
                        id="infantCostOvernight"
                        name="infant_overnight_cost"
                        v-model="priceHistory.infant_overnight_cost"
                        type="number"
                        class="form-control"
                    />
                </div>
            </div>

            <!-- <div class="row">
                <div class="form-group">
                    <div class="col-md-2">
                        <label>Family Cost Day: </label>
                    </div>
                    <div class="col-md-4">
                        <input name="family_cost"  v-model="priceHistory.family_cost" type='number' class="form-control" />
                    </div>
                    <div class="col-md-2">
                        <label>Family Cost Overnight: </label>
                    </div>
                    <div class="col-md-4">
                        <input name="family_overnight_cost"  v-model="priceHistory.family_overnight_cost" type='number' class="form-control" />
                    </div>
                </div>
            </div> -->
            <div class="row">
                <!-- Family Cost Day -->
                <div class="col-md-6 mb-3">
                    <label for="familyCostDay" class="form-label">Family Cost Day:</label>
                    <input 
                        id="familyCostDay"
                        name="family_cost"
                        v-model="priceHistory.family_cost"
                        type="number"
                        class="form-control" 
                    />
                </div>
                <!-- Family Cost Overnight -->
                <div class="col-md-6 mb-3">
                    <label for="familyCostOvernight" class="form-label">Family Cost Overnight:</label>
                    <input 
                        id="familyCostOvernight"
                        name="family_overnight_cost"
                        v-model="priceHistory.family_overnight_cost"
                        type="number"
                        class="form-control"
                    />
                </div>
            </div>

            <!-- <div class="row" id="div_mooring_groups">
                <div class="form-group">
                    <div class="col-md-2">
                        <label>Mooring Group (Collecting Agency): </label>
                    </div>
                    <div  class="col-md-4">
                        <select class="form-control" name="mooring_group" v-model="priceHistory.mooring_group">
                            <option value=""></option>
                            <option v-for="mg in mooring_groups" :value="mg.id">{{mg.name}}</option>
                        </select>
                    </div>
                </div>
            </div> -->
            <div class="row" id="div_mooring_groups">
                <div class="col-md-6 mb-3">
                    <label for="mooringGroup" class="form-label">Mooring Group (Collecting Agency):</label>
                    <select 
                        id="mooringGroup"
                        name="mooring_group"
                        class="form-select"
                        v-model="priceHistory.mooring_group"
                    >
                        <option value=""></option>
                        <option 
                            v-for="mg in mooring_groups" 
                            :key="mg.id" 
                            :value="mg.id"
                        >
                            {{ mg.name }}
                        </option>
                    </select>
                </div>
            </div>

            <!-- <reason type="price" @blur="validateReason()" v-model="priceHistory.reason" ></reason> -->
            <div class="mb-3">
                <reason 
                    type="price" 
                    @blur="validateReason()" 
                    v-model="priceHistory.reason"
                ></reason>
            </div>

            <!-- <div v-show="requireDetails" class="row">
                <div class="form-group">
                    <div class="col-md-2">
                        <label>Comment: </label>
                    </div>
                    <div class="col-md-5">
                        <textarea name="comments" @blur="validateReason()" v-model="priceHistory.comments" class="form-control"></textarea>
                    </div>
                </div>
            </div> -->
            <div v-show="requireDetails" class="row">
                <div class="col-12 mb-3">
                    <label for="priceComments" class="form-label">Comment:</label>
                    <textarea 
                        id="priceComments"
                        name="comments"
                        @blur="validateReason()" 
                        v-model="priceHistory.comments" 
                        class="form-control"
                    ></textarea>
                </div>
            </div>
        </form>
    </div>

</bootstrapModal>
</template>

<script>
import JQuery from 'jquery'
window.jQuery = JQuery
window.$ = JQuery
// import 'foundation-sites';
// import 'foundation-datepicker/js/foundation-datepicker';

import moment from 'moment'
import bootstrapModal from '../utils/bootstrap-modal.vue'
import reason from '../utils/reasons.vue'
import { api_endpoints, validate, helpers, bus } from '../hooks'
import alert from '../utils/alert.vue'
import { Tooltip } from 'bootstrap';
import { nextTick } from 'vue';

export default {
    name: 'ParkPriceHistoryDetail',
    props: {
        priceHistory: {
            type: Object,
            required: true,
        },
    },
    data: function() {
        let vm = this;
        return {
            id:'',
            title: '',
            current_closure: '',
            closeStartPicker: '',
            arrivalData: '',
            showDetails: false,
            closeEndPicker: '',
            errors: false,
            errorString: '',
            form: '',
            reasons: [],
            isOpen: false,
            mooring_groups: [],
            tooltipInstances: null
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
            return this.priceHistory.id ? this.priceHistory.id : '';
        },
        requireDetails: function() {
            let vm = this;
            var check = this.priceHistory.reason
            for (var i = 0; i < vm.reasons.length; i++){
                if (vm.reasons[i].id == check){
                    return vm.reasons[i].detailRequired;
                }
            }
        },
    },
    components: {
        bootstrapModal,
        alert,
        reason
    },
    methods: {
        close: function() {
            delete this.priceHistory.original;
            this.errors = false;
            this.selected_rate = '';
            this.priceHistory.period_start= '';
            this.priceHistory.comments= '';
            this.priceHistory.period_end='';
            this.priceHistory.adult_cost='';
            this.priceHistory.adult_overnight_cost='';
            this.priceHistory.children_cost='';
            this.priceHistory.children_overnight_cost='';
            this.priceHistory.infant_cost='';
            this.priceHistory.infant_overnight_cost='';
            this.priceHistory.family_cost='';
            this.priceHistory.family_overnight_cost='';
            this.priceHistory.reason={id:1};

            this.errorString = '';
            this.isOpen = false;
            // this.$emit("cancel");
        },
        addHistory: function() {
            if(this.validateForm()){
                if ($(this.form).valid()){
                    if (this.priceHistory.id){
                        this.$emit('updateParkPriceHistory');
                    }else {
                        this.$emit('addParkPriceHistory');
                    } 
                }
                
            }
        },
        validateForm: function(){
            var isValid = true;
            isValid = this.validatePeriodStart();
            if(isValid){
                isValid = this.validateReason();
            }
            return isValid;
        },
        validateReason: function(){
            if(!Number.isInteger(parseInt(this.priceHistory.reason))){
                this.errorString = "Please select a reason.";
                this.errors = true;
                return false;
            } else if(this.requireDetails){
                if(!this.priceHistory.comments || this.priceHistory.comments == ""){
                    this.errorString = "Please enter further details to explain the reason.";
                    this.errors = true;
                    return false;
                } else {
                    this.errorString = "";
                    this.errors = false;
                    return true;
                }
            } else {
                this.errorString = "";
                this.errors = false;
                return true;
            }  
        },
        validatePeriodStart: function(){
            if(!this.priceHistory.period_start || this.priceHistory.period_start == "" || this.priceHistory.period_start == undefined){
                this.errorString = "Please select a Period Start date.";
                this.errors = true;
                return false;
            } else {
                this.errorString = "";
                this.errors = false;
                return true;
            }
        },
        addFormValidations: function() {
            let vm = this;
            $(vm.form).validate({
                rules: {
                    period_start: "required",
                    comments: {
                        required: {
                            depends: function(el){
                                var check = vm.priceHistory.reason;
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
                    period_start: "Enter a start date",
                    comments: "Details required if certain reasons are selected"
                },
                showErrors: function(errorMap, errorList) {
                    const { showErrors } = helpers.useFormErrors();
                    showErrors(errorMap, errorList, this.validElements());
                }
            });
       }
    },
    beforeUnmount: function(){
        if (this.tooltipInstances && this.tooltipInstances.length > 0) {
            this.tooltipInstances.forEach(tooltip => tooltip.dispose());
        }
    },
    mounted: function() {
        nextTick(() => {

        var vm = this;
        // $('[data-toggle="tooltip"]').tooltip()
        const tooltipTriggerList = [].slice.call(
            this.$el.querySelectorAll('[data-bs-toggle="tooltip"]')
        );
        const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new Tooltip(tooltipTriggerEl);
        });
        vm.tooltipInstances = tooltipList;

        vm.form = document.forms.priceForm;

        var today = new Date();
        today.setDate(today.getDate()+1);
        var tomorrow = new Date(today);

        var mg = $('#mooring_groups').val();
        vm.mooring_groups = JSON.parse( mg );

        var arrivalEl = $('#period_start');
        var arrivalDate = null;

        vm.addFormValidations();
        // bus.once('reasons',setReasons => {
        //     vm.reasons = setReasons;
        // });
        const onDataLoadedOnce = (setReasons) => {
            vm.reasons = setReasons;
            bus.off('reasons', onDataLoadedOnce);
        };
        bus.on('reasons', onDataLoadedOnce);

        })
    }
};
</script>
<style lang="css" scoped>
</style>
