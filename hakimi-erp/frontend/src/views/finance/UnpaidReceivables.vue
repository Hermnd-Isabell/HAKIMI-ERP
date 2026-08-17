<template>
  <div class="page">
    <div class="header-card">
        <div class="hc-left">
          <div class="hc-icon"><svg viewBox="0 0 24 24" width="22" height="22"><circle cx="12" cy="12" r="10" fill="none" stroke="#436850" stroke-width="1.8"/><path d="M7 14l3 3 7-7" fill="none" stroke="#436850" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
          <div class="hc-text">
            <h2 class="hc-title">Unpaid Accounts Receivable</h2>
            <p class="hc-sub">Monitor collection progress in real time.</p>
          </div>
        </div>
      </div>

      <!-- Quick Stats -->
      <div class="kpi-grid">
        <div class="kpi-box">
          <span class="kpi-label">Total Unpaid</span>
          <span class="kpi-value">¥{{ format(kpis.totalUnpaid) }}</span>
        </div>
        <div class="kpi-box text-success">
          <span class="kpi-label">Month Collected</span>
          <span class="kpi-value">¥{{ format(kpis.collected) }}</span>
        </div>
        <div class="kpi-box">
          <span class="kpi-label">Collection Ratio</span>
          <span class="kpi-value">{{ totalRatio }}%</span>
        </div>
      </div>

      <div class="filter-bar">
        <div class="search-input-group">
          <input type="text" class="form-input search-inv" v-model="f.inv" placeholder="Invoice No." @keyup.enter="fetchData" />
          <input type="text" class="form-input search-cust" v-model="f.cust" placeholder="Customer" @keyup.enter="fetchData" />
          <select class="form-select search-st" v-model="f.st" @change="fetchData">
            <option value="">All Statuses</option>
            <option value="Unpaid">Unpaid</option>
            <option value="Partial">Partial</option>
          </select>
        </div>
        <button class="btn btn-primary" @click="fetchData" :disabled="loading">Search</button>
        <button class="btn btn-outline" @click="reset">Reset</button>
      </div>

      <div class="data-card">
        <table class="data-table">
          <thead><tr><th>Invoice No.</th><th>Customer</th><th>Due Date</th><th class="num">Amount</th><th class="num">Unpaid</th><th>Status</th><th class="action-col">Action</th></tr></thead>
          <tbody>
            <tr v-if="loading && displayedRows.length === 0"><td colspan="7" class="empty-cell">Syncing data...</td></tr>
            <tr v-for="row in displayedRows" :key="row.id" class="data-row">
              <td class="mono strong">{{ row.inv }}</td>
              <td>{{ row.cust }}</td>
              <td>{{ row.due }}</td>
              <td class="num mono">¥{{ format(row.amt) }}</td>
              <td class="num mono strong text-danger">¥{{ format(row.unp) }}</td>
              <td><span class="stag" :class="sc(row.st)">{{ row.st }}</span></td>
              <td class="action-col">
                <button class="action-link-btn" @click="viewDetail(row.inv)">View Details</button>
                <span class="btn-divider"></span>
                <button class="action-link-btn collect" @click="handleClear(row)">Collect</button>
              </td>
            </tr>
            <tr v-if="!loading && displayedRows.length === 0"><td colspan="7" class="empty-cell">No unpaid receivables found.</td></tr>
          </tbody>
        </table>
      </div>

      <SuccessModal v-model:visible="successVisible" title="Payment Posted" :message="successMsg" @confirm="fetchData" />
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import SuccessModal from '@/components/SuccessModal.vue'
import { alert, prompt } from '@/utils/toast'
import { fetchOpenAR, fetchInvoices, createReceipt } from '@/api/modules/finance'
import { fetchPartners } from '@/api/modules/master'
import type { Partner } from '@/api/modules/master'

const router = useRouter()
const rawOpenAR = ref<any[]>([])
const invoiceMap = ref<any>({})
const partnerMap = ref<Record<string, Partner>>({})
const loading = ref(false)
const successVisible = ref(false)
const successMsg = ref('')
const f = reactive({ inv: '', cust: '', st: '' })

let timer: any = null

const allRows = computed(() => {
  return rawOpenAR.value.map((i: any) => {
    const inv = invoiceMap.value[i.invoiceId]
    const amt = parseFloat(i.receivableAmount) || 0
    const rcv = parseFloat(i.receivedAmount) || 0
    return {
      id: i.openArId, inv: i.invoiceId, cust: partnerMap.value[inv?.payer || inv?.soldToParty || '']?.bpName || inv?.payer || 'Unknown',
      due: i.dueDate || 'N/A', amt, rcv, unp: Math.max(0, amt - rcv),
      st: (amt-rcv) <= 0 ? 'Paid' : (rcv > 0 ? 'Partial' : 'Unpaid'),
    }
  })
})
const displayedRows = computed(() => allRows.value)

const kpis = computed(() => {
  const totalUnpaid = displayedRows.value.reduce((acc, r) => acc + r.unp, 0)
  const collected = displayedRows.value.reduce((acc, r) => acc + r.rcv, 0)
  const totalAmt = displayedRows.value.reduce((acc, r) => acc + r.amt, 0)
  return { totalUnpaid, collected, totalAmt }
})
const totalRatio = computed(() => kpis.value.totalAmt > 0 ? Math.round((kpis.value.collected / kpis.value.totalAmt) * 100) : 0)

function format(n: number) { return Math.round(n).toLocaleString() }
function sc(s: string) { return s === 'Unpaid' ? 's-unpaid' : (s === 'Partial' ? 's-partial' : 's-done') }

async function fetchData() {
  loading.value = true
  try {
    const [arRes, invRes, partnerRes] = await Promise.all([
      fetchOpenAR({ pageSize: 1000, invoiceId: f.inv || undefined, customerName: f.cust || undefined }), 
      fetchInvoices({ pageSize: 1000 }),
      fetchPartners({ limit: 1000 })
    ])
    let items = arRes.items || []
    if (f.st) {
      items = items.filter((i: any) => {
        const amt = parseFloat(i.receivableAmount) || 0
        const rcv = parseFloat(i.receivedAmount) || 0
        const st = (amt-rcv) <= 0 ? 'Paid' : (rcv > 0 ? 'Partial' : 'Unpaid')
        return st === f.st
      })
    }
    rawOpenAR.value = items
    invoiceMap.value = (invRes.items || []).reduce((acc: any, inv: any) => { if (inv.invoiceId) acc[inv.invoiceId] = inv; return acc; }, {})
    partnerMap.value = {}
    ;(partnerRes.items || []).forEach((p: Partner) => { if (p.bpId) partnerMap.value[p.bpId] = p })
  } finally { loading.value = false }
}

function reset() {
  Object.assign(f, { inv: '', cust: '', st: '' })
  fetchData()
}

function viewDetail(id: string) {
  router.push(`/finance/receivable/${id}`)
}

async function handleClear(row: any) {
  const amount = await prompt(`Payment for ${row.inv}:`, row.unp.toString())
  if (!amount) return
  try {
    await createReceipt({ invoiceId: row.inv, receiptAmount: parseFloat(amount), paymentMethod: 'BANK_TRANSFER', currency: 'CNY' })
    successMsg.value = "Payment collected successfully."
    successVisible.value = true
    fetchData()
  } catch (err: any) { alert(err.message) }
}

onMounted(() => {
  fetchData()
  timer = setInterval(fetchData, 30000) // Silent background refresh
})
onUnmounted(() => { clearInterval(timer) })
</script>

<style scoped>
.page{padding:32px 40px;max-width:1200px;margin:0 auto;background:#FBFADA;min-height:calc(100vh - 64px);}
.header-card{display:flex;align-items:center;background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:16px;padding:24px 32px;border:1px solid rgba(173,188,159,0.3);box-shadow:0 8px 24px rgba(18,55,42,0.05);margin-bottom:24px;}
.hc-left{display:flex;align-items:center;gap:18px;}
.hc-icon{width:48px;height:48px;border-radius:12px;background:rgba(67,104,80,0.1);display:flex;align-items:center;justify-content:center;}
.hc-title{font-size:20px;font-weight:800;color:#12372A;margin:0;}
.hc-sub{font-size:13px;color:rgba(18,55,42,0.5);margin:2px 0 0;}

.filter-bar{display:flex;gap:16px;margin-bottom:24px;align-items:center;background:linear-gradient(145deg,#fdfce8,#f7f5d1);padding:20px;border-radius:16px;border:1px solid rgba(173,188,159,0.2);}
.search-input-group{display:flex;gap:12px;flex:1;}
.search-inv{width:160px;}
.search-cust{width:220px;}
.search-st{width:140px;}
.form-input,.form-select{height:42px;border:1px solid rgba(173,188,159,0.4);border-radius:10px;padding:0 14px;font-size:14px;color:#12372A;background:rgba(251,250,218,0.5);font-family:inherit;outline:none;width:auto;}
.form-input:focus{border-color:#436850;background:#fff;box-shadow:0 0 0 4px rgba(67,104,80,0.05);}
.btn{display:inline-flex;align-items:center;gap:8px;padding:10px 22px;font-size:13px;font-weight:700;border-radius:10px;cursor:pointer;transition:all 0.2s;font-family:inherit;}
.btn-primary{background:linear-gradient(135deg,#436850,#365440);color:#FBFADA;border:none;box-shadow:0 4px 12px rgba(67,104,80,0.2);}
.btn-outline{background:transparent;color:#436850;border:1.5px solid rgba(173,188,159,0.5);}
.btn-outline:hover{background:rgba(67,104,80,0.05);border-color:#436850;}

.kpi-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-bottom:24px;}
.kpi-box{background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:16px;padding:24px;border:1px solid rgba(173,188,159,0.3);box-shadow:0 4px 12px rgba(18,55,42,0.04);}
.kpi-label{font-size:11px;font-weight:700;color:rgba(18,55,42,0.4);text-transform:uppercase;display:block;margin-bottom:8px;letter-spacing:1px;}
.kpi-value{font-size:24px;font-weight:800;color:#12372A;font-family:'SF Mono',monospace;}
.kpi-box.text-success .kpi-value { color: #436850; }

.data-card{background:linear-gradient(145deg, #fdfce8, #f7f5d1);border-radius:16px;border:1px solid rgba(173,188,159,0.3);overflow:hidden;box-shadow:0 4px 12px rgba(18,55,42,0.03);}
.data-table{width:100%;border-collapse:collapse;}
.data-table th{text-align:left;padding:16px;font-size:11px;font-weight:700;color:rgba(18,55,42,0.4);text-transform:uppercase;background:rgba(67,104,80,0.03);border-bottom:1px solid rgba(173,188,159,0.2);letter-spacing:1px;}
.data-table td{padding:16px;border-bottom:1px solid rgba(173,188,159,0.1);color:#12372A;font-size:14px;}
.data-row:hover{background:rgba(67,104,80,0.02);}
.num{text-align:right;}

.action-link-btn{background:none;border:none;color:#436850;font-weight:700;font-size:12px;cursor:pointer;padding:6px 12px;border-radius:6px;transition:all 0.2s;}
.action-link-btn:hover{background:rgba(67,104,80,0.08);color:#2d4a38;}
.action-link-btn.collect{background:rgba(217,83,79,0.05);color:#D9534F;margin-left:4px;}
.action-link-btn.collect:hover{background:rgba(217,83,79,0.1);}
.btn-divider{display:inline-block;width:1px;height:14px;background:rgba(173,188,159,0.3);margin:0 4px;vertical-align:middle;}

.mono{font-family:'SF Mono',monospace;}
.strong{font-weight:700;}
.text-danger{color:#D9534F;}
.stag{font-size:11px;font-weight:700;padding:4px 10px;border-radius:6px;text-transform:uppercase;}
.s-unpaid{background:rgba(217,83,79,0.1);color:#D9534F;}
.s-partial{background:rgba(240,173,78,0.1);color:#c98a20;}
.s-done{background:rgba(67,104,80,0.1);color:#436850;}
.empty-cell{text-align:center;padding:60px;color:rgba(18,55,42,0.3);font-style:italic;}
</style>
