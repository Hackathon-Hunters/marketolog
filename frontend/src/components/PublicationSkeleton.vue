<script setup lang="ts">
import { Skeleton } from './ui/skeleton'
</script>

<template>
  <div class="mt-8">
    <div class="bg-white rounded-lg border shadow-sm overflow-hidden">
      <!-- Превью карточки публикации -->
      <div class="p-5">
        <!-- Заголовок публикации -->
        <div class="flex justify-center mb-3">
          <Skeleton class="h-7 w-2/3" />
        </div>
        
        <!-- Картинка публикации -->
        <div class="mb-4 relative aspect-square max-h-[400px] bg-gray-100 rounded-md mx-auto max-w-md">
          <Skeleton class="absolute inset-0 h-full w-full" />
        </div>
        
        <!-- Текст публикации -->
        <div class="mb-4">
          <div class="space-y-2">
            <Skeleton class="h-4 w-full" />
            <Skeleton class="h-4 w-full" />
            <Skeleton class="h-4 w-5/6" />
            <Skeleton class="h-4 w-full" />
            <Skeleton class="h-4 w-3/4" />
          </div>
        </div>
        
        <!-- Хештеги -->
        <div class="flex flex-wrap gap-2 mb-4">
          <Skeleton class="h-6 w-20 rounded-full" />
          <Skeleton class="h-6 w-24 rounded-full" />
          <Skeleton class="h-6 w-16 rounded-full" />
          <Skeleton class="h-6 w-28 rounded-full" />
        </div>
      </div>
      
      <!-- Кнопки действий -->
      <div class="flex justify-between items-center border-t p-4 bg-gray-50">
        <div>
          <Skeleton class="h-9 w-28" />
        </div>
        <div class="flex gap-2">
          <Skeleton class="h-9 w-32" />
          <Skeleton class="h-9 w-40" />
        </div>
      </div>
    </div>
  </div>
</template> 