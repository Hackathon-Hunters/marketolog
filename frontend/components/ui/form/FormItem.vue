<template>
  <div :class="cn('space-y-2', className)">
    <slot></slot>
  </div>
</template>

<script setup>
import { cn } from '../../../lib/utils'

defineProps({
  className: {
    type: String,
    default: ''
  }
})
</script> 