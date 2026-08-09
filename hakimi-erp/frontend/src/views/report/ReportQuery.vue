<template>
  <div class="page">
    <div class="header-card">
        <div class="hc-left">
          <div class="hc-icon"><svg viewBox="0 0 24 24" width="22" height="22"><rect x="3" y="3" width="7" height="7" rx="1" fill="none" stroke="#436850" stroke-width="1.8"/><rect x="14" y="3" width="7" height="7" rx="1" fill="none" stroke="#436850" stroke-width="1.8"/><rect x="3" y="14" width="7" height="7" rx="1" fill="none" stroke="#436850" stroke-width="1.8"/><rect x="14" y="14" width="7" height="7" rx="1" fill="none" stroke="#436850" stroke-width="1.8"/></svg></div>
          <div class="hc-text"><h2 class="hc-title">Report Query</h2><p class="hc-sub">Generate and export business intelligence reports.</p></div>
        </div>
      </div>

      <div class="report-grid" v-if="!activeReport">
        <div class="report-card" v-for="r in reports" :key="r.id">
          <div class="rc-icon" v-html="r.icon"></div>
          <div class="rc-body">
            <h3 class="rc-title">{{ r.title }}</h3>
            <p class="rc-desc">{{ r.desc }}</p>
            <div class="rc-meta">
              <span class="rc-tag">{{ r.category }}</span>
              <span class="rc-date">Updated: {{ r.updated }}</span>
            </div>
            <button class="btn btn-primary rc-btn" @click="runReport(r)">Run Report</button>
          </div>
        </div>
      </div>

      <!-- Result View -->
      <div v-else class="result-container">
        <div class="result-header">
          <button class="back-link" @click="activeReport = null">
            <svg viewBox="0 0 20 20" width="16" height="16"><path d="M12 4l-6 6 6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            Back to Reports
          </button>
          <div class="rh-main">
            <h3>{{ activeReport.title }}</h3>
            <div class="rh-actions">
              <button class="btn btn-outline btn-sm" @click="exportData">Export CSV</button>
              <button class="btn btn-primary btn-sm" @click="refreshReport">Refresh</button>
            </div>
          </div>
        </div>

        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>Processing data...</p>
        </div>

        <div v-else-if="reportData" class="report-content">
          <!-- Sales Performance View -->
          <div v-if="activeReport.id === 1" class="data-view">
            <div class="kpi-row">
              <div class="kpi-card">
                <label>Total Orders</label>
                <div class="value">{{ salesSummary.totalOrders }}</div>
              </div>
              <div class="kpi-card">
                <label>Total Revenue</label>
                <div class="value">¥{{ salesSummary.totalRevenue.toLocaleString() }}</div>
              </div>
              <div class="kpi-card">
                <label>Avg Order Value</label>
                <div class="value">¥{{ salesSummary.avgValue.toLocaleString() }}</div>
              </div>
            </div>
            <div class="table-wrap">
              <table class="report-table">
                <thead><tr><th>Date</th><th>Orders</th><th class="num">Revenue</th></tr></thead>
                <tbody>
                  <tr v-for="(label, idx) in reportData.labels" :key="label">
                    <td>{{ label }}</td>
                    <td>{{ reportData.counts[idx] }}</td>
                    <td class="num mono">¥{{ reportData.values[idx].toLocaleString() }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Delivery Analysis View -->
          <div v-else-if="activeReport.id === 2" class="data-view">
            <div class="fin-grid">
              <div class="fin-card">
                <div class="fc-header"><span class="label">Total Deliveries</span></div>
                <div class="fc-val">{{ reportData.total }}</div>
              </div>
              <div class="fin-card success">
                <div class="fc-header"><span class="label">Completed</span></div>
                <div class="fc-val">{{ reportData.completed }}</div>
              </div>
              <div class="fin-card warn">
                <div class="fc-header"><span class="label">Pending</span></div>
                <div class="fc-val">{{ reportData.pending }}</div>
              </div>
              <div class="fin-card info">
                <div class="fc-header"><span class="label">Completion Rate</span></div>
                <div class="fc-val">{{ reportData.completionRate.toFixed(1) }}%</div>
              </div>
            </div>
          </div>

          <!-- Financial Summary View -->
          <div v-else-if="activeReport.id === 3" class="data-view">
            <div class="fin-grid">
              <div class="fin-card">
                <div class="fc-header"><span class="label">Total Invoiced</span></div>
                <div class="fc-val">¥{{ reportData.totalInvoiced.toLocaleString() }}</div>
              </div>
              <div class="fin-card warn">
                <div class="fc-header"><span class="label">Open Receivables</span></div>
                <div class="fc-val">¥{{ reportData.openReceivables.toLocaleString() }}</div>
              </div>
              <div class="fin-card success">
                <div class="fc-header"><span class="label">Collected Amount</span></div>
                <div class="fc-val">¥{{ reportData.collectedAmount.toLocaleString() }}</div>
              </div>
              <div class="fin-card info">
                <div class="fc-header"><span class="label">Collection Rate</span></div>
                <div class="fc-val">{{ reportData.collectionRate.toFixed(1) }}%</div>
              </div>
            </div>
          </div>

          <!-- Generic View for others -->
          <div v-else class="empty-result">
            <svg viewBox="0 0 24 24" width="64" height="64" opacity="0.1"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z" fill="currentColor"/><path d="M13 2v7h7" fill="none" stroke="currentColor" stroke-width="2"/></svg>
            <p>Report generation completed. Detailed visualization for this report type is coming soon.</p>
          </div>
        </div>
      </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { fetchSalesPerformance, fetchFinancialSummary, fetchDeliveryStats } from '@/api/modules/report'

interface R{id:number;title:string;desc:string;category:string;updated:string;icon:string}
const reports:R[]=[
  {id:1,title:"Sales Performance Report",desc:"Monthly sales revenue, order volume, and customer acquisition analysis.",category:"Sales",updated:"2026-07-28",icon:'<svg viewBox="0 0 24 24" width="28" height="28"><path d="M3 20h2V10H3v10zm6 0h2V4H9v16zm6 0h2v-7h-2v7zm6 0h2V7h-2v13z" fill="none" stroke="#436850" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'},
  {id:2,title:"Delivery Analysis Report",desc:"On-time delivery rate, logistics cost breakdown, and shipping trends.",category:"Delivery",updated:"2026-07-25",icon:'<svg viewBox="0 0 24 24" width="28" height="28"><rect x="1" y="3" width="15" height="11" rx="1" fill="none" stroke="#436850" stroke-width="1.8"/><path d="M16 8h4l3 4v3h-3a2 2 0 0 1-4 0" fill="none" stroke="#436850" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><circle cx="7" cy="18" r="2" fill="none" stroke="#436850" stroke-width="1.5"/><circle cx="18" cy="18" r="2" fill="none" stroke="#436850" stroke-width="1.5"/></svg>'},
  {id:3,title:"Financial Summary Report",desc:"Revenue, profit margin, invoice aging, and cash flow overview.",category:"Finance",updated:"2026-07-22",icon:'<svg viewBox="0 0 24 24" width="28" height="28"><rect x="2" y="4" width="20" height="16" rx="2" fill="none" stroke="#436850" stroke-width="1.8"/><path d="M7 15l3-3 2 2 4-4" fill="none" stroke="#436850" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><circle cx="17" cy="10" r="1.5" fill="#436850"/></svg>'},
  {id:4,title:"Customer Analysis Report",desc:"Customer segmentation, retention rates, and purchasing behavior trends.",category:"Customer",updated:"2026-07-20",icon:'<svg viewBox="0 0 24 24" width="28" height="28"><circle cx="9" cy="7" r="4" fill="none" stroke="#436850" stroke-width="1.8"/><path d="M1 21c0-4.4 3.6-8 8-8s8 3.6 8 8" fill="none" stroke="#436850" stroke-width="1.8" stroke-linecap="round"/><circle cx="18" cy="6" r="3" fill="none" stroke="#436850" stroke-width="1.5"/><path d="M23 16c0-2.2-1.8-4-4-4" fill="none" stroke="#436850" stroke-width="1.5" stroke-linecap="round"/></svg>'},
  {id:5,title:"Inventory Turnover Report",desc:"Stock levels, turnover rates, and material movement analysis.",category:"Inventory",updated:"2026-07-18",icon:'<svg viewBox="0 0 24 24" width="28" height="28"><path d="M21 16V8a2 2 0 0 0-1-1.73L13 2.27a2 2 0 0 0-2 0L4 6.27A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" fill="none" stroke="#436850" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 12l7-4M12 12v9M12 12L5 8" fill="none" stroke="#436850" stroke-width="1.2" stroke-linecap="round"/></svg>'},
  {id:6,title:"Pricing Conditions Report",desc:"Discount distribution, margin analysis, and pricing strategy overview.",category:"Pricing",updated:"2026-07-15",icon:'<svg viewBox="0 0 24 24" width="28" height="28"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87L18.18 22 12 18.56 5.82 22 7 14.14l-5-4.87 6.91-1.01L12 2z" fill="none" stroke="#436850" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'},
  {id:7,title:"Tax & Compliance Report",desc:"Tax summary, compliance status, and regulatory audit trail.",category:"Finance",updated:"2026-07-12",icon:'<svg viewBox="0 0 24 24" width="28" height="28"><rect x="3" y="3" width="18" height="18" rx="2" fill="none" stroke="#436850" stroke-width="1.8"/><path d="M3 9h18M9 3v18" fill="none" stroke="#436850" stroke-width="1.2"/></svg>'},
  {id:8,title:"Quotation Conversion Report",desc:"Quotation-to-order conversion rates, win/loss analysis, and pipeline health.",category:"Sales",updated:"2026-07-10",icon:'<svg viewBox="0 0 24 24" width="28" height="28"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" fill="none" stroke="#436850" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8" fill="none" stroke="#436850" stroke-width="1.5" stroke-linecap="round"/></svg>'},
]

const activeReport = ref<R | null>(null)
const reportData = ref<any>(null)
const loading = ref(false)

async function runReport(r: R) {
  activeReport.value = r
  await refreshReport()
}

async function refreshReport() {
  if (!activeReport.value) return
  loading.value = true
  reportData.value = null
  try {
    if (activeReport.value.id === 1) {
      reportData.value = await fetchSalesPerformance({ days: 30 })
    } else if (activeReport.value.id === 3) {
      reportData.value = await fetchFinancialSummary()
    } else if (activeReport.value.id === 2) {
      reportData.value = await fetchDeliveryStats()
    } else {
      // Mock for others
      await new Promise(resolve => setTimeout(resolve, 800))
      reportData.value = { mock: true }
    }
  } catch (err: any) {
    alert('Failed to generate report: ' + err.message)
  } finally {
    loading.value = false
  }
}

const salesSummary = computed(() => {
  if (!reportData.value || activeReport.value?.id !== 1) return { totalOrders: 0, totalRevenue: 0, avgValue: 0 }
  const totalOrders = reportData.value.counts.reduce((a: number, b: number) => a + b, 0)
  const totalRevenue = reportData.value.values.reduce((a: number, b: number) => a + b, 0)
  return {
    totalOrders,
    totalRevenue,
    avgValue: totalOrders > 0 ? totalRevenue / totalOrders : 0
  }
})

function exportData() {
  alert('Exporting data as CSV...')
}
</script>

<style scoped>
.page{padding:28px 36px;max-width:1200px;margin:0 auto;}
.header-card{display:flex;align-items:center;background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:16px;padding:20px 24px;border:1px solid rgba(173,188,159,0.18);box-shadow:0 2px 8px rgba(173,188,159,0.12);margin-bottom:20px;}
.hc-left{display:flex;align-items:center;gap:14px;}
.hc-icon{width:44px;height:44px;border-radius:12px;background:rgba(67,104,80,0.08);display:flex;align-items:center;justify-content:center;}
.hc-title{font-size:18px;font-weight:800;color:#12372A;margin:0;}
.hc-sub{font-size:12px;color:rgba(18,55,42,0.45);margin:2px 0 0;}

.report-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:16px;}
.report-card{display:flex;gap:16px;background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:14px;padding:20px;border:1px solid rgba(173,188,159,0.15);box-shadow:0 2px 8px rgba(173,188,159,0.1);transition:all 0.25s;}
.report-card:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(173,188,159,0.18);border-color:rgba(67,104,80,0.15);}
.rc-icon{width:48px;height:48px;border-radius:12px;background:rgba(67,104,80,0.06);display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.rc-body{flex:1;min-width:0;display:flex;flex-direction:column;}
.rc-title{font-size:15px;font-weight:700;color:#12372A;margin:0 0 6px;}
.rc-desc{font-size:12px;color:rgba(18,55,42,0.45);line-height:1.5;margin:0 0 10px;}
.rc-meta{display:flex;align-items:center;gap:10px;margin-bottom:12px;}
.rc-tag{font-size:10px;font-weight:600;background:rgba(67,104,80,0.08);color:#436850;padding:3px 10px;border-radius:4px;text-transform:uppercase;letter-spacing:0.4px;}
.rc-date{font-size:11px;color:rgba(18,55,42,0.3);}
.rc-btn{align-self:flex-start;padding:8px 18px;font-size:12px;}

.result-container { background: linear-gradient(145deg,#fdfce8,#f7f5d1); border-radius: 16px; padding: 24px; border: 1px solid rgba(173,188,159,0.18); }
.result-header { margin-bottom: 24px; }
.back-link { background: none; border: none; color: #436850; cursor: pointer; display: flex; align-items: center; gap: 4px; font-weight: 600; font-size: 13px; margin-bottom: 12px; }
.rh-main { display: flex; justify-content: space-between; align-items: center; }
.rh-main h3 { font-size: 20px; font-weight: 800; color: #12372A; margin: 0; }
.rh-actions { display: flex; gap: 10px; }

.loading-state { padding: 60px; text-align: center; color: rgba(18,55,42,0.4); }
.spinner { width: 32px; height: 32px; border: 3px solid rgba(67, 104, 80, 0.1); border-top-color: #436850; border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 16px; }
@keyframes spin { to { transform: rotate(360deg); } }

.kpi-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px; }
.kpi-card { background: rgba(255,255,255,0.4); border-radius: 12px; padding: 16px; border: 1px solid rgba(173,188,159,0.2); }
.kpi-card label { font-size: 11px; font-weight: 700; color: rgba(18,55,42,0.4); text-transform: uppercase; display: block; margin-bottom: 4px; }
.kpi-card .value { font-size: 20px; font-weight: 800; color: #12372A; }

.table-wrap { overflow-x: auto; }
.report-table { width: 100%; border-collapse: collapse; }
.report-table th { text-align: left; padding: 12px; font-size: 11px; font-weight: 700; color: rgba(18,55,42,0.4); text-transform: uppercase; border-bottom: 2px solid rgba(173,188,159,0.2); }
.report-table td { padding: 12px; border-bottom: 1px solid rgba(173,188,159,0.1); font-size: 14px; }
.num { text-align: right; }
.mono { font-family: 'SF Mono', monospace; }

.fin-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
.fin-card { background: #fff; padding: 24px; border-radius: 16px; border-left: 6px solid #436850; box-shadow: 0 4px 12px rgba(0,0,0,0.03); }
.fin-card.warn { border-left-color: #F0AD4E; }
.fin-card.success { border-left-color: #5CB85C; }
.fin-card.info { border-left-color: #5BC0DE; }
.fc-header { margin-bottom: 8px; }
.fc-header .label { font-size: 12px; font-weight: 700; color: rgba(0,0,0,0.4); text-transform: uppercase; }
.fc-val { font-size: 28px; font-weight: 800; color: #12372A; }

.empty-result { padding: 60px; text-align: center; color: rgba(18,55,42,0.3); display: flex; flex-direction: column; align-items: center; gap: 16px; }

.btn{display:inline-flex;align-items:center;gap:6px;padding:9px 20px;font-size:13px;font-weight:600;border-radius:8px;cursor:pointer;transition:all 0.2s;font-family:inherit;border:none;}
.btn-sm { padding: 6px 14px; font-size: 12px; }
.btn-primary{background:linear-gradient(135deg,#436850,#365440);color:#FBFADA;}
.btn-primary:hover{transform:translateY(-1px);box-shadow:0 4px 12px rgba(67,104,80,0.25);}
.btn-outline{background:transparent;border:1.5px solid rgba(67,104,80,0.3);color:#436850;}
.btn-outline:hover{background:rgba(67,104,80,0.05);}
</style>
