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
  <div class="container mx-auto py-8">
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
        <Button 
          class="mt-4" 
          variant="outline"
          @click="() => router.push(`/company/${company.id}`)"
        >
          Подробнее
        </Button>
      </div>
    </div>
  </div>
</template>