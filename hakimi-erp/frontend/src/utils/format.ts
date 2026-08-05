// Formatting utilities for currency, dates, numbers and percentages.

export function formatCurrency(
  value: number | string | undefined,
  currency = 'CNY',
  locale = 'zh-CN',
): string {
  const num = typeof value === 'string' ? parseFloat(value) : value
  if (num === undefined || num === null || isNaN(num)) return '¥0.00'
  return new Intl.NumberFormat(locale, { style: 'currency', currency }).format(num)
}

export function formatNumber(
  value: number | string | undefined,
  decimals = 2,
  locale = 'zh-CN',
): string {
  const num = typeof value === 'string' ? parseFloat(value) : value
  if (num === undefined || num === null || isNaN(num)) return '0'
  return new Intl.NumberFormat(locale, {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(num)
}

export function formatDate(value: string | Date | undefined): string {
  if (!value) return 'N/A'
  const d = typeof value === 'string' ? new Date(value) : value
  if (isNaN(d.getTime())) return 'N/A'
  return d.toISOString().split('T')[0]
}

export function formatDateTime(value: string | Date | undefined): string {
  if (!value) return 'N/A'
  const d = typeof value === 'string' ? new Date(value) : value
  if (isNaN(d.getTime())) return 'N/A'
  return d.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function formatPercent(value: number | string | undefined, decimals = 2): string {
  const num = typeof value === 'string' ? parseFloat(value) : value
  if (num === undefined || num === null || isNaN(num)) return '0.00%'
  return `${(num * 100).toFixed(decimals)}%`
}

export function padZero(value: number | string, length = 6): string {
  return String(value).padStart(length, '0')
}
