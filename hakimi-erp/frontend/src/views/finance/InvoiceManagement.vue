<template>
  <MainLayout>
    <div class="page">
      <div class="header-card">
        <div class="hc-left">
          <div class="hc-icon"><svg viewBox="0 0 24 24" width="22" height="22"><rect x="3" y="5" width="18" height="14" rx="2" fill="none" stroke="#436850" stroke-width="1.8"/><path d="M3 10h18M7 15h5" fill="none" stroke="#436850" stroke-width="1.5" stroke-linecap="round"/></svg></div>
          <div class="hc-text"><h2 class="hc-title">Invoice Management</h2><p class="hc-sub">Track and manage all billing documents and invoice status.</p></div>
        </div>
      </div>
      <div class="filter-bar">
        <input type="text" class="form-input" placeholder="Invoice No." /><input type="text" class="form-input" placeholder="Customer" />
        <select class="form-select"><option>All Statuses</option><option>Open</option><option>Partial</option><option>Cleared</option><option>Void</option></select>
        <button class="btn btn-primary">Search</button><button class="btn btn-outline">Reset</button>
      </div>
      <div class="data-card"><table class="data-table">
        <thead><tr><th>Invoice No.</th><th>Customer</th><th>Date</th><th class="num">Amount</th><th class="num">Received</th><th>Status</th><th>Action</th></tr></thead>
        <tbody>
          <tr v-for="r in rows" :key="r.id" class="data-row">
            <td class="mono">{{ r.no }}</td><td>{{ r.cust }}</td><td>{{ r.date }}</td><td class="num mono">{{ r.amt }}</td><td class="num mono">{{ r.rcv }}</td>
            <td><span class="stag" :class="sc(r.st)">{{ r.st }}</span></td>
            <td><a class="link" @click="$router.push('/finance/receivable/'+r.id)">View Details</a></td>
          </tr>
        </tbody>
      </table></div>
    </div>
  </MainLayout>
</template>
<script setup lang="ts">
import MainLayout from '@/layout/MainLayout.vue'
interface R{id:number;no:string;cust:string;date:string;amt:string;rcv:string;st:string}
const rows:R[]=[
  {id:1,no:'INV-00086',cust:'The Bike Zone',date:'2026-01-28',amt:'$85,000.00',rcv:'$20,000.00',st:'Open'},
  {id:2,no:'INV-00102',cust:'GlobalTech',date:'2026-04-01',amt:'$142,500.00',rcv:'$100,000.00',st:'Partial'},
  {id:3,no:'INV-00115',cust:'Beta Ind.',date:'2026-05-10',amt:'$56,200.00',rcv:'$0.00',st:'Open'},
  {id:4,no:'INV-00128',cust:'Delta Supply',date:'2026-06-01',amt:'$210,000.00',rcv:'$210,000.00',st:'Cleared'},
]
function sc(s:string){const m:Record<string,string>={'Open':'s-open','Partial':'s-partial','Cleared':'s-done','Void':'s-cancel'};return m[s]||''}
</script>
<style scoped>
.page{padding:28px 36px;max-width:1200px;margin:0 auto;}
.header-card{display:flex;align-items:center;background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:16px;padding:20px 24px;border:1px solid rgba(173,188,159,0.18);box-shadow:0 2px 8px rgba(173,188,159,0.12);margin-bottom:20px;}
.hc-left{display:flex;align-items:center;gap:14px;}
.hc-icon{width:44px;height:44px;border-radius:12px;background:rgba(67,104,80,0.08);display:flex;align-items:center;justify-content:center;}
.hc-title{font-size:18px;font-weight:800;color:#12372A;margin:0;}
.hc-sub{font-size:12px;color:rgba(18,55,42,0.45);margin:2px 0 0;}
.filter-bar{display:flex;gap:10px;margin-bottom:16px;align-items:center;flex-wrap:wrap;}
.form-input,.form-select{height:38px;border:1px solid rgba(173,188,159,0.4);border-radius:8px;padding:0 12px;font-size:13px;color:#12372A;background:rgba(251,250,218,0.35);font-family:inherit;outline:none;min-width:130px;}
.data-card{background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:14px;border:1px solid rgba(173,188,159,0.15);box-shadow:0 2px 6px rgba(173,188,159,0.1);overflow:hidden;}
.data-table{width:100%;border-collapse:collapse;font-size:13px;}
.data-table th{text-align:left;padding:12px 14px;font-size:10px;font-weight:700;color:rgba(18,55,42,0.45);text-transform:uppercase;letter-spacing:0.8px;background:rgba(173,188,159,0.08);border-bottom:1px solid rgba(173,188,159,0.2);}
.data-table th.num{text-align:right;}
.data-table td{padding:11px 14px;border-bottom:1px solid rgba(173,188,159,0.08);color:#12372A;}
.data-table td.num{text-align:right;}
.data-row:hover{background:rgba(67,104,80,0.025);}
.mono{font-family:'SF Mono',Consolas,monospace;font-size:12px;}
.stag{font-size:11px;font-weight:600;padding:4px 10px;border-radius:6px;}
.s-open{background:rgba(67,104,80,0.1);color:#436850;}
.s-partial{background:rgba(240,173,78,0.12);color:#c98a20;}
.s-done{background:rgba(67,104,80,0.12);color:#2d4a38;}
.s-cancel{background:rgba(217,83,79,0.08);color:#c94a45;}
.link{color:#436850;cursor:pointer;font-weight:600;font-size:12px;}
.link:hover{text-decoration:underline;}
.btn{display:inline-flex;align-items:center;gap:6px;padding:9px 20px;font-size:13px;font-weight:600;border-radius:8px;cursor:pointer;transition:all 0.2s;font-family:inherit;}
.btn-primary{background:linear-gradient(135deg,#436850,#365440);color:#FBFADA;border:none;}.btn-primary:hover{transform:translateY(-1px);}
.btn-outline{background:none;color:rgba(18,55,42,0.5);border:1px solid rgba(173,188,159,0.35);}
.btn-outline:hover{border-color:rgba(18,55,42,0.3);color:#12372A;}
</style>