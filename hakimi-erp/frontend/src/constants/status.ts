// Business document status constants and UI mappings.
// All document state transitions should reference these values.

export const DOC_STATUS = {
  OPEN: 'OPEN',
  IN_PROCESS: 'IN_PROCESS',
  COMPLETED: 'COMPLETED',
  CLOSED: 'CLOSED',
  CANCELLED: 'CANCELLED',
  REJECTED: 'REJECTED',
} as const

export type DocStatus = (typeof DOC_STATUS)[keyof typeof DOC_STATUS]

export interface StatusOption {
  value: DocStatus
  label: string
  styleClass: string
}

export const statusOptions: StatusOption[] = [
  { value: DOC_STATUS.OPEN, label: 'Open', styleClass: 's-open' },
  { value: DOC_STATUS.IN_PROCESS, label: 'In Process', styleClass: 's-proc' },
  { value: DOC_STATUS.COMPLETED, label: 'Completed', styleClass: 's-done' },
  { value: DOC_STATUS.CLOSED, label: 'Closed', styleClass: 's-done' },
  { value: DOC_STATUS.CANCELLED, label: 'Cancelled', styleClass: 's-cancel' },
  { value: DOC_STATUS.REJECTED, label: 'Rejected', styleClass: 's-cancel' },
]

export function getStatusLabel(status: string): string {
  return statusOptions.find(item => item.value === status)?.label || status
}

export function getStatusClass(status: string): string {
  return statusOptions.find(item => item.value === status)?.styleClass || ''
}

// State transition guards.
export function canConvertToQuotation(status: DocStatus): boolean {
  return status === DOC_STATUS.OPEN
}

export function canConvertToOrder(status: DocStatus): boolean {
  return status === DOC_STATUS.OPEN
}

export function canConvertToDelivery(status: DocStatus): boolean {
  return status === DOC_STATUS.OPEN
}

export function canCancel(status: DocStatus): boolean {
  return status === DOC_STATUS.OPEN || status === DOC_STATUS.IN_PROCESS
}
