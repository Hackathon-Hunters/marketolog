<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { userStore } from '../store'
import { companyApi } from '../services/api'
import { Button } from '../components/ui/button'
import { useRouter } from 'vue-router'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '../components/ui/dialog'
import { Input } from '../components/ui/input'
import { Label } from '../components/ui/label'

interface Company {
  id: number
  name: string
  industry?: string
  region?: string
  short_about?: string
  [key: string]: any
}

interface CompanyCreate {
  name: string
  industry: string
  region: string
  short_about: string
}

const router = useRouter()
const companies = ref<Company[]>([])
const isLoading = ref(true)
const error = ref('')
const isOpen = ref(false)
const isSubmitting = ref(false)
const companyFormError = ref('')

const newCompany = ref<CompanyCreate>({
  name: '',
  industry: '',
  region: '',
  short_about: ''
})

const loadCompanies = async () => {
  isLoading.value = true
  try {
    const response = await companyApi.getAll()
    companies.value = response.data
  } catch (err: any) {
    error.value = err.response?.data?.message || 'Ошибка при загрузке компаний'
  } finally {
    isLoading.value = false
  }
}

const createCompany = async () => {
  if (!newCompany.value.name) {
    companyFormError.value = 'Название компании обязательно'
    return
  }
  
  isSubmitting.value = true
  companyFormError.value = ''
  
  try {
    await companyApi.create(newCompany.value)
    isOpen.value = false
    resetForm()
    await loadCompanies()
  } catch (err: any) {
    companyFormError.value = err.response?.data?.message || 'Ошибка при создании компании'
  } finally {
    isSubmitting.value = false
  }
}

const resetForm = () => {
  newCompany.value = {
    name: '',
    industry: '',
    region: '',
    short_about: ''
  }
  companyFormError.value = ''
}

onMounted(async () => {
  await loadCompanies()
})
</script>

<template>
  <div class="container mx-auto">
    <div class="mb-6 flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold">Список компаний</h1>
        <p class="text-gray-600">
          Текущий пользователь: {{ userStore.currentUser.email }}
        </p>
      </div>
      <Dialog v-model:open="isOpen">
        <DialogTrigger asChild>
          <Button @click="isOpen = true">Создать компанию</Button>
        </DialogTrigger>
        <DialogContent class="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Создание компании</DialogTitle>
            <DialogDescription>
              Заполните информацию о новой компании
            </DialogDescription>
          </DialogHeader>

          <form @submit.prevent="createCompany" class="grid gap-4 py-4">
            <div v-if="companyFormError" class="rounded-md bg-red-50 p-2 text-sm text-red-500">
              {{ companyFormError }}
            </div>
            
            <div class="grid gap-2">
              <Label for="company-name" required>Название*</Label>
              <Input 
                id="company-name" 
                v-model="newCompany.name" 
                placeholder="Введите название компании" 
                required
              />
            </div>
            
            <div class="grid gap-2">
              <Label for="company-industry">Отрасль</Label>
              <Input 
                id="company-industry" 
                v-model="newCompany.industry" 
                placeholder="Например: IT, Финансы, Производство"
              />
            </div>
            
            <div class="grid gap-2">
              <Label for="company-region">Регион</Label>
              <Input 
                id="company-region" 
                v-model="newCompany.region" 
                placeholder="Например: Москва, Санкт-Петербург"
              />
            </div>
            
            <div class="grid gap-2">
              <Label for="company-about">Краткое описание</Label>
              <textarea 
                id="company-about" 
                v-model="newCompany.short_about" 
                placeholder="Краткое описание компании"
                rows="3"
                class="flex h-auto min-h-[80px] w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
              ></textarea>
            </div>

            <DialogFooter>
              <Button 
                type="button" 
                variant="outline" 
                @click="isOpen = false"
                :disabled="isSubmitting"
              >
                Отмена
              </Button>
              <Button 
                type="submit" 
                :disabled="isSubmitting"
              >
                <span v-if="isSubmitting" class="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-background border-t-transparent"></span>
                Сохранить
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>

    <div v-if="isLoading" class="flex justify-center py-8">
      <div class="h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent"></div>
    </div>

    <div v-else-if="error" class="rounded-md bg-red-50 p-4 text-sm text-red-500">
      {{ error }}
    </div>

    <div v-else-if="companies.length === 0" class="py-8 text-center text-gray-500">
      Компании не найдены
    </div>

    <div v-else class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <div v-for="company in companies" :key="company.id" class="rounded-lg border bg-white p-6 shadow-sm">
        <h2 class="text-xl font-semibold">{{ company.name }}</h2>
        <div class="mt-2 text-sm text-gray-500">
          <p v-if="company.industry">Отрасль: {{ company.industry }}</p>
          <p v-if="company.region">Регион: {{ company.region }}</p>
        </div>
        <p v-if="company.short_about" class="mt-4 text-sm">{{ company.short_about }}</p>
        <div class="flex gap-2 mt-4">
          <Button 
            variant="outline"
            @click="() => router.push(`/main/company/${company.id}`)"
          >
            Подробнее
          </Button>
          <Button 
            variant="outline"
            @click="() => router.push(`/main/telegram/${company.id}`)"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.562 8.161c-.18 1.897-.962 6.502-1.359 8.627-.168.9-.5 1.201-.82 1.23-.697.064-1.226-.461-1.901-.904-1.056-.692-1.653-1.123-2.678-1.799-1.185-.781-.417-1.21.258-1.911.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.139-5.062 3.345-.479.329-.913.489-1.302.481-.428-.009-1.252-.242-1.865-.442-.752-.244-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.831-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635.099-.002.321.023.465.141.121.099.154.232.17.325.015.094.034.31.019.477z"/>
            </svg>
            Telegram
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>