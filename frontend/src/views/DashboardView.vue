<script setup>
import { useRouter } from 'vue-router'
import { Button } from '../components/ui/button'
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import AppSidebar from "@/components/AppSidebar.vue"
import userStore from '../store/userStore'
import RecomendationsView from './RecomendationsView.vue'
import RecommendationSkeleton from '../components/RecommendationSkeleton.vue'
const router = useRouter()
</script>

<template>
  <div class="rounded-lg">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Дашборд</h1>
      <Button @click="router.push('/main/publication')" variant="secondary">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v3m0 0v3m0-3h3m-3 0H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        Создать публикацию
      </Button>
    </div>
    
    <div v-if="userStore.currentUser.company">
      <h2 class="text-xl font-semibold mb-4">Рекомендации для вашей компании</h2>
      <Suspense>
        <template #default>
          <RecomendationsView />
        </template>
        <template #fallback>
          <RecommendationSkeleton />
        </template>
      </Suspense>
    </div>
    <div v-else class="p-4 bg-amber-50 rounded-md mb-4">
      <h2 class="text-xl font-semibold mb-2">Информация о компании отсутствует</h2>
      <p class="mb-4">Пожалуйста, добавьте информацию о вашей компании, чтобы получить персонализированные рекомендации.</p>
      <Button @click="router.push('/main/info')" class="mt-2">
        Добавить информацию о компании
      </Button>
    </div>
  </div>
</template>