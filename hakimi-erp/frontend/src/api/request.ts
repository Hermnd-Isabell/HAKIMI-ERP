import axios, { AxiosError, type AxiosInstance, type AxiosRequestConfig, type AxiosResponse } from 'axios'
import camelcaseKeys from 'camelcase-keys'
import snakecaseKeys from 'snakecase-keys'

export interface ApiResponse<T = unknown> {
  success: boolean
  data: T
  message?: string
  detail?: string
}

const request: AxiosInstance = axios.create({
  baseURL: '',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

request.interceptors.request.use(
  (config) => {
    // 自动转换发送的数据为 snake_case
    if (config.data && !(config.data instanceof FormData)) {
      config.data = snakecaseKeys(config.data, { deep: true })
    }
    // 自动转换 URL 参数为 snake_case
    if (config.params) {
      config.params = snakecaseKeys(config.params, { deep: true })
    }
    return config
  },
  (error) => Promise.reject(error)
)

request.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    // 自动转换接收的数据为 camelCase
    if (response.data && response.data.data) {
      response.data.data = camelcaseKeys(response.data.data, { deep: true })
    }
    return response
  },
  (error: AxiosError<ApiResponse>) => {
    let message = ''
    const data = error.response?.data
    
    if (data) {
      if (data.message) {
        message = data.message
      } else if (data.detail) {
        if (Array.isArray(data.detail)) {
          // 处理 FastAPI 422 验证错误
          message = data.detail.map(err => `${err.loc.join('.')}: ${err.msg}`).join('; ')
        } else {
          message = data.detail
        }
      }
    }

    if (!message) {
      message = error.message || 'Network error'
    }
    
    return Promise.reject(new Error(message))
  }
)

export async function get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
  const res = await request.get<ApiResponse<T>>(url, config)
  return res.data.data
}

export async function post<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<T> {
  const res = await request.post<ApiResponse<T>>(url, data, config)
  return res.data.data
}

export async function put<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<T> {
  const res = await request.put<ApiResponse<T>>(url, data, config)
  return res.data.data
}

export async function del<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
  const res = await request.delete<ApiResponse<T>>(url, config)
  return res.data.data
}

export default request
