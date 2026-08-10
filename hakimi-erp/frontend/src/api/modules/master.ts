import { get, post, put, del } from '../request'
import { MASTER_API } from '@/constants/api'

export interface Partner {
  bpId: string
  bpType: string
  bpRole: string
  bpName: string
  country: string
  city: string
  district?: string
  street: string
  houseNumber?: string
  postalCode: string
  telephone: string
  mobilePhone?: string
  fax?: string
  email: string
  website?: string
  searchTerm: string
  status: string
}

export interface PartnerList {
  items: Partner[]
  total: number
}

export interface Material {
  materialId: string
  materialName: string
  materialType: string
  baseUnit: string
  netWeight?: number
  status: string
}

export interface MaterialList {
  items: Material[]
  total: number
}

export function fetchPartners(params?: Record<string, any>) {
  return get<PartnerList>(MASTER_API.partners, { params })
}

export function createPartner(data: Partial<Partner>) {
  return post<Partner>(MASTER_API.partners, data)
}

export function updatePartner(id: string, data: Partial<Partner>) {
  return put<Partner>(`${MASTER_API.partners}${id}`, data)
}

export function fetchMaterials(params?: Record<string, any>) {
  return get<MaterialList>(MASTER_API.materials, { params })
}

export function createMaterial(data: Partial<Material>) {
  return post<Material>(MASTER_API.materials, data)
}

export function updateMaterial(id: string, data: Partial<Material>) {
  return put<Material>(`${MASTER_API.materials}${id}`, data)
}

export function deleteMaterial(id: string) {
  return del<void>(`${MASTER_API.materials}${id}`)
}

export function fetchPricingConditions(params?: Record<string, any>) {
  return get<any>(`${MASTER_API.materials}pricing-conditions`, { params })
}

export function fetchSalesOrganizations(params?: Record<string, any>) {
  return get<any>(`${MASTER_API.materials}sales-organizations`, { params })
}
