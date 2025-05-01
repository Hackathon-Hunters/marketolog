<template>
  <div class="container mx-auto max-w-md py-12">
    <div class="rounded-lg border bg-slate-50 p-8 shadow-md">
      <h1 class="mb-6 text-2xl font-bold">Регистрация</h1>
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
        
        <FormField v-slot="{ componentField }" name="passwordConfirm">
          <FormItem v-auto-animate>
            <FormLabel>Подтверждение пароля</FormLabel>
            <FormControl>
              <Input type="password" placeholder="Повторите пароль" v-bind="componentField" />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

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

<script setup lang="ts">
import { Button } from '../components/ui/button'
import {
  FormControl,
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
  password: z.string().min(6, { message: 'Пароль должен быть не менее 6 символов' }),
  passwordConfirm: z.string()
}).refine(data => data.password === data.passwordConfirm, {
  message: 'Пароли не совпадают',
  path: ['passwordConfirm']
}))

const form = useForm({
  validationSchema: formSchema,
})

const { handleSubmit } = form

const onSubmit = handleSubmit(async (values) => {
  isLoading.value = true
  error.value = ''
  
  try {
    const response = await authApi.register({
      email: values.email,
      password: values.password
    })
    
    localStorage.setItem('token', response.data.token)
    router.push('/brief')
  } catch (err: any) {
    error.value = err.response?.data?.message || 'Ошибка при регистрации'
  } finally {
    isLoading.value = false
  }
})
</script> 