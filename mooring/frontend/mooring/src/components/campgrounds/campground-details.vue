<template lang="html">
<div  id="cg_attr" >
    <div>
        <form id="attForm">
            <div class="col-sm-12">
                <alert :show.sync="showUpdate" type="success" :duration="7000">
                    <p>Mooring successfully updated</p>
                </alert>
                <alert :show.sync="showError" type="danger">
                    <p>{{errorString}}</p>
                </alert>
                <div class="row">
                    <div class="col-lg-12">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-group ">
                                    <label class="control-label">Mooring Specification</label>
                                    <select class="form-control form-control-input" ref="mooring_specification" v-model="campground.mooring_specification" id='mooring_specification' name='mooring_specification'>
                                        <option value="">Not Selected</option>
                                        <option v-for="m in mooring_specification" :value="m.id" >{{m.name}}</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-12" id='mooring_details'>
                        <div class="row">
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label class="control-label" >Mooring Name</label>
                                    <input type="text" name="name" id="name" class="form-control form-control-input" v-model="campground.name"/>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label class="control-label" >Mooring Oracle Code</label>
                                    <input type="text" name="oracle_code" id="oracle_code" class="form-control form-control-input" v-model="campground.oracle_code"/>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="form-group ">
                                    <label class="control-label" >Mooring Park</label>
                                    <select name="park" ref="park" id="park" class="form-control form-control-input" v-model="campground.park">
                                        <option v-for="park in parks" :value="park.id">{{ park.name }}</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-0">
                                <div class="form-group " style='display:none'>
                                    <label class="control-label" >Booking Configuration</label>
                                    <select id="site_type" name="site_type" class="form-control form-control-input"  v-model="campground.site_type">
                                        <option value="0" selected >Bookable per site</option>
                                        <option value="1" >Bookable per site type</option>
                                        <option value="2">Bookable per site type (hide site number)</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label class="control-label">Mooring Features</label>
                                    <select class="form-control form-control-input" id="features" name="features" ref="features" v-model="campground.features" multiple>
                                        <option v-for="f in features" :value="f.id">{{ f.name }}</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group ">
                                    <label class="control-label" >Mooring Group (Permissions)</label>
                                    <select class="form-control form-control-input" ref="group_permissions" v-model="campground.mooring_group" id='mooring_groups' name='mooring_groups' >
                                        <option v-for="m in mooring_groups" :value="m.id" >{{m.name}}</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-4">
                                <div class="form-group ">
                                    <label class="control-label" >Booking Type</label>
                                    <select id="campground_type" ref="campground_type" name="campground_type" class="form-control form-control-input"  v-model="campground.mooring_type">
                                        <option value="0">Bookable Online</option>
                                        <option value="1">Not Bookable Online</option>
                                        <option value="2">Public</option>
                                        <option value="3">Unpublished</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="form-group ">
                                    <label class="control-label" >Mooring Physical Type</label>
                                    <select id="campground_type_physical" ref="type_physical" name="campground_type_physical" class="form-control form-control-input"  v-model="campground.mooring_physical_type">
                                        <option value="0">Mooring</option>
                                        <option value="1">Jetty Pen</option>
                                        <option value="2">Beach Pen</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="form-group ">
                                    <label class="control-label" >Mooring Class</label>
                                    <select id="campground_class" ref="class" name="campground_class" class="form-control form-control-input"  v-model="campground.mooring_class">
                                        <option value="small">Small</option>
                                        <option value="medium">Medium</option>
                                        <option value="large">Large</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        <div class="row" style="display:none;">
                            <div class="col-sm-8">
                            </div>
                            <div class="col-sm-4">
                                <div class="col-sm-12">
                                    <div class="form-group pull-right">
                                        <a href="#" v-if="createCampground" class="btn btn-primary" @click.prevent="create">Create</a>
                                        <a href="#" v-else class="btn btn-primary" @click.prevent="update">Update</a>
                                        <a href="#" class="btn btn-primary" @click.prevent="goBack">Cancel</a>
                                    </div>
                                </div>
                            </div>
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
    height:30px;
    line-height:30px;
    padding:7px 9px;
}
.select2-container--open {
    z-index: 99999;
}

</style>

<script>
import {
    $,
    api_endpoints,
    helpers,
    validate,
    // select2
}
from '../../hooks.js'
import {
    bus,
}
from '../utils/eventBus.js';
import loader from '../utils/loader.vue'
import alert from '../utils/alert.vue'
import {mapGetters} from 'vuex'
export default {
    name: 'cg_attr',
    components: {
        alert,
        loader,
    },
    data: function() {
        let vm = this;
        return {
            features: [],
            selected_features_loaded: false,
            selected_features: Array(),
            form: null,
            errors: false,
            errorString: '',
            showUpdate: false,
            isLoading: false,
            reload : false,
            mooring_groups: [],
            MooringGroups: [{ id: 1, name: 'Principal' }, { id: 2, name: 'Dessert' }, { id: 3, name: 'Drink' }],
            mooring_specification: [],
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
                    images: []
                };
            },
            type: Object
        },
        loadingDetails: {
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
        hasSelectedFeatures: function() {
            return this.selected_features.length > 0;
        },
        allFeaturesSelected: function() {
            return this.features.length < 1;
        },
        jettyPen: function(){
            return this.campground.mooring_physical_type == 1;
        },
		...mapGetters([
          'parks',
          'mooring_groups'
        ]),
 
    },
    watch: {
        loadingDetails: {
            immediate: true,
            deep: true,
            handler: function(n, o){
                this.isLoading = n;
            }
        },
        campground: {
            handler: function() {
                // this.loadSelectedFeatures();
                let vm = this;
                $(vm.$refs.campground_type).val(vm.campground.mooring_type).trigger('change');
                $(vm.$refs.type_physical).val(vm.campground.mooring_physical_type).trigger('change');
                $(vm.$refs.class).val(vm.campground.mooring_class).trigger('change');
                $(vm.$refs.park).val(vm.campground.park).trigger('change');
            },
            deep: true,

        }
    },
    methods: {
		goBack: function() {
            helpers.goBack(this);
        },
		validateForm:function () {
			let vm = this;            
            return  vm.form.valid();
		},
        create: function() {
            console.log("CREATE");
		this.setFeatures();
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
            console.log('campground-details.vue 2')
            vm.$emit('updated', vm.campground);
            vm.$emit('save', url, method, reload, "details");
        },
        showAlert: function() {
            // bus.$emit('showAlert', 'alert1');
            bus.emit('showAlert', 'alert1');
        },
        loadParks: function() {
            var vm = this;
   	    if (vm.parks.length == 0) {
                vm.$store.dispatch("fetchParks");
            }
        },
        loadMooringGroups: function() {
            console.log("loadMooringGroups called");
            let vm =this;
            $.ajax({
                url: api_endpoints.mooring_groups,
                dataType: 'json',
                async: false,
                success: function(data, stat, xhr) {
                    vm.mooring_groups = data;
                }
            });
        },
        loadFeatures: function() {
            var vm = this;
            var url = api_endpoints.features;
            console.log(url);
            $.ajax({
                url: url,
                dataType: 'json',
                success: function(data, stat, xhr) {
                    console.log({data})
                    vm.features = data;
                }
            });
        },
        async fetchMooringSpecification() {
            console.log("fetchMooringSpecification called");
            const url = api_endpoints.mooring_specification;
            console.log("URL:", url);

            try {
                console.log("Fetching mooring specification from:", url);
                // Pause the execution until the fetch promise resolves.
                // 'response' will be a Response object.
                const response = await fetch(url);
                console.log({response})

                // The fetch API does not reject on HTTP errors (like 404 or 500).
                // We need to manually check if the response was successful.
                // The 'ok' property is true if the status code is in the 200-299 range.
                if (!response.ok) {
                    // If the response is not ok, we throw an error to be caught by the catch block.
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                // The response.json() method also returns a promise.
                // We await it to get the parsed JSON data from the response body.
                const data = await response.json();

                console.log({data})
                
                // Assign the fetched data to the component's data property.
                this.mooring_specification = data;

            } catch (error) {
                // This block will catch both network errors (if fetch fails) 
                // and the HTTP errors we threw manually.
                console.error('Failed to fetch mooring specification:', error);
                // Optionally, you could set an error state on your component here.
                // this.error = 'Could not load data.';
            }
        }
    },
    mounted: function() {
        let vm = this;
        vm.isLoading = true;
        vm.loadParks();

        vm.loadFeatures();
        vm.loadMooringGroups();

        vm.form = $('#attForm');
        // vm.addFormValidations();

        $('#cg_attr .form-control').on('blur', function(){
            console.log('campground-details.vue 1')
            vm.$emit('updated', vm.campground);
        });

        //Park
        $(vm.$refs.park).select2({
            "theme": "bootstrap",
        }).
        on("select2:select", function (e){
            var selected = $(e.currentTarget);
            vm.campground.park = selected.val();
        }).
        on("select2:unselect", function (e){
            var selected = $(e.currentTarget);
            vm.campground.park = selected.val();
        });
        //Mooring type selector
        $(vm.$refs.campground_type).select2({
            "theme": "bootstrap",
        }).
        on("select2:select", function (e){
            var selected = $(e.currentTarget);
            vm.campground.mooring_type = selected.val();
        }).
        on("select2:unselect", function (e){
            var selected = $(e.currentTarget);
            vm.campground.mooring_type = selected.val();
        });
        //Group permissions
        $(vm.$refs.group_permissions).select2({
            "theme": "bootstrap",
        }).
        on("select2:select", function (e){
            var selected = $(e.currentTarget);
            // var mooringgroups = [];
            // var select_array = selected.val();
            // for (var i = 0; i < select_array.length; i++){
            //     var val = select_array[i];
            //     var intval = parseInt(select_array[i]);
            //     mooringgroups.push(intval);
            // }
            // vm.campground.mooring_group = mooringgroups;
            vm.campground.mooring_group = [selected.val(),];
        }).
        on("select2:unselect", function (e){
            var selected = $(e.currentTarget);
            // var mooringgroups = [];
            // var select_array = selected.val();
            // for (var i = 0; i < select_array.length; i++){
            //     var val = select_array[i];
            //     var intval = parseInt(select_array[i]);
            //     mooringgroups.push(intval);
            // }
            // vm.campground.mooring_group = mooringgroups;
            vm.campground.mooring_group = [selected.val(),];
        });
        //Physical Type
        $(vm.$refs.type_physical).select2({
            "theme": "bootstrap",
        }).
        on("select2:select", function (e){
            var selected = $(e.currentTarget);
            vm.campground.mooring_physical_type = selected.val();
        }).
        on("select2:unselect", function (e){
            var selected = $(e.currentTarget);
            vm.campground.mooring_physical_type = selected.val();
        });
        //Class
        $(vm.$refs.class).select2({
            "theme": "bootstrap",
        }).
        on("select2:select", function (e){
            var selected = $(e.currentTarget);
            vm.campground.mooring_class = selected.val();
        }).
        on("select2:unselect", function (e){
            var selected = $(e.currentTarget);
            vm.campground.mooring_class = selected.val();
        });
        //Features
        $(vm.$refs.features).select2({
            "theme": "bootstrap",
        }).
        on("select2:select", function (e){
            var selected = $(e.currentTarget);
            vm.campground.features = selected.val();
        }).
        on("select2:unselect", function (e){
            var selected = $(e.currentTarget);
            vm.campground.features = selected.val();
        });

        console.log("bakabaka")
        vm.fetchMooringSpecification()
        // vm.$http.get(api_endpoints.mooring_specification).then((response) => {
        //         vm.mooring_specification = response.body
        // }, (error) => {
        //         console.log(error);
        // });

        vm.isLoading = false;       
    },
}

</script>

<style lang="css">
    #editor{
        height: 200px;
    }
    .features >.panel>.panel-body{
        padding:0;
        max-height: 300px;
        min-height: 300px;
        overflow: auto;
    }
    .features .list-group{
        margin-bottom: 0;
    }
    .features .list-group-item{
        border-radius: 0;
    }
    .list-group-item:last-child{
        border-bottom-left-radius: 5px;
        border-bottom-right-radius: 5px;
    }
    .empty-features{
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 300px;
        color: #ccc;
        font-size: 2em;
    }
</style>
