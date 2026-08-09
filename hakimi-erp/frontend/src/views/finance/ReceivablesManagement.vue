<template>
  <div class="page">
    <div class="header-card">
        <div class="hc-left">
          <div class="hc-icon"><svg viewBox="0 0 24 24" width="22" height="22"><circle cx="12" cy="12" r="10" fill="none" stroke="#436850" stroke-width="1.8"/><path d="M12 6v6l4 2M7 12h10" fill="none" stroke="#436850" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
          <div class="hc-text">
            <h2 class="hc-title">Account Receivables</h2>
            <p class="hc-sub">Monitor all accounts and collection progress.</p>
          </div>
        </div>
      </div>

      <div class="kpi-grid">
        <div class="kpi-card">
          <label>Total Outstanding</label>
          <div class="value mono">¥{{ format(kpis.totalUnpaid) }}</div>
          <span class="sub">Across all clients</span>
        </div>
        <div class="kpi-card">
          <label>Month Collected</label>
          <div class="value mono text-success">¥{{ format(kpis.collected) }}</div>
          <div class="progress-mini"><div class="fill" :style="{width: totalRatio + '%'}"></div></div>
        </div>
        <div class="kpi-card">
          <label>Collection Ratio</label>
          <div class="value mono">{{ totalRatio }}%</div>
          <span class="sub">Efficiency Index</span>
        </div>
      </div>

      <div class="filter-bar">
        <div class="search-input-group">
          <input type="text" class="form-input search-inv" v-model="f.invoiceNo" placeholder="Invoice No." @keyup.enter="fetchData" />
          <input type="text" class="form-input search-cust" v-model="f.customer" placeholder="Customer" @keyup.enter="fetchData" />
          <select class="form-select search-st" v-model="f.status" @change="fetchData">
            <option value="">All Statuses</option>
            <option value="OPEN">Open</option>
            <option value="CLEARED">Closed</option>
          </select>
        </div>
        <button class="btn btn-primary" @click="fetchData" :disabled="loading">Search</button>
        <button class="btn btn-outline" @click="reset">Reset</button>
      </div>

      <div class="data-card yellowish">
        <table class="data-table">
          <thead><tr><th>Invoice No.</th><th>Customer</th><th>Due Date</th><th class="num">Amount</th><th class="num">Outstanding</th><th>Status</th><th>Action</th></tr></thead>
          <tbody>
            <tr v-if="loading && rows.length === 0"><td colspan="7" class="empty-cell">Syncing data...</td></tr>
            <tr v-for="r in rows" :key="r.id" class="data-row">
              <td class="mono strong">{{ r.no }}</td><td>{{ r.cust }}</td><td>{{ r.due }}</td><td class="num">{{ r.amt }}</td>
              <td class="num" :class="{ 'text-danger': r.st === 'OPEN' }">{{ r.out }}</td>
              <td><span class="stag" :class="sc(r.st)">{{ r.stLabel }}</span></td>
              <td><button class="view-btn" @click="viewDetail(r.id)">View Details</button></td>
            </tr>
            <tr v-if="!loading && rows.length === 0">
              <td colspan="7" class="empty-cell">No receivable records found.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- THE "VIEW DETAILS" DRAWER - NO NAVIGATION NEEDED -->
      <Teleport to="body">
        <div class="drawer-overlay" v-if="detailVisible" @click.self="detailVisible = false">
          <div class="detail-drawer">
            <div class="drawer-header">
              <div class="dh-left">
                <span class="dh-sub">Receivable Detail</span>
                <h3 class="dh-title">{{ currentId }}</h3>
              </div>
              <button class="close-btn" @click="detailVisible = false">
                <svg viewBox="0 0 20 20" width="20" height="20"><path d="M6 6l8 8M14 6l-8 8" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
              </button>
            </div>
            <div class="drawer-body">
              <!-- Passing id prop to ReceivableDetail.vue -->
              <ReceivableDetailContent :id="currentId" is-drawer @close="detailVisible = false" />
            </div>
          </div>
        </div>
      </Teleport>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import ReceivableDetailContent from './ReceivableDetail.vue'
import { fetchOpenAR, fetchClosedAR } from '@/api/modules/finance'

const rows = ref<any[]>([])
const loading = ref(false)
const detailVisible = ref(false)
const currentId = ref('')
const f = reactive({ invoiceNo: '', customer: '', status: '' })

const kpis = computed(() => {
  const totalUnpaid = rows.value.reduce((acc, r) => acc + (parseFloat(r.out.replace(/[¥,]/g, '')) || 0), 0)
  const collected = rows.value.reduce((acc, r) => acc + (parseFloat(r.amt.replace(/[¥,]/g, '')) || 0) - (parseFloat(r.out.replace(/[¥,]/g, '')) || 0), 0)
  const totalAmt = rows.value.reduce((acc, r) => acc + (parseFloat(r.amt.replace(/[¥,]/g, '')) || 0), 0)
  return { totalUnpaid, collected, totalAmt }
})
const totalRatio = computed(() => kpis.value.totalAmt > 0 ? Math.round((kpis.value.collected / kpis.value.totalAmt) * 100) : 0)

function format(n: number) { return Math.round(n).toLocaleString() }

async function fetchData() {
  loading.value = true
  try {
    const [openRes, closedRes] = await Promise.all([
      fetchOpenAR({ pageSize: 100, invoiceId: f.invoiceNo || undefined, customerName: f.customer || undefined }),
      fetchClosedAR({ pageSize: 100, invoiceId: f.invoiceNo || undefined, customerName: f.customer || undefined })
    ])
    const openItems = (openRes.items || []).map((i: any) => ({
      id: i.openArId, no: i.invoiceId, cust: i.payer || 'Unknown',
      due: i.dueDate || 'N/A', amt: `¥${Number(i.receivableAmount || 0).toLocaleString()}`,
      out: `¥${(Number(i.receivableAmount || 0) - Number(i.receivedAmount || 0)).toLocaleString()}`,
      st: 'OPEN', stLabel: 'Open'
    }))
    const closedItems = (closedRes.items || []).map((i: any) => ({
      id: i.closedArId, no: i.invoiceId, cust: i.payer || 'Unknown',
      due: i.closedTime?.split('T')[0] || 'N/A', amt: `¥${Number(i.receivableAmount || 0).toLocaleString()}`,
      out: '¥0.00', st: 'CLEARED', stLabel: 'Closed'
    }))
    let all = [...openItems, ...closedItems]
    if (f.status) {
      all = all.filter(i => i.st === f.status)
    }
    rows.value = all
  } catch (err: any) {
    console.error('Failed to fetch receivables:', err)
  } finally { loading.value = false }
}

function reset() {
  Object.assign(f, { invoiceNo: '', customer: '', status: '' })
  fetchData()
}

function viewDetail(id: string) {
  currentId.value = id
  detailVisible.value = true
}

function sc(s:string){return s==='OPEN'?'s-open':'s-done'}
onMounted(fetchData)
</script>

<style scoped>
.page{padding:32px 40px;max-width:1200px;margin:0 auto;background:#FBFADA;min-height:calc(100vh - 64px);}
.header-card{display:flex;align-items:center;background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:16px;padding:24px 32px;border:1px solid rgba(173,188,159,0.3);margin-bottom:24px;box-shadow:0 8px 24px rgba(18,55,42,0.05);}
.hc-icon{width:48px;height:48px;background:rgba(67,104,80,0.1);border-radius:12px;display:flex;align-items:center;justify-content:center;margin-right:20px;}
.hc-title{font-size:20px;font-weight:800;color:#12372A;margin:0;}
.hc-sub{font-size:13px;color:rgba(18,55,42,0.5);margin-top:2px;}

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

.kpi-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 24px; }
.kpi-card { background: linear-gradient(145deg, #fdfce8, #f7f5d1); border-radius: 16px; padding: 24px; border: 1px solid rgba(173,188,159,0.3); box-shadow: 0 4px 12px rgba(18,55,42,0.04); }
.kpi-card label { font-size: 11px; font-weight: 700; color: rgba(18,55,42,0.4); text-transform: uppercase; display: block; margin-bottom: 8px; letter-spacing: 1px; }
.kpi-card .value { font-size: 24px; font-weight: 800; color: #12372A; }
.kpi-card .sub { font-size: 11px; color: rgba(18,55,42,0.4); margin-top: 6px; display: block; }
.progress-mini { height: 4px; background: rgba(67,104,80,0.1); border-radius: 2px; margin-top: 10px; overflow: hidden; }
.progress-mini .fill { height: 100%; background: #436850; transition: width 0.6s ease; }

.data-card{background:#fff;border-radius:16px;border:1px solid rgba(173,188,159,0.2);overflow:hidden;box-shadow:0 4px 12px rgba(18,55,42,0.03);}
.data-card.yellowish { background: linear-gradient(145deg, #fdfce8, #f7f5d1); border: 1px solid rgba(173, 188, 159, 0.3); }

.data-table{width:100%;border-collapse:collapse;}
.data-table th{text-align:left;padding:16px;font-size:11px;font-weight:700;color:rgba(18,55,42,0.4);text-transform:uppercase;letter-spacing:1px;background:rgba(67,104,80,0.03);border-bottom:1px solid rgba(173,188,159,0.2);}
.data-table td{padding:16px;border-bottom:1px solid rgba(173,188,159,0.1);color:#12372A;font-size:14px;}
.data-row:hover{background:rgba(67,104,80,0.02);}
.num{text-align:right;}
.strong{font-weight:700;}
.mono{font-family:'SF Mono',Consolas,monospace;}
.text-danger{color:#D9534F;}

.view-btn{background:linear-gradient(135deg, #436850, #365440);color:#FBFADA;border:none;padding:8px 18px;border-radius:8px;font-size:12px;font-weight:700;cursor:pointer;transition:all 0.2s;box-shadow:0 2px 6px rgba(67,104,80,0.2);}
.view-btn:hover{transform:translateY(-1px);box-shadow:0 4px 10px rgba(67,104,80,0.3);}

.stag{font-size:11px;font-weight:700;padding:4px 10px;border-radius:6px;text-transform:uppercase;}
.s-open{background:rgba(217,83,79,0.1);color:#D9534F;}
.s-done{background:rgba(67,104,80,0.1);color:#436850;}

/* Drawer Style */
.drawer-overlay{position:fixed;inset:0;background:rgba(18,55,42,0.4);backdrop-filter:blur(4px);display:flex;justify-content:flex-end;z-index:9999;}
.detail-drawer{width:900px;background:#FBFADA;height:100vh;box-shadow:-20px 0 60px rgba(18,55,42,0.2);display:flex;flex-direction:column;animation:slideIn 0.35s cubic-bezier(0.16, 1, 0.3, 1);}
@keyframes slideIn{from{transform:translateX(100%);}to{transform:translateX(0);}}
.drawer-header{padding:24px 32px;background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-bottom:1px solid rgba(173,188,159,0.2);display:flex;justify-content:space-between;align-items:center;}
.dh-sub{font-size:11px;color:rgba(18,55,42,0.4);font-weight:700;text-transform:uppercase;letter-spacing:1px;}
.dh-title{font-size:22px;font-weight:800;color:#12372A;margin:2px 0 0;}
.drawer-body{flex:1;overflow-y:auto;padding:0;}
.close-btn{background:none;border:none;color:rgba(18,55,42,0.3);cursor:pointer;padding:8px;border-radius:50%;transition:all 0.2s;display:flex;align-items:center;justify-content:center;}
.close-btn:hover{background:rgba(217,83,79,0.1);color:#D9534F;}
</style>
