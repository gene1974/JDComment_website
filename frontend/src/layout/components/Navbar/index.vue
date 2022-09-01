<template>
  <div class="navbar">
    <hamburger id="hamburger-container" class="hamburger-container" :is-active="sidebar.opened" @toggleClick="toggleSideBar"/>
    <breadcrumb id="breadcrumb-container" class="breadcrumb-container"/>
    <div class="right-menu">
      <header-search id="header-search" class="right-menu-item"/>
      <div class="right-menu-item hover-effect" @click="toggleScreenfull">
        <screenfull id="screenfull" ref="screenfull"/>
      </div>
    </div>
  </div>
</template>

<script>
  import Hamburger from '@/components/Hamburger/index.vue'
  import Breadcrumb from '@/components/Breadcrumb/index.vue'
  import Screenfull from '@/components/Screenfull/index.vue'
  import HeaderSearch from '@/components/HeaderSearch/index.vue'
  import { mapGetters } from 'vuex'
  
  export default {
    name: 'Navbar',
    components: {
      Hamburger,
      Breadcrumb,
      Screenfull,
      HeaderSearch,
    },
    computed: {
      ...mapGetters([
        'sidebar'
      ])
    },
    methods: {
      toggleSideBar() {
        this.$store.dispatch('app/toggleSideBar')
      },
      toggleScreenfull() {
        this.$refs.screenfull.clickScreenfull()
      }
    }
  }
</script>

<style lang="scss" scoped>
  .navbar {
    height: 50px;
    overflow: hidden;
    position: relative;
    background: #fff;
    box-shadow: 0 1px 4px rgba(0, 21, 41, .08);
    
    .hamburger-container {
      line-height: 46px;
      height: 100%;
      float: left;
      cursor: pointer;
      transition: background .3s;
      -webkit-tap-highlight-color:transparent;
      
      &:hover {
        background: rgba(0, 0, 0, .025);
      }
    }
    
    .breadcrumb-container {
      float: left;
    }
    
    .screenfull-container {
      float: right;
      line-height: 50px;
    }
    
    .right-menu {
      float: right;
      height: 100%;
      line-height: 50px;
      
      &:focus {
        outline: none;
      }
      
      .right-menu-item {
        display: inline-block;
        padding: 0 15px;
        height: 100%;
        font-size: 20px;
        color: #5a5e66;
        vertical-align: text-bottom;
        
        &.hover-effect {
          cursor: pointer;
          transition: background .3s;
        
          &:hover {
            background: rgba(0, 0, 0, .025)
          }
        }
      }
    }
  }
</style>
