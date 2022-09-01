<script>
  export default {
    name: 'Item',
    functional: true,
    props: {
      icon: {
        type: String,
        default: ''
      },
      title: {
        type: String,
        default: ''
      }
    },
    render: function (h, context) {
      const {icon, title} = context.props
      const vnodes = []
      if (icon) {
        if (icon.includes('el-icon')) {
          vnodes.push(<i class={[icon, 'sub-el-icon']} />)
        } else {
          vnodes.push(<svg-icon icon-class={icon}/>)
        }
      }
      if (title) {
        vnodes.push(<span slot='title'>{(title)}</span>)
      }
      
      return vnodes
    }
    // render: function (createElement, context) {
    //   const vnodes = []
    //   const { icon, title } = context.props
    //   if (icon) {
    //     const elHtml = createElement('i', {
    //       attrs: {
    //         class: icon,
    //       }
    //     })
    //     console.log(elHtml);
    //     vnodes.push(elHtml)
    //   }
    //   if (title) {
    //     const elHtml = createElement('span', {
    //       attrs: {
    //         slot: 'title'
    //       }
    //     }, title)
    //     console.log(elHtml);
    //     vnodes.push(elHtml)
    //   }
    //   return vnodes
    // }
  }
</script>

<style scoped>
.sub-el-icon {
  color: currentColor;
  width: 1em;
  height: 1em;
}
</style>
