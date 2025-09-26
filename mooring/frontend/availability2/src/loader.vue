<template lang="html">
  <div v-show="isLoading"  >
    <div class="container">
      <div class="row" style='width: 200px; border: 1px solid #ddd; background-color: #FFF;' >
        <div class="col-lg-12">
          <i class="fa fa-4x fa-spinner fa-spin"></i>
        </div>
        <div class="col-lg-12" style="margin-top:20px;">
          <slot></slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name:'spinnerLoader',
  props:{
      isLoading:{
          default:function () {
              return false;
          }
      }
  }
}
</script>
