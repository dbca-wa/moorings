
export default {
    status_history:function(id) {
        return import.meta.env.VITE_PARKSTAY_URL + "/api/mooring-areas/" + id + "/status_history.json?closures=True";
    },
    regions:import.meta.env.VITE_PARKSTAY_URL + "/api/regions.json",
    parks:import.meta.env.VITE_PARKSTAY_URL + "/api/parks.json",
    districts:import.meta.env.VITE_PARKSTAY_URL + "/api/districts.json",
    mooring_groups: import.meta.env.VITE_PARKSTAY_URL + "/api/mooring_groups.json",
    park_price_history:function (id) {
       return import.meta.env.VITE_PARKSTAY_URL + "/api/parks/price_history.json";
    },
    park_add_price:function () {
       return import.meta.env.VITE_PARKSTAY_URL + "/api/parks/add_price.json";
    },
    park_current_price:function (id,arrival) {
      return import.meta.env.VITE_PARKSTAY_URL + "/api/parks/"+id+"/current_price.json?arrival="+arrival;
    },
    park_entry_rate:function (id) {
      return import.meta.env.VITE_PARKSTAY_URL + "/api/parkentryrate/"+id+".json";
    },
    park:function (id) {
       return import.meta.env.VITE_PARKSTAY_URL + "/api/parks/"+id+".json";
    },
    // Campgrounds
    campgrounds:import.meta.env.VITE_PARKSTAY_URL + "/api/mooring-areas.json",
    campgrounds_datatable:import.meta.env.VITE_PARKSTAY_URL + "/api/mooring-areas/datatable_list.json",
    bulk_close:import.meta.env.VITE_PARKSTAY_URL + "/api/mooring-areas/bulk_close.json",
    bulk_period:import.meta.env.VITE_PARKSTAY_URL + "/api/mooring-areas/bulk_period.json",
    campground:function (id) {
        return import.meta.env.VITE_PARKSTAY_URL + "/api/mooring-areas/"+id+".json";
    },
    campground_price_history: function(id){
        return import.meta.env.VITE_PARKSTAY_URL + "/api/mooring-areas/"+ id +"/price_history.json";
    },
    campgroundStayHistory: function(id){
        return import.meta.env.VITE_PARKSTAY_URL + "/api/mooring-areas/" + id + "/stay_history.json"
    },
    campgroundCurrentStayHistory: function(id,start,end){
        return import.meta.env.VITE_PARKSTAY_URL + "/api/mooring-areas/" + id + "/stay_history.json?start="+start+"&end="+end;
    },
    campground_stay_history_detail: function(id){
        return import.meta.env.VITE_PARKSTAY_URL + "/api/mooring_stay_history/"+ id +".json";
    },
    available_campsite_classes:function (id,start,end) {
        return import.meta.env.VITE_PARKSTAY_URL + "/api/mooring-areas/" + id + "/available_campsite_classes.json?arrival="+start+"&departure="+end;
    },
    campground_stay_history: import.meta.env.VITE_PARKSTAY_URL + "/api/mooring_stay_history.json",
    addPrice: function(id){
        return import.meta.env.VITE_PARKSTAY_URL + "/api/mooring-areas/"+ id +"/addPrice.json";
    },
    editPrice: function(id){
        return import.meta.env.VITE_PARKSTAY_URL + "/api/mooring-areas/"+ id +"/updatePrice.json";
    },
    campgroundCampsites: function(id){
        return import.meta.env.VITE_PARKSTAY_URL + "/api/mooring-areas/" + id + "/campsites.json"
    },
    opencloseCG: function(id){
        return import.meta.env.VITE_PARKSTAY_URL + "/api/mooring-areas/" + id + "/open_close.json"
    },
    deleteBookingRange: function (id) {
        return import.meta.env.VITE_PARKSTAY_URL + "/api/mooring_booking_ranges/" + id + ".json"
    },
    campground_status_history_detail: function(id){
        return import.meta.env.VITE_PARKSTAY_URL + "/api/mooring_booking_ranges/"+ id +".json?original=true";
    },
    delete_campground_price: function(id){
        return import.meta.env.VITE_PARKSTAY_URL + "/api/mooring-areas/" + id + "/deletePrice.json";
    },
    // Campsites
    campsites:import.meta.env.VITE_PARKSTAY_URL + "/api/mooringsites.json",
    campsites_stay_history: import.meta.env.VITE_PARKSTAY_URL + "/api/campsites_stay_history.json",
    campsites_stay_history_detail: function(id){
        return import.meta.env.VITE_PARKSTAY_URL + "/api/campsites_stay_history/"+ id +".json";
    },
    campsites_price_history: function(id){
        return import.meta.env.VITE_PARKSTAY_URL + "/api/mooringsites/"+ id +"/price_history.json";
    },
    campsite_current_price:function (id,start,end) {
       return import.meta.env.VITE_PARKSTAY_URL + "/api/mooringsites/"+ id +"/current_price.json?arrival="+start+"&departure="+end;
    },
    campsites_status_history:function(id){
        return import.meta.env.VITE_PARKSTAY_URL + "/api/mooringsites/" + id + "/status_history.json?closures=True"
    },
    campsite:function (id) {
        return import.meta.env.VITE_PARKSTAY_URL + "/api/mooringsites/"+id+".json";
    },
    campsiteStayHistory: function(id){
        return import.meta.env.VITE_PARKSTAY_URL + "/api/mooringsites/" + id + "/stay_history.json"
    },
    opencloseCS: function(id){
        return import.meta.env.VITE_PARKSTAY_URL + "/api/mooringsites/" + id + "/open_close.json"
    },
    bulk_close_campsites: function () {
        return import.meta.env.VITE_PARKSTAY_URL + "/api/mooringsites/bulk_close.json"
    },
    deleteCampsiteBookingRange: function (id) {
        return import.meta.env.VITE_PARKSTAY_URL + "/api/campsite_booking_ranges/" + id + ".json"
    },
    campsite_status_history_detail: function(id){
        return import.meta.env.VITE_PARKSTAY_URL + "/api/campsite_booking_ranges/"+ id +".json?original=true";
    },
    available_campsites:function(campground,arrival,departure){
      return import.meta.env.VITE_PARKSTAY_URL + "/api/mooring-areas/"+campground+"/available_campsites.json?arrival="+arrival+"&departure="+departure;
    },
    available_campsites_booking:function(campground,arrival,departure,booking){
      return import.meta.env.VITE_PARKSTAY_URL + "/api/mooring-areas/"+campground+"/available_campsites_booking.json?arrival="+arrival+"&departure="+departure+"&booking="+booking;
    },
    features:import.meta.env.VITE_PARKSTAY_URL + "/api/features.json",
    campsite_rate: import.meta.env.VITE_PARKSTAY_URL + "/api/campsite_rate.json",
    campsiterate_detail:function (id) {
        return import.meta.env.VITE_PARKSTAY_URL + "/api/campsite_rate/"+id+".json"
    },
    rates:import.meta.env.VITE_PARKSTAY_URL + "/api/rates.json",

    // campsite types
    campsite_classes:import.meta.env.VITE_PARKSTAY_URL + "/api/mooringsite_classes.json",
    campsite_classes_active:import.meta.env.VITE_PARKSTAY_URL + "/api/mooringsite_classes.json?active_only=true",
    campsite_class:function (id) {
        return import.meta.env.VITE_PARKSTAY_URL + "/api/mooringsite_classes/"+id+".json"
    },
    addCampsiteClassPrice: function(id){
        return import.meta.env.VITE_PARKSTAY_URL + "/api/mooringsite_classes/"+id+"/addPrice.json"
    },
    editCampsiteClassPrice(id) {
        return import.meta.env.VITE_PARKSTAY_URL + "/api/mooringsite_classes/"+id+"/updatePrice.json"
    },
    deleteCampsiteClassPrice(id) {
        return import.meta.env.VITE_PARKSTAY_URL + "/api/mooringsite_classes/"+id+"/deletePrice.json"
    },
    campsiteclass_price_history: function(id){
        return import.meta.env.VITE_PARKSTAY_URL + "/api/mooringsite_classes/"+ id +"/price_history.json";
    },
    closureReasons:function () {
        return import.meta.env.VITE_PARKSTAY_URL + "/api/closureReasons.json";
    },
    openReasons:function () {
        return import.meta.env.VITE_PARKSTAY_URL + "/api/openReasons.json";
    },
    priceReasons:function () {
        return import.meta.env.VITE_PARKSTAY_URL + "/api/priceReasons.json";
    },
    maxStayReasons:function () {
        return import.meta.env.VITE_PARKSTAY_URL + "/api/maxStayReasons.json";
    },
    bulkPricing: function(){
        return import.meta.env.VITE_PARKSTAY_URL + "/api/bulkPricing";
    },
    //bookings
    bookings:import.meta.env.VITE_PARKSTAY_URL + "/api/booking.json",
    admissionsbookings:import.meta.env.VITE_PARKSTAY_URL + "/api/admissionsbooking.json",
    booking: function(id){
        return import.meta.env.VITE_PARKSTAY_URL + "/api/booking/"+id+".json";
    },
    booking_refunds:import.meta.env.VITE_PARKSTAY_URL + "/api/reports/booking_refunds",
    bookings_created_report: import.meta.env.VITE_PARKSTAY_URL +"/api/reports/booking-mooring-created",
    bookings_admission_created_report: import.meta.env.VITE_PARKSTAY_URL +"/api/reports/booking-admission-created",
    bookings_departure_report: import.meta.env.VITE_PARKSTAY_URL +"/api/reports/booking-mooring-departure",
    //other
    countries: import.meta.env.VITE_PARKSTAY_URL + "/api/countries.json",
    users: import.meta.env.VITE_PARKSTAY_URL + "/api/users.json",
    usersLookup: function (q) {
       return  encodeURI(import.meta.env.VITE_PARKSTAY_URL + "/api/users.json?q="+q);
    },
    profile: import.meta.env.VITE_PARKSTAY_URL + "/api/profile",
    contacts:import.meta.env.VITE_PARKSTAY_URL + "/api/contacts.json",
    mooring_specification: import.meta.env.VITE_PARKSTAY_URL + "/api/mooring_specification/",
    //Must end .json otherwise will effect other urls generated based on removing the .json.
    booking_period_options: import.meta.env.VITE_PARKSTAY_URL + "/api/bookingPeriodOptions.json",
    booking_period : import.meta.env.VITE_PARKSTAY_URL + "/api/bookingPeriod.json",
    booking_period_edit : function(id){
        return import.meta.env.VITE_PARKSTAY_URL + "/api/bookingPeriod/" + id + "/";
    },
    booking_period_options_edit : function(id){
        return import.meta.env.VITE_PARKSTAY_URL + "/api/bookingPeriodOptions/" + id + "/";
    },
    global_settings: import.meta.env.VITE_PARKSTAY_URL + "/api/global_settings",
    rate_log: function (id){
        return import.meta.env.VITE_PARKSTAY_URL + "/mooringsiteratelog/" + id + "/";
    }
};
