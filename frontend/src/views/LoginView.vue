<template>
  <div class="container mx-auto max-w-md py-12">
    <div class="rounded-lg border bg-slate-50 p-8 shadow-md">
      <h1 class="mb-6 text-2xl font-bold">Вход в аккаунт</h1>
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <FormItem>
          <Label for="email">Email</Label>
          <Input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="Введите email"
            required
          />
          <FormMessage :message="errors.email" />
        </FormItem>

        <FormItem>
          <Label for="password">Пароль</Label>
          <Input
            id="password"
            v-model="form.password"
            type="password"
            placeholder="Введите пароль"
            required
          />
          <FormMessage :message="errors.password" />
        </FormItem>

        <div v-if="error" class="rounded-md bg-red-50 p-3 text-sm text-red-500">
          {{ error }}
        </div>

        <Button type="submit" class="w-full" :disabled="isLoading">
          {{ isLoading ? 'Вход...' : 'Войти' }}
        </Button>

        <div class="text-center text-sm">
          Нет аккаунта?
          <router-link to="/register" class="text-blue-600 hover:underline">
            Зарегистрироваться
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '../services/api'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Label } from '../components/ui/label'
import { FormItem, FormMessage } from '../components/ui/form'

const router = useRouter()
const isLoading = ref(false)
const error = ref('')

const form = reactive({
  email: '',
  password: ''
})

const errors = reactive({
  email: '',
  password: ''
})

const validateForm = () => {
  let isValid = true
  
  // Сбросить все ошибки
  errors.email = ''
  errors.password = ''
  
  // Валидация email
  if (!form.email.trim()) {
    errors.email = 'Email обязателен'
    isValid = false
  } else if (!/\S+@\S+\.\S+/.test(form.email)) {
    errors.email = 'Введите корректный email'
    isValid = false
  }
  
  // Валидация пароля
  if (!form.password.trim()) {
    errors.password = 'Пароль обязателен'
    isValid = false
  }
  
  return isValid
}

const handleSubmit = async () => {
  // Проверяем валидность формы
  if (!validateForm()) return
  
  isLoading.value = true
  error.value = ''
  
  try {
    const response = await authApi.login({
      email: form.email.trim(),
      password: form.password
    })
    
    console.log('Auth response:', response.data)
    
    // Сохраняем токен в localStorage
    // Бэкенд возвращает access_token, а не token
    localStorage.setItem('token', response.data.access_token)
    
    // Перенаправляем на страницу брифа
    router.push('/brief')
  } catch (err) {
    console.error('Login error:', err)
    error.value = err.response?.data?.detail || 'Неверный email или пароль'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-view {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 2rem;
}

.form-container {
  width: 100%;
  max-width: 400px;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  background-color: white;
}

h1 {
  margin-bottom: 1.5rem;
  text-align: center;
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

.form-footer {
  margin-top: 1.5rem;
  text-align: center;
}

.form-footer a {
  margin-left: 0.5rem;
  color: #3498db;
  text-decoration: none;
}
</style> 