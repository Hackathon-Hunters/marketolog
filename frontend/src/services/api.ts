import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig, AxiosError } from 'axios'

interface RegisterData {
  email: string
  password: string
  [key: string]: any
}

interface LoginData {
  email: string
  password: string
}

interface CompanyData {
  name: string
  [key: string]: any
}

const API_URL = 'http://localhost:8000/'

const api: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use((config: AxiosRequestConfig) => {
  const token = localStorage.getItem('token')
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  response => response,
  (error: AxiosError) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authApi = {
  register: (data: RegisterData) => api.post('/auth/register', data),
  login: (data: LoginData) => {
    const formData = new URLSearchParams()
    formData.append('username', data.email)
    formData.append('password', data.password)

    return api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
  },
  getCurrentUser: () => api.get('/auth/me'),
  getRecommendations: () => api.post('/ai-requests/generate-ideas')
}

export const companyApi = {
  create: (data: CompanyData) => api.post('/companies/create', data),
  update: (id: string | number, data: Partial<CompanyData>) =>
    api.patch(`/company/${id}`, data),
  getCurrent: () => api.get('/company/me'),
  getAll: () => api.get('/companies'),

}

export default api
