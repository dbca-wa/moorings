<template lang="html">
    <div id="bulk-close">
        <modal okText="Close Moorings" @ok="closeCampgrounds" :force="true" :large="true">
            <template #header>
                <div class="modal-header">
                    <h4 class="modal-title">Bulk Close Moorings</h4>
                </div>
            </template>

            <div class="modal-body">
                <form name="closeForm" class="form-horizontal">
                    <div v-if="showErrorClose" class="alert alert-danger" role="alert">
                        {{ errorStringClose }}
                    </div>

                    <div class="row mb-3">
                        <label for="bc-moorings" class="col-md-2 col-form-label">Moorings</label>
                        <div class="col-md-10">
                            <select id="bc-campgrounds" class="form-select" name="campgrounds" multiple v-model="selected_campgrounds">
                                <option v-for="c in campgrounds" :key="c.id" :value="c.id">{{ c.name }}</option>
                            </select>
                        </div>
                    </div>

                    <div class="row mb-3">
                        <label for="closure_start_date" class="col-md-2 col-form-label">Closure start:</label>
                        <div class="col-md-4">
                            <input
                                id="closure_start_date"
                                name="closure_start"
                                v-model="range_start"
                                type="date"
                                class="form-control"
                                :min="minStartDate"
                                :max="range_end ? range_end : null"
                            />
                        </div>
                        <label for="closure_start_time" class="col-md-2 col-form-label">Start time:</label>
                        <div class="col-md-4">
                            <input id="closure_start_time" name="closure_start_time" v-model="range_start_time" type="time" class="form-control" />
                        </div>
                    </div>

                    <div class="row mb-3">
                        <label for="closure_end_date" class="col-md-2 col-form-label">Reopen:</label>
                        <div class="col-md-4">
                            <input
                                id="closure_end_date"
                                name="closure_end"
                                v-model="range_end"
                                type="date"
                                class="form-control"
                                :min="range_start ? range_start : minStartDate"
                            />
                        </div>
                        <label for="closure_end_time" class="col-md-2 col-form-label">Reopen time:</label>
                        <div class="col-md-4">
                            <input id="closure_end_time" name="closure_end_time" v-model="range_end_time" type="time" class="form-control" />
                        </div>
                    </div>

                    <reason type="close" v-model="reason" :wide="true" ></reason>
                    <div v-show="requireDetails" class="row">
                        <div class="form-group">
                            <div class="col-md-2">
                                <label>Details: </label>
                            </div>
                            <div class="col-md-10">
                                <textarea name="closure_details" v-model="details" class="form-control" id="close_cg_details"></textarea>
                            </div>
                        </div>
                    </div>
                </form>
            </div>
        </modal>
    </div>
</template>

<script>
import modal from '../bootstrap-modal.vue'
import reason from '../reasons.vue'
import alert from '../alert.vue'
import { mapGetters } from 'vuex'
import { $, api_endpoints, helpers, bus, Moment } from '../../../hooks'
// import $ from 'jquery';
// import 'select2'

export default {
    name:"bulk-close",
    data:function () {
        let vm =this;
        return {
            isModalOpen:false,
            closeEndPicker:null,
            closeEndTimePicker:null,
            closeStartPicker:null,
            closeStartTimePicker:null,
            reason:'',
            reasons: [],
            range_start:'',
            range_start_time: '',
            range_end:'',
            range_end_time: '',
            close_cg_range_end:'close_cg_range_end'+vm._uid,
            close_cg_range_end_time: 'close_cg_range_end_time'+vm.id,
            close_cg_range_start:'close_cg_range_start'+vm._uid,
            close_cg_range_start_time: 'close_cg_range_start_time'+vm.id,
            selected_campgrounds:[],
            errorStringClose: null,
            form: null,
            details: '',
        }
    },
    computed:{
        showErrorClose: function() {
            var vm = this;
            return vm.errorStringClose != null;
        },
        requireDetails:function () {
            let vm = this;
            var check = this.reason
            for (var i = 0; i < vm.reasons.length; i++){
                if (vm.reasons[i].id == check){
                    return vm.reasons[i].detailRequired;
                }
            }
        },
        minStartDate() {
            const today = new Date();
            // Adjust for timezone offset to prevent off-by-one errors with `toISOString`.
            today.setMinutes(today.getMinutes() - today.getTimezoneOffset());
            return today.toISOString().split('T')[0]; // Returns date in "YYYY-MM-DD" format
        },
        ...mapGetters([
          'campgrounds'
        ]),
    },
    watch: {
        range_start(newStartDate) {
            if (newStartDate && this.range_end && newStartDate > this.range_end) {
                this.range_end = ''; // Reset the end date
            }
        }
    },
    components:{
        modal,
        reason,
        alert
    },
    methods:{
        close:function () {
            this.isModalOpen = this.$parent.showBulkClose  = false;
            this.$parent.$refs.dtGrounds.vmDataTable.ajax.reload();
            this.range_start = "";
            this.range_start_time = "";
            this.range_end = "";
            this.range_end_time = "";
            this.campgrounds = "";
            this.selected_campgrounds = "";
            this.reason = "";
            this.errorStringClose = null;
        },
        events:function () {
            let vm = this;

            vm.addFormValidations();
            vm.fetchCampgrounds();
            vm.initSelectTwo();
        },
        fetchCampgrounds: function() {
            let vm = this;
            if (vm.campgrounds.length == 0) {
                vm.$store.dispatch("fetchCampgrounds");
            }
        },
        initSelectTwo:function () {
            let vm = this;
            setTimeout(function () {
                $('#bc-campgrounds').select2({
                    theme: 'bootstrap-5',
                    allowClear: true,
                    placeholder: "Select Moorings",
                    tags:false,
                }).
                on("select2:select",function (e) {
                    vm.selected_campgrounds = $(e.currentTarget).val();
                }).
                on("select2:unselect",function (e) {
                    vm.selected_campgrounds = $(e.currentTarget).val();
                });
            },100)
        },
        closeCampgrounds:function () {
            let vm =this;

            if (vm.form.valid() && vm.selected_campgrounds.length>0){
                let vm = this;
                let data = {
                    range_start: Moment(vm.range_start).format('DD/MM/YYYY'),
                    range_start_time: vm.range_start_time,
                    range_end: Moment(vm.range_end).format('DD/MM/YYYY'),
                    range_end_time: vm.range_end_time,
                    campgrounds: vm.selected_campgrounds,
                    reason: vm.reason,
                    status:'1'
                }
                if (vm.reason == '1') {
                    data.details = vm.details
                }
                $.ajax({
                    url:api_endpoints.bulk_close,
                    method: 'POST',
                    xhrFields: { withCredentials:true },
                    data: data,
                    headers: {'X-CSRFToken': helpers.getCookie('csrftoken')},
                    dataType: 'json',
                    success: function(data, stat, xhr) {
                        vm.$store.dispatch("updateAlert",{
        					visible:true,
        					type:"success",
        					message: data
		               });
                       vm.close();
                    },
                    error:function (resp){
                        console.log(resp);
                        if(resp.responseJSON[0].includes("is already closed")){
                            vm.errorStringClose = resp.responseJSON[0];
                        } else {
                            vm.$store.dispatch("updateAlert",{
                                visible:true,
                                type:"danger",
                                message: helpers.apiError(resp)
                            });
                            vm.close();
                        }
                    }
                });
            }

        },
        addFormValidations: function() {
            let vm = this;
            vm.form.validate({
                rules: {
                    closure_start: "required",
                    closure_status: "required",
                    open_reason: "required",
                    closure_details: {
                        required: {
                            depends: function(el){
                                var check = this.reason
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
    mounted:function () {
        let vm = this;
        vm.$nextTick(() => {
            vm.form = $(document.forms.closeForm);
            vm.events();
            // bus.$once('closeReasons',setReasons => {
            //     vm.reasons = setReasons;
            // });
            const onDataLoadedOnce = (setReasons) => {
                vm.reasons = setReasons;
                bus.off('closeReasons', onDataLoadedOnce);
            };
            bus.on('closeReasons', onDataLoadedOnce);
        })
    }
}

</script>

<style lang="css">
.body{
    padding:0 20px;
}
.danger-message{
    z-index: 999999;
    background-color: #F2DEDE;
    color: #A94442;
    border-style: solid;
    border-width: 1px;
    border-color: #A94442;
    border-radius: 5px;
    padding: 8px;
    margin-bottom: 10px;
}
</style>
