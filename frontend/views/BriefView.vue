<template>
  <div class="brief-view">
    <div class="container">
      <h1>Информация о компании</h1>
      <form @submit.prevent="submitBrief">
        <div class="section">
          <h2>Основная информация</h2>
          
          <div class="form-group">
            <label for="company_name">Название компании *</label>
            <input
              id="company_name"
              v-model="form.company_name"
              type="text"
              required
              placeholder="ООО 'Компания'"
            />
          </div>
          
          <div class="form-group">
            <label for="industry">Сфера деятельности *</label>
            <input
              id="industry"
              v-model="form.industry"
              type="text"
              required
              placeholder="Например: Косметика, общепит, IT"
            />
          </div>
          
          <div class="form-group">
            <label for="region">Регион *</label>
            <input
              id="region"
              v-model="form.region"
              type="text"
              required
              placeholder="Москва, Санкт-Петербург и т.д."
            />
          </div>
        </div>
        
        <div class="section">
          <h2>Дополнительная информация</h2>
          
          <div class="form-group">
            <label for="brand_colors">Цвета бренда</label>
            <input
              id="brand_colors"
              v-model="form.brand_colors"
              type="text"
              placeholder="#RRGGBB, #RRGGBB"
            />
          </div>
          
          <div class="form-group">
            <label for="font">Шрифт компании</label>
            <input
              id="font"
              v-model="form.font"
              type="text"
              placeholder="Например: Roboto, Arial, Open Sans"
            />
          </div>
          
          <div class="form-group">
            <label for="logo">Логотип</label>
            <input
              id="logo"
              type="file"
              @change="handleFileUpload"
              accept="image/*"
            />
          </div>
          
          <div class="form-group">
            <label for="brand_book">Ссылка на бренд-бук</label>
            <input
              id="brand_book"
              v-model="form.brand_book_url"
              type="url"
              placeholder="https://..."
            />
          </div>
        </div>
        
        <div class="section">
          <h2>Интеграции с соцсетями</h2>
          
          <div class="form-group">
            <label for="instagram">Instagram</label>
            <input
              id="instagram"
              v-model="form.instagram"
              type="text"
              placeholder="@username или ссылка"
            />
          </div>
          
          <div class="form-group">
            <label for="tiktok">TikTok</label>
            <input
              id="tiktok"
              v-model="form.tiktok"
              type="text"
              placeholder="@username или ссылка"
            />
          </div>
          
          <div class="form-group">
            <label for="telegram">Telegram</label>
            <input
              id="telegram"
              v-model="form.telegram"
              type="text"
              placeholder="@username или ссылка"
            />
          </div>
          
          <div class="form-group">
            <label for="whatsapp">WhatsApp</label>
            <input
              id="whatsapp"
              v-model="form.whatsapp"
              type="text"
              placeholder="+7XXXXXXXXXX"
            />
          </div>
        </div>
        
        <div class="error" v-if="error">{{ error }}</div>
        
        <button type="submit" class="btn primary" :disabled="isLoading">
          {{ isLoading ? 'Сохранение...' : 'Сохранить и перейти в дэшборд' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { companyApi } from '../services/api'

const router = useRouter()
const error = ref('')
const isLoading = ref(false)

const form = reactive({
  company_name: '',
  industry: '',
  region: '',
  brand_colors: '',
  font: '',
  logo: null,
  brand_book_url: '',
  instagram: '',
  tiktok: '',
  telegram: '',
  whatsapp: ''
})

const handleFileUpload = (event) => {
  form.logo = event.target.files[0]
}

const submitBrief = async () => {
  error.value = ''
  isLoading.value = true
  
  try {
    // Здесь будет API запрос на сохранение данных компании
    await new Promise(resolve => setTimeout(resolve, 1000))
    router.push('/dashboard')
  } catch (err) {
    error.value = err.message || 'Ошибка при сохранении данных'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.brief-view {
  padding: 2rem;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

h1 {
  margin-bottom: 2rem;
  text-align: center;
}

.section {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #eee;
}

h2 {
  margin-bottom: 1rem;
  font-size: 1.2rem;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.btn {
  width: 100%;
  padding: 0.75rem;
  margin-top: 1rem;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
}

.primary {
  background-color: #3498db;
  color: white;
}

.primary:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

.error {
  color: #e74c3c;
  margin-top: 1rem;
  text-align: center;
}
</style> 