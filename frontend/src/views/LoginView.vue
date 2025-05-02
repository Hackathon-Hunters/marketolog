<script setup lang="ts">
import { Button } from '../components/ui/button'
import {
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '../components/ui/form'
import { Input } from '../components/ui/input'
import { useRouter } from 'vue-router'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import { ref } from 'vue'
import * as z from 'zod'
import { authApi } from '../services/api'

const router = useRouter()
const isLoading = ref(false)
const error = ref('')

const formSchema = toTypedSchema(z.object({
  email: z.string().email({ message: 'Введите корректный email' }),
  password: z.string().min(1, { message: 'Введите пароль' }),
}))

const form = useForm({
  validationSchema: formSchema,
})

const { handleSubmit } = form

const onSubmit = handleSubmit(async (values) => {
  isLoading.value = true
  error.value = ''
  
  try {
    const response = await authApi.login({
      email: values.email,
      password: values.password
    })
    localStorage.setItem('token', response.data.access_token)
    router.push('/main')
  } catch (err: any) {
    error.value = err.response?.data?.message || 'Ошибка при входе'
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="container mx-auto max-w-md py-12">
    <div class="rounded-lg border bg-slate-50 p-8 shadow-md">
      <h1 class="mb-6 text-2xl font-bold">Вход</h1>
      <form @submit="onSubmit" class="space-y-4">
        <FormField v-slot="{ componentField }" name="email">
          <FormItem v-auto-animate>
            <FormLabel>Email</FormLabel>
            <FormControl>
              <Input type="email" placeholder="Введите email" v-bind="componentField" />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>
        
        <FormField v-slot="{ componentField }" name="password">
          <FormItem v-auto-animate>
            <FormLabel>Пароль</FormLabel>
            <FormControl>
              <Input type="password" placeholder="Введите пароль" v-bind="componentField" />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

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