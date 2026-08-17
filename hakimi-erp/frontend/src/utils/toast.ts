import { ElMessage, ElMessageBox } from 'element-plus'

export interface ToastOptions {
  message: string
  duration?: number
  showClose?: boolean
}

const TOAST_CLASS = 'hakimi-toast-center'

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

export async function confirm(message: string, title = '确认操作'): Promise<boolean> {
  try {
    await ElMessageBox.confirm(message, title, {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning',
      customClass: 'hakimi-confirm-dialog',
    })
    return true
  } catch {
    return false
  }
}

export async function alert(message: string, title = '提示'): Promise<void> {
  try {
    await ElMessageBox.alert(message, title, {
      confirmButtonText: '知道了',
      customClass: 'hakimi-alert-dialog',
    })
  } catch {
    // Dismissing an informational dialog should not raise an unhandled rejection.
  }
}

export async function prompt(message: string, defaultValue = ''): Promise<string | null> {
  try {
    const { value } = await ElMessageBox.prompt(message, '输入', {
      inputValue: defaultValue,
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      customClass: 'hakimi-prompt-dialog',
    })
    return value || null
  } catch {
    return null
  }
}
