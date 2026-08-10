<template>
  <div>
    <div class="page" :class="{ 'drawer-mode': isDrawer }" v-if="loading">
      <div class="section-card" style="padding:40px;text-align:center;color:rgba(18,55,42,0.4)">
        Loading receivable details...
      </div>
    </div>
    <div class="page" :class="{ 'drawer-mode': isDrawer }" v-else-if="error">
      <div class="error-msg">{{ error }}</div>
      <button class="btn btn-outline" @click="load">Retry</button>
    </div>
    <div class="page" :class="{ 'drawer-mode': isDrawer }" v-else-if="invoice">
      <div class="top-bar">
        <button class="back-btn" @click="goBack"><svg viewBox="0 0 20 20" width="16" height="16"><path d="M12 4l-6 6 6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>Back</button>
        <div class="hc-icon"><svg viewBox="0 0 24 24" width="22" height="22"><circle cx="12" cy="12" r="10" fill="none" stroke="#436850" stroke-width="1.8"/><path d="M7 14l3 3 7-7" fill="none" stroke="#436850" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
        <div class="top-info">
          <span class="ti-label">Invoice No.</span><span class="ti-value mono">{{ invoice.invoiceId }}</span>
          <span class="ti-sub">{{ customerName }} &middot; Sales Order {{ invoice.salesOrderId || 'N/A' }} &middot; Due {{ dueDate || 'N/A' }}</span>
        </div>
        <div style="margin-left:auto;display:flex;align-items:center;gap:10px;">
          <span class="stag" :class="statusClass">{{ statusLabel }}</span>
          <button class="btn btn-outline" @click="exportInvoice">Export</button>
          <button class="btn btn-primary" @click="openCollect" :disabled="posting || unpaidAmount <= 0 || invoice?.status === 'VOID'">
            {{ posting ? 'Posting...' : 'Collect' }}
          </button>
        </div>
      </div>

      <div class="info-cards">
        <div class="ic"><span class="ic-label">Invoice Amount</span><span class="ic-value">{{ fmt(totalAmount) }}</span></div>
        <div class="ic"><span class="ic-label">Received Amount</span><span class="ic-value">{{ fmt(receivedAmount) }}</span></div>
        <div class="ic" :class="unpaidAmount > 0 ? 'ic-danger' : 'ic'"><span class="ic-label">Unpaid Amount</span><span class="ic-value" :class="unpaidAmount > 0 ? 'ic-red' : ''">{{ fmt(unpaidAmount) }}</span></div>
        <div class="ic" :class="daysOverdue > 0 ? 'ic-warn' : 'ic'"><span class="ic-label">Days Overdue</span><span class="ic-value" :class="daysOverdue > 0 ? 'ic-amber' : ''">{{ daysOverdue > 0 ? daysOverdue + ' days' : 'On time' }}</span></div>
      </div>

      <div class="section-card">
        <h3 class="sc-title">Collection Progress</h3>
        <p class="sc-hint">Current stage reflects the invoice and receivable status.</p>
        <div class="timeline">
          <div v-for="(s,i) in steps" :key="i" class="tl-step" :class="{done:s.done,cur:s.cur,alert:s.alert,future:s.future}">
            <div class="tl-dot"></div><div v-if="i<3" class="tl-line" :class="{future:s.future}"></div>
            <div class="tl-info"><span class="tl-status">{{ s.label }}</span><span class="tl-time">{{ s.time }}</span></div>
          </div>
        </div>
      </div>

      <div class="two-col">
        <div class="section-card">
          <h3 class="sc-title">Customer &amp; Terms</h3>
          <div class="si-grid">
            <div class="si-item"><span class="si-label">Customer</span><span class="si-value">{{ customerName }}</span></div>
            <div class="si-item"><span class="si-label">Contact</span><span class="si-value">{{ customerEmail }}</span></div>
            <div class="si-item"><span class="si-label">Payment Terms</span><span class="si-value">Net 30</span></div>
            <div class="si-item"><span class="si-label">Currency</span><span class="si-value mono">{{ invoice.currency }}</span></div>
            <div class="si-item"><span class="si-label">Risk Level</span><span class="si-value"><span class="risk-tag" :class="riskClass">{{ riskLabel }}</span></span></div>
          </div>
        </div>
        <div class="section-card">
          <h3 class="sc-title">Payment History</h3>
          <table class="data-table">
            <thead><tr><th>Date</th><th>Method</th><th class="num">Amount</th><th>Reference</th></tr></thead>
            <tbody>
              <tr v-for="pmt in paymentHistory" :key="pmt.receiptId">
                <td>{{ pmt.date }}</td><td>{{ pmt.method }}</td><td class="num mono">{{ fmt(pmt.amount) }}</td><td class="mono">{{ pmt.ref }}</td>
              </tr>
              <tr v-if="paymentHistory.length === 0"><td colspan="4" style="text-align:center;padding:20px;color:rgba(18,55,42,0.3)">No payment records.</td></tr>
              <tr v-if="unpaidAmount > 0"><td colspan="2" class="pending-row">Pending</td><td class="num mono" style="color:#D9534F">{{ fmt(unpaidAmount) }}</td><td class="mono"><span class="stag" :class="statusClass">{{ statusLabel }}</span></td></tr>
            </tbody>
          </table>
          <div class="ratio-bar-wrap"><span class="ratio-label">Collection ratio</span><div class="ratio-bar"><div class="ratio-fill" :style="{width:collectionRatio+'%'}"></div></div><span class="ratio-pct">{{ collectionRatio }}%</span></div>
        </div>
      </div>

      <div class="section-card" v-if="invoice.items && invoice.items.length">
        <h3 class="sc-title">Invoice Items</h3>
        <table class="data-table">
          <thead><tr><th>Item</th><th>Material</th><th class="num">Quantity</th><th class="num">Net Price</th><th class="num">Tax</th></tr></thead>
          <tbody>
            <tr v-for="(it, idx) in invoice.items" :key="it.invoiceItemId || idx">
              <td>{{ idx + 1 }}</td><td class="mono">{{ it.materialId }}</td>
              <td class="num mono">{{ Number(it.quantity || 0).toLocaleString() }}</td>
              <td class="num mono">{{ fmt(it.netPrice || 0) }}</td>
              <td class="num mono">{{ fmt(it.taxAmount || 0) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Collect Modal -->
    <Teleport to="body">
      <div class="modal-overlay" v-if="collectVisible" @click.self="collectVisible = false">
        <div class="collect-card">
          <div class="cc-header">
            <h3 class="cc-title">Collect Payment</h3>
            <button class="cc-close" @click="collectVisible = false">✕</button>
          </div>
          <div class="cc-body">
            <div class="cc-row">
              <span class="cc-label">Invoice</span>
              <span class="cc-value mono">{{ invoice?.invoiceId }}</span>
            </div>
            <div class="cc-row">
              <span class="cc-label">Customer</span>
              <span class="cc-value">{{ customerName }}</span>
            </div>
            <div class="cc-row">
              <span class="cc-label">Unpaid Amount</span>
              <span class="cc-value mono strong">{{ fmt(unpaidAmount) }}</span>
            </div>
            <div class="cc-field">
              <label class="cc-field-label">Payment Amount</label>
              <input type="number" class="cc-input" v-model.number="collectForm.amount" :max="unpaidAmount" step="0.01" />
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
            <button class="btn btn-primary" @click="submitCollect" :disabled="posting">Confirm</button>
          </div>
        </div>
      </div>
    </Teleport>

    <SuccessModal
      v-model:visible="successVisible"
      title="Payment Collected"
      :message="successMsg"
      @confirm="onSuccessConfirm"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import SuccessModal from '@/components/SuccessModal.vue'
import { fetchInvoiceById, fetchOpenAR, fetchClosedAR, fetchReceipts, createReceipt, fetchPartners } from '@/api'
import type { Invoice, OpenAccountReceivable, ClosedAccountReceivable, Receipt } from '@/api/modules/finance'
import type { Partner } from '@/api/modules/master'

const props = withDefaults(defineProps<{
  id?: string
  isDrawer?: boolean
}>(), {
  id: '',
  isDrawer: false
})

const emit = defineEmits<{ (e: 'close'): void }>()

const route = useRoute()
const router = useRouter()
const invoiceId = computed(() => props.id || (route.params.id as string) || '')

const invoice = ref<Invoice | null>(null)
const partnerMap = ref<Record<string, Partner>>({})
const openAr = ref<OpenAccountReceivable | null>(null)
const closedAr = ref<ClosedAccountReceivable | null>(null)
const receiptList = ref<Receipt[]>([])
const loading = ref(false)
const error = ref('')
const posting = ref(false)
const successVisible = ref(false)
const successMsg = ref('')

// collect modal
const collectVisible = ref(false)
const collectForm = reactive({ amount: 0, paymentMethod: 'BANK_TRANSFER', referenceNo: '' })

const currencySymbol = computed(() => invoice.value?.currency === 'USD' ? '$' : '¥')
const totalAmount = computed(() => Number(invoice.value?.totalAmount || 0))
const receivedAmount = computed(() => {
  if (openAr.value) return Number(openAr.value.receivedAmount) || 0
  if (closedAr.value) return Number(closedAr.value.receivedAmount) || 0
  return 0
})
const unpaidAmount = computed(() => Math.max(0, totalAmount.value - receivedAmount.value))
const dueDate = computed(() => {
  if (openAr.value?.dueDate) return openAr.value.dueDate
  if (closedAr.value?.closedTime) return closedAr.value.closedTime.split('T')[0]
  return invoice.value?.billingDate || 'N/A'
})
const daysOverdue = computed(() => {
  const due = openAr.value?.dueDate
  if (!due || unpaidAmount.value <= 0) return 0
  const dueD = new Date(due)
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  dueD.setHours(0, 0, 0, 0)
  const diff = Math.floor((today.getTime() - dueD.getTime()) / (1000 * 60 * 60 * 24))
  return diff > 0 ? diff : 0
})
const collectionRatio = computed(() => totalAmount.value > 0 ? Math.round((receivedAmount.value / totalAmount.value) * 100) : 0)

const customer = computed(() => {
  const bpId = invoice.value?.payer || invoice.value?.soldToParty || ''
  return partnerMap.value[bpId] || null
})
const customerName = computed(() => customer.value?.bpName || invoice.value?.payer || invoice.value?.soldToParty || 'Unknown')
const customerEmail = computed(() => customer.value?.email || 'N/A')

const statusLabel = computed(() => {
  if (invoice.value?.status === 'VOID') return 'Void'
  if (unpaidAmount.value === 0 && receivedAmount.value > 0) return 'Closed'
  if (daysOverdue.value > 0) return 'Overdue'
  if (receivedAmount.value > 0) return 'Partially Paid'
  return 'Open'
})
const statusClass = computed(() => {
  switch (statusLabel.value) {
    case 'Closed': return 's-done'
    case 'Overdue': return 's-overdue'
    case 'Partially Paid': return 's-partial'
    case 'Void': return 's-void'
    default: return 's-open'
  }
})

const riskLabel = computed(() => {
  if (daysOverdue.value > 90) return 'High'
  if (daysOverdue.value > 30) return 'Medium'
  return 'Low'
})
const riskClass = computed(() => riskLabel.value === 'High' ? 'high' : riskLabel.value === 'Medium' ? 'medium' : 'low')

const paymentHistory = computed(() => {
  return (receiptList.value || []).map((r: Receipt) => ({
    receiptId: r.receiptId,
    date: r.receiptDate ? r.receiptDate.split('T')[0] : 'N/A',
    method: r.paymentMethod || 'N/A',
    amount: Number(r.receiptAmount) || 0,
    ref: r.referenceNo || r.receiptId,
  }))
})

const steps = computed(() => {
  const isVoid = invoice.value?.status === 'VOID'
  const issued = true
  const partial = receivedAmount.value > 0
  const overdue = daysOverdue.value > 0 && unpaidAmount.value > 0
  const closed = unpaidAmount.value === 0 && receivedAmount.value > 0
  let cur = -1
  if (isVoid) cur = -2
  else if (closed) cur = 3
  else if (overdue) cur = 2
  else if (partial) cur = 1
  else cur = 0
  return [
    { label: 'Invoice Issued', done: issued && !isVoid, time: invoice.value?.invoiceDate || 'Pending', cur: cur === 0, alert: false, future: isVoid },
    { label: 'Partially Paid', done: partial, time: partial ? 'Received' : 'Pending', cur: cur === 1, alert: false, future: !partial && cur < 1 && !isVoid },
    { label: 'Overdue Notice', done: overdue, time: overdue ? 'Sent' : 'Pending', cur: cur === 2, alert: overdue, future: !overdue && cur < 2 && !isVoid },
    { label: 'Closed', done: closed, time: closed ? 'Done' : 'Pending', cur: cur === 3, alert: false, future: !closed && cur < 3 && !isVoid },
  ]
})

function fmt(n: number) {
  return `${currencySymbol.value}${Number(n || 0).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
}

async function load() {
  if (!invoiceId.value) return
  loading.value = true
  error.value = ''
  try {
    const [partners, inv] = await Promise.all([
      fetchPartners({ limit: 1000 }),
      fetchInvoiceById(invoiceId.value),
    ])
    invoice.value = inv
    partnerMap.value = {}
    ;(partners.items || []).forEach((p: Partner) => {
      if (p.bpId) partnerMap.value[p.bpId] = p
    })

    // Load AR and receipts in parallel
    const [openRes, closedRes, receiptRes] = await Promise.all([
      fetchOpenAR({ pageSize: 1000 }),
      fetchClosedAR({ pageSize: 1000 }),
      fetchReceipts({ pageSize: 1000 }),
    ])

    const openItem = (openRes.items || []).find((ar: OpenAccountReceivable) => ar.invoiceId === invoiceId.value)
    const closedItem = (closedRes.items || []).find((ar: ClosedAccountReceivable) => ar.invoiceId === invoiceId.value)
    if (openItem) openAr.value = openItem
    if (closedItem) closedAr.value = closedItem

    receiptList.value = (receiptRes.items || []).filter((r: Receipt) => r.invoiceId === invoiceId.value)
  } catch (err: any) {
    error.value = err?.message || 'Failed to load receivable details'
    console.error('Fetch receivable detail failed:', err)
  } finally {
    loading.value = false
  }
}

function goBack() {
  if (props.isDrawer) {
    emit('close')
    return
  }
  if (window.history.length > 1) {
    router.back()
  } else {
    router.push('/finance/invoice')
  }
}

function exportInvoice() {
  window.print()
}

function openCollect() {
  collectForm.amount = unpaidAmount.value
  collectForm.paymentMethod = 'BANK_TRANSFER'
  collectForm.referenceNo = ''
  collectVisible.value = true
}

async function submitCollect() {
  if (!invoice.value || posting.value) return
  const payAmt = collectForm.amount
  if (isNaN(payAmt) || payAmt <= 0) {
    alert('Invalid amount')
    return
  }
  if (payAmt > unpaidAmount.value) {
    alert('Payment amount cannot exceed unpaid amount')
    return
  }
  posting.value = true
  collectVisible.value = false
  try {
    await createReceipt({
      invoiceId: invoice.value.invoiceId,
      receiptAmount: payAmt,
      paymentMethod: collectForm.paymentMethod,
      currency: invoice.value.currency || 'CNY',
      referenceNo: collectForm.referenceNo || undefined,
    })
    successMsg.value = `Payment ${fmt(payAmt)} collected successfully for invoice ${invoice.value.invoiceId}.`
    successVisible.value = true
    load()
  } catch (err: any) {
    alert('Collect failed: ' + (err?.message || 'Unknown error'))
  } finally {
    posting.value = false
  }
}

function onSuccessConfirm() {
  load()
}

// re-load when id changes (drawer mode)
watch(() => invoiceId.value, (v) => { if (v) load() })

onMounted(() => load())
</script>

<style scoped>
.page{padding:28px 36px;max-width:1200px;margin:0 auto;}
.page.drawer-mode{padding:24px 28px;max-width:none;}
.top-bar{display:flex;align-items:center;gap:16px;margin-bottom:22px;flex-wrap:wrap;}
.back-btn{display:inline-flex;align-items:center;gap:6px;background:none;border:1px solid rgba(173,188,159,0.35);border-radius:8px;padding:8px 16px;font-size:13px;color:rgba(18,55,42,0.55);cursor:pointer;font-family:inherit;transition:all 0.2s;}
.back-btn:hover{border-color:#436850;color:#436850;}
.hc-icon{width:42px;height:42px;border-radius:10px;background:rgba(67,104,80,0.08);display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.top-info{display:flex;flex-direction:column;}
.ti-label{font-size:10px;color:rgba(18,55,42,0.35);text-transform:uppercase;letter-spacing:1px;font-weight:600;}
.ti-value{font-size:22px;font-weight:800;color:#12372A;}
.ti-sub{font-size:12px;color:rgba(18,55,42,0.4);}
.stag{font-size:11px;font-weight:600;padding:5px 12px;border-radius:6px;}
.s-open{background:rgba(67,104,80,0.1);color:#436850;}
.s-partial{background:rgba(240,173,78,0.12);color:#c98a20;}
.s-done{background:rgba(67,104,80,0.12);color:#2d4a38;}
.s-overdue{background:rgba(217,83,79,0.1);color:#D9534F;}
.s-void{background:rgba(120,120,120,0.12);color:#888;}

.info-cards{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:20px;}
.ic{background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:12px;padding:16px 18px;border:1px solid rgba(173,188,159,0.15);box-shadow:0 2px 6px rgba(173,188,159,0.1);}
.ic-danger{border-left:3px solid #D9534F;}
.ic-warn{border-left:3px solid #F0AD4E;}
.ic-label{font-size:10px;color:rgba(18,55,42,0.4);font-weight:600;text-transform:uppercase;letter-spacing:0.5px;display:block;margin-bottom:6px;}
.ic-value{font-size:15px;font-weight:700;color:#12372A;font-family:'SF Mono',Consolas,monospace;}
.ic-red{color:#D9534F;}
.ic-amber{color:#c98a20;}

.section-card{background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:14px;padding:22px;border:1px solid rgba(173,188,159,0.15);box-shadow:0 2px 6px rgba(173,188,159,0.1);margin-bottom:18px;}
.sc-title{font-size:14px;font-weight:700;color:#436850;margin:0 0 12px;display:flex;align-items:center;gap:8px;}
.sc-title::before{content:'';width:3px;height:13px;background:#436850;border-radius:2px;}
.sc-hint{font-size:12px;color:rgba(18,55,42,0.4);margin:0 0 18px;font-style:italic;}

.timeline{display:flex;align-items:flex-start;padding:8px 0;}
.tl-step{flex:1;position:relative;display:flex;flex-direction:column;align-items:center;}
.tl-dot{width:13px;height:13px;border-radius:50%;border:2px solid rgba(173,188,159,0.35);background:#FBFADA;z-index:1;}
.tl-step.done .tl-dot{background:#436850;border-color:#436850;}
.tl-step.cur:not(.future) .tl-dot{background:#436850;border-color:#436850;box-shadow:0 0 0 4px rgba(67,104,80,0.12);}
.tl-step.cur.future .tl-dot{background:#FBFADA;border:2px dashed rgba(120,120,120,0.4);box-shadow:none;}
.tl-step.alert .tl-dot{background:#D9534F;border-color:#D9534F;box-shadow:0 0 0 4px rgba(217,83,79,0.12);}
.tl-step.future:not(.cur) .tl-dot{background:#FBFADA;border:2px solid rgba(120,120,120,0.25);}
.tl-line{position:absolute;top:6px;left:50%;width:100%;height:2px;background:rgba(173,188,159,0.25);}
.tl-step.done .tl-line{background:#436850;}
.tl-step.future .tl-line{background:rgba(120,120,120,0.12);}
.tl-info{margin-top:10px;text-align:center;}
.tl-status{font-size:11px;font-weight:600;color:rgba(18,55,42,0.45);display:block;}
.tl-step.cur .tl-status,.tl-step.done .tl-status{color:#436850;}
.tl-step.alert .tl-status{color:#D9534F;}
.tl-step.future .tl-status{color:rgba(120,120,120,0.5);}
.tl-time{font-size:10px;color:rgba(18,55,42,0.28);display:block;margin-top:2px;}

.two-col{display:grid;grid-template-columns:1fr 1fr;gap:18px;}
.si-grid{display:flex;flex-direction:column;gap:14px;}
.si-item{display:flex;flex-direction:column;gap:2px;}
.si-label{font-size:10px;color:rgba(18,55,42,0.38);font-weight:600;text-transform:uppercase;letter-spacing:0.5px;}
.si-value{font-size:13px;color:#12372A;line-height:1.6;}
.risk-tag{font-size:11px;font-weight:600;padding:3px 10px;border-radius:6px;}
.risk-tag.low{background:rgba(67,104,80,0.1);color:#436850;}
.risk-tag.medium{background:rgba(240,173,78,0.15);color:#c98a20;}
.risk-tag.high{background:rgba(217,83,79,0.1);color:#D9534F;}

.data-table{width:100%;border-collapse:collapse;font-size:13px;}
.data-table th{text-align:left;padding:9px 12px;font-size:10px;font-weight:700;color:rgba(18,55,42,0.4);text-transform:uppercase;letter-spacing:0.5px;border-bottom:1px solid rgba(173,188,159,0.2);}
.data-table th.num{text-align:right;}
.data-table td{padding:9px 12px;border-bottom:1px solid rgba(173,188,159,0.07);color:#12372A;}
.data-table td.num{text-align:right;}
.pending-row{color:#D9534F;font-weight:600;}

.ratio-bar-wrap{display:flex;align-items:center;gap:10px;margin-top:16px;}
.ratio-label{font-size:11px;color:rgba(18,55,42,0.4);white-space:nowrap;}
.ratio-bar{flex:1;height:7px;background:rgba(173,188,159,0.2);border-radius:4px;overflow:hidden;}
.ratio-fill{height:100%;background:#436850;border-radius:4px;transition:width 0.6s ease;}
.ratio-pct{font-size:13px;font-weight:700;color:#12372A;}
.mono{font-family:'SF Mono',Consolas,monospace;font-size:12px;}

.btn{display:inline-flex;align-items:center;gap:6px;padding:9px 18px;font-size:13px;font-weight:600;border-radius:8px;cursor:pointer;transition:all 0.2s;font-family:inherit;}
.btn-primary{background:linear-gradient(135deg,#436850,#365440);color:#FBFADA;border:none;box-shadow:0 2px 8px rgba(67,104,80,0.25);}
.btn-primary:hover{transform:translateY(-1px);}
.btn-primary:disabled{opacity:0.6;cursor:not-allowed;transform:none;}
.btn-outline{background:none;color:rgba(18,55,42,0.5);border:1px solid rgba(173,188,159,0.35);}
.btn-outline:hover{border-color:#436850;color:#436850;}
.error-msg{color:#D9534F;font-size:13px;padding:10px 14px;background:rgba(217,83,79,0.08);border-radius:8px;margin-bottom:14px;}

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
