import { get, post, put } from '../request'

// --- Delivery Item ---
export interface DeliveryItem {
  deliveryItemId: string
  deliveryId: string
  itemNo: number
  soItemId?: string
  materialId: string
  materialName?: string
  baseUnit?: string
  orderQuantity?: number
  deliveryQuantity: number
  pickedQuantity?: number
  salesUnit?: string
  plant?: string
  storageLocation?: string
  itemDescription?: string
  itemStatus?: string
}

// --- Delivery (Detail) ---
export interface Delivery {
  deliveryId: string
  salesOrderId?: string
  deliveryType: string
  deliveryStatus: string
  shipToParty: string
  shipToPartyName?: string
  shipToAddress?: string
  plannedDeliveryDate?: string
  plannedGiDate?: string
  actualGiDate?: string
  pickingDate?: string
  shippingPoint?: string
  carrier?: string
  driverName?: string
  route?: string
  trackingNo?: string
  totalQuantity?: number
  deliveredQuantity?: number
  items: DeliveryItem[]
}

// --- Delivery List Item ---
export interface DeliveryListItem {
  deliveryId: string
  salesOrderId?: string
  deliveryType: string
  deliveryStatus: string
  shipToParty: string
  shipToPartyName?: string
  plannedDeliveryDate?: string
  plannedGiDate?: string
  actualGiDate?: string
  pickingDate?: string
  shippingPoint?: string
  totalQuantity?: number
  deliveredQuantity?: number
}

// --- Pagination ---
export interface Pagination {
  page: number
  pageSize: number
  total: number
  totalPages: number
}

// --- Delivery List Response ---
export interface DeliveryListResponse {
  items: DeliveryListItem[]
  pagination: Pagination
}

// --- Goods Issue ---
export interface GoodsIssue {
  goodsIssueId: string
  deliveryItemId: string
  actualQuantity: number
  postingDate: string
  goodsIssueTime: string
  warehouse?: string
  materialId?: string
  materialName?: string
  batchNo: number
}


// --- Partial Picking / PGI ---
export interface PartialItemQuantity {
  deliveryItemId: string
  quantity: number
}

export interface PartialPickingRequest {
  items: PartialItemQuantity[]
}

export interface PartialPgiRequest {
  items: PartialItemQuantity[]
}

// --- SO Remaining Quantities ---
export interface SoItemRemaining {
  soItemId: string
  materialId: string
  materialName?: string
  orderQuantity: number
  alreadyDelivered: number
  remainingQuantity: number
  salesUnit?: string
}


// --- Pick Record (batch picking) ---
export interface PickRecord {
  pickId: string
  deliveryItemId: string
  batchNo: number
  pickQuantity: number
  storageLocation?: string
  pickDate: string
  pickedBy?: string
  materialId?: string
  materialName?: string
}

export interface PickBatchRequest {
  items: PartialItemQuantity[]
  storageLocation?: string
  pickedBy?: string
}


export interface StorageLocation {
  slocId: string
  slocName: string
  plant: string
  warehouseNo?: string
  storageType?: string
  storageBin?: string
  description?: string
}
// --- Status Labels ---
export interface StatusLabels {
  [key: string]: string
}

// === API Functions ===

const BASE = '/api/v1/logistics'

export function fetchDeliveries(params?: {
  page?: number
  pageSize?: number
  deliveryNo?: string
  salesOrderNo?: string
  customerName?: string
  status?: string
}) {
  return get<DeliveryListResponse>(`${BASE}/deliveries`, { params })
}

export function fetchDeliveryById(id: string) {
  return get<Delivery>(`${BASE}/deliveries/${id}`)
}

export function createDeliveryFromSalesOrder(soId: string) {
  return post<Delivery>(`${BASE}/deliveries/from-so/${soId}`)
}

export function startPicking(deliveryId: string) {
  return post<Delivery>(`${BASE}/deliveries/${deliveryId}/start-picking`)
}

export function confirmPicking(deliveryId: string) {
  return post<Delivery>(`${BASE}/deliveries/${deliveryId}/confirm-picking`)
}

export function shipDelivery(deliveryId: string) {
  return post<Delivery>(`${BASE}/deliveries/${deliveryId}/ship`)
}

export function postGoodsIssue(deliveryId: string, body?: PartialPgiRequest) {
  return post<Delivery>(`${BASE}/deliveries/${deliveryId}/pgi`, body)
}

export function fetchGoodsIssues(deliveryId: string) {
  return get<GoodsIssue[]>(`${BASE}/deliveries/${deliveryId}/goods-issues`)
}

export function pickBatch(deliveryId: string, body: PickBatchRequest) {
  return post<Delivery>(`${BASE}/deliveries/${deliveryId}/pick-batch`, body)
}

export function fetchPickRecords(deliveryId: string) {
  return get<PickRecord[]>(`${BASE}/deliveries/${deliveryId}/pick-records`)
}

export function fetchSoRemaining(soId: string) {
  return get<SoItemRemaining[]>(`${BASE}/sales-orders/${soId}/remaining-quantities`)
}

export function fetchStorageLocations(params?: { keyword?: string; plant?: string }) {
  return get<StorageLocation[]>(`${BASE}/storage-locations`, { params })
}

export function fetchStatusLabels() {
  return get<StatusLabels>(`${BASE}/delivery-status-labels`)
}
