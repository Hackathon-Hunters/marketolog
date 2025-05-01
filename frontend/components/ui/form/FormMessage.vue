<template>
  <p
    v-if="!!message"
    :class="cn('text-sm font-medium text-red-500', className)"
    :id="id"
  >
    {{ message }}
  </p>
</template>

<script setup>
import { cn } from '../../../lib/utils'

defineProps({
  id: {
    type: String,
    default: ''
  },
  message: {
    type: String,
    default: ''
  },
  className: {
    type: String,
    default: ''
  }
})
</script> 