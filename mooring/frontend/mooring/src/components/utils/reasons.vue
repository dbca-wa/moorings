<template lang="html">
    <div class="row mb-3" id="reasons">
        <div :class="labelClasses">
            <label>Reason: </label>
        </div>
        <div :class="selectWrapperClasses">
            <select v-if="!reasons.length > 0" class="form-select" disabled>
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
}from '../../hooks.js'
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
        modelValue:{
            type: [String, Number],
            default: ''
        },
        large:{
            default:function () {
                return false;
            }
        },
        wide: {
            default: function(){
                return false;
            }
        },
        threenine: {
            default: function() {
                return false;
            }
        }
    },
    computed: {
        selectWrapperClasses: function () {
            let vm = this;
            if (vm.wide) {
                return { 'col-md-10': true };
            }
            if (vm.threenine) {
                return { 'col-md-9': true };
            }
            if (vm.large) {
                return { 'col-md-8': true };
            }
            return { 'col-md-4': true };
        },
        labelClasses: function () {
            let vm = this;
            return {
                'col-md-2': !vm.large,
                'col-md-3': vm.threenine,
                'col-md-4': vm.large,
                'col-form-label': true
            };
        }
    },
    methods:{
        fetchOpenReasons:function () {
            let vm = this;
            $.get(api_endpoints.openReasons(),function (data) {
                vm.reasons = data;
                // bus.$emit('openReasons', vm.reasons);
                bus.emit('openReasons', vm.reasons);
            });
        },
        fetchClosureReasons:function () {
            let vm = this;
            $.get(api_endpoints.closureReasons(),function (data) {
                vm.reasons = data;
                // bus.$emit('closeReasons', vm.reasons);
                bus.emit('closeReasons', vm.reasons);
            });
        },
        fetchMaxStayReasons:function () {
            let vm = this;
            $.get(api_endpoints.maxStayReasons(),function (data) {
                vm.reasons = data;
                // bus.$emit('maxStayReasons', vm.reasons);
                bus.emit('maxStayReasons', vm.reasons);
            });
        },
        fetchPriceReasons:function () {
            let vm = this;
            $.get(api_endpoints.priceReasons(),function (data) {
                vm.reasons = data;
                // bus.$emit('priceReasons', vm.reasons);
                bus.emit('priceReasons', vm.reasons);
            });
        }
    },
    mounted:function(){
        let vm =this;
        if(vm.type){
            switch (vm.type.toLowerCase()) {
                case 'close':
                    vm.fetchClosureReasons();
                    break;
                case 'open':
                    vm.fetchOpenReasons();
                    break;
                case 'stay':
                    vm.fetchMaxStayReasons();
                    break;
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
