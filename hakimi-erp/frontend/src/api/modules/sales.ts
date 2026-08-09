import { get, post, put, del } from '../request'
import { SALES_API } from '@/constants/api'

export interface InquiryItem {
  inquiry_item_id: string
  inquiry_id?: string
  item_no: number
  material_id: string
  item_description?: string
  order_quantity: number
  sales_unit: string
  expected_order_value?: number
  unit_price?: number
  discount?: number
  net_price?: number
  remark?: string
  search_term?: string
}

export interface Inquiry {
  inquiry_id: string
  inquiry_type: string
  status: string
  customer_id: string
  sold_to_party?: string
  ship_to_party?: string
  sales_area?: string
  customer_reference?: string
  customer_reference_date?: string
  sales_org?: string
  distribution_channel?: string
  division?: string
  sales_office?: string
  sales_group?: string
  requested_delivery_date?: string
  valid_from?: string
  valid_to?: string
  pricing_date?: string
  currency?: string
  delivering_plant?: string
  incoterms?: string
  delivery_location?: string
  payment_terms?: string
  max_partial_deliveries?: number
  net_value?: number
  inquiry_address?: string
  remark?: string
  search_term?: string
  created_time?: string
  created_by?: string
  items: InquiryItem[]
}

export interface InquiryList {
  items: Inquiry[]
  total: number
}

export interface QuotationItem {
  quotation_item_id: string
  quotation_id?: string
  item_no: number
  material_id: string
  item_description?: string
  order_quantity: number
  sales_unit: string
  expected_order_value?: number
  unit_price?: number
  discount?: number
  net_price?: number
  remark?: string
  search_term?: string
}

export interface Quotation {
  quotation_id: string
  inquiry_id?: string
  quotation_type: string
  status: string
  customer_id: string
  sold_to_party?: string
  ship_to_party?: string
  sales_area?: string
  customer_reference?: string
  customer_reference_date?: string
  sales_org?: string
  distribution_channel?: string
  division?: string
  sales_office?: string
  sales_group?: string
  requested_delivery_date?: string
  valid_from?: string
  valid_to?: string
  pricing_date?: string
  currency?: string
  delivering_plant?: string
  incoterms?: string
  payment_terms?: string
  max_partial_deliveries?: number
  net_value?: number
  quotation_address?: string
  remark?: string
  search_term?: string
  created_time?: string
  created_by?: string
  items: QuotationItem[]
}

export interface QuotationList {
  items: Quotation[]
  total: number
}

export interface SalesOrderItem {
  so_item_id: string
  sales_order_id?: string
  item_no: number
  material_id: string
  item_description?: string
  item_category?: string
  order_quantity: number
  confirmed_quantity?: number
  sales_unit: string
  plant?: string
  storage_location?: string
  shipping_point?: string
  unit_price?: number
  discount?: number
  net_price?: number
  availability_status?: string
  remark?: string
  search_term?: string
}

export interface SalesOrder {
  sales_order_id: string
  quotation_id?: string
  order_type: string
  reference_type?: string
  reference_document?: string
  status: string
  customer_id: string
  sold_to_party?: string
  ship_to_party?: string
  customer_reference?: string
  customer_reference_date?: string
  sales_org?: string
  distribution_channel?: string
  division?: string
  sales_office?: string
  sales_group?: string
  requested_delivery_date?: string
  pricing_date?: string
  currency?: string
  payment_terms?: string
  incoterms?: string
  delivering_plant?: string
  shipping_condition?: string
  delivery_priority?: string
  billing_block?: string
  delivery_block?: string
  max_partial_deliveries?: number
  net_value?: number
  remark?: string
  search_term?: string
  created_time?: string
  created_by?: string
  items: SalesOrderItem[]
}

export interface SalesOrderList {
  items: SalesOrder[]
  total: number
}

// Inquiry APIs
export function fetchInquiries(params?: Record<string, any>) {
  return get<InquiryList>(SALES_API.inquiries, { params })
}

export function fetchInquiryById(id: string) {
  return get<Inquiry>(SALES_API.inquiryById(id))
}

export function createInquiry(data: Partial<Inquiry>) {
  return post<Inquiry>(SALES_API.inquiries, data)
}

export function updateInquiry(id: string, data: Partial<Inquiry>) {
  return put<Inquiry>(SALES_API.inquiryById(id), data)
}

// Quotation APIs
export function fetchQuotations(params?: Record<string, any>) {
  return get<QuotationList>(SALES_API.quotations, { params })
}

export function fetchQuotationById(id: string) {
  return get<Quotation>(SALES_API.quotationById(id))
}

export function createQuotation(data: Partial<Quotation>) {
  return post<Quotation>(SALES_API.quotations, data)
}

export function updateQuotation(id: string, data: Partial<Quotation>) {
  return put<Quotation>(SALES_API.quotationById(id), data)
}

// Sales Order APIs
export function fetchOrders(params?: Record<string, any>) {
  return get<SalesOrderList>(SALES_API.orders, { params })
}

export function fetchOrderById(id: string) {
  return get<SalesOrder>(SALES_API.orderById(id))
}

export function createOrder(data: Partial<SalesOrder>) {
  return post<SalesOrder>(SALES_API.orders, data)
}

export function updateOrder(id: string, data: Partial<SalesOrder>) {
  return put<SalesOrder>(SALES_API.orderById(id), data)
}

export function deleteOrder(id: string) {
  return del<void>(SALES_API.orderById(id))
}
