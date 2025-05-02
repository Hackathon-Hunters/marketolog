<script setup lang="ts">
import { Skeleton } from './ui/skeleton'
</script>

<template>
  <div class="space-y-8">
    <!-- Скелетон для карусели -->
    <div class="relative w-full max-w-3xl mx-auto">
      <!-- Скелетон карточки -->
      <div class="rounded-lg border bg-white p-6 shadow-sm h-full">
        <!-- Заголовок -->
        <Skeleton class="h-7 w-3/4 mb-4" />
        
        <!-- Описание -->
        <div class="space-y-2 mb-6">
          <Skeleton class="h-4 w-full" />
          <Skeleton class="h-4 w-5/6" />
          <Skeleton class="h-4 w-4/6" />
        </div>
        
        <!-- Преимущества -->
        <div class="mb-4">
          <Skeleton class="h-5 w-1/3 mb-2" />
          <div class="space-y-2 ml-5">
            <Skeleton class="h-4 w-2/3" />
            <Skeleton class="h-4 w-3/4" />
            <Skeleton class="h-4 w-1/2" />
          </div>
        </div>
        
        <!-- Хештеги -->
        <div class="flex flex-wrap gap-2 mb-4">
          <Skeleton class="h-6 w-20 rounded-full" />
          <Skeleton class="h-6 w-24 rounded-full" />
          <Skeleton class="h-6 w-16 rounded-full" />
          <Skeleton class="h-6 w-28 rounded-full" />
        </div>
        
        <!-- Промпт для изображения -->
        <Skeleton class="h-5 w-1/2 mb-2" />
        <Skeleton class="h-20 w-full mb-4" />
        
        <!-- Кнопка -->
        <Skeleton class="h-9 w-full" />
      </div>
      
      <!-- Скелетоны для кнопок навигации -->
      <div class="absolute left-2 top-1/2 -translate-y-1/2 z-10">
        <Skeleton class="h-8 w-8 rounded-full" />
      </div>
      <div class="absolute right-2 top-1/2 -translate-y-1/2 z-10">
        <Skeleton class="h-8 w-8 rounded-full" />
      </div>
    </div>
  </div>
</template> 