import { defineComponent, h } from 'vue'

export const Skeleton = defineComponent({
  name: 'Skeleton',
  props: {
    class: {
      type: String,
      default: ''
    }
  },
  setup(props) {
    return () => h('div', {
      class: `animate-pulse rounded-md bg-gray-200 ${props.class}`
    })
  }
}) 