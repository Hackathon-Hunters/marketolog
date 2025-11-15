<script setup lang="ts">
import { authApi } from '../services/api'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Button } from '../components/ui/button'
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from '../components/ui/carousel'

const router = useRouter()
const recommendations = ref<any[]>([])
const isLoading = ref(true)
const error = ref('')
const generatingPostId = ref<number | null>(null)

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

async function useIdea(recommendation: any, index: number) {
  generatingPostId.value = index
  
  try {
    // Формируем промпт из данных рекомендации
    const prompt = `${recommendation.title}. ${recommendation.description}`
    
    // Вызываем API генерации поста
    const response = await authApi.generatePost(prompt)
    const generatedPost = response.data
    
    // Сохраняем сгенерированный пост в sessionStorage для передачи на страницу публикации
    sessionStorage.setItem('generatedPost', JSON.stringify(generatedPost))
    
    // Переходим на страницу публикации
    router.push('/main/publication')
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Ошибка при генерации поста'
    console.error('Ошибка при генерации поста:', err)
  } finally {
    generatingPostId.value = null
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

              <Button 
                class="w-full" 
                @click="useIdea(recommendation, index)"
                :disabled="generatingPostId === index"
              >
                <template v-if="generatingPostId === index">
                  <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Генерация...
                </template>
                <template v-else>
                  Использовать идею
                </template>
              </Button>
            </div>
          </CarouselItem>
        </CarouselContent>
        <CarouselPrevious />
        <CarouselNext />
      </Carousel>
    </div>
  </div>
</template>