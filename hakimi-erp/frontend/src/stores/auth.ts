import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

import {
  fetchMe,
  login as loginRequest,
  logout as logoutRequest,
  register as registerRequest,
  type AuthUser,
  type LoginPayload,
  type RegisterPayload,
} from '@/api/modules/auth'
import {
  clearAuth,
  getStoredAuth,
  saveAuth,
  type StoredAuthUser,
} from '@/utils/auth'


export const useAuthStore = defineStore('auth', () => {
  const stored = getStoredAuth()
  const token = ref<string | null>(stored?.token ?? null)
  const user = ref<AuthUser | null>(
    stored?.user
      ? {
          id: stored.user.id,
          username: stored.user.username,
          email: stored.user.email,
          fullName: stored.user.fullName,
          role: stored.user.role,
          isActive: stored.user.isActive,
          createdTime: stored.user.createdTime || '',
          lastLoginTime: stored.user.lastLoginTime,
        }
      : null,
  )

  const isAuthenticated = computed(() => Boolean(token.value))
  const displayName = computed(() => user.value?.fullName || user.value?.username || 'User')
  const initials = computed(() => {
    const name = displayName.value
    return name
      .split(/\s+/)
      .filter(Boolean)
      .map((part) => part[0])
      .join('')
      .slice(0, 2)
      .toUpperCase()
  })

  function applyToken(data: { accessToken: string; user: AuthUser }, remember: boolean) {
    token.value = data.accessToken
    user.value = data.user
    const storedUser: StoredAuthUser = {
      id: data.user.id,
      username: data.user.username,
      email: data.user.email,
      fullName: data.user.fullName,
      role: data.user.role,
      isActive: data.user.isActive,
      createdTime: data.user.createdTime,
      lastLoginTime: data.user.lastLoginTime,
    }
    saveAuth(data.accessToken, storedUser, remember)
  }

  async function login(payload: LoginPayload) {
    const data = await loginRequest(payload)
    applyToken(data, payload.rememberMe)
  }

  async function register(payload: RegisterPayload) {
    const data = await registerRequest(payload)
    applyToken(data, false)
  }

  async function refreshMe() {
    if (!token.value) return
    const data = await fetchMe()
    user.value = data
    saveAuth(token.value, {
      id: data.id,
      username: data.username,
      email: data.email,
      fullName: data.fullName,
      role: data.role,
      isActive: data.isActive,
      createdTime: data.createdTime,
      lastLoginTime: data.lastLoginTime,
    }, Boolean(getStoredAuth()?.remember))
  }

  async function logout() {
    if (token.value) {
      try {
        await logoutRequest()
      } catch {
        // Local logout still succeeds even if the server session already expired.
      }
    }
    token.value = null
    user.value = null
    clearAuth()
  }

  return {
    token,
    user,
    isAuthenticated,
    displayName,
    initials,
    login,
    register,
    refreshMe,
    logout,
  }
})
