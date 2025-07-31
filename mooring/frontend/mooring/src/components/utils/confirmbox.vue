/**
* confirmBox components
* author: Tawanda Nyakudjga
* date: 9/10/2016
* alertOptions:{
    icon:"<i class='fa fa-exclamation-triangle fa-2x text-danger' aria-hidden='true'></i>",
    message:"Are you sure you want to Delete!!!" ,
    buttons:[
        {
          text:"Delete",
          event: "delete",
          bsColor:"btn-danger",
          handler:function(e) {

             vm.showAlert();
          },
          autoclose:true
        }
    ]
    }
**/
<template lang="html" id="confirmbox">
    <div :id="confirmModal" class="modal fade">
      <div class="modal-dialog modal-sm">
      <div class="modal-content">
          <!-- dialog body -->
          <div class="modal-body">
          <div class="row">
              <div :id="icon" class="col-sm-12 text-center" style="font-size:75px; ">
                  <!--icon goes here-->
              </div>
              <div class="col-sm-12 text-center">
                  <p :id="text"><!--modal text--></p>
              </div>
          </div>
          </div>
          <!-- dialog buttons -->
          <div  class="modal-footer">
              <div class="row">
                  <div class="col-lg-12" :id="buttons">
                      <!--buttons-->
                  </div>
              </div>
          </div>
      </div>
      </div>
  </div>
</template>

<script>
import {$} from '../../hooks.js'
import {bus} from './eventBus.js'

export default {
    data:function () {
        return {
            confirmModal: '',
            icon: '',
            text: '',
            buttons: '',
            eventHandler: Array(),
        }
    },
    props:{
        options:{
            required:true,
            type:Object
        },
        id:{
            required:true
        },
        cancelText:{
            default:function () {
                return "Cancel";
            }
        }
    },
    methods:{
        confirmBox:function(json){
            let vm = this;
            var Obj = json;
            var confirmModal = $("#"+vm.confirmModal);
            var icon = $("#"+vm.icon);
            var text = $("#"+vm.text);
            var buttons = ("#"+vm.buttons);
            var passed_id = Obj.id;
            var autoclose =(typeof Obj.autoclose != "undefined")? Obj.autoclose: true;
            $(icon).html(Obj.icon);
            $(text).html(Obj.message);
            $(buttons).html("");
            if (typeof Obj.buttons != "undefined")
            {
               $.each(Obj.buttons, function (i, btn)
               {
                   var eventHandler = (typeof btn.handler != "undefined") ? btn.handler : "@click";
                   $(buttons).append("<button type=\"button\" data-click="+btn.event+" class=\"btn " + btn.bsColor + "\" style='margin-bottom:10px;margin-right:10px;'>" + btn.text + "</button>");
                   $(function () {
                          if(passed_id === vm.id){
                               $('button[data-click]').on('click',function () {

                                   if ($(this).attr('data-click') ==  btn.event) {
                                      btn.handler();
                                   }
                                   if(autoclose){
                                       vm.hideConfirmModal();
                                   }
                               });
                          }
                   })
               });
            }
            $(buttons).append(`<button type="button" class="btn btn-primary cancel-btn" style="margin-bottom:10px;">${vm.cancelText}</button>`);
                $(buttons).find('.cancel-btn').on('click', function () {
                     vm.hideConfirmModal();
                });
        },
        showConfirmModal:function() {
            const $modal = $("#"+this.confirmModal);
            $modal.addClass('show');
            $modal.css('display', 'block');
            $('body').addClass('modal-open');

             $('<div class="modal-backdrop fade show confirm-box-modal"></div>').appendTo(document.body);
        },
        hideConfirmModal:function() {
            const $modal = $("#"+this.confirmModal);

            $modal.removeClass('show');
            $modal.css('display', 'none');
            $('body').removeClass('modal-open');

            $('.modal-backdrop.fade.show.confirm-box-modal').remove();
        }

   },
   mounted:function () {
       var vm = this;
       vm.confirmBox(this.options);
       bus.on('showAlert', function(id) {
            if(id === vm.id){
            vm.showConfirmModal();
            }
        });
    },
    created() {
        this._uid  = Math.random().toString(36).substring(2, 16);
        this.confirmModal = 'confirmModal' + this._uid;
        this.icon = 'modalIcon' + this._uid;
        this.text = 'mdalText' + this._uid;
        this.buttons = 'modalButtons' + this._uid;
  }
}

</script>

<style scoped>
    .modal-body,.modal-footer {
        background-color: #fff;
        color: #333;
    }
    .modal-footer .btn+.btn {
        margin-bottom: 10px;
        margin-left: 5px;
    }
    .modal-backdrop {
        background-color: rgba(128, 128, 128, 0.3);
        opacity: 1 !important;
    }
</style>
