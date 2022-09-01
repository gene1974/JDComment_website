<template>
  <div>
    <el-scrollbar wrap-class="scrollbar-wrapper">
      <el-menu 
      :default-active="activeMenu"
      :collapse="isCollapse"
      :background-color="variables.menuBg"
      :text-color="variables.menuText"
      :active-text-color="variables.menuActiveText"
      :collapse-transition="false"
      :unique-opened="false"
      mode="vertical"
      >
        <sidebar-item v-for="route in routes" :key="route.path" :item="route" :base-path="route.path" />
      </el-menu>
    </el-scrollbar>
  </div>
</template>

<script>
  import variables from '@/styles/variables.scss'
  import SidebarItem from './SidebarItem.vue'
  import { routes } from '@/router/index.js'
  import { mapGetters } from 'vuex'

  export default {
    name: 'Sidebar',
    components: {
      SidebarItem
    },
    computed: {
      ...mapGetters([
        'sidebar'
      ]),
      routes() {
        return routes
      },
      activeMenu() {
        const {meta, path} = this.$route
        if (meta.activeMenu) {
          return meta.activeMenu
        }
        return path
      },
      variables() {
        return variables
      },
      isCollapse() {
        return !this.sidebar.opened
      }
    },
  }
</script>

<style scoped>
</style>
