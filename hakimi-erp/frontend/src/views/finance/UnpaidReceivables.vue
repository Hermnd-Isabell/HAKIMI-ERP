<template>
  <MainLayout>
    <div class="page">
      <!-- Header Card -->
      <div class="header-card">
        <div class="hc-left">
          <div class="hc-icon"><svg viewBox="0 0 24 24" width="22" height="22"><circle cx="12" cy="12" r="10" fill="none" stroke="#436850" stroke-width="1.8"/><path d="M7 14l3 3 7-7" fill="none" stroke="#436850" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
          <div class="hc-text">
            <h2 class="hc-title">Unpaid Accounts Receivable</h2>
            <p class="hc-sub">Monitor unpaid receivables and collection progress in real time.</p>
          </div>
        </div>
        <div class="hc-right">
          <label class="auto-refresh"><input type="checkbox" v-model="autoRefresh" /> Auto Refresh</label>
          <select class="form-select form-select-sm" v-model="refreshInterval"><option>30s</option><option>60s</option><option>5min</option></select>
        </div>
      </div>

      <!-- KPI Cards -->
      <div class="kpi-cards">
        <div class="kpi-card"><span class="kpi-label">Total Unpaid Amount</span><span class="kpi-value">¥{{ format(kpis.totalUnpaid) }}</span></div>
        <div class="kpi-card kpi-warn"><span class="kpi-label">Overdue Amount</span><span class="kpi-value kpi-amber">¥{{ format(kpis.overdue) }}</span></div>
        <div class="kpi-card"><span class="kpi-label">Collected This Month</span><span class="kpi-value">¥{{ format(kpis.collected) }}</span></div>
        <div class="kpi-card"><span class="kpi-label">Remaining This Month</span><span class="kpi-value">¥{{ format(kpis.remaining) }}</span></div>
      </div>

      <!-- Filter Bar -->
      <div class="filter-bar">
        <input type="text" class="form-input" v-model="f.customer" placeholder="Customer (BP ID)" @keyup.enter="search" />
        <input type="text" class="form-input" v-model="f.invoice" placeholder="Invoice No." @keyup.enter="search" />
        <select class="form-select" v-model="f.status">
          <option value="">All Statuses</option>
          <option>Unpaid</option><option>Partially Paid</option><option>Overdue</option>
        </select>
        <button class="btn btn-primary" @click="search" :disabled="loading">Search</button>
        <button class="btn btn-outline" @click="reset" :disabled="loading">Reset</button>
      </div>

      <div v-if="error" class="error-msg">{{ error }}</div>

      <!-- Table -->
      <div class="data-card">
        <table class="data-table">
          <thead><tr>
            <th>Invoice No.</th><th>Customer</th><th>Invoice Date</th><th>Due Date</th>
            <th class="num">Invoice Amount</th><th class="num">Received Amount</th><th class="num">Unpaid Amount</th>
            <th>Status</th><th>Collection Progress</th><th>Action</th>
          </tr></thead>
          <tbody>
            <tr v-if="loading && pagedRows.length === 0">
              <td colspan="10" class="empty-cell">Loading receivables...</td>
            </tr>
            <tr v-for="row in pagedRows" :key="row.id" class="data-row">
              <td class="mono">{{ row.inv }}</td><td>{{ row.cust }}</td><td>{{ row.date }}</td><td>{{ row.due }}</td>
              <td class="num mono">¥{{ format(row.amt) }}</td>
              <td class="num mono">¥{{ format(row.rcv) }}</td>
              <td class="num mono strong">¥{{ format(row.unp) }}</td>
              <td><span class="stag" :class="sc(row.st)">{{ row.st }}</span></td>
              <td><div class="prog-cell"><div class="prog-bar"><div class="prog-fill" :style="{width:row.pct+'%'}"></div></div><span class="prog-pct">{{ row.pct }}%</span></div></td>
              <td>
                <a class="link" :class="{disabled: postingId === row.id}" @click="handleOpenCollect(row)">
                  {{ postingId === row.id ? 'Posting...' : 'Post Payment' }}
                </a>
              </td>
            </tr>
            <tr v-if="!loading && pagedRows.length === 0"><td colspan="10" class="empty-cell">No unpaid receivables found.</td></tr>
          </tbody>
        </table>
        <div class="table-footer">
          <div class="tf-left">
            <span class="tf-total">共 {{ displayedRows.length }} 条</span>
            <select class="form-select form-select-sm" v-model.number="pageSize">
              <option :value="20">20 / 页</option><option :value="50">50 / 页</option><option :value="100">100 / 页</option>
            </select>
          </div>
          <div class="pager">
            <button class="pg-btn" :disabled="currentPage <= 1" @click="currentPage--">‹</button>
            <button v-for="p in pageNumbers" :key="p" class="pg-btn" :class="{active: p === currentPage}" @click="currentPage = p">{{ p }}</button>
            <button class="pg-btn" :disabled="currentPage >= totalPages" @click="currentPage++">›</button>
          </div>
          <div class="tf-right"><span class="tf-label">Go to</span><input type="text" class="pg-input" v-model="goToPage" @keyup.enter="goToPageNum(parseInt(goToPage))" placeholder="page" /></div>
        </div>
      </div>
    </div>

    <!-- Collect Drawer -->
    <Teleport to="body">
      <div class="modal-overlay" v-if="collectVisible" @click.self="collectVisible = false">
        <div class="collect-card">
          <div class="cc-header">
            <h3 class="cc-title">Post Payment</h3>
            <button class="cc-close" @click="collectVisible = false">✕</button>
          </div>
          <div class="cc-body">
            <div class="cc-row">
              <span class="cc-label">Invoice</span>
              <span class="cc-value mono">{{ collectRow?.inv }}</span>
            </div>
            <div class="cc-row">
              <span class="cc-label">Customer</span>
              <span class="cc-value">{{ collectRow?.cust }}</span>
            </div>
            <div class="cc-row">
              <span class="cc-label">Unpaid Amount</span>
              <span class="cc-value mono strong">¥{{ format(collectRow?.unp || 0) }}</span>
            </div>
            <div class="cc-field">
              <label class="cc-field-label">Payment Amount</label>
              <input type="number" class="cc-input" v-model.number="collectForm.amount" :max="collectRow?.unp" step="0.01" />
            </div>
            <div class="cc-field">
              <label class="cc-field-label">Payment Method</label>
              <select class="cc-select" v-model="collectForm.paymentMethod">
                <option value="BANK_TRANSFER">Bank Transfer</option>
                <option value="CASH">Cash</option>
                <option value="CHECK">Check</option>
                <option value="CREDIT_CARD">Credit Card</option>
              </select>
            </div>
            <div class="cc-field">
              <label class="cc-field-label">Reference No.</label>
              <input type="text" class="cc-input" v-model="collectForm.referenceNo" placeholder="Optional" />
            </div>
          </div>
          <div class="cc-footer">
            <button class="btn btn-outline" @click="collectVisible = false">Cancel</button>
            <button class="btn btn-primary" @click="submitCollect" :disabled="postingId !== ''">Confirm</button>
          </div>
        </div>
      </div>
    </Teleport>

    <SuccessModal
      v-model:visible="successVisible"
      title="Payment Posted"
      :message="successMsg"
      @confirm="onSuccessConfirm"
    />
  </MainLayout>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue'
import MainLayout from '@/layout/MainLayout.vue'
import SuccessModal from '@/components/SuccessModal.vue'
import { fetchOpenAR, fetchReceipts, createReceipt, fetchPartners } from '@/api'
import type { OpenAccountReceivable, Invoice } from '@/api/modules/finance'
import type { Partner } from '@/api/modules/master'
import { fetchInvoices } from '@/api'

const autoRefresh = ref(true)
const refreshInterval = ref('30s')
const f = reactive({ customer: '', invoice: '', status: '', from: '', to: '' })

const rawOpenAR = ref<OpenAccountReceivable[]>([])
const invoiceMap = ref<Record<string, Invoice>>({})
const partnerMap = ref<Record<string, Partner>>({})
const monthReceiptsTotal = ref(0)
const loading = ref(false)
const error = ref('')
const postingId = ref('')
const successVisible = ref(false)
const successMsg = ref('')

// pagination
const currentPage = ref(1)
const pageSize = ref(20)
const goToPage = ref('')

// collect drawer
const collectVisible = ref(false)
const collectRow = ref<any>(null)
const collectForm = reactive({ amount: 0, paymentMethod: 'BANK_TRANSFER', referenceNo: '' })

let refreshTimer: ReturnType<typeof setInterval> | null = null

const allRows = computed(() => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return rawOpenAR.value.map((i: any) => {
    const invoice = invoiceMap.value[i.invoice_id]
    const bpId = invoice?.payer || invoice?.sold_to_party || i.invoice_id
    const amt = parseFloat(i.receivable_amount) || 0
    const rcv = parseFloat(i.received_amount) || 0
    const unp = Math.max(0, amt - rcv)
    const dueDate = i.due_date ? new Date(i.due_date) : null
    let st = 'Unpaid'
    if (rcv >= amt) st = 'Paid'
    else if (rcv > 0) st = 'Partially Paid'
    if (dueDate && dueDate < today && rcv < amt) st = 'Overdue'
    const invoiceDate = invoice?.invoice_date || 'N/A'
    return {
      id: i.open_ar_id,
      inv: i.invoice_id,
      cust: partnerMap.value[bpId]?.bp_name || bpId,
      date: invoiceDate,
      due: i.due_date || 'N/A',
      amt, rcv, unp, st,
      pct: amt > 0 ? Math.round((rcv / amt) * 100) : 0,
    }
  })
})

const displayedRows = computed(() => {
  return allRows.value.filter(r => {
    if (f.customer && !r.cust.toLowerCase().includes(f.customer.toLowerCase()) && !r.inv.toLowerCase().includes(f.customer.toLowerCase())) return false
    if (f.invoice && !r.inv.toLowerCase().includes(f.invoice.toLowerCase())) return false
    if (f.status && r.st !== f.status) return false
    return true
  })
})

const totalPages = computed(() => Math.ceil(displayedRows.value.length / pageSize.value) || 1)
const pagedRows = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return displayedRows.value.slice(start, start + pageSize.value)
})
const pageNumbers = computed(() => {
  const tp = totalPages.value
  const cur = currentPage.value
  const arr: number[] = []
  let start = Math.max(1, cur - 2)
  let end = Math.min(tp, start + 4)
  start = Math.max(1, end - 4)
  for (let i = start; i <= end; i++) arr.push(i)
  return arr
})

const kpis = computed(() => {
  const totalUnpaid = displayedRows.value.reduce((acc, r) => acc + r.unp, 0)
  const overdue = displayedRows.value.filter(r => r.st === 'Overdue').reduce((acc, r) => acc + r.unp, 0)
  const collected = monthReceiptsTotal.value
  return {
    totalUnpaid,
    overdue,
    collected,
    remaining: totalUnpaid
  }
})

function format(n: number) {
  return Math.round(n).toLocaleString()
}

function sc(s: string) {
  const m: Record<string, string> = { 'Unpaid': 's-unpaid', 'Paid': 's-paid', 'Partially Paid': 's-partial', 'Overdue': 's-overdue' }
  return m[s] || ''
}

function goToPageNum(p: number) {
  if (p < 1 || p > totalPages.value) return
  currentPage.value = p
  goToPage.value = ''
}

async function fetchData() {
  loading.value = true
  error.value = ''
  try {
    const now = new Date()
    const monthStart = new Date(now.getFullYear(), now.getMonth(), 1)

    const [arRes, invRes, receiptRes, partnerRes] = await Promise.all([
      fetchOpenAR({ page_size: 1000 }),
      fetchInvoices({ page_size: 1000 }),
      fetchReceipts({ page_size: 1000 }),
      fetchPartners({ limit: 1000 }),
    ])

    rawOpenAR.value = arRes.items || []
    invoiceMap.value = (invRes.items || []).reduce((acc: Record<string, Invoice>, inv: Invoice) => {
      if (inv.invoice_id) acc[inv.invoice_id] = inv
      return acc
    }, {})
    partnerMap.value = (partnerRes.items || []).reduce((acc: Record<string, Partner>, p: Partner) => {
      if (p.bp_id) acc[p.bp_id] = p
      return acc
    }, {})

    // KPI: Collected This Month — sum receipts in current month
    monthReceiptsTotal.value = (receiptRes.items || [])
      .filter((r: any) => {
        if (!r.receipt_date) return false
        const d = new Date(r.receipt_date)
        return d >= monthStart && d <= now
      })
      .reduce((sum: number, r: any) => sum + (Number(r.receipt_amount) || 0), 0)

    currentPage.value = 1
  } catch (err: any) {
    error.value = err?.message || 'Failed to load receivables'
    console.error('Fetch open AR failed:', err)
  } finally {
    loading.value = false
  }
}

function startRefreshTimer() {
  if (refreshTimer) clearInterval(refreshTimer)
  if (!autoRefresh.value) return
  const ms = refreshInterval.value === '30s' ? 30000 : refreshInterval.value === '60s' ? 60000 : 300000
  refreshTimer = setInterval(() => fetchData(), ms)
}

function search() { currentPage.value = 1; fetchData() }
function reset() {
  Object.assign(f, { customer: '', invoice: '', status: '', from: '', to: '' })
  currentPage.value = 1
  fetchData()
}

function handleOpenCollect(row: any) {
  if (postingId.value) return
  collectRow.value = row
  collectForm.amount = row.unp
  collectForm.paymentMethod = 'BANK_TRANSFER'
  collectForm.referenceNo = ''
  collectVisible.value = true
}

async function submitCollect() {
  if (!collectRow.value || postingId.value) return
  const payAmt = collectForm.amount
  if (isNaN(payAmt) || payAmt <= 0) {
    alert('Invalid amount')
    return
  }
  if (payAmt > collectRow.value.unp) {
    alert('Payment amount cannot exceed unpaid amount')
    return
  }
  postingId.value = collectRow.value.id
  collectVisible.value = false
  try {
    await createReceipt({
      invoice_id: collectRow.value.inv,
      receipt_amount: payAmt,
      payment_method: collectForm.paymentMethod,
      currency: 'CNY',
      reference_no: collectForm.referenceNo || undefined,
    })
    successMsg.value = `Payment ¥${payAmt.toLocaleString()} posted successfully for invoice ${collectRow.value.inv}.`
    successVisible.value = true
    fetchData()
  } catch (err: any) {
    alert('Post receipt failed: ' + (err?.message || 'Unknown error'))
  } finally {
    postingId.value = ''
  }
}

function onSuccessConfirm() {
  fetchData()
}

onMounted(() => {
  fetchData()
  startRefreshTimer()
})

onUnmounted(() => {
  if (refreshTimer) clearInterval(refreshTimer)
})

watch([autoRefresh, refreshInterval], startRefreshTimer)
watch(displayedRows, () => { if (currentPage.value > totalPages.value) currentPage.value = 1 })
</script>

<style scoped>
.page{padding:28px 36px;max-width:1400px;margin:0 auto;}

.header-card{display:flex;align-items:center;justify-content:space-between;background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:16px;padding:20px 24px;border:1px solid rgba(173,188,159,0.18);box-shadow:0 2px 8px rgba(173,188,159,0.12);margin-bottom:20px;}
.hc-left{display:flex;align-items:center;gap:14px;}
.hc-icon{width:44px;height:44px;border-radius:12px;background:rgba(67,104,80,0.08);display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.hc-title{font-size:18px;font-weight:800;color:#12372A;margin:0;}
.hc-sub{font-size:12px;color:rgba(18,55,42,0.45);margin:2px 0 0;}
.hc-right{display:flex;align-items:center;gap:12px;}
.auto-refresh{font-size:12px;color:rgba(18,55,42,0.5);display:flex;align-items:center;gap:6px;cursor:pointer;}
.form-select-sm{height:32px;padding:0 8px;font-size:11px;}

.kpi-cards{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:20px;}
.kpi-card{background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:12px;padding:18px 20px;border:1px solid rgba(173,188,159,0.15);box-shadow:0 2px 6px rgba(173,188,159,0.1);}
.kpi-card.kpi-warn{border-left:3px solid #F0AD4E;}
.kpi-label{font-size:10px;color:rgba(18,55,42,0.4);font-weight:700;text-transform:uppercase;letter-spacing:0.8px;display:block;margin-bottom:8px;}
.kpi-value{font-size:22px;font-weight:800;color:#12372A;font-family:'SF Mono',Consolas,monospace;}
.kpi-amber{color:#c98a20;}

.filter-bar{display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap;align-items:center;}
.form-input,.form-select{height:38px;border:1px solid rgba(173,188,159,0.4);border-radius:8px;padding:0 12px;font-size:13px;color:#12372A;background:rgba(251,250,218,0.35);font-family:inherit;outline:none;min-width:130px;transition:all 0.2s;}
.form-input:focus,.form-select:focus{border-color:#436850;box-shadow:0 0 0 3px rgba(67,104,80,0.06);background:#fff;}

.error-msg{color:#D9534F;font-size:13px;padding:10px 14px;background:rgba(217,83,79,0.08);border-radius:8px;margin-bottom:14px;}

.data-card{background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:14px;border:1px solid rgba(173,188,159,0.15);box-shadow:0 2px 6px rgba(173,188,159,0.1);overflow:hidden;}
.data-table{width:100%;border-collapse:collapse;font-size:13px;}
.data-table th{text-align:left;padding:12px 14px;font-size:10px;font-weight:700;color:rgba(18,55,42,0.45);text-transform:uppercase;letter-spacing:0.8px;background:rgba(173,188,159,0.08);border-bottom:1px solid rgba(173,188,159,0.2);}
.data-table th.num{text-align:right;}
.data-table td{padding:11px 14px;border-bottom:1px solid rgba(173,188,159,0.08);color:#12372A;}
.data-table td.num{text-align:right;}
.data-row:hover{background:rgba(67,104,80,0.025);}
.mono{font-family:'SF Mono',Consolas,monospace;font-size:12px;}
.strong{font-weight:700;}
.empty-cell{text-align:center;padding:40px;color:rgba(18,55,42,0.4);}

.stag{font-size:11px;font-weight:600;padding:4px 10px;border-radius:6px;}
.s-unpaid{background:rgba(67,104,80,0.1);color:#436850;}
.s-paid{background:rgba(67,104,80,0.12);color:#2d4a38;}
.s-partial{background:rgba(240,173,78,0.12);color:#c98a20;}
.s-overdue{background:rgba(217,83,79,0.1);color:#D9534F;}

.prog-cell{display:flex;align-items:center;gap:8px;min-width:110px;}
.prog-bar{flex:1;height:5px;background:rgba(173,188,159,0.2);border-radius:3px;overflow:hidden;}
.prog-fill{height:100%;background:#436850;border-radius:3px;transition:width 0.4s;}
.prog-pct{font-size:11px;color:rgba(18,55,42,0.4);min-width:30px;}
.link{color:#436850;cursor:pointer;font-weight:600;font-size:12px;}
.link:hover{text-decoration:underline;}
.link.disabled{color:rgba(18,55,42,0.3);cursor:not-allowed;text-decoration:none;}

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

.btn{display:inline-flex;align-items:center;gap:6px;padding:9px 20px;font-size:13px;font-weight:600;border-radius:8px;cursor:pointer;transition:all 0.2s;font-family:inherit;}
.btn-primary{background:linear-gradient(135deg,#436850,#365440);color:#FBFADA;border:none;box-shadow:0 2px 8px rgba(67,104,80,0.25);}
.btn-primary:hover{transform:translateY(-1px);box-shadow:0 4px 16px rgba(67,104,80,0.3);}
.btn-primary:disabled{opacity:0.6;cursor:not-allowed;transform:none;}
.btn-outline{background:none;color:rgba(18,55,42,0.5);border:1px solid rgba(173,188,159,0.35);}
.btn-outline:hover{border-color:rgba(18,55,42,0.3);color:#12372A;}
.btn-outline:disabled{opacity:0.6;cursor:not-allowed;}

/* Collect Modal */
.modal-overlay{position:fixed;inset:0;background:rgba(18,55,42,0.3);backdrop-filter:blur(4px);display:flex;align-items:center;justify-content:center;z-index:2000;}
.collect-card{width:480px;background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:18px;box-shadow:0 20px 60px rgba(18,55,42,0.22);border:1px solid rgba(173,188,159,0.2);overflow:hidden;}
.cc-header{display:flex;align-items:center;justify-content:space-between;padding:22px 28px 16px;border-bottom:1px solid rgba(173,188,159,0.12);}
.cc-title{font-size:18px;font-weight:800;color:#436850;margin:0;}
.cc-close{background:none;border:none;font-size:18px;color:rgba(18,55,42,0.35);cursor:pointer;padding:4px;}
.cc-body{padding:20px 28px;display:flex;flex-direction:column;gap:14px;}
.cc-row{display:flex;justify-content:space-between;align-items:center;}
.cc-label{font-size:12px;color:rgba(18,55,42,0.4);font-weight:600;}
.cc-value{font-size:14px;color:#12372A;}
.cc-field{display:flex;flex-direction:column;gap:6px;}
.cc-field-label{font-size:12px;color:rgba(18,55,42,0.5);font-weight:600;text-transform:uppercase;letter-spacing:0.5px;}
.cc-input,.cc-select{height:40px;border:1px solid rgba(173,188,159,0.4);border-radius:8px;padding:0 12px;font-size:14px;color:#12372A;background:#fff;font-family:inherit;outline:none;}
.cc-input:focus,.cc-select:focus{border-color:#436850;box-shadow:0 0 0 3px rgba(67,104,80,0.06);}
.cc-footer{display:flex;justify-content:flex-end;gap:10px;padding:14px 28px;background:rgba(251,250,218,0.25);border-top:1px solid rgba(173,188,159,0.1);}
</style>
