<template>
  <div class="page">
    <div class="header-card">
      <div class="hc-left">
        <div class="hc-icon">
          <svg viewBox="0 0 24 24" width="22" height="22">
            <rect x="2" y="5" width="20" height="13" rx="2" fill="none" stroke="#436850" stroke-width="1.8"/>
            <path d="M6 5V3M18 5V3M2 11h20M7 16h3" fill="none" stroke="#436850" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
        </div>
        <div class="hc-text">
          <h2 class="hc-title">Delivery List</h2>
          <p class="hc-sub">View and manage all delivery orders.</p>
        </div>
      </div>
    </div>

    <div class="filter-bar">
      <input type="text" class="form-input search-so" v-model="filters.salesOrder" placeholder="Sales Order" />
      <input type="text" class="form-input search-cust" v-model="filters.customer" placeholder="Customer" />
      <select class="form-select search-st" v-model="filters.status">
        <option value="">All Statuses</option>
        <option value="Creating">Creating</option>
        <option value="Picking">Picking</option>
        <option value="Picked">Picked</option>
        <option value="In Transit">In Transit</option>
        <option value="Completed">Completed</option>
        <option value="Cancelled">Cancelled</option>
      </select>
      <button class="btn btn-primary" @click="search">Search</button>
      <button class="btn btn-outline" @click="reset">Reset</button>
    </div>

    <div v-if="error" class="error-msg">{{ error }}</div>

    <div class="data-card">
      <table class="data-table">
        <thead>
          <tr>
            <th>Delivery No.</th>
            <th>Sales Order</th>
            <th>Customer</th>
            <th>GI Date</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td colspan="6" style="text-align:center;padding:40px;color:#999;">Loading deliveries...</td>
          </tr>
          <template v-else>
            <tr v-for="r in rows" :key="r.id" class="data-row">
              <td class="mono">{{ r.no }}</td>
              <td class="mono">{{ r.so }}</td>
              <td>{{ r.cust }}</td>
              <td>{{ r.date }}</td>
              <td><span class="stag" :class="sc(r.st)">{{ r.st }}</span></td>
              <td>
                <a class="link" @click="viewDetail(r.id)">View</a>
                <template v-if="r.canPgi">
                  <span class="divider">|</span>
                  <a class="link" @click="processDelivery(r)">{{ r.actionLabel }}</a>
                </template>
                <template v-if="r.st === 'Completed'">
                  <span class="divider">|</span>
                  <a v-if="r.invoiceId" class="link muted-link" @click="viewInvoice(r.invoiceId)">Invoice: {{ r.invoiceId }}</a>
                  <a v-else class="link" @click="createInvoice(r.id)">Create Invoice</a>
                </template>
              </td>
            </tr>
          </template>
          <tr v-if="!loading && rows.length === 0">
            <td colspan="6" style="text-align:center;padding:40px;color:#999;">No deliveries found.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { alert, confirm } from '@/utils/toast'
import { confirmPicking, fetchDeliveries, postGoodsIssue, shipDelivery, startPicking } from '@/api/modules/logistics'
import { createInvoiceFromDelivery } from '@/api/modules/finance'
import type { DeliveryListItem } from '@/api/modules/logistics'

const router = useRouter()

interface Row { id: string; no: string; so: string; cust: string; date: string; st: string; rawStatus: string; canPgi: boolean; actionLabel: string; invoiceId?: string }
const rows = ref<Row[]>([])
const loading = ref(false)
const error = ref('')

const filters = reactive({
  deliveryNo: '',
  salesOrder: '',
  customer: '',
  status: '',
})

const STATUS_LABEL: Record<string, string> = {
  OPEN: 'Creating', PICKING: 'Picking', SHIPPED: 'Picked',
  IN_TRANSIT: 'In Transit', PGI_DONE: 'Completed', CANCELLED: 'Cancelled',
}

const ACTION_LABEL: Record<string, string> = {
  OPEN: 'Start Picking',
  PICKING: '',
  SHIPPED: 'Ship',
  IN_TRANSIT: 'Post GI',
}

async function fetchData() {
  loading.value = true
  error.value = ''
  try {
    const params: Record<string, any> = { page: 1, pageSize: 100 }
    if (filters.deliveryNo) params.deliveryNo = filters.deliveryNo
    if (filters.salesOrder) params.salesOrderNo = filters.salesOrder
    if (filters.customer) params.customerName = filters.customer
    if (filters.status) params.status = filters.status

    const res = await fetchDeliveries(params)
    rows.value = (res.items || []).map((i: DeliveryListItem) => ({
      id: i.deliveryId,
      no: i.deliveryId,
      so: i.salesOrderId || 'N/A',
      cust: i.shipToPartyName || i.shipToParty || 'N/A',
      date: i.actualGiDate?.split('T')[0] || i.plannedGiDate || 'N/A',
      st: STATUS_LABEL[i.deliveryStatus] || i.deliveryStatus,
      rawStatus: i.deliveryStatus,
      canPgi: i.deliveryStatus !== 'PGI_DONE' && i.deliveryStatus !== 'CANCELLED',
      actionLabel: ACTION_LABEL[i.deliveryStatus] || '',
      invoiceId: i.invoiceId,
    }))
  } catch (err: any) {
    error.value = err?.message || 'Failed to load deliveries'
    console.error('Fetch deliveries failed:', err)
  } finally {
    loading.value = false
  }
}

function search() { fetchData() }

function reset() {
  Object.assign(filters, { deliveryNo: '', salesOrder: '', customer: '', status: '' })
  fetchData()
}

function sc(s: string) {
  const m: Record<string, string> = {
    Completed: 's-done', Picking: 's-proc', Picked: 's-proc',
    'In Transit': 's-proc', Creating: 's-proc', Cancelled: 's-cancel',
  }
  return m[s] || ''
}

function viewDetail(id: string) {
  router.push('/delivery/detail/' + id)
}

function viewInvoice(invoiceId: string) {
  router.push({ path: '/finance/invoice', query: { invoiceNo: invoiceId } })
}

async function processDelivery(row: Row) {
  if (row.rawStatus === 'PICKING') {
    router.push('/delivery/detail/' + row.id)
    return
  }
  if (!row.actionLabel) return
  if (!(await confirm(`${row.actionLabel} for delivery ${row.id}?`))) return
  try {
    if (row.rawStatus === 'OPEN') await startPicking(row.id)
    else if (row.rawStatus === 'SHIPPED') await shipDelivery(row.id)
    else if (row.rawStatus === 'IN_TRANSIT') await postGoodsIssue(row.id)
    alert(`${row.actionLabel} completed`)
    fetchData()
  } catch (err: any) {
    alert(`${row.actionLabel} failed: ` + (err?.message || 'Unknown error'))
  }
}

async function createInvoice(id: string) {
  if (!(await confirm(`Create invoice for delivery ${id}?`))) return
  try {
    const res = await createInvoiceFromDelivery(id)
    alert(`Invoice ${res.invoiceId} created successfully!`)
    router.push('/finance/invoice')
  } catch (err: any) {
    alert('Failed to create invoice: ' + (err.message || 'Unknown error'))
  }
}

onMounted(fetchData)
</script>

<style scoped>
.page{padding:28px 36px;max-width:1200px;margin:0 auto;}
.header-card{display:flex;align-items:center;background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:16px;padding:20px 24px;border:1px solid rgba(173,188,159,0.18);box-shadow:0 2px 8px rgba(173,188,159,0.12);margin-bottom:20px;}
.hc-left{display:flex;align-items:center;gap:14px;}
.hc-icon{width:44px;height:44px;border-radius:12px;background:rgba(67,104,80,0.08);display:flex;align-items:center;justify-content:center;}
.hc-title{font-size:18px;font-weight:800;color:#12372A;margin:0;}
.hc-sub{font-size:12px;color:rgba(18,55,42,0.45);margin:2px 0 0;}
.filter-bar{display:flex;gap:10px;margin-bottom:16px;align-items:center;flex-wrap:wrap;}
.search-so{width:140px;}
.search-cust{width:200px;}
.search-st{width:130px;}
.form-input,.form-select{height:38px;border:1px solid rgba(173,188,159,0.4);border-radius:8px;padding:0 12px;font-size:13px;color:#12372A;background:rgba(251,250,218,0.35);font-family:inherit;outline:none;transition:all 0.2s;}
.data-card{background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:14px;border:1px solid rgba(173,188,159,0.15);box-shadow:0 2px 6px rgba(173,188,159,0.1);overflow:hidden;}
.data-table{width:100%;border-collapse:collapse;font-size:13px;}
.data-table th{text-align:left;padding:12px 14px;font-size:10px;font-weight:700;color:rgba(18,55,42,0.45);text-transform:uppercase;letter-spacing:0.8px;background:rgba(173,188,159,0.08);border-bottom:1px solid rgba(173,188,159,0.2);}
.data-table td{padding:11px 14px;border-bottom:1px solid rgba(173,188,159,0.08);color:#12372A;}
.data-row:hover{background:rgba(67,104,80,0.025);}
.mono{font-family:'SF Mono',Consolas,monospace;font-size:12px;}
.stag{font-size:11px;font-weight:600;padding:4px 10px;border-radius:6px;}
.s-done{background:rgba(67,104,80,0.1);color:#436850;}
.s-proc{background:rgba(240,173,78,0.12);color:#c98a20;}
.s-cancel{background:rgba(217,83,79,0.08);color:#c94a45;}
.link{color:#436850;cursor:pointer;font-weight:600;font-size:12px;}
.link:hover{text-decoration:underline;}
.muted-link{color:rgba(18,55,42,0.55);font-weight:500;}
.divider{margin:0 8px;color:rgba(18,55,42,0.15);font-size:12px;}
.error-msg{color:#D9534F;font-size:13px;padding:10px 14px;background:rgba(217,83,79,0.08);border-radius:8px;margin-bottom:14px;}
.btn{display:inline-flex;align-items:center;gap:6px;padding:9px 20px;font-size:13px;font-weight:600;border-radius:8px;cursor:pointer;transition:all 0.2s;font-family:inherit;}
.btn-primary{background:linear-gradient(135deg,#436850,#365440);color:#FBFADA;border:none;}
.btn-primary:hover{transform:translateY(-1px);}
.btn-outline{background:none;color:rgba(18,55,42,0.5);border:1px solid rgba(173,188,159,0.35);}
.btn-outline:hover{border-color:rgba(18,55,42,0.3);color:#12372A;}
</style>
