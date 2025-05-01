<template>
  <div class="home-view">
    <h1>AI-маркетолог для Instagram-магазинов</h1>
    <div class="actions">
      <router-link to="/register" class="btn primary">Регистрация</router-link>
      <router-link to="/login" class="btn secondary">Вход</router-link>
    </div>
  </div>
</template>

<script setup>
// Главная страница
</script>

<style scoped>
.home-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 2rem;
}

h1 {
  margin-bottom: 2rem;
  text-align: center;
}

.actions {
  display: flex;
  gap: 1rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 600;
}

.primary {
  background-color: #3498db;
  color: white;
}

.secondary {
  background-color: #ecf0f1;
  color: #2c3e50;
}
</style> 