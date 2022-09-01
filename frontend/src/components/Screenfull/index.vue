<template>
  <div>
    <svg-icon :icon-class="isFullscreen? 'exit-fullscreen':'fullscreen'" />
  </div>
</template>

<script>
  import screenfull from 'screenfull'
  
  export default {
    name: 'Screenfull',
    data() {
      return {
        isFullscreen: false
      }
    },
    mounted() {
      this.init()
    },
    beforeDestroy() {
      this.destroy()
    },
    methods: {
      clickScreenfull() {
        if (!screenfull.enabled) {
          this.$message({
            message: 'Full screen can not work',
            type: 'warning'
          })
          return false
        }
        screenfull.toggle()
      },
      change() {
        this.isFullscreen = screenfull.isFullscreen
      },
      init() {
        if (screenfull.enabled) {
          screenfull.on('change', this.change)
        }
      },
      destroy() {
        if (screenfull.enabled) {
          screenfull.off('change', this.change)
        }
      }
    }
  }
</script>

<style scoped>
</style>
