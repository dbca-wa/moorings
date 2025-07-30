import { createStore } from 'vuex'
import {
    $,
    api_endpoints
} from '../hooks'

var store = createStore({
    state: {
        alert:{
            visible:false,
            type:"danger",
            message: ""
        },
        regions:[],
        parks:[],
        districts:[],
        mooring_groups: [],
        campgrounds:[],
        campsite_classes:[],
        booking_period_options:[],
        booking_periods:[],
        show_loader: false,
        app_loader_text: ''
    },
    mutations: {
        SETALERT(state, a) {
            state.alert = a;
        },
        SETREGIONS(state, regions) {
            state.regions = regions;
        },
        SETPARKS(state, parks) {
            state.parks = parks;
        },
        SETDISTRICTS(state, districts) {
            state.districts = districts;
        },
        SETCAMPGROUNDS(state,campgrounds){
            state.campgrounds = campgrounds;
        },
        SETCAMPSITECLASSES(state,campsite_classes){
            state.campsite_classes = campsite_classes;
        },
        SET_LOADER_STATE(state,val){
            state.show_loader = val;
            !val ? state.app_loader_text = '': '';
        },
        SET_LOADER_TEXT(state,val){
            state.app_loader_text = val;
        },
        SETMOORINGGROUP(state, mooring_groups) {
            state.mooring_groups = mooring_groups;
        },
        SETBOOKINGPERIODOPTIONS(state, val){
            state.booking_period_options = val;
        },
        SETBOOKINGPERIODS(state, val){
            state.booking_periods = val;
        }

    },
    actions: {
        updateAlert(context,payload) {
            context.commit('SETALERT',payload);
        },
        fetchRegions(context) {
            $.get(api_endpoints.regions,function(data){
                context.commit('SETREGIONS',data);
            });
        },
        fetchParks(context) {
            $.get(api_endpoints.parks,function(data){
                context.commit('SETPARKS',data);
            });
        },
        fetchMooringGroups(context) {
            $.get(api_endpoints.mooring_groups,function(data){
                context.commit('SETMOORINGGROUP',data);
            });
        },
        fetchDistricts(context) {
            $.get(api_endpoints.districts,function(data){
                context.commit('SETDISTRICTS',data);
            });
        },
        async fetchCampgrounds(context){
            try {
                // 1. Send a request to the API endpoint and wait for the response
                const response = await fetch(api_endpoints.campgrounds);

                // 2. Check for HTTP errors (e.g., 404 Not Found, 500 Server Error)
                if (!response.ok) {
                    // If an error occurred, stop execution here and jump to the catch block
                    throw new Error(`API Error: ${response.status} ${response.statusText}`);
                }

                // 3. Parse the response body as JSON and wait for it to be converted to a JavaScript object/array
                const campgroundsData = await response.json();

                // 4. Commit the converted data to a mutation to update the state
                context.commit('SETCAMPGROUNDS', campgroundsData);

                // 5. (Optional) Return the data to the caller of this action
                return campgroundsData;

            } catch (error) {
                // Catch any network errors or errors thrown above
                console.error("Failed to fetch campgrounds:", error);
                // Re-throw the error to allow for further error handling by the caller
                throw error;
            }
        },
        fetchCampsiteClasses(context){
            $.get(api_endpoints.campsite_classes,function(data){
                context.commit('SETCAMPSITECLASSES',data);
            });
        },
        fetchBookingPeriodOptions(context){
            $.get(api_endpoints.booking_period_options,function(data){
                context.commit('SETBOOKINGPERIODOPTIONS', data);
            });
        },
        fetchBookingPeriods(context){
            $.get(api_endpoints.booking_period, function(data){
                context.commit('SETBOOKINGPERIODS', data);
            });
        }
    },
    getters:{
        showAlert: state => {
            return state.alert.visible;
        },
        alertType: state => {
            return state.alert.type;
        },
        alertMessage: (state) =>  {
            return state.alert.message;
        },
        regions: state => {
            return state.regions;
        },
        parks: state => {
            return state.parks;
        },
        districts: state => {
            return state.districts;
        },
        campgrounds: state => {
            return state.campgrounds;
        },
        campsite_classes: state => {
            return state.campsite_classes;
        },
        booking_period_options: state => {
            return state.booking_period_options;
        },
        booking_periods: state => {
            return state.booking_periods;
        },
        app_loader_state: (state) => {
            return state.show_loader;
        },
        app_loader_text: (state) => {
            return state.app_loader_text;
        }
    }
});

export default store;
export const useStore = () => store;