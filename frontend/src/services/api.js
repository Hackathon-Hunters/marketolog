import axios from 'axios'

const API_URL = '/api'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Интерцептор для добавления токена в заголовки запросов
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Интерцептор для обработки ошибок
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authApi = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => {
    // В FastAPI с OAuth2PasswordRequestForm ожидаются поля username и password
    const formData = new URLSearchParams();
    formData.append('username', data.email); // Email используется как username
    formData.append('password', data.password);
    
    return api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
  },
  getCurrentUser: () => api.get('/auth/me')
}

export const companyApi = {
  create: (data) => api.post('/company', data),
  update: (id, data) => api.patch(`/company/${id}`, data),
  getCurrent: () => api.get('/company/me')
}

export default api 