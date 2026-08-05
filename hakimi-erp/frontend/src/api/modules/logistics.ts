import { get, post, put } from '../request'
import { LOGISTICS_API } from '@/constants/api'

// --- Delivery Item ---
export interface DeliveryItem {
  delivery_item_id: string
  delivery_id: string
  item_no: number
  so_item_id?: string
  material_id: string
  material_name?: string
  base_unit?: string
  order_quantity?: number
  delivery_quantity: number
  picked_quantity?: number
  sales_unit?: string
  plant?: string
  storage_location?: string
  item_description?: string
  item_status?: string
}

// --- Delivery (Detail) ---
export interface Delivery {
  delivery_id: string
  sales_order_id?: string
  delivery_type: string
  delivery_status: string
  ship_to_party: string
  ship_to_party_name?: string
  ship_to_address?: string
  planned_delivery_date?: string
  planned_gi_date?: string
  actual_gi_date?: string
  picking_date?: string
  shipping_point?: string
  carrier?: string
  driver_name?: string
  route?: string
  tracking_no?: string
  total_quantity?: number
  delivered_quantity?: number
  items: DeliveryItem[]
}

// --- Delivery List Item ---
export interface DeliveryListItem {
  delivery_id: string
  sales_order_id?: string
  delivery_type: string
  delivery_status: string
  ship_to_party: string
  ship_to_party_name?: string
  planned_delivery_date?: string
  planned_gi_date?: string
  actual_gi_date?: string
  picking_date?: string
  shipping_point?: string
  total_quantity?: number
  delivered_quantity?: number
}

// --- Pagination ---
export interface Pagination {
  page: number
  page_size: number
  total: number
  total_pages: number
}

// --- Delivery List Response ---
export interface DeliveryListResponse {
  items: DeliveryListItem[]
  pagination: Pagination
}

// --- Goods Issue ---
export interface GoodsIssue {
  goods_issue_id: string
  delivery_item_id: string
  actual_quantity: number
  posting_date: string
  goods_issue_time: string
  warehouse?: string
  material_id?: string
  material_name?: string
}


// --- Partial Picking / PGI ---
export interface PartialItemQuantity {
  delivery_item_id: string
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
  so_item_id: string
  material_id: string
  material_name?: string
  order_quantity: number
  already_delivered: number
  remaining_quantity: number
  sales_unit?: string
}


// --- Pick Record (batch picking) ---
export interface PickRecord {
  pick_id: string
  delivery_item_id: string
  batch_no: number
  pick_quantity: number
  storage_location?: string
  pick_date: string
  picked_by?: string
  material_id?: string
  material_name?: string
}

export interface PickBatchRequest {
  items: PartialItemQuantity[]
  storage_location?: string
  picked_by?: string
}


export interface StorageLocation {
  sloc_id: string
  sloc_name: string
  plant: string
  warehouse_no?: string
  storage_type?: string
  storage_bin?: string
  description?: string
}
// --- Status Labels ---
export interface StatusLabels {
  [key: string]: string
}

// === API Functions ===

export function fetchDeliveries(params?: {
  page?: number
  page_size?: number
  delivery_no?: string
  sales_order_no?: string
  customer_name?: string
  status?: string
}) {
  return get<DeliveryListResponse>(LOGISTICS_API.deliveries, { params })
}

export function fetchDeliveryById(id: string) {
  return get<Delivery>(LOGISTICS_API.deliveryById(id))
}

export function createDeliveryFromSalesOrder(soId: string) {
  return post<Delivery>(LOGISTICS_API.createFromSo(soId))
}

export function startPicking(deliveryId: string) {
  return post<Delivery>(LOGISTICS_API.startPicking(deliveryId))
}

export function confirmPicking(deliveryId: string) {
  return post<Delivery>(LOGISTICS_API.confirmPicking(deliveryId))
}

export function shipDelivery(deliveryId: string) {
  return post<Delivery>(LOGISTICS_API.ship(deliveryId))
}

export function postGoodsIssue(deliveryId: string, body?: PartialPgiRequest) {
  return post<Delivery>(LOGISTICS_API.postPgi(deliveryId), body)
}

export function fetchGoodsIssues(deliveryId: string) {
  return get<GoodsIssue[]>(`${LOGISTICS_API.deliveryById(deliveryId)}/goods-issues`)
}

export function pickBatch(deliveryId: string, body: PickBatchRequest) {
  return post<Delivery>(LOGISTICS_API.pickBatch(deliveryId), body)
}

export function fetchPickRecords(deliveryId: string) {
  return get<PickRecord[]>(LOGISTICS_API.pickRecords(deliveryId))
}

export function fetchSoRemaining(soId: string) {
  return get<SoItemRemaining[]>(LOGISTICS_API.soRemaining(soId))
}

export function fetchStorageLocations(params?: { keyword?: string; plant?: string }) {
  return get<StorageLocation[]>(LOGISTICS_API.storageLocations, { params })
}

export function fetchStatusLabels() {
  return get<StatusLabels>(`${LOGISTICS_API.deliveries.replace('/deliveries', '/delivery-status-labels')}`)
}

export function updateDelivery(id: string, data: Partial<Delivery>) {
  return put<Delivery>(LOGISTICS_API.deliveryById(id), data)
}
