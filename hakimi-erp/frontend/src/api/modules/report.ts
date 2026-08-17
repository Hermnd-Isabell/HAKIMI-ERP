import { get } from '../request'

const BASE = '/api/v1/reports'

export function fetchSalesPerformance(params?: { days?: number }) {
  return get<any>(`${BASE}/sales-performance`, { params })
}

export function fetchFinancialSummary() {
  return get<any>(`${BASE}/financial-summary`)
}

export function fetchFinancialDetail() {
  return get<any>(`${BASE}/financial-detail`)
}

export function fetchDeliveryStats() {
  return get<any>(`${BASE}/delivery-stats`)
}

export function fetchDashboardSummary() {
  return get<any>(`${BASE}/dashboard-summary`)
}

