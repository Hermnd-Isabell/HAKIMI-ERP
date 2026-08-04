import { COLORS } from '@/constants/colors'

export interface ValidationRule {
  required?: boolean
  email?: boolean
  phone?: boolean
  postalCode?: boolean
  minLength?: number
  maxLength?: number
  min?: number
  max?: number
  pattern?: RegExp
  custom?: (value: unknown) => string | undefined
  message?: string
}

export interface FieldRules {
  [field: string]: ValidationRule
}

export interface FieldErrors {
  [field: string]: string
}

export function required(value: unknown): string | undefined {
  if (value === undefined || value === null || value === '') {
    return '此项为必填项'
  }
}

export function email(value: string): string | undefined {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!re.test(value)) return '邮箱格式不正确'
}

export function phone(value: string): string | undefined {
  const re = /^[\d+\-()\s]{7,20}$/
  if (!re.test(value)) return '电话格式不正确'
}

export function postalCode(value: string): string | undefined {
  const v = value?.toString().trim() || ''
  if (v.length < 4) return '邮政编码长度不能少于 4 位'
  if (!/^\d+$/.test(v)) return '邮政编码只能包含数字'
}

export function numberRange(value: number, min: number, max: number): string | undefined {
  if (typeof value !== 'number' || isNaN(value)) return '请输入有效数字'
  if (value < min) return `不能小于 ${min}`
  if (value > max) return `不能大于 ${max}`
}

export function dateRange(start: string, end: string, startLabel = '开始日期', endLabel = '结束日期'): string | undefined {
  if (!start || !end) return
  if (new Date(start) > new Date(end)) {
    return `${endLabel}不可早于${startLabel}`
  }
}

function getFieldError(
  field: string,
  value: unknown,
  rule: ValidationRule,
): string | undefined {
  const strValue = typeof value === 'string' ? value : String(value ?? '')

  if (rule.required) {
    const err = required(value)
    if (err) return `${field}${err}`
  }

  if (value === undefined || value === null || value === '') return

  if (rule.minLength !== undefined && strValue.length < rule.minLength) {
    return `${field}长度不能少于 ${rule.minLength} 个字符`
  }

  if (rule.maxLength !== undefined && strValue.length > rule.maxLength) {
    return `${field}长度不能超过 ${rule.maxLength} 个字符`
  }

  if (rule.email) {
    const err = email(strValue)
    if (err) return `${field}${err}`
  }

  if (rule.phone) {
    const err = phone(strValue)
    if (err) return `${field}${err}`
  }

  if (rule.postalCode) {
    const err = postalCode(strValue)
    if (err) return `${field}${err}`
  }

  if (rule.pattern && !rule.pattern.test(strValue)) {
    return rule.message || `${field}格式不正确`
  }

  if (rule.min !== undefined || rule.max !== undefined) {
    const num = parseFloat(strValue)
    const err = numberRange(num, rule.min ?? -Infinity, rule.max ?? Infinity)
    if (err) return `${field}${err}`
  }

  if (rule.custom) {
    const err = rule.custom(value)
    if (err) return err
  }
}

export function validateForm(values: Record<string, unknown>, rules: FieldRules): FieldErrors {
  const errors: FieldErrors = {}
  for (const [field, rule] of Object.entries(rules)) {
    const err = getFieldError(field, values[field], rule)
    if (err) errors[field] = err
  }
  return errors
}

export function hasErrors(errors: FieldErrors): boolean {
  return Object.keys(errors).length > 0
}

export function countErrors(errors: FieldErrors): number {
  return Object.keys(errors).length
}

// Visual helpers for ERP forms.
export const VALIDATION_STYLE = {
  errorColor: COLORS.danger,
  reserveHeight: '20px',
} as const
