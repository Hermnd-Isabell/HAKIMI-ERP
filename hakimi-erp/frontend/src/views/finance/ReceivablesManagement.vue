<template>
  <MainLayout>
    <div class="page">
      <div class="header-card">
        <div class="hc-left">
          <div class="hc-icon"><svg viewBox="0 0 24 24" width="22" height="22"><circle cx="12" cy="12" r="10" fill="none" stroke="#436850" stroke-width="1.8"/><path d="M12 6v6l4 2M7 12h10" fill="none" stroke="#436850" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
          <div class="hc-text"><h2 class="hc-title">Receivables Management</h2><p class="hc-sub">Monitor all receivables, collections, and aging analysis.</p></div>
        </div>
      </div>
      <div class="filter-bar">
        <input type="text" class="form-input" v-model="f.customer" placeholder="Customer (BP ID)" @keyup.enter="search" />
        <input type="text" class="form-input" v-model="f.invoiceNo" placeholder="Invoice No." @keyup.enter="search" />
        <select class="form-select" v-model="f.status">
          <option value="">All Statuses</option>
          <option value="Open">Open</option>
          <option value="Closed">Closed</option>
        </select>
        <button class="btn btn-primary" @click="search" :disabled="loading">Search</button>
        <button class="btn btn-outline" @click="reset" :disabled="loading">Reset</button>
      </div>
      <div v-if="error" class="error-msg">{{ error }}</div>
      <div class="data-card">
        <table class="data-table">
          <thead><tr>
            <th>Invoice No.</th><th>Customer</th><th>Due Date</th>
            <th class="num">Amount</th><th class="num">Outstanding</th><th>Status</th><th>Action</th>
          </tr></thead>
          <tbody>
            <tr v-if="loading && rows.length === 0"><td colspan="7" class="empty-cell">Loading receivables...</td></tr>
            <tr v-for="r in filteredRows" :key="r.id" class="data-row">
              <td class="mono">{{ r.no }}</td>
              <td>{{ r.cust }}</td>
              <td>{{ r.due }}</td>
              <td class="num mono">{{ fmt(r.amt) }}</td>
              <td class="num mono">{{ fmt(r.out) }}</td>
              <td><span class="stag" :class="sc(r.st)">{{ r.st }}</span></td>
              <td><a class="link" @click="$router.push('/finance/receivable/' + r.no)">View Details</a></td>
            </tr>
            <tr v-if="!loading && filteredRows.length === 0"><td colspan="7" class="empty-cell">No receivables found.</td></tr>
          </tbody>
        </table>
        <div class="table-footer">
          <div class="tf-left">
            <span class="tf-total">共 {{ filteredRows.length }} 条</span>
            <select class="form-select form-select-sm" v-model="pageSize" @change="loadData">
              <option :value="20">20 / 页</option><option :value="50">50 / 页</option><option :value="100">100 / 页</option>
            </select>
          </div>
          <div class="pager">
            <button class="pg-btn" :disabled="page <= 1" @click="goPage(page - 1)">‹</button>
            <button v-for="p in pageNumbers" :key="p" class="pg-btn" :class="{ active: p === page }" @click="goPage(p)">{{ p }}</button>
            <button class="pg-btn" :disabled="page >= totalPages" @click="goPage(page + 1)">›</button>
          </div>
          <div class="tf-right"><span class="tf-label">Go to</span><input type="text" class="pg-input" v-model="goToPage" @keyup.enter="goPage(parseInt(goToPage))" placeholder="page" /></div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import MainLayout from '@/layout/MainLayout.vue'
import { fetchOpenAR, fetchClosedAR, fetchPartners } from '@/api'
import type { OpenAccountReceivable, ClosedAccountReceivable } from '@/api/modules/finance'
import type { Partner } from '@/api/modules/master'

interface RowData {
  id: string
  no: string
  cust: string
  due: string
  amt: number
  out: number
  st: string
}

const f = reactive({ customer: '', invoiceNo: '', status: '' })
const loading = ref(false)
const error = ref('')
const allRows = ref<RowData[]>([])
const page = ref(1)
const pageSize = ref(20)
const goToPage = ref('')
const partnerMap = ref<Record<string, Partner>>({})

const totalPages = computed(() => Math.ceil(allRows.value.length / pageSize.value) || 1)

const filteredRows = computed(() => {
  const start = (page.value - 1) * pageSize.value
  return allRows.value.slice(start, start + pageSize.value)
})

const pageNumbers = computed(() => {
  const tp = totalPages.value
  const cur = page.value
  const arr: number[] = []
  let start = Math.max(1, cur - 2)
  let end = Math.min(tp, start + 4)
  start = Math.max(1, end - 4)
  for (let i = start; i <= end; i++) arr.push(i)
  return arr
})

function fmt(n: number) {
  return '¥' + Number(n || 0).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

function sc(s: string) {
  const m: Record<string, string> = { Open: 's-open', Closed: 's-done' }
  return m[s] || ''
}

async function loadPartners() {
  try {
    const res = await fetchPartners({ limit: 1000 })
    partnerMap.value = (res.items || []).reduce((acc: Record<string, Partner>, p: Partner) => {
      if (p.bp_id) acc[p.bp_id] = p
      return acc
    }, {})
  } catch { /* silent */ }
}

async function loadData() {
  loading.value = true
  error.value = ''
  try {
    const [openRes, closedRes] = await Promise.all([
      fetchOpenAR({ page_size: 1000 }),
      fetchClosedAR({ page_size: 1000 }),
    ])

    const openItems = (openRes.items || []).map((ar: OpenAccountReceivable) => ({
      id: ar.open_ar_id,
      no: ar.invoice_id,
      cust: partnerMap.value[ar.invoice_id]?.bp_name || ar.invoice_id,
      due: ar.due_date || 'N/A',
      amt: Number(ar.receivable_amount) || 0,
      out: Math.max(0, (Number(ar.receivable_amount) || 0) - (Number(ar.received_amount) || 0)),
      st: 'Open',
    }))

    const closedItems = (closedRes.items || []).map((ar: ClosedAccountReceivable) => ({
      id: ar.closed_ar_id,
      no: ar.invoice_id,
      cust: partnerMap.value[ar.invoice_id]?.bp_name || ar.invoice_id,
      due: ar.closed_time ? ar.closed_time.split('T')[0] : 'N/A',
      amt: Number(ar.receivable_amount) || 0,
      out: 0,
      st: 'Closed',
    }))

    let combined = [...openItems, ...closedItems]

    if (f.customer) {
      combined = combined.filter(r => r.cust.toLowerCase().includes(f.customer.toLowerCase()) || r.no.toLowerCase().includes(f.customer.toLowerCase()))
    }
    if (f.invoiceNo) {
      combined = combined.filter(r => r.no.toLowerCase().includes(f.invoiceNo.toLowerCase()))
    }
    if (f.status) {
      combined = combined.filter(r => r.st === f.status)
    }

    allRows.value = combined
    page.value = 1
  } catch (err: any) {
    error.value = err?.message || 'Failed to load receivables'
    console.error('Fetch AR failed:', err)
  } finally {
    loading.value = false
  }
}

function search() { loadData() }
function reset() {
  Object.assign(f, { customer: '', invoiceNo: '', status: '' })
  loadData()
}
function goPage(p: number) {
  if (p < 1 || p > totalPages.value) return
  page.value = p
  goToPage.value = ''
}

onMounted(async () => {
  await loadPartners()
  loadData()
})
</script>

<style scoped>
.page{padding:28px 36px;max-width:1400px;margin:0 auto;}
.header-card{display:flex;align-items:center;background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:16px;padding:20px 24px;border:1px solid rgba(173,188,159,0.18);box-shadow:0 2px 8px rgba(173,188,159,0.12);margin-bottom:20px;}
.hc-left{display:flex;align-items:center;gap:14px;}
.hc-icon{width:44px;height:44px;border-radius:12px;background:rgba(67,104,80,0.08);display:flex;align-items:center;justify-content:center;}
.hc-title{font-size:18px;font-weight:800;color:#12372A;margin:0;}
.hc-sub{font-size:12px;color:rgba(18,55,42,0.45);margin:2px 0 0;}
.filter-bar{display:flex;gap:10px;margin-bottom:16px;align-items:center;flex-wrap:wrap;}
.form-input,.form-select{height:38px;border:1px solid rgba(173,188,159,0.4);border-radius:8px;padding:0 12px;font-size:13px;color:#12372A;background:rgba(251,250,218,0.35);font-family:inherit;outline:none;min-width:130px;transition:all 0.2s;}
.form-input:focus,.form-select:focus{border-color:#436850;box-shadow:0 0 0 3px rgba(67,104,80,0.06);background:#fff;}
.form-select-sm{height:32px;padding:0 8px;font-size:11px;}
.error-msg{color:#D9534F;font-size:13px;padding:10px 14px;background:rgba(217,83,79,0.08);border-radius:8px;margin-bottom:14px;}
.data-card{background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:14px;border:1px solid rgba(173,188,159,0.15);box-shadow:0 2px 6px rgba(173,188,159,0.1);overflow:hidden;}
.data-table{width:100%;border-collapse:collapse;font-size:13px;}
.data-table th{text-align:left;padding:12px 14px;font-size:10px;font-weight:700;color:rgba(18,55,42,0.45);text-transform:uppercase;letter-spacing:0.8px;background:rgba(173,188,159,0.08);border-bottom:1px solid rgba(173,188,159,0.2);}
.data-table th.num{text-align:right;}
.data-table td{padding:11px 14px;border-bottom:1px solid rgba(173,188,159,0.08);color:#12372A;}
.data-table td.num{text-align:right;}
.data-row:hover{background:rgba(67,104,80,0.025);}
.mono{font-family:'SF Mono',Consolas,monospace;font-size:12px;}
.empty-cell{text-align:center;padding:40px;color:rgba(18,55,42,0.4);}
.stag{font-size:11px;font-weight:600;padding:4px 10px;border-radius:6px;}
.s-open{background:rgba(67,104,80,0.1);color:#436850;}
.s-done{background:rgba(67,104,80,0.12);color:#2d4a38;}
.link{color:#436850;cursor:pointer;font-weight:600;font-size:12px;}
.link:hover{text-decoration:underline;}
.btn{display:inline-flex;align-items:center;gap:6px;padding:9px 20px;font-size:13px;font-weight:600;border-radius:8px;cursor:pointer;transition:all 0.2s;font-family:inherit;}
.btn-primary{background:linear-gradient(135deg,#436850,#365440);color:#FBFADA;border:none;box-shadow:0 2px 8px rgba(67,104,80,0.25);}
.btn-primary:hover{transform:translateY(-1px);}
.btn-primary:disabled{opacity:0.6;cursor:not-allowed;transform:none;}
.btn-outline{background:none;color:rgba(18,55,42,0.5);border:1px solid rgba(173,188,159,0.35);}
.btn-outline:hover{border-color:rgba(18,55,42,0.3);color:#12372A;}
.btn-outline:disabled{opacity:0.6;cursor:not-allowed;}
.table-footer{display:flex;align-items:center;justify-content:space-between;padding:12px 16px;border-top:1px solid rgba(173,188,159,0.15);}
.tf-left{display:flex;align-items:center;gap:10px;}
.tf-total{font-size:12px;color:rgba(18,55,42,0.4);}
.tf-right{display:flex;align-items:center;gap:8px;}
.tf-label{font-size:11px;color:rgba(18,55,42,0.35);}
.pg-input{width:50px;height:30px;border:1px solid rgba(173,188,159,0.35);border-radius:6px;text-align:center;font-size:12px;outline:none;}
.pager{display:flex;gap:4px;}
.pg-btn{min-width:30px;height:30px;border:1px solid rgba(173,188,159,0.25);border-radius:6px;background:rgba(251,250,218,0.3);font-size:12px;color:#12372A;cursor:pointer;display:flex;align-items:center;justify-content:center;}
.pg-btn.active{background:#436850;color:#FBFADA;border-color:#436850;}
.pg-btn:disabled{opacity:0.4;cursor:not-allowed;}
</style>
