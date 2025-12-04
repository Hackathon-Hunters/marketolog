<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Button } from '../components/ui/button'
import { Textarea } from '../components/ui/textarea'
import axios from 'axios'
import PublicationSkeleton from '../components/PublicationSkeleton.vue'
import { telegramApi, companyApi } from '../services/api'

const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const prompt = ref('')
const isLoading = ref(false)
const error = ref('')
const generatedPost = ref<any>(null)
const isPromptValid = ref(false)
const copySuccess = ref(false)
const isSendingToTelegram = ref(false)
const telegramSuccess = ref(false)
const telegramError = ref('')
const companies = ref<any[]>([])
const selectedCompanyId = ref<number | null>(null)
const isTelegramConfigured = ref(false)

// Загрузка компаний и проверка настроек Telegram
const loadCompanies = async () => {
  try {
    const response = await companyApi.getAll()
    companies.value = response.data
    
    if (companies.value.length > 0) {
      selectedCompanyId.value = companies.value[0].id
      await checkTelegramSettings()
    }
  } catch (err) {
    console.error('Ошибка при загрузке компаний:', err)
  }
}

const checkTelegramSettings = async () => {
  if (!selectedCompanyId.value) return
  
  try {
    const response = await telegramApi.getSettings(selectedCompanyId.value)
    isTelegramConfigured.value = response.data.is_configured
  } catch (err) {
    isTelegramConfigured.value = false
  }
}

const sendToTelegram = async () => {
  if (!generatedPost.value || !selectedCompanyId.value) return
  
  isSendingToTelegram.value = true
  telegramError.value = ''
  telegramSuccess.value = false
  
  try {
    await telegramApi.sendPost({
      company_id: selectedCompanyId.value,
      title: generatedPost.value.title,
      description: generatedPost.value.description,
      hashtags: generatedPost.value.hashtags,
      image_base64: generatedPost.value.image_base64
    })
    
    telegramSuccess.value = true
    setTimeout(() => {
      telegramSuccess.value = false
    }, 3000)
  } catch (err: any) {
    telegramError.value = err.response?.data?.detail || 'Ошибка при отправке в Telegram'
  } finally {
    isSendingToTelegram.value = false
  }
}

// Проверяем наличие предзагруженного поста из sessionStorage
onMounted(async () => {
  await loadCompanies()
  
  const storedPost = sessionStorage.getItem('generatedPost')
  if (storedPost) {
    try {
      generatedPost.value = JSON.parse(storedPost)
      // Очищаем sessionStorage после использования
      sessionStorage.removeItem('generatedPost')
    } catch (err) {
      console.error('Ошибка при парсинге сохраненного поста:', err)
      sessionStorage.removeItem('generatedPost')
    }
  }
})

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
        
        <!-- Отправка в Telegram -->
        <div class="border-t p-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-500" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.562 8.161c-.18 1.897-.962 6.502-1.359 8.627-.168.9-.5 1.201-.82 1.23-.697.064-1.226-.461-1.901-.904-1.056-.692-1.653-1.123-2.678-1.799-1.185-.781-.417-1.21.258-1.911.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.139-5.062 3.345-.479.329-.913.489-1.302.481-.428-.009-1.252-.242-1.865-.442-.752-.244-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.831-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635.099-.002.321.023.465.141.121.099.154.232.17.325.015.094.034.31.019.477z"/>
              </svg>
              <span class="font-medium">Отправить в Telegram</span>
            </div>
            
            <div class="flex items-center gap-3">
              <!-- Выбор компании если их несколько -->
              <select 
                v-if="companies.length > 1"
                v-model="selectedCompanyId"
                @change="checkTelegramSettings"
                class="text-sm border rounded-md px-2 py-1.5 bg-white"
              >
                <option v-for="company in companies" :key="company.id" :value="company.id">
                  {{ company.name }}
                </option>
              </select>
              
              <Button 
                v-if="isTelegramConfigured"
                size="sm"
                :disabled="isSendingToTelegram"
                @click="sendToTelegram"
                :class="{ 'bg-green-600 hover:bg-green-700': telegramSuccess }"
              >
                <span v-if="isSendingToTelegram" class="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-background border-t-transparent"></span>
                <svg v-else-if="telegramSuccess" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                {{ telegramSuccess ? 'Отправлено!' : isSendingToTelegram ? 'Отправка...' : 'Отправить' }}
              </Button>
              
              <div v-else class="flex items-center gap-2">
                <span class="text-sm text-amber-600">Настройте Telegram</span>
                <Button 
                  size="sm" 
                  variant="outline"
                  @click="$router.push(`/main/telegram/${selectedCompanyId}`)"
                >
                  Настроить
                </Button>
              </div>
            </div>
          </div>
          
          <!-- Ошибка Telegram -->
          <div v-if="telegramError" class="mt-3 rounded-md bg-red-50 p-2 text-sm text-red-600">
            {{ telegramError }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
