<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { telegramApi } from '../services/api'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Label } from '../components/ui/label'

const route = useRoute()

const companyId = ref<number>(0)
const isLoading = ref(true)
const isSaving = ref(false)
const isTesting = ref(false)
const error = ref('')
const success = ref('')

const settings = ref({
  telegram_bot_token: '',
  telegram_chat_id: '',
  is_configured: false,
  masked_token: ''
})

const formData = ref({
  telegram_bot_token: '',
  telegram_chat_id: ''
})

const loadSettings = async () => {
  isLoading.value = true
  error.value = ''
  
  try {
    const response = await telegramApi.getSettings(companyId.value)
    settings.value = {
      telegram_bot_token: response.data.telegram_bot_token || '',
      telegram_chat_id: response.data.telegram_chat_id || '',
      is_configured: response.data.is_configured,
      masked_token: response.data.telegram_bot_token || ''
    }
    formData.value.telegram_chat_id = response.data.telegram_chat_id || ''
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Ошибка при загрузке настроек'
  } finally {
    isLoading.value = false
  }
}

const saveSettings = async () => {
  isSaving.value = true
  error.value = ''
  success.value = ''
  
  try {
    const dataToSave: any = {
      telegram_chat_id: formData.value.telegram_chat_id
    }
    
    // Отправляем токен только если он был изменён
    if (formData.value.telegram_bot_token) {
      dataToSave.telegram_bot_token = formData.value.telegram_bot_token
    }
    
    await telegramApi.updateSettings(companyId.value, dataToSave)
    success.value = 'Настройки успешно сохранены'
    formData.value.telegram_bot_token = ''
    await loadSettings()
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Ошибка при сохранении настроек'
  } finally {
    isSaving.value = false
  }
}

const testConnection = async () => {
  isTesting.value = true
  error.value = ''
  success.value = ''
  
  try {
    const response = await telegramApi.testConnection(companyId.value)
    success.value = response.data.message
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Ошибка при тестировании подключения'
  } finally {
    isTesting.value = false
  }
}

onMounted(async () => {
  companyId.value = parseInt(route.params.companyId as string)
  if (companyId.value) {
    await loadSettings()
  }
})
</script>

<template>
  <div class="max-w-2xl">
    <h1 class="text-2xl font-bold mb-6">Настройки Telegram</h1>
    
    <div class="bg-white rounded-lg border p-6">
      <!-- Статус подключения -->
      <div class="mb-6 flex items-center gap-2">
        <div 
          :class="[
            'w-3 h-3 rounded-full',
            settings.is_configured ? 'bg-green-500' : 'bg-gray-300'
          ]"
        ></div>
        <span class="text-sm text-gray-600">
          {{ settings.is_configured ? 'Подключение настроено' : 'Подключение не настроено' }}
        </span>
      </div>
      
      <!-- Инструкция -->
      <div class="mb-6 p-4 bg-blue-50 rounded-md text-sm">
        <p class="font-medium text-blue-800 mb-2">Как настроить:</p>
        <ol class="list-decimal list-inside text-blue-700 space-y-1">
          <li>Создайте бота через <a href="https://t.me/BotFather" target="_blank" class="underline">@BotFather</a> и получите токен</li>
          <li>Добавьте бота в ваш канал/группу как администратора</li>
          <li>Для канала: Chat ID имеет формат <code class="bg-blue-100 px-1 rounded">@channel_username</code> или числовой ID</li>
          <li>Для группы: отправьте сообщение и получите Chat ID через API</li>
        </ol>
      </div>
      
      <div v-if="isLoading" class="flex justify-center py-8">
        <div class="h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent"></div>
      </div>
      
      <form v-else @submit.prevent="saveSettings" class="space-y-4">
        <!-- Ошибка -->
        <div v-if="error" class="rounded-md bg-red-50 p-3 text-sm text-red-600">
          {{ error }}
        </div>
        
        <!-- Успех -->
        <div v-if="success" class="rounded-md bg-green-50 p-3 text-sm text-green-600">
          {{ success }}
        </div>
        
        <!-- Токен бота -->
        <div class="space-y-2">
          <Label for="bot-token">Токен бота</Label>
          <div v-if="settings.masked_token" class="text-sm text-gray-500 mb-1">
            Текущий токен: {{ settings.masked_token }}
          </div>
          <Input 
            id="bot-token"
            v-model="formData.telegram_bot_token"
            type="password"
            :placeholder="settings.masked_token ? 'Введите новый токен для изменения' : 'Введите токен бота'"
          />
          <p class="text-xs text-gray-500">
            Формат: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz
          </p>
        </div>
        
        <!-- Chat ID -->
        <div class="space-y-2">
          <Label for="chat-id">Chat ID или @username канала</Label>
          <Input 
            id="chat-id"
            v-model="formData.telegram_chat_id"
            placeholder="@mychannel или -1001234567890"
          />
          <p class="text-xs text-gray-500">
            Для каналов используйте @username или числовой ID (начинается с -100)
          </p>
        </div>
        
        <!-- Кнопки -->
        <div class="flex gap-3 pt-4">
          <Button type="submit" :disabled="isSaving">
            <span v-if="isSaving" class="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-background border-t-transparent"></span>
            {{ isSaving ? 'Сохранение...' : 'Сохранить настройки' }}
          </Button>
          
          <Button 
            type="button" 
            variant="outline" 
            :disabled="!settings.is_configured || isTesting"
            @click="testConnection"
          >
            <span v-if="isTesting" class="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-primary border-t-transparent"></span>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {{ isTesting ? 'Проверка...' : 'Проверить подключение' }}
          </Button>
        </div>
      </form>
    </div>
  </div>
</template>

