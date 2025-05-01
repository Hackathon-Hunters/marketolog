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
import { h } from 'vue'
import * as z from 'zod'
import { authApi } from '../services/api'

const router = useRouter()

const formSchema = toTypedSchema(z.object({
  email: z.string().email(),
  password: z.string().min(1).max(50),
}))

const form = useForm({
  validationSchema: formSchema,
})

const { handleSubmit } = form

const onSubmit = handleSubmit(async (values) => {
  console.log(values)

  try {
    const response = await authApi.login({
      email: values.email,
      password: values.password
    })
    localStorage.setItem('token', response.data.access_token)
    router.push('/main')
  } catch (err) {
    console.error('Login error:', err)
  }
})
</script>

<template>
  <form class="w-2/3 space-y-6" @submit="onSubmit">
    <FormField v-slot="{ componentField }" name="email">
      <FormItem v-auto-animate>
        <FormLabel>Email</FormLabel>
        <FormControl>
          <Input type="email" placeholder="your@email.com" v-bind="componentField" />
        </FormControl>
        <FormMessage />
      </FormItem>
    </FormField>
    <FormField v-slot="{ componentField }" name="password">
      <FormItem v-auto-animate>
        <FormLabel>Password</FormLabel>
        <FormControl>
          <Input type="password" placeholder="password" v-bind="componentField" />
        </FormControl>
        <FormMessage />
      </FormItem>
    </FormField>
    <Button type="submit">
      Submit
    </Button>
  </form>
</template>