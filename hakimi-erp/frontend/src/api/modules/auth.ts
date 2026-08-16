import { get, post } from '../request'
import { AUTH_API } from '@/constants/api'

export interface AuthUser {
  id: number
  username: string
  email: string
  fullName?: string | null
  role: string
  isActive: boolean
  createdTime: string
  lastLoginTime?: string | null
}

export interface LoginPayload {
  account: string
  password: string
  rememberMe: boolean
}

export interface RegisterPayload {
  username: string
  email: string
  password: string
  fullName?: string
}

export interface AuthToken {
  accessToken: string
  tokenType: string
  expiresAt: string
  user: AuthUser
}

export function login(payload: LoginPayload) {
  return post<AuthToken>(AUTH_API.login, payload)
}

export function register(payload: RegisterPayload) {
  return post<AuthToken>(AUTH_API.register, payload)
}

export function fetchMe() {
  return get<AuthUser>(AUTH_API.me)
}

export function logout() {
  return post<boolean>(AUTH_API.logout)
}
