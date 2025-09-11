
export default {
    status_history:function(id) {
        return "/api/mooring-areas/" + id + "/status_history.json?closures=True";
    },
    regions: "/api/regions.json",
    parks: "/api/parks.json",
    districts: "/api/districts.json",
    mooring_groups: "/api/mooring_groups.json",
    park_price_history:function (id) {
       return "/api/parks/price_history.json";
    },
    park_add_price:function () {
       return "/api/parks/add_price.json";
    },
    park_current_price:function (id,arrival) {
      return "/api/parks/"+id+"/current_price.json?arrival="+arrival;
    },
    park_entry_rate:function (id) {
      return "/api/parkentryrate/"+id+".json";
    },
    park:function (id) {
       return "/api/parks/"+id+".json";
    },
    // Campgrounds
    campgrounds:"/api/mooring-areas.json",
    campgrounds_datatable:"/api/mooring-areas/datatable_list.json",
    bulk_close:"/api/mooring-areas/bulk_close.json",
    bulk_period:"/api/mooring-areas/bulk_period.json",
    campground:function (id) {
        return "/api/mooring-areas/"+id+".json";
    },
    campground_price_history: function(id){
        return "/api/mooring-areas/"+ id +"/price_history.json";
    },
    campgroundStayHistory: function(id){
        return "/api/mooring-areas/" + id + "/stay_history.json"
    },
    campgroundCurrentStayHistory: function(id,start,end){
        return "/api/mooring-areas/" + id + "/stay_history.json?start="+start+"&end="+end;
    },
    campground_stay_history_detail: function(id){
        return "/api/mooring_stay_history/"+ id +".json";
    },
    available_campsite_classes:function (id,start,end) {
        return "/api/mooring-areas/" + id + "/available_campsite_classes.json?arrival="+start+"&departure="+end;
    },
    campground_stay_history: "/api/mooring_stay_history.json",
    addPrice: function(id){
        return "/api/mooring-areas/"+ id +"/addPrice.json";
    },
    editPrice: function(id){
        return "/api/mooring-areas/"+ id +"/updatePrice.json";
    },
    campgroundCampsites: function(id){
        return "/api/mooring-areas/" + id + "/campsites.json"
    },
    opencloseCG: function(id){
        return "/api/mooring-areas/" + id + "/open_close.json"
    },
    deleteBookingRange: function (id) {
        return "/api/mooring_booking_ranges/" + id + ".json"
    },
    campground_status_history_detail: function(id){
        return "/api/mooring_booking_ranges/"+ id +".json?original=true";
    },
    delete_campground_price: function(id){
        return "/api/mooring-areas/" + id + "/deletePrice.json";
    },
    // Campsites
    campsites:"/api/mooringsites.json",
    campsites_stay_history: "/api/campsites_stay_history.json",
    campsites_stay_history_detail: function(id){
        return "/api/campsites_stay_history/"+ id +".json";
    },
    campsites_price_history: function(id){
        return "/api/mooringsites/"+ id +"/price_history.json";
    },
    campsite_current_price:function (id,start,end) {
       return "/api/mooringsites/"+ id +"/current_price.json?arrival="+start+"&departure="+end;
    },
    campsites_status_history:function(id){
        return "/api/mooringsites/" + id + "/status_history.json?closures=True"
    },
    campsite:function (id) {
        return "/api/mooringsites/"+id+".json";
    },
    campsiteStayHistory: function(id){
        return "/api/mooringsites/" + id + "/stay_history.json"
    },
    opencloseCS: function(id){
        return "/api/mooringsites/" + id + "/open_close.json"
    },
    bulk_close_campsites: function () {
        return "/api/mooringsites/bulk_close.json"
    },
    deleteCampsiteBookingRange: function (id) {
        return "/api/campsite_booking_ranges/" + id + ".json"
    },
    campsite_status_history_detail: function(id){
        return "/api/campsite_booking_ranges/"+ id +".json?original=true";
    },
    available_campsites:function(campground,arrival,departure){
      return "/api/mooring-areas/"+campground+"/available_campsites.json?arrival="+arrival+"&departure="+departure;
    },
    available_campsites_booking:function(campground,arrival,departure,booking){
      return "/api/mooring-areas/"+campground+"/available_campsites_booking.json?arrival="+arrival+"&departure="+departure+"&booking="+booking;
    },
    features:"/api/features.json",
    campsite_rate: "/api/campsite_rate.json",
    campsiterate_detail:function (id) {
        return "/api/campsite_rate/"+id+".json"
    },
    rates:"/api/rates.json",

    // campsite types
    campsite_classes:"/api/mooringsite_classes.json",
    campsite_classes_active:"/api/mooringsite_classes.json?active_only=true",
    campsite_class:function (id) {
        return "/api/mooringsite_classes/"+id+".json"
    },
    addCampsiteClassPrice: function(id){
        return "/api/mooringsite_classes/"+id+"/addPrice.json"
    },
    editCampsiteClassPrice(id) {
        return "/api/mooringsite_classes/"+id+"/updatePrice.json"
    },
    deleteCampsiteClassPrice(id) {
        return "/api/mooringsite_classes/"+id+"/deletePrice.json"
    },
    campsiteclass_price_history: function(id){
        return "/api/mooringsite_classes/"+ id +"/price_history.json";
    },
    closureReasons:function () {
        return "/api/closureReasons.json";
    },
    openReasons:function () {
        return "/api/openReasons.json";
    },
    priceReasons:function () {
        return "/api/priceReasons.json";
    },
    maxStayReasons:function () {
        return "/api/maxStayReasons.json";
    },
    bulkPricing: function(){
        return "/api/bulkPricing";
    },
    //bookings
    bookings:"/api/booking.json",
    admissionsbookings:"/api/admissionsbooking.json",
    booking: function(id){
        return "/api/booking/"+id+".json";
    },
    booking_refunds:"/api/reports/booking_refunds",
    bookings_created_report: "/api/reports/booking-mooring-created",
    bookings_admission_created_report: "/api/reports/booking-admission-created",
    bookings_departure_report: "/api/reports/booking-mooring-departure",
    //other
    countries: "/api/countries.json",
    users: "/api/users.json",
    usersLookup: function (q) {
       return  encodeURI("/api/users.json?q="+q);
    },
    profile: "/api/profile",
    contacts:"/api/contacts.json",
    mooring_specification: "/api/mooring_specification/",
    //Must end .json otherwise will effect other urls generated based on removing the .json.
    booking_period_options: "/api/bookingPeriodOptions.json",
    booking_period : "/api/bookingPeriod.json",
    booking_period_edit : function(id){
        return "/api/bookingPeriod/" + id + "/";
    },
    booking_period_options_edit : function(id){
        return "/api/bookingPeriodOptions/" + id + "/";
    },
    global_settings: "/api/global_settings",
    rate_log: function (id){
        return "/mooringsiteratelog/" + id + "/";
    }
};
