<script setup lang="ts">
import { ref } from 'vue'
import { Button } from '../components/ui/button'
import { Textarea } from '../components/ui/textarea'
import axios from 'axios'
import PublicationSkeleton from '../components/PublicationSkeleton.vue'

const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const prompt = ref('')
const isLoading = ref(false)
const error = ref('')
const generatedPost = ref<any>(null)
const isPromptValid = ref(false)
const copySuccess = ref(false)

const validatePrompt = () => {
  isPromptValid.value = prompt.value.length >= 10
  return isPromptValid.value
}

const onSubmit = async (e: Event) => {
  e.preventDefault()
  
  if (!validatePrompt()) return
  
  isLoading.value = true
  error.value = ''
  
  try {
    const token = localStorage.getItem('token')
    const response = await axios.post(`${baseUrl}/ai-requests/generate-post`, {
      prompt: prompt.value
    }, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    
    generatedPost.value = response.data
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Ошибка при генерации поста'
    console.error('Ошибка:', err)
  } finally {
    isLoading.value = false
  }
}

const resetForm = () => {
  prompt.value = ''
  generatedPost.value = null
  isPromptValid.value = false
  copySuccess.value = false
}

const copyPostText = async () => {
  if (!generatedPost.value?.description) return
  
  try {
    let textToCopy = generatedPost.value.title 
      ? `${generatedPost.value.title}\n\n${generatedPost.value.description}` 
      : generatedPost.value.description
      
    // Добавляем хештеги, если они есть
    if (generatedPost.value.hashtags && generatedPost.value.hashtags.length) {
      const hashtagsText = generatedPost.value.hashtags.join(' ')
      textToCopy += `\n\n${hashtagsText}`
    }
    
    await navigator.clipboard.writeText(textToCopy)
    copySuccess.value = true
    
    // Сбрасываем статус успешного копирования через 2 секунды
    setTimeout(() => {
      copySuccess.value = false
    }, 2000)
  } catch (err) {
    console.error('Ошибка при копировании текста:', err)
  }
}

const downloadImage = (imageBase64: string) => {
  if (!imageBase64) return
  
  // Создаем ссылку для скачивания
  const downloadLink = document.createElement('a')
  downloadLink.href = `data:image/jpeg;base64,${imageBase64}`
  downloadLink.download = `publication_image_${new Date().getTime()}.jpg`
  
  // Добавляем ссылку в DOM, кликаем по ней и удаляем
  document.body.appendChild(downloadLink)
  downloadLink.click()
  document.body.removeChild(downloadLink)
}
</script>

<template>
  <div class="rounded-lg">
    <h1 class="text-2xl font-bold mb-6">Генерация публикации</h1>
    
    <form @submit="onSubmit" class="space-y-4">
      <div class="space-y-2">
        <label for="prompt" class="block text-sm font-medium">
          Опишите, какую публикацию вы хотите сгенерировать
        </label>
        <Textarea 
          id="prompt"
          :modelValue="prompt"
          @update:modelValue="(value: string) => { prompt = value; validatePrompt(); }"
          placeholder="Например: Напиши пост о преимуществах нашего нового продукта для социальных сетей"
          class="w-full min-h-[120px]"
          :disabled="isLoading"
        />
        <p v-if="prompt && !isPromptValid" class="text-sm text-red-500">
          Опишите запрос подробнее (минимум 10 символов)
        </p>
      </div>
      
      <div v-if="error" class="rounded-md bg-red-50 p-3 text-sm text-red-500">
        {{ error }}
      </div>
      
      <Button type="submit" class="w-full" :disabled="isLoading || !isPromptValid">
        <template v-if="isLoading">
          <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Генерация...
        </template>
        <template v-else>
          Сгенерировать публикацию
        </template>
      </Button>
    </form>
    
    <!-- Скелетон загрузки -->
    <PublicationSkeleton v-if="isLoading" />
    
    <!-- Результат генерации -->
    <div v-if="generatedPost" class="mt-8">
      <div class="bg-white rounded-lg border shadow-sm overflow-hidden">
        <!-- Превью карточки публикации -->
        <div class="p-5">
          <!-- Заголовок публикации -->
          <h3 class="text-xl font-bold mb-3 text-center" v-if="generatedPost.title">
            {{ generatedPost.title }}
          </h3>
          
          <!-- Картинка публикации -->
          <div v-if="generatedPost.image_base64" class="mb-4 relative aspect-square max-h-[400px] overflow-hidden rounded-md mx-auto max-w-md">
            <img 
              :src="`data:image/jpeg;base64,${generatedPost.image_base64}`" 
              alt="Изображение для публикации" 
              class="w-full h-full object-contain absolute inset-0"
            />
            <div class="absolute bottom-2 right-2">
              <Button 
                size="sm" 
                variant="secondary" 
                class="bg-white/70 hover:bg-white/90 text-gray-700 text-xs"
                @click="downloadImage(generatedPost.image_base64)"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                Скачать
              </Button>
            </div>
          </div>
          <div v-else class="mb-4 bg-gray-100 rounded-md flex items-center justify-center h-60 aspect-square max-h-[400px] mx-auto max-w-md">
            <p class="text-gray-500">Изображение будет сгенерировано позже</p>
          </div>
          
          <!-- Текст публикации -->
          <div class="mb-4" v-if="generatedPost.description">
            <p class="text-gray-700 whitespace-pre-line">{{ generatedPost.description }}</p>
          </div>
          
          <!-- Хештеги -->
          <div class="flex flex-wrap gap-2 mb-4" v-if="generatedPost.hashtags && generatedPost.hashtags.length">
            <span 
              v-for="(hashtag, index) in generatedPost.hashtags" 
              :key="index"
              class="inline-flex items-center rounded-full bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700"
            >
              {{ hashtag }}
            </span>
          </div>
        </div>
        
        <!-- Кнопки действий -->
        <div class="flex justify-between items-center border-t p-4 bg-gray-50">
          <div>
            <Button variant="outline" size="sm" @click="resetForm">
              Создать новую
            </Button>
          </div>
          <div class="flex gap-2">
            <Button 
              variant="outline" 
              size="sm" 
              @click="copyPostText"
              :class="{ 'bg-green-50 text-green-700 border-green-200': copySuccess }"
            >
              {{ copySuccess ? 'Скопировано!' : 'Копировать текст' }}
            </Button>
            <Button size="sm">
              Сохранить публикацию
            </Button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
