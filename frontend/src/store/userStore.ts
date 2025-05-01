import { reactive } from 'vue'

interface User {
  email: string
  id?: string | number
  company?: any
  [key: string]: any
}

interface UserStore {
  currentUser: User
  isAuthenticated: boolean
  setUser: (userData: User) => void
  clearUser: () => void
}

const userStore = reactive<UserStore>({
  currentUser: {} as User,
  isAuthenticated: false,

  setUser(userData: User) {
    this.currentUser = userData
    this.isAuthenticated = true
  },

  clearUser() {
    this.currentUser = {} as User
    this.isAuthenticated = false
  }
})

export default userStore 