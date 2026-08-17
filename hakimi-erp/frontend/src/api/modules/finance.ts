import { get, post, put } from '../request'

export interface InvoiceItem {
  invoiceItemId: string
  itemNo: number
  materialId: string
  quantity?: number
  unitPrice?: number
  taxAmount?: number
  netPrice?: number
}

export interface Invoice {
  invoiceId: string
  deliveryId?: string
  salesOrderId?: string
  billingType: string
  invoiceDate: string
  billingDate: string
  soldToParty?: string
  payer?: string
  currency: string
  totalAmount?: number
  status: string
  items: InvoiceItem[]
  createdTime?: string
}

export interface InvoiceList {
  items: Invoice[]
  total: number
}

export interface OpenAccountReceivable {
  openArId: string
  invoiceId: string
  receivableAmount: number
  receivedAmount: number
  dueDate?: string
  status: string
  createdTime?: string
}

export interface ClosedAccountReceivable {
  closedArId: string
  invoiceId: string
  receivableAmount: number
  receivedAmount: number
  createdTime?: string
  closedTime?: string
}

export interface ReceivableList {
  items: any[]
  total: number
}

export interface Receipt {
  receiptId: string
  invoiceId: string
  payer: string
  receiptAmount: number
  paymentMethod?: string
  currency: string
  referenceNo?: string
  receiptDate?: string
}

const BASE = '/api/v1/finance'

export function fetchInvoices(params?: Record<string, any>) {
  return get<InvoiceList>(`${BASE}/invoices`, { params })
}

export function fetchInvoiceById(id: string) {
  return get<Invoice>(`${BASE}/invoices/${id}`)
}

export function createInvoiceFromDelivery(deliveryId: string) {
  return post<Invoice>(`${BASE}/invoices/from-delivery/${deliveryId}`)
}

export function fetchOpenAR(params?: Record<string, any>) {
  return get<ReceivableList>(`${BASE}/ar/open`, { params })
}

export function fetchClosedAR(params?: Record<string, any>) {
  return get<ReceivableList>(`${BASE}/ar/closed`, { params })
}

export function createReceipt(data: Partial<Receipt>) {
  return post<Receipt>(`${BASE}/receipts`, data)
}

export function fetchReceipts(params?: Record<string, any>) {
  return get<ReceivableList>(`${BASE}/receipts`, { params })
}
