import { defineStore } from 'pinia'
import request from '../api'

export const useUserStore = defineStore('user', {
  state: () => ({
    userInfo: null,
    isLoggedIn: false,
  }),
  actions: {
    async login(username, password) {
      const data = await request.post('/auth/login/', { username, password })
      this.userInfo = data
      this.isLoggedIn = true
      return data
    },
    async logout() {
      await request.post('/auth/logout/')
      this.userInfo = null
      this.isLoggedIn = false
    },
    async fetchUserInfo() {
      const data = await request.get('/auth/userinfo/')
      this.userInfo = data
      this.isLoggedIn = true
      return data
    },
  },
})
