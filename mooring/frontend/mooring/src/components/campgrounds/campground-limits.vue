<template lang="html">
    <div id="cg_limits" >
        <div>
            <form id="limitsForm">
                <div class="col-sm-12">
                    <alert v-model:show="showUpdate" type="success" :duration="7000">
                        <p>Mooring successfully updated</p>
                    </alert>
                    <alert v-model:show="showError" type="danger">
                        <p>{{errorString}}</p>
                    </alert>
                    <div class="row align-items-center mb-3">
                        <div class="col-md-3">
                            <label class="control-label" >Maximum Vessel Size (Meters)</label>
                        </div>
                        <div class="col-md-1">
                            <input type="number" name="vessel_size_limit" id="vessel_size_limit" class="form-control form-control-input" v-model="campground.vessel_size_limit" @blur="validateSize()"required/>
                        </div>
                    </div>
                    <div class="row align-items-center mb-3">
                        <div class="col-md-3">
                            <label class="control-label" >Maximum Vessel Draft (Meters)</label>
                        </div>
                        <div class="col-md-1">
                            <input type="number" name="vessel_draft_limit" id="vessel_draft_limit" class="form-control form-control-input" v-model="campground.vessel_draft_limit" @blur="validateDraft()" required/>
                        </div>
                    </div>
                    <div class="row align-items-center mb-3">
                        <template v-if="campground.mooring_physical_type == 1 || campground.mooring_physical_type == 2">
                            <div class="col-md-3">
                                <label class="control-label" >Maximum Vessel Beam (Meters)</label>
                            </div>
                            <div class="col-md-1">
                                <input type="number" name="vessel_beam_limit" id="vessel_beam_limit" class="form-control form-control-input" v-model="campground.vessel_beam_limit" @blur="validateBeamWeight()" required/>
                            </div>
                        </template>
                        <template v-else>
                            <div class="col-md-3">
                                <label class="control-label" >Maximum Vessel Weight (Tonnes)</label>
                            </div>
                            <div class="col-md-1">
                                <input type="number" name="vessel_weight_limit" id="vessel_weight_limit" style="margin-top:10px;" class="form-control form-control-input" v-model="campground.vessel_weight_limit" @blur="validateBeamWeight()" required/>
                            </div>
                        </template>
                    </div>
                    <div class="row" style="display:none;">
                        <div class="col-md-12" style="margin-top:20px;">
                            <div class="form-group pull-right">
                                <a href="#" v-if="createCampground" class="btn btn-primary" @click.prevent="create">Create</a>
                                <a href="#" v-else class="btn btn-primary" @click.prevent="update">Update</a>
                                <a href="#" class="btn btn-primary" @click.prevent="goBack">Cancel</a>
                            </div>
                        </div>
                    </div>
                </div>
			</form>
		</div>
	</div>
</template>
<style>
.alert{
    display:none;
    margin-left:15px;
}

</style>
<script>
import {
    $,
    api_endpoints,
    helpers
}
from '../../hooks.js'
import {
    bus,
}
from '../utils/eventBus.js';
import loader from '../utils/loader.vue'
import alert from '../utils/alert.vue'
export default {
    name: 'cg_limits',
    components: {
        alert,
        loader,
    },
    data: function() {
        let vm = this;
        return {
            form: null,
            errors: false,
            errorString: '',
            showUpdate: false,
            isLoading: false,
            reload : false
        }
    },
    props: {
        createCampground: {
            default: function() {
                return true;
            }
        },
        campground: {
            default: function() {
                return {
                    address: {},
                };
            },
            type: Object
        },
        loadingLimits: {
            type: Boolean,
            default: function(){
                return false;
            }
        }
    },
    computed: {
        showError: function() {
            var vm = this;
            return vm.errors;
        },
        jettyPen: function(){
            

            return this.campground.mooring_physical_type == 1;
        },
    },
    watch: {
        loadingLimits: {
            immediate: true,
            deep: true,
            handler: function(n, o){
                this.isLoading = n;
            }
        },
        campground: {
            handler: function() {
            },
            deep: true

        }
    },
    methods: {
		goBack: function() {
            helpers.goBack(this);
        },
        validateSize: function(){
            let vm = this;
            var isValid = true;
            if(!parseFloat(vm.campground.vessel_size_limit) > 0){
                isValid = false;
                var error = {
                    title : "Invalid Size",
                    text : "Please select a size greater than 0",
                    type : "warning",
                }
                vm.$emit('error', error);
            }
            return isValid;
        },
        validateDraft: function(){
            let vm = this;
            var isValid = true;
            if(!parseFloat(vm.campground.vessel_draft_limit) > 0){
                isValid = false;
                var error = {
                    title : "Invalid Draft",
                    text : "Please select a draft greater than 0",
                    type : "warning",
                }
                vm.$emit('error', error);
            }
            return isValid;
        },
        validateBeamWeight: function(){
            let vm = this;
            var isValid = true;
            if(vm.campground.mooring_physical_type == 1 || vm.campground.mooring_physical_type == 2) {
                if(!parseFloat(vm.campground.vessel_beam_limit) > 0){
                    isValid = false;
                    var error = {
                        title : "Invalid Beam",
                        text : "Please select a beam greater than 0",
                        type : "warning",
                    }
                    vm.$emit('error', error);
                }
            } else {
                if(!parseFloat(vm.campground.vessel_weight_limit) > 0){
                    isValid = false;
                    var error = {
                        title : "Invalid Weight",
                        text : "Please select a weight greater than 0",
                        type : "warning",
                    }
                    vm.$emit('error', error);
                }
            }
            return isValid;
        },
        validateLimits: function() {
            let vm = this;
            var isValid = true;
            isValid = vm.validateSize();
            if (isValid){
                isValid = vm.validateDraft();
            }
            if (isValid){
                isValid = vm.validateBeamWeight();
            }
            return isValid;
        },
		validateForm:function () {
			let vm = this;
            var isValid = vm.validateLimits();
            return  vm.form.valid() && isValid;
		},
        create: function() {
			if(this.validateForm()){
				this.sendData(api_endpoints.campgrounds, 'POST');
			}
        },
        update: function() {
			if(this.validateForm()){
				this.sendData(api_endpoints.campground(this.campground.id), 'PUT',true); 
			}	
        },
        sendData: function(url, method, reload=false) {
            let vm = this;
            vm.isLoading =true;
            vm.reload = reload;
            if ( vm.campground.contact == "undefined") {
                vm.campground.contact = '';
            }
            if (vm.campground.mooring_physical_type == 1){
                vm.campground.vessel_weight_limit = 0;
            } else {
                vm.campground.vessel_beam_limit = 0;
            }
            console.log('campground-limits.vue 1');
            vm.$emit('updated', vm.campground);
            vm.$emit('save', url, method, reload, "limits");
        },
        showAlert: function() {
            // bus.$emit('showAlert', 'alert1');
            bus.emit('showAlert', 'alert1');
        },
    },
    mounted: function() {
        let vm = this;
        vm.form = $('#limitsForm');
        // vm.addFormValidations();
        $('#cg_limits .form-control').on('blur', function(){
            console.log('campground-limits.vue 2');
            vm.$emit('updated', vm.campground);
        });
    },
}

</script>

