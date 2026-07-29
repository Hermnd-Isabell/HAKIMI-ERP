<template>
  <MainLayout>
    <div class="page">
      <div class="header-card">
        <div class="hc-left">
          <div class="hc-icon"><svg viewBox="0 0 24 24" width="22" height="22"><path d="M3 8l1.7-4.3A1 1 0 0 1 5.6 3h12.8a1 1 0 0 1 .9.7L21 8M5 8v11a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8" fill="none" stroke="#436850" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M10 12h4" fill="none" stroke="#436850" stroke-width="1.5" stroke-linecap="round"/></svg></div>
          <div class="hc-text"><h2 class="hc-title">Inquiry Management</h2><p class="hc-sub">Track and manage customer inquiries, convert to quotations.</p></div>
        </div>
      </div>

      <div class="filter-bar">
        <input type="text" class="form-input" placeholder="Inquiry No." />
        <input type="text" class="form-input" placeholder="Customer Name" />
        <select class="form-select"><option>All Statuses</option><option>Open</option><option>Converted</option><option>Rejected</option></select>
        <button class="btn btn-primary">Search</button>
        <button class="btn btn-outline">Reset</button>
      </div>

      <div class="data-card">
        <table class="data-table">
          <thead><tr><th>Inquiry No.</th><th>Customer</th><th>Inquiry Date</th><th>Material</th><th class="num">Quantity</th><th>Status</th><th>Action</th></tr></thead>
          <tbody>
            <tr v-for="r in rows" :key="r.id" class="data-row">
              <td class="mono">{{ r.no }}</td><td>{{ r.cust }}</td><td>{{ r.date }}</td><td>{{ r.mat }}</td><td class="num mono">{{ r.qty }}</td>
              <td><span class="stag" :class="sc(r.st)">{{ r.st }}</span></td>
              <td><a class="link" @click="viewDetail(r.id)">View Details</a></td>
            </tr>
          </tbody>
        </table>
        <div class="table-footer">
          <span class="tf-total">Total {{ rows.length }} items</span>
          <div class="pager"><button class="pg-btn active">1</button><button class="pg-btn">2</button></div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from "@/layout/MainLayout.vue"
interface R{id:number;no:string;cust:string;date:string;mat:string;qty:string;st:string}
const rows:R[]=[
  {id:1,no:"INQ00001",cust:"The Bike Zone",date:"2026-01-10",mat:"Bicycle Frame X200",qty:"50",st:"Converted"},
  {id:2,no:"INQ00002",cust:"Acme Corp",date:"2026-02-14",mat:"Gear Set Pro",qty:"200",st:"Open"},
  {id:3,no:"INQ00003",cust:"GlobalTech",date:"2026-03-05",mat:"Brake Pads V3",qty:"1,000",st:"Open"},
  {id:4,no:"INQ00004",cust:"Beta Industries",date:"2026-04-22",mat:"Chain Assembly",qty:"350",st:"Rejected"},
  {id:5,no:"INQ00005",cust:"Delta Supply",date:"2026-05-18",mat:"Pedal Set Light",qty:"800",st:"Converted"},
]
function sc(s:string){const m:Record<string,string>={"Open":"s-open","Converted":"s-done","Rejected":"s-cancel"};return m[s]||""}
function viewDetail(id:number){alert("Viewing inquiry "+id+" details")}
</script>

<style scoped>
.page{padding:28px 36px;max-width:1200px;margin:0 auto;}
.header-card{display:flex;align-items:center;background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:16px;padding:20px 24px;border:1px solid rgba(173,188,159,0.18);box-shadow:0 2px 8px rgba(173,188,159,0.12);margin-bottom:20px;}
.hc-left{display:flex;align-items:center;gap:14px;}
.hc-icon{width:44px;height:44px;border-radius:12px;background:rgba(67,104,80,0.08);display:flex;align-items:center;justify-content:center;}
.hc-title{font-size:18px;font-weight:800;color:#12372A;margin:0;}
.hc-sub{font-size:12px;color:rgba(18,55,42,0.45);margin:2px 0 0;}
.filter-bar{display:flex;gap:10px;margin-bottom:16px;align-items:center;flex-wrap:wrap;}
.form-input,.form-select{height:38px;border:1px solid rgba(173,188,159,0.4);border-radius:8px;padding:0 12px;font-size:13px;color:#12372A;background:rgba(251,250,218,0.35);font-family:inherit;outline:none;min-width:140px;transition:all 0.2s;}
.form-input:focus,.form-select:focus{border-color:#436850;box-shadow:0 0 0 3px rgba(67,104,80,0.06);}
.data-card{background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:14px;border:1px solid rgba(173,188,159,0.15);box-shadow:0 2px 6px rgba(173,188,159,0.1);overflow:hidden;}
.data-table{width:100%;border-collapse:collapse;font-size:13px;}
.data-table th{text-align:left;padding:12px 14px;font-size:10px;font-weight:700;color:rgba(18,55,42,0.45);text-transform:uppercase;letter-spacing:0.8px;background:rgba(173,188,159,0.08);border-bottom:1px solid rgba(173,188,159,0.2);}
.data-table th.num{text-align:right;}
.data-table td{padding:11px 14px;border-bottom:1px solid rgba(173,188,159,0.08);color:#12372A;}
.data-table td.num{text-align:right;}
.data-row:hover{background:rgba(67,104,80,0.025);}
.mono{font-family:"SF Mono",Consolas,monospace;font-size:12px;}
.stag{font-size:11px;font-weight:600;padding:4px 10px;border-radius:6px;}
.s-open{background:rgba(67,104,80,0.1);color:#436850;}
.s-done{background:rgba(67,104,80,0.12);color:#2d4a38;}
.s-cancel{background:rgba(217,83,79,0.08);color:#c94a45;}
.link{color:#436850;cursor:pointer;font-weight:600;font-size:12px;}
.link:hover{text-decoration:underline;}
.table-footer{display:flex;align-items:center;justify-content:space-between;padding:12px 16px;border-top:1px solid rgba(173,188,159,0.15);}
.tf-total{font-size:12px;color:rgba(18,55,42,0.4);}
.pager{display:flex;gap:4px;}
.pg-btn{min-width:30px;height:30px;border:1px solid rgba(173,188,159,0.25);border-radius:6px;background:rgba(251,250,218,0.3);font-size:12px;color:#12372A;cursor:pointer;display:flex;align-items:center;justify-content:center;}
.pg-btn.active{background:#436850;color:#FBFADA;border-color:#436850;}
.btn{display:inline-flex;align-items:center;gap:6px;padding:9px 20px;font-size:13px;font-weight:600;border-radius:8px;cursor:pointer;transition:all 0.2s;font-family:inherit;}
.btn-primary{background:linear-gradient(135deg,#436850,#365440);color:#FBFADA;border:none;}
.btn-primary:hover{transform:translateY(-1px);}
.btn-outline{background:none;color:rgba(18,55,42,0.5);border:1px solid rgba(173,188,159,0.35);}
.btn-outline:hover{border-color:rgba(18,55,42,0.3);color:#12372A;}
</style>
