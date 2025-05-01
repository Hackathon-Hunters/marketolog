<template>
  <div class="container mx-auto max-w-md py-12">
    <div class="rounded-lg border bg-slate-50 p-8 shadow-md">
      <h1 class="mb-6 text-2xl font-bold">Регистрация</h1>
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

        <FormItem>
          <Label for="passwordConfirm">Подтверждение пароля</Label>
          <Input
            id="passwordConfirm"
            v-model="form.passwordConfirm"
            type="password"
            placeholder="Повторите пароль"
            required
          />
          <FormMessage :message="errors.passwordConfirm" />
        </FormItem>

        <div v-if="error" class="rounded-md bg-red-50 p-3 text-sm text-red-500">
          {{ error }}
        </div>

        <Button type="submit" class="w-full" :disabled="isLoading">
          {{ isLoading ? 'Регистрация...' : 'Зарегистрироваться' }}
        </Button>

        <div class="text-center text-sm">
          Уже есть аккаунт?
          <router-link to="/login" class="text-blue-600 hover:underline">
            Войти
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
  password: '',
  passwordConfirm: ''
})

const errors = reactive({
  email: '',
  password: '',
  passwordConfirm: ''
})

const validateForm = () => {
  let isValid = true
  
  // Сбросить все ошибки
  errors.email = ''
  errors.password = ''
  errors.passwordConfirm = ''
  
  // Валидация email
  if (!form.email) {
    errors.email = 'Email обязателен'
    isValid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = 'Введите корректный email'
    isValid = false
  }
  
  // Валидация пароля
  if (!form.password) {
    errors.password = 'Пароль обязателен'
    isValid = false
  } else if (form.password.length < 6) {
    errors.password = 'Пароль должен быть не менее 6 символов'
    isValid = false
  }
  
  // Валидация подтверждения пароля
  if (form.password !== form.passwordConfirm) {
    errors.passwordConfirm = 'Пароли не совпадают'
    isValid = false
  }
  
  return isValid
}

const handleSubmit = async () => {
  if (!validateForm()) return
  
  isLoading.value = true
  error.value = ''
  
  try {
    const response = await authApi.register({
      email: form.email,
      password: form.password
    })
    
    // Сохраняем токен в localStorage
    localStorage.setItem('token', response.data.token)
    
    // Перенаправляем на страницу брифа
    router.push('/brief')
  } catch (err) {
    error.value = err.response?.data?.message || 'Ошибка при регистрации'
  } finally {
    isLoading.value = false
  }
}
</script> 