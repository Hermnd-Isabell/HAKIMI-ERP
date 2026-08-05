// API endpoint constants.
// Use these instead of scattering path strings across views.

export const API_BASE = '/api'

export const MASTER_API = {
  partners: `${API_BASE}/v1/master/partners/`,
  materials: `${API_BASE}/v1/master/materials/`,
  pricingConditions: `${API_BASE}/v1/master/materials/pricing-conditions`,
  salesOrganizations: `${API_BASE}/v1/master/materials/sales-organizations`,
} as const

export const SALES_API = {
  inquiries: `${API_BASE}/v1/sales/inquiries`,
  inquiryById: (id: string) => `${API_BASE}/v1/sales/inquiries/${id}`,
  quotations: `${API_BASE}/v1/sales/quotations`,
  quotationById: (id: string) => `${API_BASE}/v1/sales/quotations/${id}`,
  orders: `${API_BASE}/v1/sales/orders`,
  orderById: (id: string) => `${API_BASE}/v1/sales/orders/${id}`,
} as const

export const LOGISTICS_API = {
  deliveries: `${API_BASE}/v1/logistics/deliveries`,
  deliveryById: (id: string) => `${API_BASE}/v1/logistics/deliveries/${id}`,
  createFromSo: (soId: string) => `${API_BASE}/v1/logistics/deliveries/from-so/${soId}`,
  startPicking: (id: string) => `${API_BASE}/v1/logistics/deliveries/${id}/start-picking`,
  confirmPicking: (id: string) => `${API_BASE}/v1/logistics/deliveries/${id}/confirm-picking`,
  pickBatch: (id: string) => `${API_BASE}/v1/logistics/deliveries/${id}/pick-batch`,
  pickRecords: (id: string) => `${API_BASE}/v1/logistics/deliveries/${id}/pick-records`,
  ship: (id: string) => `${API_BASE}/v1/logistics/deliveries/${id}/ship`,
  postPgi: (id: string) => `${API_BASE}/v1/logistics/deliveries/${id}/pgi`,
  soRemaining: (soId: string) => `${API_BASE}/v1/logistics/sales-orders/${soId}/remaining-quantities`,
  storageLocations: `${API_BASE}/v1/logistics/storage-locations`,
} as const

export const FINANCE_API = {
  invoices: `${API_BASE}/v1/finance/invoices`,
  invoiceById: (id: string) => `${API_BASE}/v1/finance/invoices/${id}`,
  invoiceFromDelivery: (deliveryId: string) => `${API_BASE}/v1/finance/invoices/from-delivery/${deliveryId}`,
  arOpen: `${API_BASE}/v1/finance/ar/open`,
  arClosed: `${API_BASE}/v1/finance/ar/closed`,
  receipts: `${API_BASE}/v1/finance/receipts`,
} as const