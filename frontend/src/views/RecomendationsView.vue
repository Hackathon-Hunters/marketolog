<script setup lang="ts">
import { authApi } from '../services/api'
import { onMounted, ref } from 'vue'
import { Button } from '../components/ui/button'
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from '../components/ui/carousel'

const recommendations = ref<any[]>([])
const isLoading = ref(true)
const error = ref('')

async function fetchRecommendations() {
  isLoading.value = true
  try {
    const response = await authApi.getRecommendations()
    recommendations.value = response.data.ideas || []
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Ошибка загрузки рекомендаций'
  } finally {
    isLoading.value = false
  }
}

await fetchRecommendations()
</script>

<template>
  <div class="space-y-6">
    <div v-if="isLoading" class="flex justify-center py-6">
      <div class="text-center">
        <svg class="animate-spin h-8 w-8 text-primary mx-auto mb-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <p>Загрузка рекомендаций...</p>
      </div>
    </div>

    <div v-else-if="error" class="rounded-md bg-red-50 p-4 text-red-500">
      {{ error }}
    </div>

    <div v-else-if="recommendations.length === 0" class="text-center py-6">
      <p>Рекомендации пока не доступны</p>
    </div>

    <div v-else>
      <Carousel class="w-full max-w-3xl mx-auto">
        <CarouselContent>
          <CarouselItem v-for="(recommendation, index) in recommendations" :key="index" class="md:basis-1/1">
            <div class="rounded-lg border bg-white p-6 shadow-sm h-full">
              <div class="mb-4">
                <h3 class="text-xl font-semibold mb-2">{{ recommendation.title }}</h3>
                <p class="text-gray-700">{{ recommendation.description }}</p>
              </div>
              
              <div v-if="recommendation.benefits && recommendation.benefits.length > 0" class="mb-4">
                <h4 class="font-medium mb-2">Преимущества:</h4>
                <ul class="list-disc ml-5 space-y-1">
                  <li v-for="(benefit, benefitIndex) in recommendation.benefits" :key="benefitIndex">
                    {{ benefit }}
                  </li>
                </ul>
              </div>
              
              <div v-if="recommendation.hashtags && recommendation.hashtags.length > 0" class="flex flex-wrap gap-2 mb-4">
                <span v-for="(hashtag, hashtagIndex) in recommendation.hashtags" :key="hashtagIndex" 
                      class="inline-flex items-center rounded-full bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700">
                  {{ hashtag }}
                </span>
              </div>

              <div class="mb-4">
                <h4 class="font-medium mb-1">Промпт для изображения:</h4>
                <p class="text-sm text-gray-600 italic">{{ recommendation.image_prompt }}</p>
              </div>

              <Button class="w-full">Использовать идею</Button>
            </div>
          </CarouselItem>
        </CarouselContent>
        <CarouselPrevious />
        <CarouselNext />
      </Carousel>
    </div>
  </div>
</template>