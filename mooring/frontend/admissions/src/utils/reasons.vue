<template lang="html">
    <div class="row mb-3" id="reasons">
        <div :class="{'col-md-4':large,'col-md-2':!large}">
            <label>Reason: </label>
        </div>
        <div :class="{'col-md-8':large,'col-md-4':!large}">
            <select v-if="!reasons || reasons.length === 0" class="form-select" disabled>
                <option value="">Loading...</option>
            </select>
            <select v-else name="open_reason" :value="modelValue" @change="$emit('update:modelValue', $event.target.value)" class="form-select">
                <option value=""></option>
                <option v-for="reason in reasons" :value="reason.id" :key="reason.id">
                    {{reason.text}}
                </option>
            </select>
        </div>
    </div>
</template>

<script>
import {
    $,
    api_endpoints,
    bus
}from '../hooks.js'
export default {
    name:'reasons',
    data:function () {
        let vm =this;
        return {
            reasons:[]
        }
    },
    props:{
        type:{
            required:true
        },
        // value:{

        // },
        modelValue: {
            type: [String, Number],
            required: true,
            default: ''
        },
        large:{
            default:function () {
                return false;
            }
        }
    },
    methods:{
        fetchPriceReasons:function () {
            let vm = this;
            $.get(api_endpoints.priceReasons(),function (data) {
                vm.reasons = data;
                bus.emit('reasons', vm.reasons);
            });
        }
    },
    mounted:function(){
        let vm =this;
        if(vm.type){
            switch (vm.type.toLowerCase()) {
                case 'price':
                    vm.fetchPriceReasons();
                    break;
            }
        }
    }
}
</script>

<style lang="css">
</style>
