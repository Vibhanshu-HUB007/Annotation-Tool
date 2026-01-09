import api from './client'
import { useAuthStore } from '../store/authStore'

export interface LoginCredentials {
  username: string
  password: string
}

export interface RegisterData {
  username: string
  email: string
  password: string
  full_name?: string
  role?: string
}

export const authApi = {
  login: async (credentials: LoginCredentials) => {
    const params = new URLSearchParams()
    params.append('username', credentials.username)
    params.append('password', credentials.password)
    
    const response = await api.post('/auth/login', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    
    const { access_token, user } = response.data
    useAuthStore.getState().setAuth(user, access_token)
    return { token: access_token, user }
  },

  register: async (data: RegisterData) => {
    const response = await api.post('/auth/register', data)
    return response.data
  },

  getCurrentUser: async () => {
    const response = await api.get('/auth/me')
    return response.data
  },

  logout: () => {
    useAuthStore.getState().logout()
  },
}
