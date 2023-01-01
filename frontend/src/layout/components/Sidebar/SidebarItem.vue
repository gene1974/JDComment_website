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
      resolve(...paths){
        let resolvePath = '';
        let isAbsolutePath = false;
        for(let i = paths.length-1; i > -1; i--){
            let path = paths[i];
            if(isAbsolutePath){
                break;
            }
            if(!path){
                continue
            }
            resolvePath = path + '/' + resolvePath;
            isAbsolutePath = path.charCodeAt(0) === 47;
        }
        if(/^\/+$/.test(resolvePath)){
            resolvePath = resolvePath.replace(/(\/+)/,'/')
        }else{
            resolvePath = resolvePath.replace(/(?!^)\w+\/+\.{2}\//g, '')
            .replace(/(?!^)\.\//g,'')
            .replace(/\/+$/, '')
        }
        return resolvePath;
    },
      resolvePath(routePath) {
        return this.resolve(this.basePath, routePath)
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
