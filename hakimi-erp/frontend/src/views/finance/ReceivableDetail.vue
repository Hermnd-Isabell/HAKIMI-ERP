<template>
  <div class="receivable-detail-wrapper">
    <div class="receivable-detail" :class="{ 'in-drawer': isDrawer }">
      <!-- Loading State -->
      <div v-if="loading" class="state-container">
        <div class="spinner"></div>
        <p>Fetching receivable intelligence...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="state-container error">
        <div class="error-icon">!</div>
        <h3>Analysis Failed</h3>
        <p>{{ error }}</p>
        <button class="btn btn-outline" @click="load">Retry Sync</button>
      </div>

      <!-- Content -->
      <div v-else-if="invoice" class="detail-content">
        <!-- Action Header -->
        <div class="action-header" v-if="!isDrawer">
          <button class="back-btn" @click="$router.back()">
            <svg viewBox="0 0 20 20" width="16" height="16"><path d="M12 4l-6 6 6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            Back to List
          </button>
          <div class="header-main">
            <span class="doc-type">Billing Document</span>
            <h2 class="doc-id mono">{{ invoice.invoiceId }}</h2>
          </div>
          <div class="header-actions">
            <span class="status-badge" :class="statusClass">{{ statusLabel }}</span>
            <button class="btn btn-primary" @click="openCollect" :disabled="posting || unpaidAmount <= 0">
              Post Payment
            </button>
            <button class="btn btn-border" @click="print">Print</button>
          </div>
        </div>

        <div class="action-header-drawer" v-else>
          <div class="header-actions">
            <span class="status-badge" :class="statusClass">{{ statusLabel }}</span>
            <button class="btn btn-primary btn-sm" @click="openCollect" :disabled="posting || unpaidAmount <= 0">
              Post Payment
            </button>
          </div>
        </div>

        <!-- KPI Row -->
        <div class="kpi-grid">
          <div class="kpi-card">
            <label>Total Amount</label>
            <div class="value mono">{{ fmt(totalAmount) }}</div>
            <span class="sub">{{ invoice.currency }}</span>
          </div>
          <div class="kpi-card">
            <label>Received</label>
            <div class="value mono text-success">{{ fmt(receivedAmount) }}</div>
            <div class="progress-mini"><div class="fill" :style="{width: collectionRatio + '%'}"></div></div>
          </div>
          <div class="kpi-card" :class="{ 'warn': unpaidAmount > 0 }">
            <label>Balance Due</label>
            <div class="value mono" :class="{ 'text-danger': unpaidAmount > 0 }">{{ fmt(unpaidAmount) }}</div>
            <span class="sub">{{ unpaidAmount > 0 ? 'Awaiting Payment' : 'Fully Paid' }}</span>
          </div>
          <div class="kpi-card" :class="{ 'danger': daysOverdue > 0 && unpaidAmount > 0 }">
            <label>Overdue Days</label>
            <div class="value mono">{{ daysOverdue }}</div>
            <span class="sub">{{ dueDate }}</span>
          </div>
        </div>

        <!-- Main Info Sections -->
        <div class="detail-grid">
          <div class="grid-left">
            <!-- Items Table -->
            <div class="content-card">
              <h3 class="card-title">Invoice Items</h3>
              <table class="item-table">
                <thead><tr><th>Pos</th><th>Material</th><th>Description</th><th class="num">Qty</th><th class="num">Net Value</th></tr></thead>
                <tbody>
                  <tr v-for="(it, idx) in invoice.items" :key="it.invoiceItemId">
                    <td>{{ (idx + 1) * 10 }}</td>
                    <td class="mono">{{ it.materialId }}</td>
                    <td>{{ it.itemDescription || 'N/A' }}</td>
                    <td class="num">{{ it.quantity }} {{ it.salesUnit }}</td>
                    <td class="num mono strong">{{ fmt(it.netPrice) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Document Flow -->
            <div class="content-card">
              <h3 class="card-title">Document Flow</h3>
              <div class="flow-list">
                <div v-for="(doc, idx) in docFlowList" :key="idx" class="flow-item">
                  <div class="flow-icon" :class="doc.type">
                    <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  </div>
                  <div class="flow-info">
                    <span class="label">{{ doc.label }}</span>
                    <span class="id mono">{{ doc.id }}</span>
                  </div>
                  <div class="flow-status">
                    <span class="status-tag">{{ doc.status }}</span>
                  </div>
                  <div class="flow-line" v-if="!doc.isLast"></div>
                </div>
              </div>
            </div>
          </div>

          <div class="grid-right">
            <!-- Customer Info -->
            <div class="content-card">
              <h3 class="card-title">Partner Information</h3>
              <div class="info-list">
                <div class="info-item"><label>Payer</label><span>{{ customerName }}</span></div>
                <div class="info-item"><label>Customer ID</label><span class="mono">{{ invoice.payer }}</span></div>
                <div class="info-item"><label>Billing Date</label><span>{{ invoice.billingDate }}</span></div>
                <div class="info-item"><label>Due Date</label><span class="text-danger">{{ dueDate }}</span></div>
                <div class="info-item"><label>Sales Org</label><span>{{ invoice.salesOrg }} / {{ invoice.distributionChannel }}</span></div>
              </div>
            </div>

            <!-- Collection History -->
            <div class="content-card">
              <h3 class="card-title">Collection History</h3>
              <div class="history-list" v-if="paymentHistory.length > 0">
                <div v-for="pmt in paymentHistory" :key="pmt.id" class="history-item">
                  <div class="hi-main">
                    <span class="hi-date">{{ pmt.date }}</span>
                    <span class="hi-amt text-success">+{{ fmt(pmt.amount) }}</span>
                  </div>
                  <div class="hi-sub">
                    <span>{{ pmt.method }}</span>
                    <span class="mono">{{ pmt.ref }}</span>
                  </div>
                </div>
              </div>
              <div class="empty-msg" v-else>No payment history recorded.</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Payment Modal -->
    <Teleport to="body">
      <div class="modal-overlay" v-if="collectVisible" @click.self="collectVisible = false">
        <div class="modal-card">
          <div class="modal-header">
            <h3>Post Payment Receipt</h3>
            <button class="close-btn" @click="collectVisible = false">✕</button>
          </div>
          <div class="modal-body" v-if="invoice">
            <div class="balance-card">
              <label>Open Balance</label>
              <div class="balance-val mono text-danger">{{ fmt(unpaidAmount) }}</div>
            </div>
            
            <div class="form-group">
              <label>Receipt Amount ({{ invoice.currency }})</label>
              <input type="number" class="form-input" v-model.number="collectForm.amount" :max="unpaidAmount" />
            </div>
            
            <div class="form-group">
              <label>Payment Method</label>
              <select class="form-select" v-model="collectForm.paymentMethod">
                <option value="BANK_TRANSFER">Bank Transfer</option>
                <option value="CASH">Cash</option>
                <option value="CHECK">Check</option>
              </select>
            </div>

            <div class="form-group">
              <label>Bank Reference</label>
              <input type="text" class="form-input" v-model="collectForm.referenceNo" placeholder="Reference or Check No." />
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-border" @click="collectVisible = false">Cancel</button>
            <button class="btn btn-primary" @click="submitCollect" :disabled="posting || collectForm.amount <= 0">Post Receipt</button>
          </div>
        </div>
      </div>
    </Teleport>

    <SuccessModal v-model:visible="successVisible" :message="successMsg" @confirm="load" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import SuccessModal from '@/components/SuccessModal.vue'
import { fetchInvoiceById, fetchOpenAR, fetchClosedAR, createReceipt, fetchReceipts } from '@/api/modules/finance'
import { fetchPartners } from '@/api/modules/master'
import type { Invoice, OpenAccountReceivable, ClosedAccountReceivable, Receipt } from '@/api/modules/finance'

const props = defineProps({
  id: { type: String, default: '' },
  isDrawer: { type: Boolean, default: false }
})

const emit = defineEmits(['close'])
const route = useRoute()
const effectiveId = computed(() => props.id || (route.params.id as string))

const invoice = ref<Invoice | null>(null)
const partnerMap = ref<Record<string, any>>({})
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

const customerName = computed(() => partnerMap.value[invoice.value?.payer || '']?.bpName || invoice.value?.payer || 'Unknown')

const statusLabel = computed(() => {
  if (unpaidAmount.value <= 0) return 'Cleared'
  if (daysOverdue.value > 0) return 'Overdue'
  if (receivedAmount.value > 0) return 'Partial'
  return 'Open'
})

const statusClass = computed(() => {
  const s = statusLabel.value
  if (s === 'Cleared') return 's-done'
  if (s === 'Overdue') return 's-overdue'
  if (s === 'Partial') return 's-partial'
  return 's-open'
})

const docFlowList = computed(() => {
  if (!invoice.value) return []
  const list = []
  if (invoice.value.salesOrderId) list.push({ type: 'SO', label: 'Sales Order', id: invoice.value.salesOrderId, status: 'Completed' })
  if (invoice.value.deliveryId) list.push({ type: 'DEL', label: 'Delivery', id: invoice.value.deliveryId, status: 'Completed' })
  list.push({ type: 'INV', label: 'Invoice', id: invoice.value.invoiceId, status: 'Posted' })
  receiptList.value.forEach((r, idx) => list.push({ type: 'RCP', label: `Receipt #${idx+1}`, id: r.receiptId, status: 'Settled' }))
  return list.map((item, index) => ({ ...item, isLast: index === list.length - 1 }))
})

const paymentHistory = computed(() => receiptList.value.map(r => ({
  id: r.receiptId,
  date: r.receiptDate?.split('T')[0] || 'N/A',
  method: r.paymentMethod,
  amount: Number(r.receiptAmount),
  ref: r.referenceNo || r.receiptId
})))

function fmt(n: number) {
  const sym = invoice.value?.currency === 'USD' ? '$' : '¥'
  return `${sym}${Number(n || 0).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
}

async function load() {
  if (!effectiveId.value || effectiveId.value === 'debug') return
  loading.value = true
  error.value = ''
  try {
    const [partners, openRes, closedRes, receiptRes] = await Promise.all([
      fetchPartners({ pageSize: 1000 }),
      fetchOpenAR({ pageSize: 1000 }),
      fetchClosedAR({ pageSize: 1000 }),
      fetchReceipts({ pageSize: 1000 }),
    ])

    partnerMap.value = (partners.items || []).reduce((acc: any, p: any) => { acc[p.bpId] = p; return acc }, {})

    const openItem = (openRes.items || []).find((ar: any) => ar.openArId === effectiveId.value || ar.invoiceId === effectiveId.value)
    const closedItem = (closedRes.items || []).find((ar: any) => ar.closedArId === effectiveId.value || ar.invoiceId === effectiveId.value)
    
    openAr.value = openItem || null
    closedAr.value = closedItem || null

    const invId = openItem?.invoiceId || closedItem?.invoiceId || effectiveId.value
    invoice.value = await fetchInvoiceById(invId)
    receiptList.value = (receiptRes.items || []).filter((r: any) => r.invoiceId === invId)
  } catch (err: any) {
    error.value = err.message || 'Failed to sync data'
  } finally {
    loading.value = false
  }
}

function openCollect() {
  collectForm.amount = unpaidAmount.value
  collectVisible.value = true
}

async function submitCollect() {
  if (!invoice.value || posting.value) return
  posting.value = true
  try {
    await createReceipt({
      invoiceId: invoice.value.invoiceId,
      receiptAmount: collectForm.amount,
      paymentMethod: collectForm.paymentMethod,
      currency: invoice.value.currency || 'CNY',
      referenceNo: collectForm.referenceNo || undefined,
    })
    successMsg.value = 'Payment receipt processed successfully.'
    successVisible.value = true
    collectVisible.value = false
    load()
  } catch (err: any) {
    alert('Operation failed: ' + err.message)
  } finally {
    posting.value = false
  }
}

function print() { window.print() }

watch(effectiveId, () => load(), { immediate: true })
</script>

<script lang="ts">
export default { name: 'ReceivableDetail' }
</script>

<style scoped>
.receivable-detail { background: #FBFADA; min-height: 100%; color: #12372A; }
.receivable-detail.in-drawer { padding: 32px; }
.detail-content { max-width: 1200px; margin: 0 auto; padding: 32px 40px; }
.in-drawer .detail-content { padding: 0; }

.state-container { padding: 80px 0; text-align: center; color: rgba(18,55,42,0.4); }
.spinner { width: 32px; height: 32px; border: 3px solid rgba(67, 104, 80, 0.1); border-top-color: #436850; border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 16px; }
@keyframes spin { to { transform: rotate(360deg); } }

.action-header { display: flex; align-items: center; gap: 24px; margin-bottom: 32px; }
.action-header-drawer { margin-bottom: 24px; display: flex; justify-content: flex-end; }
.header-main { flex: 1; }
.doc-type { font-size: 11px; font-weight: 700; color: rgba(18,55,42,0.4); text-transform: uppercase; letter-spacing: 1px; }
.doc-id { font-size: 28px; font-weight: 800; margin-top: 4px; }
.header-actions { display: flex; align-items: center; gap: 12px; }

.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 32px; }
.kpi-card { background: linear-gradient(145deg, #fdfce8, #f7f5d1); border-radius: 16px; padding: 20px; border: 1px solid rgba(173,188,159,0.3); box-shadow: 0 4px 12px rgba(18,55,42,0.04); }
.kpi-card label { font-size: 11px; font-weight: 700; color: rgba(18,55,42,0.4); text-transform: uppercase; display: block; margin-bottom: 8px; }
.kpi-card .value { font-size: 20px; font-weight: 800; }
.kpi-card .sub { font-size: 11px; color: rgba(18,55,42,0.4); margin-top: 6px; display: block; }
.kpi-card.warn { border-left: 4px solid #F0AD4E; }
.kpi-card.danger { border-left: 4px solid #D9534F; }

.progress-mini { height: 4px; background: rgba(67, 104, 80, 0.1); border-radius: 2px; margin-top: 10px; overflow: hidden; }
.progress-mini .fill { height: 100%; background: #436850; transition: width 0.6s ease; }

.detail-grid { display: grid; grid-template-columns: 1.6fr 1fr; gap: 24px; }
.content-card { background: linear-gradient(145deg, #fdfce8, #f7f5d1); border-radius: 16px; padding: 24px; border: 1px solid rgba(173,188,159,0.3); margin-bottom: 24px; }
.card-title { font-size: 14px; font-weight: 800; color: #436850; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 0.5px; }

.item-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.item-table th { text-align: left; padding: 12px; font-weight: 700; color: rgba(18,55,42,0.4); border-bottom: 2px solid rgba(173,188,159,0.2); }
.item-table td { padding: 12px; border-bottom: 1px solid rgba(173,188,159,0.1); }
.num { text-align: right; }

.flow-list { display: flex; flex-direction: column; padding-left: 8px; }
.flow-item { display: flex; align-items: center; gap: 16px; padding: 14px 0; position: relative; }
.flow-icon { width: 30px; height: 30px; border-radius: 8px; background: #fff; border: 1.5px solid #436850; color: #436850; display: flex; align-items: center; justify-content: center; z-index: 2; }
.flow-info { flex: 1; display: flex; flex-direction: column; }
.flow-info .label { font-size: 10px; font-weight: 700; color: rgba(18,55,42,0.4); text-transform: uppercase; }
.flow-info .id { font-size: 14px; font-weight: 600; }
.flow-line { position: absolute; left: 14px; top: 40px; width: 2px; height: calc(100% - 10px); background: rgba(173,188,159,0.2); z-index: 1; }

.info-list { display: flex; flex-direction: column; gap: 16px; }
.info-item { display: flex; flex-direction: column; gap: 4px; }
.info-item label { font-size: 11px; font-weight: 700; color: rgba(18,55,42,0.4); text-transform: uppercase; }
.info-item span { font-size: 14px; font-weight: 500; }

.history-item { padding: 12px 14px; background: rgba(255,255,255,0.4); border-radius: 12px; border: 1px solid rgba(173,188,159,0.1); margin-bottom: 10px; }
.hi-main { display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }
.hi-date { font-weight: 700; font-size: 13px; }
.hi-sub { display: flex; justify-content: space-between; font-size: 11px; color: rgba(18,55,42,0.4); }

.status-badge { font-size: 11px; font-weight: 700; padding: 6px 14px; border-radius: 8px; text-transform: uppercase; letter-spacing: 0.5px; }
.s-open { background: rgba(217,83,79,0.1); color: #D9534F; }
.s-partial { background: rgba(240,173,78,0.1); color: #c98a20; }
.s-done { background: rgba(67,104,80,0.1); color: #436850; }
.s-overdue { background: #D9534F; color: #fff; }

.btn { display: inline-flex; align-items: center; justify-content: center; padding: 10px 20px; font-size: 13px; font-weight: 700; border-radius: 10px; cursor: pointer; transition: all 0.2s; font-family: inherit; }
.btn-sm { padding: 6px 14px; font-size: 12px; }
.btn-primary { background: linear-gradient(135deg, #436850, #365440); color: #FBFADA; border: none; box-shadow: 0 4px 12px rgba(67,104,80,0.2); }
.btn-primary:hover { transform: translateY(-1px); box-shadow: 0 6px 16px rgba(67,104,80,0.3); }
.btn-border { background: transparent; border: 1.5px solid rgba(173,188,159,0.5); color: #436850; }
.btn-border:hover { background: rgba(67,104,80,0.05); border-color: #436850; }
.back-btn { background: transparent; border: none; color: #436850; cursor: pointer; display: flex; align-items: center; gap: 8px; font-weight: 700; font-size: 13px; }

.mono { font-family: 'SF Mono', Consolas, monospace; }
.text-success { color: #436850; }
.text-danger { color: #D9534F; }
.strong { font-weight: 800; }

/* Modal Style */
.modal-overlay { position: fixed; inset: 0; background: rgba(18,55,42,0.4); backdrop-filter: blur(6px); display: flex; align-items: center; justify-content: center; z-index: 10000; }
.modal-card { width: 440px; background: linear-gradient(145deg, #fdfce8, #f7f5d1); border-radius: 24px; padding: 32px; box-shadow: 0 20px 60px rgba(18,55,42,0.2); border: 1px solid rgba(173,188,159,0.3); }
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.modal-header h3 { font-size: 18px; font-weight: 800; margin: 0; }
.balance-card { background: rgba(217,83,79,0.05); border-radius: 12px; padding: 16px; margin-bottom: 20px; text-align: center; }
.balance-card label { font-size: 11px; font-weight: 700; color: rgba(217,83,79,0.6); text-transform: uppercase; }
.balance-val { font-size: 24px; font-weight: 800; margin-top: 4px; }
.form-group { margin-bottom: 18px; }
.form-group label { display: block; font-size: 11px; font-weight: 700; color: rgba(18,55,42,0.4); text-transform: uppercase; margin-bottom: 6px; }
.form-input, .form-select { width: 100%; height: 42px; border-radius: 10px; border: 1px solid rgba(173,188,159,0.3); padding: 0 12px; font-family: inherit; font-size: 14px; outline: none; }
.form-input:focus { border-color: #436850; background: #fff; }
.modal-footer { display: flex; justify-content: flex-end; gap: 12px; margin-top: 28px; }

@media print {
  .action-header, .header-actions, .modal-overlay { display: none !important; }
  .receivable-detail { background: #fff; }
  .content-card, .kpi-card { box-shadow: none; border: 1px solid #eee; }
}
</style>
