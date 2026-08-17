export interface StoredAuthUser {
  id: number
  username: string
  email: string
  fullName?: string | null
  role: string
  isActive: boolean
  createdTime?: string
  lastLoginTime?: string | null
}

export interface StoredAuth {
  token: string
  user: StoredAuthUser
  remember: boolean
}

const TOKEN_KEY = 'hakimi-auth-token'
const USER_KEY = 'hakimi-auth-user'
const REMEMBER_KEY = 'hakimi-auth-remember'

function tokenStorage(remember: boolean): Storage {
  return remember ? window.localStorage : window.sessionStorage
}

export function saveAuth(token: string, user: StoredAuthUser, remember: boolean): void {
  clearAuth()
  const storage = tokenStorage(remember)
  storage.setItem(TOKEN_KEY, token)
  storage.setItem(USER_KEY, JSON.stringify(user))
  storage.setItem(REMEMBER_KEY, remember ? '1' : '0')
}

export function getStoredAuth(): StoredAuth | null {
  if (typeof window === 'undefined') return null

  const localToken = window.localStorage.getItem(TOKEN_KEY)
  const sessionToken = window.sessionStorage.getItem(TOKEN_KEY)
  const storage = localToken ? window.localStorage : window.sessionStorage
  const token = storage.getItem(TOKEN_KEY)
  if (!token) return null

  try {
    const user = storage.getItem(USER_KEY)
    if (!user) return null
    return {
      token,
      user: JSON.parse(user) as StoredAuthUser,
      remember: storage === window.localStorage,
    }
  } catch {
    clearAuth()
    return null
  }
}

export function getAuthToken(): string | null {
  return getStoredAuth()?.token ?? null
}

export function clearAuth(): void {
  if (typeof window === 'undefined') return
  window.localStorage.removeItem(TOKEN_KEY)
  window.localStorage.removeItem(USER_KEY)
  window.localStorage.removeItem(REMEMBER_KEY)
  window.sessionStorage.removeItem(TOKEN_KEY)
  window.sessionStorage.removeItem(USER_KEY)
  window.sessionStorage.removeItem(REMEMBER_KEY)
}
