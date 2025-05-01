<template>
  <div class="register-view">
    <div class="form-container">
      <h1>Регистрация</h1>
      <form @submit.prevent="register">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            placeholder="your@email.com"
          />
        </div>
        
        <div class="form-group">
          <label for="password">Пароль</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            placeholder="********"
          />
        </div>
        
        <div class="form-group">
          <label for="confirm_password">Подтверждение пароля</label>
          <input
            id="confirm_password"
            v-model="confirmPassword"
            type="password"
            required
            placeholder="********"
          />
        </div>
        
        <button type="submit" class="btn primary" :disabled="isLoading">
          {{ isLoading ? 'Загрузка...' : 'Зарегистрироваться' }}
        </button>
        
        <div class="error" v-if="error">{{ error }}</div>
        
        <div class="form-footer">
          <span>Уже есть аккаунт?</span>
          <router-link to="/login">Войти</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')
const isLoading = ref(false)

const register = async () => {
  error.value = ''
  
  if (password.value !== confirmPassword.value) {
    error.value = 'Пароли не совпадают'
    return
  }
  
  isLoading.value = true
  
  try {
    // Здесь будет API запрос на регистрацию
    await new Promise(resolve => setTimeout(resolve, 1000))
    router.push('/brief')
  } catch (err) {
    error.value = err.message || 'Ошибка при регистрации'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.register-view {
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