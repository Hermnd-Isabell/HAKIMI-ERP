import { ElMessage, ElMessageBox } from 'element-plus'
import type { MessageBoxData } from 'element-plus'

export interface ToastOptions {
  message: string
  duration?: number
  showClose?: boolean
}

const TOAST_CLASS = 'hakimi-toast-bottom'

function showToast({
  message,
  duration = 3000,
  showClose = false,
}: ToastOptions) {
  ElMessage({
    message,
    duration,
    showClose,
    customClass: TOAST_CLASS,
    grouping: true,
  })
}

export const toast = {
  success(message: string, nextStep?: string) {
    const fullMessage = nextStep ? `${message}，${nextStep}` : message
    showToast({ message: fullMessage, duration: 3000, showClose: false })
  },

  error(message: string) {
    showToast({ message, duration: 0, showClose: true })
  },

  warning(message: string) {
    showToast({ message, duration: 5000, showClose: true })
  },

  info(message: string) {
    showToast({ message, duration: 3000, showClose: false })
  },
}

export function confirm(message: string, title = '确认操作'): Promise<MessageBoxData> {
  return ElMessageBox.confirm(message, title, {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
    customClass: 'hakimi-confirm-dialog',
  })
}

export function alert(message: string, title = '提示'): Promise<MessageBoxData> {
  return ElMessageBox.alert(message, title, {
    confirmButtonText: '知道了',
    customClass: 'hakimi-alert-dialog',
  })
}
