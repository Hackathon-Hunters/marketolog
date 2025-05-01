<template>
  <div class="flex min-h-screen">
    <SidebarProvider>
      <AppSidebar />
      <main class="flex-1">
        <SidebarTrigger />
        <div class="container mx-auto px-4 py-8">
          <div class="rounded-lg border bg-slate-50 p-8 shadow-md">
            <h1 class="mb-6 text-2xl font-bold">Заполнение брифа компании</h1>
            
            <div v-if="isLoading" class="flex justify-center py-4">
              <p>Загрузка данных...</p>
            </div>
            
            <div v-else>
              <p class="text-lg mb-8">Добро пожаловать, {{ user.email }}! Заполните информацию о вашей компании.</p>
              <Button @click="logout" variant="outline" class="mt-4">Выйти из аккаунта</Button>
            </div>
          </div>
        </div>
      </main>
    </SidebarProvider>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '../services/api'
import { Button } from '../components/ui/button'
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import AppSidebar from "@/components/AppSidebar.vue";

const router = useRouter()
const isLoading = ref(true)
const user = ref({})
const error = ref('')

const fetchCurrentUser = async () => {
  isLoading.value = true
  
  try {
    const response = await authApi.getCurrentUser()
    user.value = response.data
  } catch (err) {
    error.value = 'Ошибка при загрузке данных пользователя'
    localStorage.removeItem('token')
    router.push('/login')
  } finally {
    isLoading.value = false
  }
}

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

onMounted(() => {
  fetchCurrentUser()
})
</script>

<style scoped>
.flex {
  display: flex;
}

.min-h-screen {
  min-height: 100vh;
}

.flex-1 {
  flex: 1;
}

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