import { get, post } from '../request'
import { FINANCE_API } from '@/constants/api'

// ------------------------------------------------------------------ //
//  Pagination
// ------------------------------------------------------------------ //
export interface Pagination {
  page: number
  page_size: number
  total: number
  total_pages: number
}

export interface PaginatedData<T> {
  items: T[]
  pagination: Pagination
}

// ------------------------------------------------------------------ //
//  Invoice
// ------------------------------------------------------------------ //
export interface InvoiceItem {
  invoice_item_id: string
  item_no: number
  material_id: string
  quantity?: number
  sales_unit?: string
  unit_price?: number
  discount?: number
  tax_amount?: number
  net_price?: number
  item_description?: string
  remark?: string
}

export interface Invoice {
  invoice_id: string
  delivery_id?: string
  sales_order_id?: string
  billing_type: string
  invoice_date: string
  billing_date: string
  sales_org?: string
  distribution_channel?: string
  division?: string
  shipping_point?: string
  sold_to_party?: string
  payer?: string
  destination_country?: string
  currency: string
  total_amount?: number
  status: string
  remark?: string
  search_term?: string
  items: InvoiceItem[]
}

export interface InvoiceQuery {
  page?: number
  page_size?: number
  customer?: string
  invoice_no?: string
  status?: string
  date_from?: string
  date_to?: string
}

export function fetchInvoices(params?: InvoiceQuery) {
  return get<PaginatedData<Invoice>>(FINANCE_API.invoices, { params })
}

export function fetchInvoiceById(id: string) {
  return get<Invoice>(FINANCE_API.invoiceById(id))
}

export function createInvoiceFromDelivery(deliveryId: string) {
  return post<Invoice>(FINANCE_API.invoiceFromDelivery(deliveryId))
}

export function voidInvoice(id: string) {
  return post<Invoice>(FINANCE_API.invoiceVoid(id))
}

// ------------------------------------------------------------------ //
//  Document Flow
// ------------------------------------------------------------------ //
export interface DocumentFlow {
  invoice: { invoice_id: string; status: string }
  sales_order?: {
    sales_order_id: string
    status: string
    customer_id?: string
    net_value?: number
  }
  delivery?: {
    delivery_id: string
    delivery_status: string
    ship_to_party: string
  }
  receipts?: Array<{
    receipt_id: string
    receipt_amount: number
    receipt_date: string | null
    payment_method: string | null
  }>
  account_receivable?: {
    type: 'open' | 'closed'
    open_ar_id?: string
    closed_ar_id?: string
    receivable_amount: number
    received_amount: number
    due_date?: string
    status: string
  }
}

export function fetchDocumentFlow(id: string) {
  return get<DocumentFlow>(FINANCE_API.invoiceDocumentFlow(id))
}

// ------------------------------------------------------------------ //
//  Account Receivable
// ------------------------------------------------------------------ //
export interface OpenAccountReceivable {
  open_ar_id: string
  invoice_id: string
  receivable_amount: number
  received_amount: number
  due_date?: string
  status: string
  remark?: string
  search_term?: string
  created_time?: string
}

export interface ClosedAccountReceivable {
  closed_ar_id: string
  invoice_id: string
  receivable_amount: number
  received_amount: number
  created_time?: string
  closed_time?: string
  remark?: string
  search_term?: string
}

export interface ARQuery {
  page?: number
  page_size?: number
  customer?: string
  invoice_no?: string
  status?: string
}

export function fetchOpenAR(params?: ARQuery) {
  return get<PaginatedData<OpenAccountReceivable>>(FINANCE_API.arOpen, { params })
}

export function fetchClosedAR(params?: ARQuery) {
  return get<PaginatedData<ClosedAccountReceivable>>(FINANCE_API.arClosed, { params })
}

export function fetchOpenARByInvoice(invoiceId: string) {
  return get<OpenAccountReceivable>(FINANCE_API.arOpenByInvoice(invoiceId))
}

export function fetchClosedARByInvoice(invoiceId: string) {
  return get<ClosedAccountReceivable[]>(FINANCE_API.arClosedByInvoice(invoiceId))
}

// ------------------------------------------------------------------ //
//  Receipt
// ------------------------------------------------------------------ //
export interface Receipt {
  receipt_id: string
  invoice_id: string
  payer: string
  receipt_amount: number
  payment_method?: string
  currency: string
  reference_no?: string
  receipt_date?: string
  remark?: string
  search_term?: string
}

export interface ReceiptQuery {
  page?: number
  page_size?: number
  customer?: string
  invoice_no?: string
}

export function fetchReceipts(params?: ReceiptQuery) {
  return get<PaginatedData<Receipt>>(FINANCE_API.receipts, { params })
}

export function fetchReceiptById(id: string) {
  return get<Receipt>(FINANCE_API.receiptById(id))
}

export interface ReceiptCreate {
  invoice_id: string
  receipt_amount: number
  payment_method?: string
  currency?: string
  reference_no?: string
  remark?: string
  search_term?: string
}

export function createReceipt(data: ReceiptCreate) {
  return post<Receipt>(FINANCE_API.receipts, data)
}
