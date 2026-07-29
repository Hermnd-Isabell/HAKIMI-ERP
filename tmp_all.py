# ================================================================
# 2. Product Page
# ================================================================
prod = r"""<template>
  <MainLayout>
    <div class="page">
      <div class="header-card">
        <div class="hc-left">
          <div class="hc-icon"><svg viewBox="0 0 24 24" width="22" height="22"><path d="M12 2l7 4.5v9L12 20l-7-4.5v-9L12 2z" fill="none" stroke="#436850" stroke-width="1.8" stroke-linejoin="round"/><path d="M12 7v8M5 9l7 4 7-4" fill="none" stroke="#436850" stroke-width="1.3" stroke-linecap="round"/></svg></div>
          <div class="hc-text"><h2 class="hc-title">Product Catalog</h2><p class="hc-sub">Browse and manage product listings with pricing and availability.</p></div>
        </div>
      </div>
      <div class="filter-bar">
        <input class="form-input" placeholder="Product ID" /><input class="form-input" placeholder="Product Name" />
        <select class="form-select"><option>All Categories</option><option>Electronics</option><option>Mechanical</option><option>Raw Materials</option></select>
        <button class="btn btn-primary">Search</button><button class="btn btn-outline">Reset</button>
      </div>
      <div class="data-card"><table class="dt">
        <thead><tr><th>Product ID</th><th>Name</th><th>Category</th><th class="num">Unit Price</th><th>UoM</th><th class="num">Stock</th><th>Status</th></tr></thead>
        <tbody>
          <tr v-for="p in prods" :key="p.id" class="dr">
            <td class="mono">{{ p.id }}</td><td>{{ p.name }}</td><td>{{ p.cat }}</td><td class="num mono">{{ p.price }}</td><td>{{ p.uom }}</td><td class="num mono">{{ p.stock }}</td>
            <td><span class="stag" :class="p.st==='Available'?'s-done':'s-warn'">{{ p.st }}</span></td>
          </tr>
        </tbody>
      </table></div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from '@/layout/MainLayout.vue'
const prods=[{id:'DXTR1026',name:'Industrial Sensor X200',cat:'Electronics',price:'$2,950.00',uom:'EA',stock:'1,250',st:'Available'},{id:'CABL4400',name:'Fiber Optic Cable 50m',cat:'Electronics',price:'$185.00',uom:'M',stock:'3,400',st:'Available'},{id:'FG-1001',name:'Mountain Bike Frame',cat:'Mechanical',price:'$1,200.00',uom:'EA',stock:'450',st:'Available'},{id:'BRKT220',name:'Mounting Bracket Set',cat:'Mechanical',price:'$89.00',uom:'EA',stock:'0',st:'Out of Stock'},{id:'SP-7780',name:'Brake Assembly Kit',cat:'Mechanical',price:'$320.00',uom:'EA',stock:'180',st:'Available'}]
</script>

<style scoped>
.page{padding:28px 36px;max-width:1200px;margin:0 auto;}
.header-card{display:flex;align-items:center;background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:16px;padding:20px 24px;border:1px solid rgba(173,188,159,0.18);box-shadow:0 2px 8px rgba(173,188,159,0.12);margin-bottom:20px;}
.hc-left{display:flex;align-items:center;gap:14px;}
.hc-icon{width:44px;height:44px;border-radius:12px;background:rgba(67,104,80,0.08);display:flex;align-items:center;justify-content:center;}
.hc-title{font-size:18px;font-weight:800;color:#12372A;margin:0;}
.hc-sub{font-size:12px;color:rgba(18,55,42,0.45);margin:2px 0 0;}
.filter-bar{display:flex;gap:10px;margin-bottom:16px;align-items:center;flex-wrap:wrap;}
.form-input,.form-select{height:38px;border:1px solid rgba(173,188,159,0.4);border-radius:8px;padding:0 12px;font-size:13px;color:#12372A;background:rgba(251,250,218,0.35);font-family:inherit;outline:none;min-width:140px;}
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
.s-warn{background:rgba(217,83,79,0.08);color:#c94a45;}
.btn{display:inline-flex;align-items:center;gap:6px;padding:9px 20px;font-size:13px;font-weight:600;border-radius:8px;cursor:pointer;transition:all 0.2s;font-family:inherit;}
.btn-primary{background:linear-gradient(135deg,#436850,#365440);color:#FBFADA;border:none;}.btn-primary:hover{transform:translateY(-1px);}
.btn-outline{background:none;color:rgba(18,55,42,0.5);border:1px solid rgba(173,188,159,0.35);}.btn-outline:hover{border-color:rgba(18,55,42,0.3);color:#12372A;}
</style>"""

with open(r'D:\HAKIMI-ERP\hakimi-erp\frontend\src\views\customer\Product.vue', 'w', encoding='utf-8') as f:
    f.write(prod)
print('2. Product OK')

# ================================================================
# 3. Pricing Conditions
# ================================================================
pricing = r"""<template>
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
</style>"""

with open(r'D:\HAKIMI-ERP\hakimi-erp\frontend\src\views\customer\PricingConditions.vue', 'w', encoding='utf-8') as f:
    f.write(pricing)
print('3. Pricing OK')

# ================================================================
# 4. Sales Organization
# ================================================================
sorg = r"""<template>
  <MainLayout>
    <div class="page">
      <div class="header-card">
        <div class="hc-left">
          <div class="hc-icon"><svg viewBox="0 0 24 24" width="22" height="22"><rect x="2" y="3" width="20" height="17" rx="2" fill="none" stroke="#436850" stroke-width="1.8"/><path d="M2 9h20M7 3v3M17 3v3M8 13h3M8 16h5" fill="none" stroke="#436850" stroke-width="1.5" stroke-linecap="round"/></svg></div>
          <div class="hc-text"><h2 class="hc-title">Sales Organization</h2><p class="hc-sub">Configure sales org structure, distribution channels, and divisions.</p></div>
        </div>
      </div>
      <div class="data-card"><table class="dt">
        <thead><tr><th>Sales Org</th><th>Description</th><th>Dist. Channel</th><th>Division</th><th>Currency</th><th>Country</th><th>Status</th></tr></thead>
        <tbody>
          <tr v-for="r in rows" :key="r.id" class="dr">
            <td class="mono">{{ r.so }}</td><td>{{ r.desc }}</td><td class="mono">{{ r.dc }}</td><td class="mono">{{ r.div }}</td><td>{{ r.curr }}</td><td>{{ r.cty }}</td>
            <td><span class="stag s-done">{{ r.st }}</span></td>
          </tr>
        </tbody>
      </table></div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from '@/layout/MainLayout.vue'
const rows=[{id:1,so:'1000',desc:'US East Sales',dc:'10 - Direct',div:'01 - Standard',curr:'USD',cty:'US',st:'Active'},{id:2,so:'1100',desc:'US West Sales',dc:'10 - Direct',div:'01 - Standard',curr:'USD',cty:'US',st:'Active'},{id:3,so:'2000',desc:'APAC Sales',dc:'20 - Wholesale',div:'02 - Special',curr:'CNY',cty:'CN',st:'Active'},{id:4,so:'3000',desc:'EU Central',dc:'10 - Direct',div:'01 - Standard',curr:'EUR',cty:'DE',st:'Active'},{id:5,so:'4000',desc:'LATAM Sales',dc:'30 - Retail',div:'03 - Export',curr:'USD',cty:'BR',st:'Inactive'}]
</script>

<style scoped>
.page{padding:28px 36px;max-width:1100px;margin:0 auto;}
.header-card{display:flex;align-items:center;background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:16px;padding:20px 24px;border:1px solid rgba(173,188,159,0.18);box-shadow:0 2px 8px rgba(173,188,159,0.12);margin-bottom:20px;}
.hc-left{display:flex;align-items:center;gap:14px;}
.hc-icon{width:44px;height:44px;border-radius:12px;background:rgba(67,104,80,0.08);display:flex;align-items:center;justify-content:center;}
.hc-title{font-size:18px;font-weight:800;color:#12372A;margin:0;}
.hc-sub{font-size:12px;color:rgba(18,55,42,0.45);margin:2px 0 0;}
.data-card{background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:14px;border:1px solid rgba(173,188,159,0.15);box-shadow:0 2px 6px rgba(173,188,159,0.1);overflow:hidden;}
.dt{width:100%;border-collapse:collapse;font-size:13px;}
.dt th{text-align:left;padding:12px 14px;font-size:10px;font-weight:700;color:rgba(18,55,42,0.45);text-transform:uppercase;letter-spacing:0.8px;background:rgba(173,188,159,0.08);border-bottom:1px solid rgba(173,188,159,0.2);}
.dt td{padding:11px 14px;border-bottom:1px solid rgba(173,188,159,0.08);color:#12372A;}
.dr:hover{background:rgba(67,104,80,0.025);}
.mono{font-family:'SF Mono',Consolas,monospace;font-size:12px;}
.stag{font-size:10px;font-weight:600;padding:3px 8px;border-radius:5px;}
.s-done{background:rgba(67,104,80,0.1);color:#436850;}
</style>"""

with open(r'D:\HAKIMI-ERP\hakimi-erp\frontend\src\views\customer\SalesOrganization.vue', 'w', encoding='utf-8') as f:
    f.write(sorg)
print('4. SalesOrg OK')
