<template>
  <div v-if="!item.hidden">
    <template v-if="hasOneShowingChild(item.children, item) && (!onlyOneChild.children||onlyOneChild.noShowingChildren)">
      <app-link v-if="onlyOneChild.meta" :to="resolvePath(onlyOneChild.path)">
        <el-menu-item :index="resolvePath(onlyOneChild.path)" :class="{'submenu-title-noDropdown':!isNest}">
          <item :icon="onlyOneChild.meta.icon||(item.meta&&item.meta.icon)" :title="onlyOneChild.meta.title"></item>
        </el-menu-item>
      </app-link>
    </template>
    
    <el-submenu v-else ref="subMenu" :index="resolvePath(item.path)" popper-append-to-body>
      <template slot="title">
        <item v-if="item.meta" :icon="item.meta&&item.meta.icon" :title="item.meta.title"></item>
      </template>
      <sidebar-item v-for="child in item.children" 
      :key="child.path"
      :is-nest="true"
      :item="child"
      :base-path="resolvePath(child.path)"
      class="nest-menu"/>
    </el-submenu>
  </div>
</template>

<script>
  import path from 'path'
  import AppLink from './Link.vue'
  import Item from './Item.vue'
  
  export default {
    name: 'SidebarItem',
    components: {
      AppLink,
      Item,
    },
    props: {
      item: {
        type: Object,
        required: true
      },
      basePath: {
        type: String,
        default: ''
      },
      isNest: {
        type: Boolean,
        default: false
      }
    },
    data() {
      return {
        onlyOneChild: null
      }
    },
    methods: {
      resolvePath(routePath) {
        return path.resolve(this.basePath, routePath)
      },
      hasOneShowingChild(children=[], parent) {
        const showingChildren = children.filter(item=>{return !item.hidden})
        if (showingChildren.length === 1) {
          this.onlyOneChild = showingChildren[0]
          return true
        } else if (showingChildren.length === 0) {
          this.onlyOneChild = { ... parent, path:'', noShowingChildren: true}
          return true
        }
        return false
      }
    }
  }
</script>

<style>
</style>
