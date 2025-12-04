<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { companyApi, telegramApi } from '../services/api'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Label } from '../components/ui/label'

interface Company {
  id: number
  name: string
  industry: string
  region: string
  short_about: string
  long_about?: string
  brand_colors?: string
  brand_font?: string
  logo_url?: string
  brand_book_url?: string
  telegram_bot_token?: string
  telegram_chat_id?: string
}

const route = useRoute()
const router = useRouter()

const company = ref<Company | null>(null)
const isLoading = ref(true)
const isSaving = ref(false)
const error = ref('')
const success = ref('')
const isEditing = ref(false)

const formData = ref<Partial<Company>>({})

const telegramStatus = ref({
  is_configured: false,
  masked_token: ''
})

const loadCompany = async () => {
  isLoading.value = true
  error.value = ''
  
  try {
    const companyId = route.params.id as string
    const response = await companyApi.getById(companyId)
    company.value = response.data
    formData.value = { ...response.data }
    
    // Загружаем статус Telegram
    try {
      const telegramResponse = await telegramApi.getSettings(parseInt(companyId))
      telegramStatus.value = telegramResponse.data
    } catch {
      // Игнорируем ошибку если настройки не найдены
    }
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Ошибка при загрузке компании'
  } finally {
    isLoading.value = false
  }
}

const saveCompany = async () => {
  if (!company.value) return
  
  isSaving.value = true
  error.value = ''
  success.value = ''
  
  try {
    await companyApi.update(company.value.id, formData.value)
    success.value = 'Изменения сохранены'
    isEditing.value = false
    await loadCompany()
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Ошибка при сохранении'
  } finally {
    isSaving.value = false
  }
}

const cancelEdit = () => {
  formData.value = { ...company.value }
  isEditing.value = false
}

onMounted(() => {
  loadCompany()
})
</script>

<template>
  <div class="max-w-3xl">
    <div class="flex items-center gap-4 mb-6">
      <Button variant="ghost" size="sm" @click="router.push('/main/info')">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        Назад
      </Button>
      <h1 class="text-2xl font-bold">{{ company?.name || 'Загрузка...' }}</h1>
    </div>
    
    <div v-if="isLoading" class="flex justify-center py-12">
      <div class="h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent"></div>
    </div>
    
    <div v-else-if="error && !company" class="rounded-md bg-red-50 p-4 text-sm text-red-600">
      {{ error }}
    </div>
    
    <div v-else-if="company" class="space-y-6">
      <!-- Статус Telegram -->
      <div class="bg-white rounded-lg border p-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-500" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.562 8.161c-.18 1.897-.962 6.502-1.359 8.627-.168.9-.5 1.201-.82 1.23-.697.064-1.226-.461-1.901-.904-1.056-.692-1.653-1.123-2.678-1.799-1.185-.781-.417-1.21.258-1.911.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.139-5.062 3.345-.479.329-.913.489-1.302.481-.428-.009-1.252-.242-1.865-.442-.752-.244-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.831-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635.099-.002.321.023.465.141.121.099.154.232.17.325.015.094.034.31.019.477z"/>
          </svg>
          <div>
            <p class="font-medium">Telegram</p>
            <p class="text-sm text-gray-500">
              {{ telegramStatus.is_configured ? 'Подключено' : 'Не настроено' }}
            </p>
          </div>
        </div>
        <Button 
          variant="outline" 
          size="sm"
          @click="router.push(`/main/telegram/${company.id}`)"
        >
          {{ telegramStatus.is_configured ? 'Изменить' : 'Настроить' }}
        </Button>
      </div>
      
      <!-- Информация о компании -->
      <div class="bg-white rounded-lg border p-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-semibold">Информация о компании</h2>
          <Button 
            v-if="!isEditing" 
            variant="outline" 
            size="sm"
            @click="isEditing = true"
          >
            Редактировать
          </Button>
        </div>
        
        <!-- Сообщения -->
        <div v-if="error" class="mb-4 rounded-md bg-red-50 p-3 text-sm text-red-600">
          {{ error }}
        </div>
        <div v-if="success" class="mb-4 rounded-md bg-green-50 p-3 text-sm text-green-600">
          {{ success }}
        </div>
        
        <form v-if="isEditing" @submit.prevent="saveCompany" class="space-y-4">
          <div class="grid gap-4 md:grid-cols-2">
            <div class="space-y-2">
              <Label for="name">Название</Label>
              <Input id="name" v-model="formData.name" />
            </div>
            
            <div class="space-y-2">
              <Label for="industry">Отрасль</Label>
              <Input id="industry" v-model="formData.industry" />
            </div>
            
            <div class="space-y-2">
              <Label for="region">Регион</Label>
              <Input id="region" v-model="formData.region" />
            </div>
            
            <div class="space-y-2">
              <Label for="brand_colors">Цвета бренда</Label>
              <Input id="brand_colors" v-model="formData.brand_colors" placeholder="#FF5733, #3498DB" />
            </div>
          </div>
          
          <div class="space-y-2">
            <Label for="short_about">Краткое описание</Label>
            <textarea 
              id="short_about" 
              v-model="formData.short_about"
              rows="2"
              class="flex w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            ></textarea>
          </div>
          
          <div class="space-y-2">
            <Label for="long_about">Подробное описание</Label>
            <textarea 
              id="long_about" 
              v-model="formData.long_about"
              rows="4"
              class="flex w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            ></textarea>
          </div>
          
          <div class="flex gap-3 pt-2">
            <Button type="submit" :disabled="isSaving">
              <span v-if="isSaving" class="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-background border-t-transparent"></span>
              {{ isSaving ? 'Сохранение...' : 'Сохранить' }}
            </Button>
            <Button type="button" variant="outline" @click="cancelEdit">
              Отмена
            </Button>
          </div>
        </form>
        
        <!-- Просмотр -->
        <div v-else class="space-y-4">
          <div class="grid gap-4 md:grid-cols-2">
            <div>
              <p class="text-sm text-gray-500">Название</p>
              <p class="font-medium">{{ company.name }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Отрасль</p>
              <p class="font-medium">{{ company.industry || '—' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Регион</p>
              <p class="font-medium">{{ company.region || '—' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Цвета бренда</p>
              <p class="font-medium">{{ company.brand_colors || '—' }}</p>
            </div>
          </div>
          
          <div>
            <p class="text-sm text-gray-500">Краткое описание</p>
            <p>{{ company.short_about || '—' }}</p>
          </div>
          
          <div v-if="company.long_about">
            <p class="text-sm text-gray-500">Подробное описание</p>
            <p class="whitespace-pre-line">{{ company.long_about }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

