export default {
    
    park_price_history:function (id) {
       return window.parkstayUrl + "/api/admissions/price_history.json";
    },
    park_get_price: function(){
        return window.parkstayUrl + "/api/admissions/get_price_by_location.json";
    },
    park_add_price:function () {
       return  window.parkstayUrl + "/api/admissions/add_price.json";
    },
    park_entry_rate:function (id) {
      return window.parkstayUrl + "/api/admissions/"+id+".json";
    },
    addPrice: function(id){
        return window.parkstayUrl + "/api/mooring-areas/"+ id +"/addPrice.json";
    },
    editPrice: function(id){
        return window.parkstayUrl + "/api/mooring-areas/"+ id +"/updatePrice.json";
    },
    addCampsiteClassPrice: function(id){
        return window.parkstayUrl + "/api/mooringsite_classes/"+id+"/addPrice.json"
    },
    editCampsiteClassPrice(id) {
        return window.parkstayUrl + "/api/admissions/"+id+"/updatePrice.json"
    },
    priceReasons:function () {
        return window.parkstayUrl + "/api/admissionsReasons.json";
    },
    profile: import.meta.env.VITE_PARKSTAY_URL + "/api/profile",
};
