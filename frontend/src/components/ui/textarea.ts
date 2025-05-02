import { defineComponent, h } from 'vue'

export const Textarea = defineComponent({
  name: 'Textarea',
  props: {
    modelValue: {
      type: String,
      default: ''
    },
    placeholder: {
      type: String,
      default: ''
    },
    disabled: {
      type: Boolean,
      default: false
    },
    id: {
      type: String,
      default: undefined
    },
    class: {
      type: String,
      default: ''
    }
  },
  
  emits: ['update:modelValue'],
  
  setup(props, { emit }) {
    return () => h('textarea', {
      class: `flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 ${props.class}`,
      value: props.modelValue,
      placeholder: props.placeholder,
      disabled: props.disabled,
      id: props.id,
      onInput: (e: Event) => {
        const target = e.target as HTMLTextAreaElement
        if (target) {
          emit('update:modelValue', target.value)
        }
      }
    })
  }
}) 