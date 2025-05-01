<template>
  <component
    :is="tag"
    :class="buttonVariants({ variant, size, class: className })"
    :disabled="disabled"
    v-bind="buttonProps"
  >
    <slot></slot>
  </component>
</template>

<script setup>
import { buttonVariants } from './utils'
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'default',
  },
  size: {
    type: String,
    default: 'default',
  },
  tag: {
    type: String,
    default: 'button',
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  className: {
    type: String,
    default: '',
  },
})

const buttonProps = computed(() => {
  const { variant, size, className, ...rest } = props
  return rest
})
</script> 