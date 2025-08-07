<template lang="html">
    <div  id="cg_additional" >
        <div>
            <form id="additionalForm">
                <div class="col-sm-12">
                <alert v-model:show="showUpdate" type="success" :duration="7000">
                    <p>Mooring successfully updated</p>
                </alert>
                <alert v-model:show="showError" type="danger">
                    <p>{{errorString}}</p>
                </alert>
					<div class="row">
						<div class="col-lg-12">
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <label class="control-label" >Description</label>
                                        <div id="editor" name="description" class="form-control form-control-input"></div>
                                    </div>
                                </div>
                            </div>
                            <div class="row" style="margin-top: 40px;">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <label class="control-label" >Additional confirmation information</label>
                                        <textarea id="additional_info" class="form-control form-control-input" v-model="campground.additional_info"/>
                                    </div>
                                </div>
                            </div>
                            <div class="row" style="margin-top: 40px;display:none;" >
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
    display:none;
    height:30px;
    line-height:30px;
    padding:7px 9px;
}

</style>

<script>
import {
    $,
    api_endpoints,
    helpers,
    validate
}
from '../../hooks.js'
import {
    bus,
}
from '../utils/eventBus.js';
import Quill from 'quill';
import Render from 'quill-render';
import loader from '../utils/loader.vue'
import alert from '../utils/alert.vue'
export default {
    name: 'cg_additional',
    components: {
        alert,
        loader,
    },
    data: function() {
        let vm = this;
        return {
            editor: null,
            editor_updated: false,
            form: null,
            errors: false,
            errorString: '',
            showUpdate: false,
            isLoading: false,
            reload : false,
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
        loadingAdditional: {
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
    },
    watch: {
        loadingAdditional: {
            immediate: true,
            deep: true,
            handler: function(n, o){
                this.isLoading = n;
            }
        },
        campground: {
            handler: function() {
                // this.loadSelectedFeatures();
            },
            deep: true

        }
    },
    methods: {
		goBack: function() {
            helpers.goBack(this);
        },
		validateForm:function () {
            console.log("campground-additional.vue validateForm");
			let vm = this;
            var isValid = vm.validateEditor($('#editor'))
            return  vm.form.valid() && isValid;
		},
        create: function() {
            console.log("in campground-additional.vue create");
			if(this.validateForm()){
				this.sendData(api_endpoints.campgrounds, 'POST');
			}
        },
        update: function() {
            console.log("in campground-additional.vue update");
			if(this.validateForm()){
				this.sendData(api_endpoints.campground(this.campground.id), 'PUT',true); 
			}	
        },
        validateEditor: function(el) {
            console.log('in validateEditor');
            console.log({ el });
            el = el[0] || el; // Ensure el is a DOM element
            const vm = this;
            const formGroup = el.closest('.form-group');

            // Remove error tooltip if already exists
            if (formGroup.classList && formGroup.classList.contains('has-error')) {
                const instance = bootstrap.Tooltip.getInstance(el);
                if (instance) {
                    instance.dispose();
                }
                el.removeAttribute('data-bs-original-title');
                formGroup.classList.remove('has-error');
            }

            // Check if editor is empty
            if (vm.editor.getText().trim().length === 0) {
                el.setAttribute('data-bs-toggle', 'tooltip');
                el.setAttribute('data-bs-placement', 'top');
                el.setAttribute('title', 'Description is required');

                // Create tooltip instance (only once)
                let tooltip = bootstrap.Tooltip.getInstance(el);
                if (!tooltip) {
                    tooltip = new bootstrap.Tooltip(el, {
                        trigger: 'focus',
                    });
                }

                formGroup.classList.add('has-error');
                return false;
            }

            return true;
        },
        sendData: function(url, method, reload=false) {
            let vm = this;
            vm.isLoading =true;
            vm.reload = reload;
            console.log('campground-additional.vue sendData');
            vm.$emit('updated', vm.campground);
            vm.$emit('save', url, method, reload, "additional");
        },
        showAlert: function() {
            // bus.$emit('showAlert', 'alert1');
            bus.emit('showAlert', 'alert1');
        },
    },
    mounted: function() {
        console.log('campground-additional.vue mounted');
        let vm = this;
        vm.editor = new Quill('#editor', {
            modules: {
                toolbar: true
            },
            theme: 'snow'
        });
        vm.editor.on('text-change', function(delta, oldDelta, source) {
            console.log('campground-additional.vue text-change');
            var text = $('#editor >.ql-editor').html();
            vm.campground.description = text;
            vm.validateEditor($('#editor'));
        });
        vm.form = $('#additionalForm');

        $.ajax({
            url: api_endpoints.profile,
            method: 'GET',
            dataType: 'json',
            success: function(data, stat, xhr){
                if(data.is_inventory){
                    vm.invent = true;
                }
                if(!vm.invent){
                    vm.editor.enable(false);
                }
            }
        });

        $('#cg_additional .form-control').on('blur', function(){
            console.log('campground-additional.vue blur');
            if (vm.validateForm()){
                console.log('campground-additional.vue blur');
                vm.$emit('updated', vm.campground);
            }
        });
    },
    updated: function() {
        let vm = this;
        var changed = false;
        if (vm.campground.description != null && vm.editor_updated == false) {
            vm.editor.clipboard.dangerouslyPasteHTML(0, vm.campground.description, 'api');
            changed = true;
        }
        if (changed) {
            vm.editor_updated = true;
        }
    }
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
