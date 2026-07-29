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
          <button class="btn-icon" title="Export"><svg viewBox="0 0 20 20" width="16" height="16"><path d="M10 3v10M6 9l4 4 4-4M3 17h14" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
        </div>
      </div>

      <!-- KPI Cards -->
      <div class="kpi-cards">
        <div class="kpi-card"><span class="kpi-label">Total Unpaid Amount</span><span class="kpi-value">$627,860.00</span></div>
        <div class="kpi-card kpi-warn"><span class="kpi-label">Overdue Amount</span><span class="kpi-value kpi-amber">$128,540.00</span></div>
        <div class="kpi-card"><span class="kpi-label">Collected This Month</span><span class="kpi-value">$215,300.00</span></div>
        <div class="kpi-card"><span class="kpi-label">Remaining This Month</span><span class="kpi-value">$198,760.00</span></div>
      </div>

      <!-- Filter Bar -->
      <div class="filter-bar">
        <input type="text" class="form-input" v-model="f.customer" placeholder="Customer Name" />
        <input type="text" class="form-input" v-model="f.invoice" placeholder="Invoice No." />
        <select class="form-select" v-model="f.status"><option value="">All Statuses</option><option>Unpaid</option><option>Partially Paid</option><option>Overdue</option><option>Paid</option></select>
        <div class="date-range">
          <svg viewBox="0 0 20 20" width="14" height="14" class="date-icon"><rect x="2" y="4" width="16" height="13" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M2 8h16M6 2v4M14 2v4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
          <input type="date" class="form-input date-input" v-model="f.from" placeholder="Start Date" />
        </div>
        <div class="date-range">
          <svg viewBox="0 0 20 20" width="14" height="14" class="date-icon"><rect x="2" y="4" width="16" height="13" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M2 8h16M6 2v4M14 2v4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
          <input type="date" class="form-input date-input" v-model="f.to" placeholder="End Date" />
        </div>
        <button class="btn btn-primary" @click="search">Search</button>
        <button class="btn btn-outline" @click="reset">Reset</button>
      </div>

      <!-- Table -->
      <div class="data-card">
        <table class="data-table">
          <thead><tr>
            <th>Invoice No.</th><th>Customer Name</th><th>Invoice Date</th><th>Due Date</th>
            <th class="num">Invoice Amount</th><th class="num">Received Amount</th><th class="num">Unpaid Amount</th>
            <th>Status</th><th>Collection Progress</th><th>Action</th>
          </tr></thead>
          <tbody>
            <tr v-for="row in rows" :key="row.id" class="data-row">
              <td class="mono">{{ row.inv }}</td><td>{{ row.cust }}</td><td>{{ row.date }}</td><td>{{ row.due }}</td>
              <td class="num mono">{{ row.amt }}</td><td class="num mono">{{ row.rcv }}</td><td class="num mono strong">{{ row.unp }}</td>
              <td><span class="stag" :class="sc(row.st)">{{ row.st }}</span></td>
              <td><div class="prog-cell"><div class="prog-bar"><div class="prog-fill" :style="{width:row.pct+'%'}"></div></div><span class="prog-pct">{{ row.pct }}%</span></div></td>
              <td><a class="link" @click="$router.push('/finance/receivable/'+row.id)">View Details</a></td>
            </tr>
          </tbody>
        </table>
        <div class="table-footer">
          <div class="tf-left"><span class="tf-total">Total 18 items</span><select class="form-select form-select-sm" style="width:80px"><option>10 / page</option><option>20</option><option>50</option></select></div>
          <div class="pager"><button class="pg-btn">1</button><button class="pg-btn active">2</button><button class="pg-btn">3</button></div>
          <div class="tf-right"><span class="tf-label">Go to</span><input type="text" class="pg-input" placeholder="page" /></div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import MainLayout from '@/layout/MainLayout.vue'
const autoRefresh=ref(true); const refreshInterval=ref('30s')
const f=reactive({customer:'',invoice:'',status:'',from:'',to:''})
interface R{id:number;inv:string;cust:string;date:string;due:string;amt:string;rcv:string;unp:string;st:string;pct:number}
const rows:R[]=[
  {id:1,inv:'INV-2026-00089',cust:'The Bike Zone',date:'03/01/26',due:'03/31/26',amt:'$120,000.00',rcv:'$70,000.00',unp:'$50,000.00',st:'Unpaid',pct:58},
  {id:2,inv:'INV-2026-00102',cust:'GlobalTech Ltd',date:'04/01/26',due:'05/01/26',amt:'$142,500.00',rcv:'$100,000.00',unp:'$42,500.00',st:'Partially Paid',pct:70},
  {id:3,inv:'INV-2026-00115',cust:'Beta Industries',date:'05/10/26',due:'06/09/26',amt:'$56,200.00',rcv:'$0.00',unp:'$56,200.00',st:'Overdue',pct:0},
  {id:4,inv:'INV-2026-00128',cust:'Delta Supply',date:'06/01/26',due:'07/01/26',amt:'$210,000.00',rcv:'$210,000.00',unp:'$0.00',st:'Paid',pct:100},
  {id:5,inv:'INV-2026-00140',cust:'Omega Retail',date:'06/20/26',due:'07/20/26',amt:'$78,900.00',rcv:'$40,000.00',unp:'$38,900.00',st:'Partially Paid',pct:51},
]
function sc(s:string){const m:Record<string,string>={'Unpaid':'s-unpaid','Paid':'s-paid','Partially Paid':'s-partial','Overdue':'s-overdue'};return m[s]||''}
function search(){}
function reset(){Object.assign(f,{customer:'',invoice:'',status:'',from:'',to:''})}
</script>

<style scoped>
.page{padding:28px 36px;max-width:1340px;margin:0 auto;}

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
.date-range{position:relative;display:flex;align-items:center;}
.date-icon{position:absolute;left:10px;color:rgba(18,55,42,0.3);pointer-events:none;z-index:1;}
.date-input{padding-left:30px;min-width:150px;}

.data-card{background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:14px;border:1px solid rgba(173,188,159,0.15);box-shadow:0 2px 6px rgba(173,188,159,0.1);overflow:hidden;}
.data-table{width:100%;border-collapse:collapse;font-size:13px;}
.data-table th{text-align:left;padding:12px 14px;font-size:10px;font-weight:700;color:rgba(18,55,42,0.45);text-transform:uppercase;letter-spacing:0.8px;background:rgba(173,188,159,0.08);border-bottom:1px solid rgba(173,188,159,0.2);}
.data-table th.num{text-align:right;}
.data-table td{padding:11px 14px;border-bottom:1px solid rgba(173,188,159,0.08);color:#12372A;}
.data-table td.num{text-align:right;}
.data-row:hover{background:rgba(67,104,80,0.025);}
.mono{font-family:'SF Mono',Consolas,monospace;font-size:12px;}
.strong{font-weight:700;}

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

.table-footer{display:flex;align-items:center;justify-content:space-between;padding:12px 16px;border-top:1px solid rgba(173,188,159,0.15);}
.tf-left{display:flex;align-items:center;gap:10px;}
.tf-total{font-size:12px;color:rgba(18,55,42,0.4);}
.tf-right{display:flex;align-items:center;gap:8px;}
.tf-label{font-size:11px;color:rgba(18,55,42,0.35);}
.pg-input{width:50px;height:30px;border:1px solid rgba(173,188,159,0.35);border-radius:6px;text-align:center;font-size:12px;outline:none;}
.pager{display:flex;gap:4px;}
.pg-btn{min-width:30px;height:30px;border:1px solid rgba(173,188,159,0.25);border-radius:6px;background:rgba(251,250,218,0.3);font-size:12px;color:#12372A;cursor:pointer;display:flex;align-items:center;justify-content:center;}
.pg-btn.active{background:#436850;color:#FBFADA;border-color:#436850;}

.btn{display:inline-flex;align-items:center;gap:6px;padding:9px 20px;font-size:13px;font-weight:600;border-radius:8px;cursor:pointer;transition:all 0.2s;font-family:inherit;}
.btn-primary{background:linear-gradient(135deg,#436850,#365440);color:#FBFADA;border:none;box-shadow:0 2px 8px rgba(67,104,80,0.25);}
.btn-primary:hover{transform:translateY(-1px);box-shadow:0 4px 16px rgba(67,104,80,0.3);}
.btn-outline{background:none;color:rgba(18,55,42,0.5);border:1px solid rgba(173,188,159,0.35);}
.btn-outline:hover{border-color:rgba(18,55,42,0.3);color:#12372A;}
.btn-icon{background:none;border:1px solid rgba(173,188,159,0.3);border-radius:8px;padding:6px;cursor:pointer;color:rgba(18,55,42,0.45);display:flex;transition:all 0.2s;}
.btn-icon:hover{border-color:#436850;color:#436850;background:rgba(67,104,80,0.05);}
</style>