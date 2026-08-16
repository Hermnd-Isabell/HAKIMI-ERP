<template>
  <div class="page" v-if="loading">
      <div class="section-card" style="padding:40px;text-align:center;color:rgba(18,55,42,0.4)">
        <p>Loading delivery details...</p>
        <p style="font-size:11px;margin-top:8px">{{ loadMsg }}</p>
      </div>
    </div>
    <div class="page" v-else-if="error">
      <div class="error-msg">{{ error }}</div>
      <button class="btn btn-outline" @click="loadData" style="margin-right:8px">Retry</button>
      <button class="back-btn" @click="$router.push('/delivery/monitor')">Back to Monitor</button>
    </div>
    <div class="page" v-else-if="delivery">
      <!-- Top Bar -->
      <div class="top-bar">
        <button class="back-btn" @click="$router.push('/delivery/monitor')">
          <svg viewBox="0 0 20 20" width="16" height="16"><path d="M12 4l-6 6 6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Back
        </button>
        <div class="hc-icon">
          <svg viewBox="0 0 24 24" width="22" height="22"><rect x="2" y="5" width="20" height="13" rx="2" fill="none" stroke="#436850" stroke-width="1.8"/><path d="M6 5V3M18 5V3M2 11h20M7 16h3" fill="none" stroke="#436850" stroke-width="1.5" stroke-linecap="round"/></svg>
        </div>
        <div class="top-info">
          <span class="ti-label">Delivery No.</span>
          <span class="ti-value">{{ delivery.deliveryId }}</span>
          <span class="ti-sub">SO {{ delivery.salesOrderId || 'N/A' }} &middot; {{ delivery.shipToPartyName || delivery.shipToParty }}</span>
        </div>
        <div style="margin-left:auto;display:flex;align-items:center;gap:10px;">
          <span class="stag" :class="statusClass">{{ statusLabel }}</span>
          <template v-if="delivery.deliveryStatus === 'PICKING'">
            <button class="btn btn-primary" @click="showPickDialog = true">Pick Batch</button>
            <button class="btn btn-outline" @click="doConfirmPicking" :disabled="!allFullyPicked || posting">
              {{ posting ? '...' : 'Confirm Picking Complete' }}
            </button>
          </template>
          <template v-else-if="nextActionLabel">
            <button class="btn btn-primary" @click="handleAction" :disabled="posting">
              {{ posting ? '...' : nextActionLabel }}
            </button>
          </template>
          <button class="btn btn-outline" @click="print">Print</button>
        </div>
      </div>

      <!-- Info Cards -->
      <div class="info-cards">
        <div class="ic"><span class="ic-label">Delivery Date</span><span class="ic-value">{{ delivery.plannedDeliveryDate || 'N/A' }}</span></div>
        <div class="ic"><span class="ic-label">Planned GI Date</span><span class="ic-value">{{ delivery.plannedGiDate || 'N/A' }}</span></div>
        <div class="ic"><span class="ic-label">Shipping Point</span><span class="ic-value">{{ delivery.shippingPoint || 'N/A' }}</span></div>
        <div class="ic"><span class="ic-label">Picked / Total</span><span class="ic-value mono">{{ pickedTotal }} / {{ totalQty }}</span></div>
      </div>

      <!-- Progress Timeline -->
      <div class="section-card">
        <h3 class="sc-title">Delivery Progress</h3>
        <div class="timeline">
          <div v-for="(s,i) in steps" :key="i" class="tl-step" :class="{done:s.done, cur:s.cur}">
            <div class="tl-dot"></div><div v-if="i < steps.length - 1" class="tl-line"></div>
            <div class="tl-info"><span class="tl-status">{{ s.label }}</span><span class="tl-time">{{ s.time }}</span></div>
          </div>
        </div>
      </div>

      <!-- Items Table -->
      <div class="section-card">
        <h3 class="sc-title">Order Items &amp; Picking Status</h3>
        <div class="table-scroll">
          <table class="data-table">
            <thead><tr>
              <th>Material</th><th class="num">Order Qty</th><th class="num">Del Qty</th><th class="num">Picked</th><th class="num">Remaining</th><th>Status</th>
            </tr></thead>
            <tbody>
              <tr v-for="it in dItems" :key="it.id">
                <td><div class="mtl-name">{{ it.matName }}</div><div class="mtl-code">{{ it.matId }}</div></td>
                <td class="num">{{ it.orderQty }} {{ it.uom }}</td>
                <td class="num">{{ it.delQty }} {{ it.uom }}</td>
                <td class="num" :class="{ 'partial': it.pickedNum > 0 && it.pickedNum < it.delQtyNum }">{{ it.picked }} {{ it.uom }}</td>
                <td class="num" :class="{ 'remaining-num': it.rem > 0 }">{{ it.rem }} {{ it.uom }}</td>
                <td><span class="istag" :class="it.stCls">{{ it.stLbl }}</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Pick History -->
      <div class="section-card" v-if="pickRecords.length > 0">
        <h3 class="sc-title">Pick Batch History ({{ pickRecords.length }} records)</h3>
        <div class="table-scroll">
          <table class="data-table">
            <thead><tr><th>Batch</th><th>Material</th><th class="num">Pick Qty</th><th>Location</th><th>Time</th><th>By</th></tr></thead>
            <tbody>
              <tr v-for="pr in pickRecords" :key="pr.pickId">
                <td><span class="batch-badge">#{{ pr.batchNo }}</span></td>
                <td>{{ pr.materialName || pr.materialId }}</td>
                <td class="num">{{ fmtNum(pr.pickQuantity) }}</td>
                <td>{{ pr.storageLocation || '-' }}</td>
                <td class="time-cell">{{ fmtTs(pr.pickDate) }}</td>
                <td>{{ pr.pickedBy || '-' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- GI History -->
      <div class="section-card" v-if="giRecords.length > 0">
        <h3 class="sc-title">Goods Issue History ({{ giRecords.length }} records)</h3>
        <div class="table-scroll">
          <table class="data-table">
            <thead><tr><th>Batch</th><th>Material</th><th class="num">GI Qty</th><th>Date</th><th>Warehouse</th></tr></thead>
            <tbody>
              <tr v-for="gi in giRecords" :key="gi.goodsIssueId">
                <td><span class="batch-badge">#{{ gi.batchNo }}</span></td>
                <td>{{ gi.materialName || gi.materialId }}</td>
                <td class="num">{{ fmtNum(gi.actualQuantity) }}</td>
                <td>{{ gi.postingDate ? gi.postingDate.split('T')[0] : '-' }}</td>
                <td>{{ gi.warehouse || '-' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Shipment Info -->
      <div class="section-card">
        <h3 class="sc-title">Shipment Information</h3>
        <div class="si-grid">
          <div class="si-item"><span class="si-label">Ship-to</span><span class="si-value">{{ delivery.shipToPartyName || delivery.shipToParty }}</span></div>
          <div class="si-item"><span class="si-label">Address</span><span class="si-value mono">{{ delivery.shipToAddress || 'N/A' }}</span></div>
          <div class="si-item"><span class="si-label">Shipping Point</span><span class="si-value">{{ delivery.shippingPoint || 'N/A' }}</span></div>
          <div class="si-item"><span class="si-label">Route</span><span class="si-value">{{ delivery.route || 'N/A' }}</span></div>
          <div class="si-item"><span class="si-label">Carrier / Driver</span><span class="si-value">{{ delivery.carrier || 'N/A' }}{{ delivery.driverName ? ' . ' + delivery.driverName : '' }}</span></div>
          <div class="si-item"><span class="si-label">Tracking No.</span><span class="si-value">{{ delivery.trackingNo || 'N/A' }}</span></div>
        </div>
      </div>
    </div>

    <!-- ====== Pick Batch Modal ====== -->
    <div class="modal-overlay" v-if="showPickDialog" @click.self="showPickDialog=false">
      <div class="modal-card">
        <div class="modal-header">
          <h3>Record Pick Batch</h3>
          <button class="modal-close" @click="showPickDialog=false">&times;</button>
        </div>
        <div class="modal-body">
          <p class="modal-hint">Enter integer quantities picked in this batch. Multiple batches can be recorded.</p>
          <div class="pick-meta">
            <label class="meta-field"><span>Storage Location</span><div class="f4-inline"><input :value="batchLocDisplay" class="form-input-inline" placeholder="Click to search..." readonly @click="openSlocF4" style="cursor:pointer;min-width:200px;background:#fff" /><button class="f4-btn-inline" @click="openSlocF4" title="F4 Search"><svg viewBox="0 0 16 16" width="13" height="13"><circle cx="7" cy="7" r="4.5" fill="none" stroke="currentColor" stroke-width="1.3"/><path d="M10.5 10.5l3.5 3.5" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg></button></div></label>
            <label class="meta-field"><span>Picked By</span><input v-model="batchBy" class="form-input-inline" placeholder="Operator name" /></label>
          </div>
          <table class="data-table">
            <thead><tr><th>Material</th><th class="num">Delivery Qty</th><th class="num">Already Picked</th><th class="num">This Batch</th></tr></thead>
            <tbody>
              <tr v-for="it in dItems" :key="it.id">
                <td>{{ it.matName }}</td>
                <td class="num">{{ it.delQty }} {{ it.uom }}</td>
                <td class="num">{{ it.picked }} {{ it.uom }}</td>
                <td class="num">
                  <input type="number" class="qty-input" v-model.number="pickIn[it.id]" :max="it.rem" min="0" step="1" :disabled="it.rem <= 0" />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="modal-footer">
          <button class="btn btn-outline" @click="showPickDialog=false">Cancel</button>
          <button class="btn btn-primary" @click="doPickBatch" :disabled="pickBusy">
            {{ pickBusy ? 'Recording...' : 'Record Pick Batch' }}
          </button>
        </div>
      </div>
    </div>

    <!-- ====== Storage Location F4 Popup ====== -->
    <div class="modal-overlay" v-if="showSlocF4" @click.self="showSlocF4=false">
      <div class="modal-card" style="min-width:600px;max-height:70vh">
        <div class="modal-header">
          <h3>Storage Location Search</h3>
          <button class="modal-close" @click="showSlocF4=false">&times;</button>
        </div>
        <div class="modal-body">
          <div style="display:flex;gap:8px;margin-bottom:12px">
            <input v-model="slocKeyword" class="form-input-inline" placeholder="Search by ID, name, or bin..." style="flex:1" @keyup.enter="searchSloc" />
            <button class="btn btn-outline" @click="searchSloc" style="padding:6px 12px;font-size:12px">Search</button>
          </div>
          <div class="table-scroll" style="max-height:300px">
            <table class="data-table">
              <thead><tr><th>Location</th><th>Name</th><th>Plant</th><th>Warehouse</th><th>Type</th><th>Bin</th></tr></thead>
              <tbody>
                <tr v-for="sl in slocList" :key="sl.slocId" class="data-row" style="cursor:pointer" @click="selectSloc(sl)">
                  <td class="mono">{{ sl.slocId }}</td>
                  <td>{{ sl.slocName }}</td>
                  <td>{{ sl.plant }}</td>
                  <td>{{ sl.warehouseNo || '-' }}</td>
                  <td>{{ sl.storageType || '-' }}</td>
                  <td class="mono">{{ sl.storageBin || '-' }}</td>
                </tr>
                <tr v-if="slocList.length===0"><td colspan="6" style="text-align:center;padding:16px;color:rgba(18,55,42,0.4)">No locations found. Try a different keyword.</td></tr>
              </tbody>
            </table>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-outline" @click="showSlocF4=false">Cancel</button>
        </div>
      </div>
    </div>
    <!-- ====== Pick Batch Success Summary Modal ====== -->
    <div class="modal-overlay" v-if="showPickSummary" @click.self="closePickSummary">
      <div class="modal-card" style="min-width:420px">
        <div class="modal-header" style="background:rgba(67,104,80,0.06)">
          <h3 style="color:#436850">Pick Batch Recorded</h3>
        </div>
        <div class="modal-body">
          <div class="summary-table">
            <div v-for="s in pickSummaryItems" :key="s.id" class="summary-row">
              <span>{{ s.name }}</span>
              <span class="summary-val">{{ s.qty }} {{ s.uom }} <span v-if="s.remaining > 0" class="remaining-num">({{ s.remaining }} remaining)</span><span v-else class="done-text"> - Complete</span></span>
            </div>
          </div>
          <div style="margin-top:16px;padding:12px;background:rgba(67,104,80,0.05);border-radius:8px;font-size:12px;color:rgba(18,55,42,0.55);text-align:center">
            <template v-if="allFullyPicked">All items fully picked. You may now Confirm Picking Complete.</template>
            <template v-else>Partial pick recorded. {{ remainingCount }} item(s) still need picking.</template>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-outline" @click="closePickSummary">Continue Picking</button>
          <button v-if="allFullyPicked" class="btn btn-primary" @click="closePickSummary(); doConfirmPicking()">Confirm Picking Complete</button>
        </div>
      </div>
    </div>

    <!-- ====== Confirm Action Modal ====== -->
    <div class="modal-overlay" v-if="showConfirmModal" @click.self="showConfirmModal=false">
      <div class="modal-card" style="min-width:400px">
        <div class="modal-header">
          <h3>{{ confirmTitle }}</h3>
        </div>
        <div class="modal-body">
          <p style="font-size:13px;color:rgba(18,55,42,0.6);margin:0">{{ confirmMsg }}</p>
        </div>
        <div class="modal-footer">
          <button class="btn btn-outline" @click="showConfirmModal=false; confirmReject?.()">Cancel</button>
          <button class="btn btn-primary" @click="showConfirmModal=false; confirmResolve?.()" :disabled="confirmBusy">
            {{ confirmBusy ? 'Processing...' : 'Confirm' }}
          </button>
        </div>
      </div>
    </div>

    <!-- ====== Result Toast Modal ====== -->
    <div class="modal-overlay" v-if="showResultModal" @click.self="showResultModal=false">
      <div class="modal-card" style="min-width:360px">
        <div class="modal-header" :style="resultOk ? 'background:rgba(67,104,80,0.06)' : 'background:rgba(217,83,79,0.06)'">
          <h3 :style="resultOk ? 'color:#436850' : 'color:#D9534F'">{{ resultTitle }}</h3>
        </div>
        <div class="modal-body">
          <p style="font-size:13px;color:rgba(18,55,42,0.6);margin:0;white-space:pre-wrap">{{ resultMsg }}</p>
        </div>
        <div class="modal-footer" style="justify-content:center">
          <button class="btn btn-primary" @click="showResultModal=false">OK</button>
        </div>
      </div>
    </div>

    <!-- ====== PGI Modal ====== -->
    <div class="modal-overlay" v-if="showPgiDialog" @click.self="showPgiDialog=false">
      <div class="modal-card">
        <div class="modal-header">
          <h3>Post Goods Issue</h3>
          <button class="modal-close" @click="showPgiDialog=false">&times;</button>
        </div>
        <div class="modal-body">
          <p class="modal-hint">Enter integer goods issue quantities. Cannot exceed picked quantity.</p>
          <table class="data-table">
            <thead><tr><th>Material</th><th class="num">Picked</th><th class="num">Already Issued</th><th class="num">This Batch</th></tr></thead>
            <tbody>
              <tr v-for="it in dItems" :key="it.id">
                <td>{{ it.matName }}</td>
                <td class="num">{{ it.picked }} {{ it.uom }}</td>
                <td class="num">{{ it.issued }} {{ it.uom }}</td>
                <td class="num">
                  <input type="number" class="qty-input" v-model.number="pgiIn[it.id]" :max="it.pickedNum - it.issuedNum" min="0" step="1" :disabled="it.pickedNum <= 0" />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="modal-footer">
          <button class="btn btn-outline" @click="showPgiDialog=false">Cancel</button>
          <button class="btn btn-primary" @click="doPostGi" :disabled="pgiBusy">
            {{ pgiBusy ? 'Posting...' : 'Post Goods Issue' }}
          </button>
        </div>
      </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { 
  fetchDeliveryById, 
  startPicking, 
  confirmPicking, 
  shipDelivery, 
  pickBatch, 
  fetchPickRecords, 
  postGoodsIssue, 
  fetchGoodsIssues, 
  fetchStorageLocations 
} from '@/api/modules/logistics'

const route = useRoute()
const router = useRouter()

const delivery = ref<any>(null)
const loading = ref(false)
const error = ref('')
const loadMsg = ref('Initializing...')
const posting = ref(false)

// Pick batch
const showPickDialog = ref(false)
const pickBusy = ref(false)
const pickIn = reactive<Record<string, number>>({})
const batchLoc = ref('')
const batchLocName = ref('')
const batchBy = ref('')

// Storage Location F4
const showSlocF4 = ref(false)
const slocKeyword = ref('')
const slocList = ref<any[]>([])
const showPickSummary = ref(false)
const pickSummaryItems = ref<any[]>([])

// Confirm modal
const showConfirmModal = ref(false)
const confirmTitle = ref('')
const confirmMsg = ref('')
const confirmBusy = ref(false)
let confirmResolve: (() => void) | null = null
let confirmReject: (() => void) | null = null

// Result modal
const showResultModal = ref(false)
const resultOk = ref(true)
const resultTitle = ref('')
const resultMsg = ref('')

// PGI
const showPgiDialog = ref(false)
const pgiBusy = ref(false)
const pgiIn = reactive<Record<string, number>>({})

// History
const pickRecords = ref<any[]>([])
const giRecords = ref<any[]>([])

const S: Record<string, string> = { OPEN: 'Creating', PICKING: 'Picking', SHIPPED: 'Picked', IN_TRANSIT: 'In Transit', PGI_DONE: 'Completed', CANCELLED: 'Cancelled' }
const A: Record<string, string> = { OPEN: 'Start Picking', SHIPPED: 'Ship', IN_TRANSIT: 'Post Goods Issue' }
const SC: Record<string, string> = { PGI_DONE: 's-done', SHIPPED: 's-pick', PICKING: 's-pick', IN_TRANSIT: 's-pick', OPEN: 's-creating', CANCELLED: 's-cancel' }
const SM: Record<string, string> = { OPEN: 'Open', PARTIAL_PICKED: 'Partial', PICKED: 'Picked', COMPLETED: 'Done', PARTIAL_ISSUED: 'Partial GI' }
const CL: Record<string, string> = { OPEN: 'is-open', PARTIAL_PICKED: 'is-partial', PICKED: 'is-picked', COMPLETED: 'is-done', PARTIAL_ISSUED: 'is-partial' }

const statusLabel = computed(() => delivery.value ? (S[delivery.value.deliveryStatus] || delivery.value.deliveryStatus) : '')
const statusClass = computed(() => delivery.value ? (SC[delivery.value.deliveryStatus] || '') : '')
const nextActionLabel = computed(() => delivery.value ? (A[delivery.value.deliveryStatus] || '') : '')
const totalQty = computed(() => delivery.value ? Number(delivery.value.totalQuantity || 0).toFixed(0) : '0')
const pickedTotal = computed(() => {
  if (!delivery.value) return '0'
  return (delivery.value.items || []).reduce((s: number, it: any) => s + (it.pickedQuantity || 0), 0).toString()
})

const batchLocDisplay = computed(() => {
  if (batchLoc.value && batchLocName.value) return batchLoc.value + ' - ' + batchLocName.value
  if (batchLoc.value) return batchLoc.value
  return ''
})

const dItems = computed(() => {
  if (!delivery.value?.items) return []
  return delivery.value.items.map((it: any) => {
    const dq = Math.floor(Number(it.deliveryQuantity || 0))
    const pk = Math.floor(Number(it.pickedQuantity || 0))
    const rem = Math.max(0, dq - pk)
    const st = it.itemStatus || 'OPEN'
    
    // Calculate issued quantity from giRecords
    const issuedNum = (giRecords.value || [])
      .filter((gi: any) => gi.deliveryItemId === it.deliveryItemId)
      .reduce((sum: number, gi: any) => sum + Number(gi.actualQuantity || 0), 0)

    return {
      id: it.deliveryItemId, matId: it.materialId, matName: it.materialName || it.materialId,
      orderQty: Math.floor(Number(it.orderQuantity || 0)).toString(),
      delQty: dq.toString(), delQtyNum: dq, uom: it.baseUnit || it.salesUnit || '',
      picked: pk.toString(), pickedNum: pk, rem: rem.toString(), remNum: rem,
      issued: issuedNum.toString(), issuedNum: issuedNum,
      stLbl: SM[st] || st, stCls: CL[st] || 'is-open',
    }
  })
})

watch(showPgiDialog, (v) => {
  if (v && delivery.value) {
    // Pre-fill PGI quantities with remaining to issue
    dItems.value.forEach(it => {
      const remainingToIssue = it.pickedNum - it.issuedNum
      pgiIn[it.id] = remainingToIssue > 0 ? remainingToIssue : 0
    })
  }
})

const allFullyPicked = computed(() => dItems.value.every((it: any) => it.remNum <= 0))
const remainingCount = computed(() => dItems.value.filter((it: any) => it.remNum > 0).length)

const steps = computed(() => {
  if (!delivery.value) return []
  const m: Record<string, number> = { OPEN: 0, PICKING: 1, SHIPPED: 2, IN_TRANSIT: 2, PGI_DONE: 3, CANCELLED: -1 }
  const si = m[delivery.value.deliveryStatus] ?? 0
  return [
    { label: 'Created', time: '', done: si >= 0, cur: si === 0 },
    { label: 'Picking', time: delivery.value.pickingDate || '', done: si >= 1, cur: si === 1 },
    { label: 'Picked', time: (si >= 2 ? (delivery.value.plannedGiDate || '') : ''), done: si >= 2, cur: si === 2 },
    { label: 'Goods Issue', time: delivery.value.actualGiDate ? delivery.value.actualGiDate.split('T')[0] : '', done: si >= 3, cur: si === 3 },
  ]
})

function fmtNum(v: any) { return Math.floor(Number(v || 0)).toString() }
function fmtTs(ts: string) {
  if (!ts) return '-'
  try { return new Date(ts).toLocaleString('zh-CN', { month:'2-digit', day:'2-digit', hour:'2-digit', minute:'2-digit' }) } catch { return ts }
}

function showResult(ok: boolean, title: string, msg: string) {
  resultOk.value = ok; resultTitle.value = title; resultMsg.value = msg; showResultModal.value = true
}

function askConfirm(title: string, msg: string): Promise<boolean> {
  return new Promise((resolve) => {
    confirmTitle.value = title; confirmMsg.value = msg; showConfirmModal.value = true
    confirmResolve = () => resolve(true); confirmReject = () => resolve(false)
  })
}

function closePickSummary() { showPickSummary.value = false; pickSummaryItems.value = [] }

async function searchSloc() {
  try {
    const res: any = await fetchStorageLocations({ keyword: slocKeyword.value })
    slocList.value = res || []
  } catch { slocList.value = [] }
}
function selectSloc(sl: any) {
  batchLoc.value = sl.slocId
  batchLocName.value = sl.slocName
  showSlocF4.value = false
}
watch(showSlocF4, (v) => { if (v) { slocKeyword.value = ''; searchSloc() } })


// ====== F4 Storage Location ======
function openSlocF4() { showSlocF4.value = true; slocKeyword.value = ''; searchSloc() }

async function loadData() {
  const id = route.params.id as string
  if (!id) { error.value = 'No delivery ID'; loading.value = false; return }
  loading.value = true; error.value = ''; loadMsg.value = 'Fetching delivery...'
  try {
    loadMsg.value = 'Loading delivery data...'
    const res: any = await fetchDeliveryById(id)
    delivery.value = res
    loadMsg.value = 'Initializing...'
    for (const it of (res.items || [])) {
      pickIn[it.deliveryItemId] = 0; pgiIn[it.deliveryItemId] = 0
    }
    loadMsg.value = 'Loading pick history...'
    try { const pr: any = await fetchPickRecords(id); pickRecords.value = pr || [] } catch { pickRecords.value = [] }
    loadMsg.value = 'Loading GI history...'
    try { const gi: any = await fetchGoodsIssues(id); giRecords.value = gi || [] } catch { giRecords.value = [] }
  } catch (err: any) {
    error.value = err.message || 'Failed to load delivery'; console.error(err)
  } finally { loading.value = false }
}

async function handleAction() {
  if (!delivery.value) return
  const s = delivery.value.deliveryStatus
  if (s === 'IN_TRANSIT') { showPgiDialog.value = true; return }
  const label = A[s]
  if (!label) return
  const ok = await askConfirm(label, `${label} for delivery ${delivery.value.deliveryId}?`)
  if (!ok) return
  posting.value = true
  try {
    if (s === 'OPEN') await startPicking(delivery.value.deliveryId)
    else if (s === 'SHIPPED') await shipDelivery(delivery.value.deliveryId)
    showResult(true, 'Success', `${label} completed successfully.`)
    await loadData()
  } catch (err: any) {
    showResult(false, 'Error', `${label} failed: ${err.message || 'Unknown error'}`)
  } finally { posting.value = false }
}

async function doPickBatch() {
  if (!delivery.value) return
  const items = dItems.value.filter((it: any) => (pickIn[it.id] || 0) > 0).map((it: any) => ({ deliveryItemId: it.id, quantity: pickIn[it.id] }))
  if (items.length === 0) { showResult(false, 'Invalid Input', 'Please enter at least one pick quantity.'); return }
  pickBusy.value = true
  try {
    await pickBatch(delivery.value.deliveryId, {
      items,
      storageLocation: batchLoc.value || undefined,
      pickedBy: batchBy.value || undefined,
    })
    // Build summary
    const summary = dItems.value.filter((it: any) => (pickIn[it.id] || 0) > 0).map((it: any) => {
      const qty = pickIn[it.id]; const remaining = Math.max(0, it.delQtyNum - it.pickedNum - qty)
      return { id: it.id, name: it.matName, qty: qty, uom: it.uom, remaining }
    })
    pickSummaryItems.value = summary
    showPickDialog.value = false
    for (const k in pickIn) pickIn[k] = 0
    batchLoc.value = ''; batchLocName.value = ''; batchBy.value = ''
    await loadData()
    showPickSummary.value = true
  } catch (err: any) {
    showResult(false, 'Pick Batch Failed', err.message || 'Unknown error')
  } finally { pickBusy.value = false }
}

async function doConfirmPicking() {
  if (!delivery.value || !allFullyPicked.value) return
  const ok = await askConfirm('Confirm Picking Complete', 'All items have been fully picked. Confirm and move to Picked (SHIPPED) status?')
  if (!ok) return
  posting.value = true
  try {
    await confirmPicking(delivery.value.deliveryId)
    showResult(true, 'Picking Confirmed', 'All items are now in Picked status. Delivery is ready to ship.')
    await loadData()
  } catch (err: any) {
    showResult(false, 'Confirmation Failed', err.message || 'Unknown error')
  } finally { posting.value = false }
}

async function doPostGi() {
  if (!delivery.value) return
  const items = dItems.value.filter((it: any) => (pgiIn[it.id] || 0) > 0).map((it: any) => ({ deliveryItemId: it.id, quantity: pgiIn[it.id] }))
  if (items.length === 0) { showResult(false, 'Invalid Input', 'Please enter at least one GI quantity.'); return }
  pgiBusy.value = true
  try {
    await postGoodsIssue(delivery.value.deliveryId, { items })
    showPgiDialog.value = false
    for (const k in pgiIn) pgiIn[k] = 0
    showResult(true, 'Goods Issue Posted', 'Goods issue recorded successfully.')
    await loadData()
  } catch (err: any) {
    showResult(false, 'Post GI Failed', err.message || 'Unknown error')
  } finally { pgiBusy.value = false }
}

function print() { window.print() }

onMounted(() => loadData())
</script>

<style scoped>
.page{padding:28px 36px;max-width:1300px;margin:0 auto;}
.top-bar{display:flex;align-items:center;gap:16px;margin-bottom:22px;flex-wrap:wrap;}
.back-btn{display:inline-flex;align-items:center;gap:6px;background:none;border:1px solid rgba(173,188,159,0.35);border-radius:8px;padding:8px 16px;font-size:13px;color:rgba(18,55,42,0.55);cursor:pointer;font-family:inherit;transition:all 0.2s;}
.back-btn:hover{border-color:#436850;color:#436850;}
.hc-icon{width:42px;height:42px;border-radius:10px;background:rgba(67,104,80,0.08);display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.top-info{display:flex;flex-direction:column;}
.ti-label{font-size:10px;color:rgba(18,55,42,0.35);text-transform:uppercase;letter-spacing:1px;font-weight:600;}
.ti-value{font-size:22px;font-weight:800;color:#12372A;font-family:'SF Mono',Consolas,monospace;}
.ti-sub{font-size:12px;color:rgba(18,55,42,0.4);}
.stag{font-size:11px;font-weight:600;padding:5px 12px;border-radius:6px;}
.s-done{background:rgba(67,104,80,0.1);color:#436850;}
.s-pick{background:rgba(240,173,78,0.12);color:#c98a20;}
.s-creating{background:rgba(173,188,159,0.2);color:#436850;}
.s-cancel{background:rgba(217,83,79,0.1);color:#D9534F;}

.info-cards{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:20px;}
.ic{background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:12px;padding:16px 18px;border:1px solid rgba(173,188,159,0.15);box-shadow:0 2px 6px rgba(173,188,159,0.1);}
.ic-label{font-size:10px;color:rgba(18,55,42,0.4);font-weight:600;text-transform:uppercase;letter-spacing:0.5px;display:block;margin-bottom:6px;}
.ic-value{font-size:15px;font-weight:700;color:#12372A;}

.section-card{background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:14px;padding:22px;border:1px solid rgba(173,188,159,0.15);box-shadow:0 2px 6px rgba(173,188,159,0.1);margin-bottom:18px;}
.sc-title{font-size:14px;font-weight:700;color:#436850;margin:0 0 12px;display:flex;align-items:center;gap:8px;}
.sc-title::before{content:'';width:3px;height:13px;background:#436850;border-radius:2px;}

.timeline{display:flex;align-items:flex-start;padding:8px 0;}
.tl-step{flex:1;position:relative;display:flex;flex-direction:column;align-items:center;}
.tl-dot{width:13px;height:13px;border-radius:50%;border:2px solid rgba(173,188,159,0.35);background:#FBFADA;z-index:1;}
.tl-step.done .tl-dot{background:#436850;border-color:#436850;}
.tl-step.cur .tl-dot{background:#436850;border-color:#436850;box-shadow:0 0 0 4px rgba(67,104,80,0.12);}
.tl-line{position:absolute;top:6px;left:50%;width:100%;height:2px;background:rgba(173,188,159,0.25);}
.tl-step.done .tl-line{background:#436850;}
.tl-info{margin-top:10px;text-align:center;}
.tl-status{font-size:11px;font-weight:600;color:rgba(18,55,42,0.45);display:block;}
.tl-step.cur .tl-status,.tl-step.done .tl-status{color:#436850;}
.tl-time{font-size:10px;color:rgba(18,55,42,0.28);display:block;margin-top:2px;}

.si-grid{display:flex;flex-direction:column;gap:14px;}
.si-item{display:flex;flex-direction:column;gap:2px;}
.si-label{font-size:10px;color:rgba(18,55,42,0.38);font-weight:600;text-transform:uppercase;letter-spacing:0.5px;}
.si-value{font-size:13px;color:#12372A;line-height:1.6;}

.table-scroll{overflow-x:auto;}
.data-table{width:100%;border-collapse:collapse;font-size:13px;}
.data-table th{text-align:left;padding:9px 12px;font-size:10px;font-weight:700;color:rgba(18,55,42,0.4);text-transform:uppercase;letter-spacing:0.5px;border-bottom:1px solid rgba(173,188,159,0.2);white-space:nowrap;}
.data-table th.num{text-align:right;}
.data-table td{padding:9px 12px;border-bottom:1px solid rgba(173,188,159,0.07);color:#12372A;}
.data-table td.num{text-align:right;}
.data-table td.time-cell{font-size:11px;color:rgba(18,55,42,0.5);}
.mono{font-family:'SF Mono',Consolas,monospace;font-size:12px;}
.mtl-name{font-size:13px;font-weight:600;color:#12372A;}
.mtl-code{font-size:10px;color:rgba(18,55,42,0.35);margin-top:1px;}
.partial{color:#c98a20;font-weight:700;}
.remaining-num{color:#D9534F;font-weight:600;}
.done-text{color:#436850;font-weight:600;}

.istag{font-size:10px;font-weight:600;padding:3px 8px;border-radius:4px;}
.is-open{background:rgba(173,188,159,0.2);color:#5a7a5f;}
.is-picked{background:rgba(67,104,80,0.12);color:#436850;}
.is-partial{background:rgba(240,173,78,0.15);color:#c98a20;}
.is-done{background:rgba(67,104,80,0.08);color:#2d4a38;}

.batch-badge{display:inline-block;background:rgba(67,104,80,0.08);color:#436850;font-size:11px;font-weight:700;padding:2px 8px;border-radius:4px;}

.pick-meta{display:flex;gap:16px;margin-bottom:16px;}
.meta-field{display:flex;flex-direction:column;gap:4px;font-size:11px;color:rgba(18,55,42,0.5);}
.form-input-inline{height:32px;border:1px solid rgba(173,188,159,0.4);border-radius:6px;padding:0 10px;font-size:12px;font-family:inherit;background:#fff;color:#12372A;outline:none;min-width:150px;}
.form-input-inline:focus{border-color:#436850;box-shadow:0 0 0 3px rgba(67,104,80,0.06);}

.summary-table{display:flex;flex-direction:column;gap:8px;}
.summary-row{display:flex;justify-content:space-between;align-items:center;font-size:13px;color:#12372A;padding:8px 12px;background:rgba(173,188,159,0.08);border-radius:6px;}
.summary-val{font-weight:600;color:#436850;}

.modal-overlay{position:fixed;inset:0;background:rgba(18,55,42,0.3);backdrop-filter:blur(4px);display:flex;align-items:center;justify-content:center;z-index:2000;}
.modal-card{background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:18px;padding:0;box-shadow:0 20px 60px rgba(18,55,42,0.22);border:1px solid rgba(173,188,159,0.2);min-width:560px;max-width:720px;max-height:82vh;overflow-y:auto;}
.modal-header{display:flex;align-items:center;justify-content:space-between;padding:18px 24px;border-bottom:1px solid rgba(173,188,159,0.18);}
.modal-header h3{font-size:16px;font-weight:700;color:#12372A;margin:0;}
.modal-close{background:none;border:none;font-size:18px;color:rgba(18,55,42,0.35);cursor:pointer;padding:4px;border-radius:6px;line-height:1;transition:all 0.2s;}
.modal-close:hover{background:rgba(217,83,79,0.08);color:#D9534F;}
.modal-body{padding:20px 24px;}
.modal-hint{font-size:12px;color:rgba(18,55,42,0.45);margin:0 0 14px;}
.modal-footer{display:flex;justify-content:flex-end;gap:10px;padding:14px 24px;border-top:1px solid rgba(173,188,159,0.15);background:rgba(251,250,218,0.25);}
.qty-input{width:80px;height:30px;border:1px solid rgba(173,188,159,0.4);border-radius:6px;text-align:right;padding:0 8px;font-size:13px;font-family:inherit;background:#fff;color:#12372A;}
.qty-input:focus{border-color:#436850;outline:none;box-shadow:0 0 0 3px rgba(67,104,80,0.06);}
.qty-input:disabled{background:rgba(173,188,159,0.1);color:rgba(18,55,42,0.25);cursor:not-allowed;}

.btn{display:inline-flex;align-items:center;gap:6px;padding:10px 22px;font-size:13px;font-weight:600;border-radius:8px;cursor:pointer;transition:all 0.2s;font-family:inherit;}
.btn-primary{background:linear-gradient(135deg,#436850,#365440);color:#FBFADA;border:none;box-shadow:0 4px 12px rgba(67,104,80,0.2);}
.btn-primary:hover{transform:translateY(-1px);}
.btn-primary:disabled{opacity:0.6;cursor:not-allowed;transform:none;}
.btn-outline{background:rgba(173,188,159,0.2);color:#436850;border:1px solid rgba(173,188,159,0.3);}
.btn-outline:hover{background:rgba(173,188,159,0.3);border-color:#436850;color:#436850;}
.btn-outline:disabled{opacity:0.5;cursor:not-allowed;}
.f4-inline{display:flex;align-items:center;gap:0;}
.f4-btn-inline{display:flex;align-items:center;justify-content:center;width:32px;height:32px;border:1px solid rgba(173,188,159,0.4);border-left:none;border-radius:0 6px 6px 0;background:rgba(67,104,80,0.06);color:#436850;cursor:pointer;padding:0;}
.f4-btn-inline:hover{background:rgba(67,104,80,0.12);}
.error-msg{color:#D9534F;font-size:13px;padding:10px 14px;background:rgba(217,83,79,0.08);border-radius:8px;margin-bottom:14px;}

/* Print Styles for Delivery Note */
@media print {
  .top-bar .btn, .top-bar .back-btn, .hc-icon, .timeline, .modal-overlay, .tf-right {
    display: none !important;
  }
  .page {
    padding: 0 !important;
    max-width: 100% !important;
    background: #fff !important;
  }
  .section-card {
    background: #fff !important;
    border: 1px solid #eee !important;
    box-shadow: none !important;
    break-inside: avoid;
  }
  .ti-value {
    font-size: 28px !important;
  }
  .data-table th {
    background: #f9f9f9 !important;
    color: #000 !important;
    border-bottom: 2px solid #000 !important;
  }
  .data-table td {
    border-bottom: 1px solid #eee !important;
  }
  body {
    background: #fff !important;
  }
  .MainLayout {
    padding: 0 !important;
  }
}
</style>
