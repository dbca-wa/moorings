export default {
    
    park_price_history:function (id) {
       return "/api/admissions/price_history.json";
    },
    park_get_price: function(){
        return "/api/admissions/get_price_by_location.json";
    },
    park_add_price:function () {
       return  "/api/admissions/add_price.json";
    },
    park_entry_rate:function (id) {
      return "/api/admissions/"+id+".json";
    },
    addPrice: function(id){
        return "/api/mooring-areas/"+ id +"/addPrice.json";
    },
    editPrice: function(id){
        return "/api/mooring-areas/"+ id +"/updatePrice.json";
    },
    addCampsiteClassPrice: function(id){
        return "/api/mooringsite_classes/"+id+"/addPrice.json"
    },
    editCampsiteClassPrice(id) {
        return "/api/admissions/"+id+"/updatePrice.json"
    },
    priceReasons:function () {
        return "/api/admissionsReasons.json";
    },
    profile: "/api/profile",
};
