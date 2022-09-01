<template>
  <div class="drawer-container">
    <h3 class="drawer-title">Page style setting</h3>
    
    <div class="drawer-item">
      <span>Open Tags-View</span>
      <el-switch v-model="tagsView" class="drawer-switch" />
    </div>
    
    <div class="drawer-item">
      <span>Fixed Header</span>
      <el-switch v-model="fixedHeader" class="drawer-switch" />
    </div>
    
  </div>
</template>

<script>
  export default {
    name: 'Settings',
    computed: {
      tagsView: {
        get() {
          return this.$store.state.settings.tagsView
        },
        set(val) {
          this.$store.dispatch('settings/changeSetting', {
            key: 'tagsView',
            value: val
          })
        }
      },
      fixedHeader: {
        get() {
          return this.$store.state.settings.fixedHeader
        },
        set(val) {
          this.$store.dispatch('settings/changeSetting', {
            key: 'fixedHeader',
            value: val
          })
        }
      },
    }
  }
</script>

<style lang="scss" scoped>
  .drawer-container {
    padding: 24px;
    font-size: 14px;
    line-height: 1.5;
    word-wrap: break-word;
  
    .drawer-title {
      // margin-bottom: 20px;
      color: rgba(0, 0, 0, .85);
      font-size: 16px;
      line-height: 22px;
      padding-bottom: 15px;
      border-bottom: 1px solid #d8dce5;
    }
  
    .drawer-item {
      color: rgba(0, 0, 0, .65);
      font-size: 14px;
      padding: 12px 0;
    }
  
    .drawer-switch {
      float: right
    }
  }
</style>
