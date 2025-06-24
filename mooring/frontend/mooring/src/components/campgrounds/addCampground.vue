<template lang="html" id="pkCGADD">

   <div class="panel-group" id="applications-accordion" role="tablist" aria-multiselectable="true">
      <div class="panel panel-default" id="applications">
        <div class="panel-heading" role="tab" id="applications-heading">
            <h4 class="panel-title">
                <a role="button" data-toggle="collapse" href="#applications-collapse"
                   aria-expanded="false" aria-controls="applications-collapse">
                    <h3>Add Mooring</h3>
                </a>
            </h4>
        </div>
        <div id="applications-collapse" class="panel-collapse collapse in" role="tabpanel"
             aria-labelledby="applications-heading">
            <div class="panel-body">
               <div class="col-lg-12">
                  <div class="row">
                    <div class="col-sm-12" style="overflow:visible;">
                    </div>
                     <campgroundAttr :campground="campground" :loadingDetails="loadingDetails" @updated="updateCampground" @save="sendData">
                     </campgroundAttr>
                  </div>
               </div>
            </div>
         </div>
      </div>
      <div class="navbar navbar-default" id="footer">
        <div class="container">
            <div class="navbar navbar-nav navbar-right" style="margin-top:5px;">
                <a href="#" class="btn btn-primary" @click.prevent="sendData">Create</a>
                <a href="/dashboard/moorings/" class="btn btn-default">Cancel</a>
            </div>
        </div>
    </div>
   </div>

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
        }
    },
    methods: {
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
