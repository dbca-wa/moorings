<template>
    <div id="app">
        <router-view></router-view>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
    name: 'App',
    computed: {
        ...mapGetters([
            'showAlert',
            'alertType',
            'alertMessage'
        ])
    },
    watch: {
        $route() {
            this.$store.dispatch("updateAlert", {
                visible: false,
                type: "danger",
                message: ""
            });
        }
    }
}

</script>

<style>
</style>