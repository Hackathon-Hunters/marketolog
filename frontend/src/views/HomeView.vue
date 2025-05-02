<template>
  <div class="landing-page">
    <header class="hero">
      <div class="hero-content">
        <h1>AI Маркетолог</h1>
        <p class="subtitle">Автоматизируйте ваш маркетинг с помощью искусственного интеллекта</p>
        <div class="actions">
          <router-link to="/register" class="btn primary">Начать бесплатно</router-link>
          <router-link to="/login" class="btn secondary">Войти</router-link>
        </div>
      </div>
      <div class="hero-image">
        <img src="/hero-image.svg" alt="AI Маркетолог" />
      </div>
    </header>

    <section class="features">
      <h2>Что умеет наш сервис</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">🤖</div>
          <h3>AI-генерация идей</h3>
          <p>Автоматическая генерация маркетинговых идей для постов в социальных сетях</p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">🖼️</div>
          <h3>Генерация изображений</h3>
          <p>Создание уникальных изображений для ваших постов</p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">#️⃣</div>
          <h3>Умные хештеги</h3>
          <p>Автоматический подбор релевантных хештегов для максимального охвата</p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">📊</div>
          <h3>Аналитика и метрики</h3>
          <p>Отслеживание эффективности ваших постов и кампаний</p>
        </div>
      </div>
    </section>

    <section class="how-it-works">
      <h2>Как это работает</h2>
      <div class="steps">
        <div class="step">
          <div class="step-number">1</div>
          <h3>Создайте аккаунт</h3>
          <p>Зарегистрируйтесь и заполните информацию о вашей компании</p>
        </div>
        
        <div class="step">
          <div class="step-number">2</div>
          <h3>Получите рекомендации</h3>
          <p>AI проанализирует вашу нишу и предложит идеи для контента</p>
        </div>
        
        <div class="step">
          <div class="step-number">3</div>
          <h3>Создайте пост</h3>
          <p>Отредактируйте предложенные идеи и опубликуйте их</p>
        </div>
      </div>
    </section>

    <section class="cta">
      <h2>Готовы автоматизировать ваш маркетинг?</h2>
      <p>Присоединяйтесь к тысячам бизнесов, которые уже используют AI для создания контента</p>
      <div class="actions">
        <router-link to="/register" class="btn primary">Регистрация</router-link>
        <router-link to="/login" class="btn secondary">Вход</router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
</script>

<style scoped>
.landing-page {
  width: 100%;
  max-width: 100%;
  margin: 0;
  padding: 0;
}

.hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4rem 10%;
  background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
  color: var(--color-primary-foreground);
  border-radius: 0 0 2rem 2rem;
}

.hero-content {
  flex: 1;
  max-width: 600px;
}

.hero-image {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.hero-image img {
  max-width: 100%;
  height: auto;
}

h1 {
  font-size: 3.5rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.subtitle {
  font-size: 1.5rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.actions {
  display: flex;
  gap: 1rem;
}

.btn {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  text-align: center;
  transition: all 0.3s ease;
}

.primary {
  background-color: var(--color-background);
  color: var(--color-primary);
}

.secondary {
  background-color: transparent;
  color: var(--color-primary-foreground);
  border: 2px solid var(--color-primary-foreground);
}

.primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.secondary:hover {
  background-color: rgba(255, 255, 255, 0.1);
  transform: translateY(-3px);
}

section {
  padding: 5rem 2rem;
  text-align: center;
}

h2 {
  font-size: 2.5rem;
  margin-bottom: 3rem;
  color: var(--color-foreground);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background-color: var(--color-card);
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: var(--color-foreground);
}

.steps {
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
  max-width: 1200px;
  margin: 0 auto;
}

.step {
  flex: 1;
  min-width: 250px;
  max-width: 350px;
  background-color: var(--color-card);
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  position: relative;
}

.step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 3rem;
  height: 3rem;
  background-color: var(--color-primary);
  color: var(--color-primary-foreground);
  border-radius: 50%;
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 auto 1.5rem;
}

.cta {
  background-color: var(--color-accent);
  color: var(--color-accent-foreground);
  border-radius: 2rem 2rem 0 0;
}

.cta .actions {
  justify-content: center;
  margin-top: 2rem;
}

@media (max-width: 768px) {
  .hero {
    flex-direction: column;
    text-align: center;
  }
  
  .hero-content {
    margin-bottom: 2rem;
  }
  
  .steps {
    flex-direction: column;
    align-items: center;
  }
  
  .actions {
    flex-direction: column;
  }
  
  h1 {
    font-size: 2.5rem;
  }
  
  h2 {
    font-size: 2rem;
  }
}
</style> 