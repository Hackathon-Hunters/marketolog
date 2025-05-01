import { createApp } from 'vue'
import './index.css'
import router from './router/index'
import App from './App.vue'
import { authApi } from './services/api'
import { userStore } from './store'

// Инициализируем загрузку данных пользователя, если есть токен
const initUserData = async () => {
  const token = localStorage.getItem('token')
  if (token) {
    try {
      const response = await authApi.getCurrentUser()
      userStore.setUser(response.data)
    } catch (error) {
      console.error('Ошибка при загрузке данных пользователя:', error)
      localStorage.removeItem('token')
    }
  }
}

// Загружаем данные пользователя перед монтированием приложения
initUserData().then(() => {
  const app = createApp(App)
  app.use(router)
  app.mount('#app')
})
