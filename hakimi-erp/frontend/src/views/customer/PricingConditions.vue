<template>
  <MainLayout>
    <div class="page">
      <div class="header-card">
        <div class="hc-left">
          <div class="hc-icon"><svg viewBox="0 0 24 24" width="22" height="22"><circle cx="12" cy="12" r="10" fill="none" stroke="#436850" stroke-width="1.8"/><path d="M12 7v5l3 2M7 12h10" fill="none" stroke="#436850" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
          <div class="hc-text"><h2 class="hc-title">Pricing Conditions</h2><p class="hc-sub">Define and maintain pricing condition records for materials and customers.</p></div>
        </div>
      </div>
      <div class="filter-bar">
        <input class="form-input" placeholder="Condition Type" /><input class="form-input" placeholder="Material" />
        <input class="form-input" placeholder="Customer" />
        <select class="form-select"><option>All Types</option><option>PR00 - Price</option><option>K004 - Material</option><option>K007 - Discount</option></select>
        <button class="btn btn-primary">Search</button><button class="btn btn-outline">Reset</button>
      </div>
      <div class="data-card"><table class="dt">
        <thead><tr><th>Cond. Type</th><th>Name</th><th>Material</th><th>Customer</th><th class="num">Amount</th><th>Crcy</th><th>Valid From</th><th>Valid To</th><th>Status</th></tr></thead>
        <tbody>
          <tr v-for="r in rows" :key="r.id" class="dr">
            <td class="mono">{{ r.ct }}</td><td>{{ r.name }}</td><td class="mono">{{ r.mat }}</td><td>{{ r.cust }}</td>
            <td class="num mono">{{ r.amt }}</td><td>{{ r.crcy }}</td><td>{{ r.from }}</td><td>{{ r.to }}</td>
            <td><span class="stag" :class="r.st==='Active'?'s-done':'s-cancel'">{{ r.st }}</span></td>
          </tr>
        </tbody>
      </table></div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from '@/layout/MainLayout.vue'
const rows=[{id:1,ct:'PR00',name:'Price',mat:'DXTR1026',cust:'*',amt:'2,950.00',crcy:'USD',from:'2026-01-01',to:'2026-12-31',st:'Active'},{id:2,ct:'PR00',name:'Price',mat:'FG-1001',cust:'*',amt:'1,200.00',crcy:'USD',from:'2026-01-01',to:'2026-12-31',st:'Active'},{id:3,ct:'K004',name:'Material Surcharge',mat:'DXTR1026',cust:'*',amt:'50.00',crcy:'USD',from:'2026-03-01',to:'2026-06-30',st:'Active'},{id:4,ct:'K007',name:'Customer Discount',mat:'*',cust:'The Bike Zone',amt:'5.00%',crcy:'%',from:'2026-01-01',to:'2026-12-31',st:'Active'},{id:5,ct:'PR00',name:'Price',mat:'CABL4400',cust:'*',amt:'185.00',crcy:'USD',from:'2025-06-01',to:'2025-12-31',st:'Expired'}]
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
.dt{width:100%;border-collapse:collapse;font-size:13px;}
.dt th{text-align:left;padding:12px 14px;font-size:10px;font-weight:700;color:rgba(18,55,42,0.45);text-transform:uppercase;letter-spacing:0.8px;background:rgba(173,188,159,0.08);border-bottom:1px solid rgba(173,188,159,0.2);}
.dt th.num{text-align:right;}
.dt td{padding:11px 14px;border-bottom:1px solid rgba(173,188,159,0.08);color:#12372A;}
.dt td.num{text-align:right;}
.dr:hover{background:rgba(67,104,80,0.025);}
.mono{font-family:'SF Mono',Consolas,monospace;font-size:12px;}
.stag{font-size:10px;font-weight:600;padding:3px 8px;border-radius:5px;}
.s-done{background:rgba(67,104,80,0.1);color:#436850;}
.s-cancel{background:rgba(217,83,79,0.08);color:#c94a45;}
.btn{display:inline-flex;align-items:center;gap:6px;padding:9px 20px;font-size:13px;font-weight:600;border-radius:8px;cursor:pointer;transition:all 0.2s;font-family:inherit;}
.btn-primary{background:linear-gradient(135deg,#436850,#365440);color:#FBFADA;border:none;}.btn-primary:hover{transform:translateY(-1px);}
.btn-outline{background:none;color:rgba(18,55,42,0.5);border:1px solid rgba(173,188,159,0.35);}.btn-outline:hover{border-color:rgba(18,55,42,0.3);color:#12372A;}
</style>