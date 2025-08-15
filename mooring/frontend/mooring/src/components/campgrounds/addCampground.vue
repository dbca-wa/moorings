<template lang="html" id="pkCGADD">
    <div class="card" id="applications">
        <div class="card-header" role="tab" id="addmooring-heading">
            <h2 class="mb-0">
                <button 
                    class="btn d-flex justify-content-between align-items-center w-100 text-start text-decoration-none"
                    type="button"
                    :aria-expanded="isExpandedAddMooring"
                    aria-controls="addmooring-collapse"
                    @click="toggleCollapseAddMooring"
                >
                    <h3 class="mb-0">Add Mooring</h3>
                    <i :class="['bi', isExpandedAddMooring ? 'bi-chevron-up' : 'bi-chevron-down', 'fs-4', 'fw-bold']"></i>
                </button>
            </h2>
        </div>
        <!-- <div id="applications-collapse" class="card-body"> -->
        <div
            id="addmooring-collapse"
            class="collapse show"
            aria-labelledby="addmooring-heading"
            ref="collapseElementAddMooring"
        >
            <div class="card-body">
                <campgroundAttr :campground="campground" :loadingDetails="loadingDetails" @updated="updateCampground" @save="sendData" />
            </div>
        </div>
    </div>
    <!-- <div class="navbar navbar-default" id="footer">
        <div class="container">
            <div class="navbar navbar-nav navbar-right" style="margin-top:5px;">
                <a href="#" class="btn btn-primary" @click.prevent="sendData">Create</a>
                <a href="/dashboard/moorings/" class="btn btn-default">Cancel</a>
            </div>
        </div>
    </div> -->
    <!-- 
    Using the semantic <footer> tag.
    The 'mt-auto' class is useful for pushing the footer to the bottom
    of the viewport when the page content is short (within a flexbox layout).
    -->
    <footer id="footer" class="bg-light border-top py-3 mt-auto">
        <div class="container">
            <!-- 
                Use Flexbox to align content to the right.
                d-flex: Enables Flexbox container.
                justify-content-end: Aligns items to the end (right side).
                gap-2: Adds a gap between flex items (e.g., 0.5rem).
            -->
            <div class="d-flex justify-content-end gap-2">
                <!-- 'btn-primary' remains unchanged. -->
                <a href="#" class="btn btn-primary" @click.prevent="sendData">Create</a>

                <!-- 'btn-default' is replaced with 'btn-secondary' in Bootstrap 5. -->
                <a href="/dashboard/moorings/" class="btn btn-secondary">Cancel</a>
            </div>
        </div>
    </footer>
</template>

<script>
import campgroundAttr from './campground-details.vue'
import {
    $,
    Moment,
    api_endpoints,
    helpers,
} from '../../hooks.js'
import alert from '../utils/alert.vue'
import swal from 'sweetalert2';
export default {
    name: 'addCampground',
    components: {
        campgroundAttr,
        alert
    },
    data: function() {
        return {
            campground:{
                address: {},
                images:[],
                mooring_specification: '',
                mooring_group: [],
                name: '',
                features: []
            },
            loadingDetails: false,
            title:'',
            errors:false,
            errorString: '',

            isExpandedAddMooring: true,
            collapseInstanceAddMooring: null,
        }
    },
    methods: {
        toggleCollapseAddMooring: function() {
            if (this.collapseInstanceAddMooring) {
                this.collapseInstanceAddMooring.toggle();
            }
        },
       mooringSpecificationCheck: function() {
        let vm = this;
        console.log('mooringSpecificationCheck');
        var mooring_specification = $('#mooring_specification').val();
        if (mooring_specification) {
              $('#mooring_details').show();
        } else {
              $('#mooring_details').hide();
        }
        vm.addFormValidations();

       },
 
       updateCampground: function(value){
            var vm = this;
            vm.campground = value;
        },
        swalMessage: function(value){
            swal({
            title: value.title,
            text: value.text,
            type: value.type,
            showCancelButton: false,
            confirmButtonText: 'OK',
            showLoaderOnConfirm: true,
            allowOutsideClick: false
            });
        },
        addFormValidations: function() {
            console.log("validating");

            var mooring_specification = $('#mooring_specification').val();
            console.log(mooring_specification);
            if (mooring_specification == '2') {
                console.log("VALIDATE PRUCVA");

                 $('#attForm').validate({
                     rules: {
                         name: "required",
                         park: "required",
                         campground_type: "required",
                         campground_type_physical: "required",
                         campground_class: "required",
                     },
                     messages: {
                         name: "Enter a mooring name",
                         park: "Select a park from the options",
                         campground_type: "Select a booking type from the options",
                         campground_type_physical: "Select a mooring type from the options",
                         campground_class: "Select a mooring class from the options",
                     },
                     showErrors: function(errorMap, errorList) {
                        const { showErrors } = helpers.useFormErrors();
                        showErrors(errorMap, errorList, this.validElements());
                     }
                 });

         
            } else { 
                 $('#attForm').validate({
                     rules: {
                         name: "required",
                         park: "required",
                         campground_type: "required",
                         campground_type_physical: "required",
                         campground_class: "required",
                     },
                     messages: {
                         name: "Enter a mooring name",
                         park: "Select a park from the options",
                         campground_type: "Select a booking type from the options",
                         campground_type_physical: "Select a mooring type from the options",
                         campground_class: "Select a mooring class from the options",
                     },
                     showErrors: function(errorMap, errorList) {
                        const { showErrors } = helpers.useFormErrors();
                        showErrors(errorMap, errorList, this.validElements());
                     }
                 });
            }
        },
        validateName: function(){
            let vm = this;
            var isValid = true;
            console.log('validateMooringGroups');
            console.log(vm.campground.name);
            if (vm.campground.name.length == 0){
                isValid = false;
                var error = {
                    title: "Invalid Mooring Name",
                    text: "Please enter a valid mooring name (min characters 4)",
                    type: "warning"
                }
                $('#name').focus();
                vm.swalMessage(error);
            }

            return isValid;
        },

        validateMooringFeatures: function(){
            let vm = this;
            var isValid = true;
            if (vm.campground.features.length == 0){
                isValid = false;
                var error = {
                    title: "No Features",
                    text: "Please select at least 1 mooring feature.",
                    type: "warning"
                }
                $('#mooring_groups').focus();
                vm.swalMessage(error);
            }

            return isValid;
        },


        validateMooringGroups: function(){
            let vm = this;
            var isValid = true;
            console.log('validateMooringGroups');
            console.log(vm.campground.mooring_group);
            if (vm.campground.mooring_group.length == 0){
                isValid = false;
                var error = {
                    title: "No Group",
                    text: "Please select at least 1 mooring group (permissions)",
                    type: "warning"
                }
                $('#mooring_groups').focus();
                vm.swalMessage(error);
            }

            return isValid;
        },
        validateForm: function() {
            let vm = this;
            var isValid = true;
            isValid = vm.validateName();
 
            if (isValid) {
               isValid = vm.validateMooringFeatures();
	    }
            if (isValid) {
               isValid = vm.validateMooringGroups();
            }
            if (isValid){
                $('form').each(function(){
                    if (!$(this).valid()){
                        isValid = false;
                        var message = {
                            title: "Failure",
                            text: "Mooring not created, there was an error.\nPlease check all mandatory fields are complete.",
                            type: "error"
                        }
                        vm.swalMessage(message);
                        return false;
                    }
                }); 
            }            
            return isValid;
        },
        sendData: function(){
            let vm = this;
            var isValid = vm.validateForm();
            if (isValid){
                $.ajax({
                    beforeSend: function(xhrObj) {
                        xhrObj.setRequestHeader("Content-Type", "application/json");
                        xhrObj.setRequestHeader("Accept", "application/json");
                    },
                    url: api_endpoints.campgrounds,
                    method: "POST",
                    xhrFields: {
                        withCredentials: true
                    },
                    data: JSON.stringify(vm.campground),
                    headers: {'X-CSRFToken': helpers.getCookie('csrftoken')},
                    contentType: "application/x-www-form-urlencoded",
                    dataType: 'json',
                    success: function(data, stat, xhr) {
                        console.log("SUCCESS!!");
                        var message = {
                            title: "Success",
                            text: "Mooring created",
                            type: "success"
                        }
                        vm.swalMessage(message);
                        vm.$router.push({
                            name: 'cg_detail',
                            params: {
                                id: data.id
                            }
                        });
                    vm.$store.dispatch("updateAlert",{
                        visible:false,
                        type:"danger",
                        message: ""
                    });
                    },
                    error: function(resp) {
                        console.log("There was an error sending data.");
                        console.log(resp);
                        var message = {
                            title: "Failure: Mooring not saved",
                            text: resp.responseText,
                            type: "error"
                        }
                        vm.swalMessage(message);
                        vm.$store.dispatch("updateAlert",{
                            visible:true,
                            type:"danger",
                            message: helpers.apiError(resp)
                        });
                    }
                });
            }
        }
    },
    mounted:function () {
        let vm = this;

        vm.$nextTick(() => {
            const collapseElAddMooring = vm.$refs.collapseElementAddMooring;
            if (collapseElAddMooring) {
                vm.collapseInstanceAddMooring = new bootstrap.Collapse(collapseElAddMooring, {
                    toggle: false
                });
            }
            collapseElAddMooring.addEventListener('show.bs.collapse', () => {
                vm.isExpandedAddMooring = true;
            });
            collapseElAddMooring.addEventListener('hide.bs.collapse', () => {
                vm.isExpandedAddMooring = false;
            });
        })

        vm.mooringSpecificationCheck();
        $( "#mooring_specification" ).change(function() {
          vm.mooringSpecificationCheck();
        });
        setTimeout(function(){
            vm.addFormValidations();
        }, 50);
    }
}
</script>

<style lang="css">
.well{
   background-color: #fff;
}
.btn{
   margin-bottom: 10px;
}
</style>
