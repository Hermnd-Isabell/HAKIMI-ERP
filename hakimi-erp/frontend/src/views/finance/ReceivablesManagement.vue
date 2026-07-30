<template>
  <MainLayout>
    <div class="page">
      <div class="header-card">
        <div class="hc-left">
          <div class="hc-icon"><svg viewBox="0 0 24 24" width="22" height="22"><circle cx="12" cy="12" r="10" fill="none" stroke="#436850" stroke-width="1.8"/><path d="M12 6v6l4 2M7 12h10" fill="none" stroke="#436850" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
          <div class="hc-text"><h2 class="hc-title">Receivables Management</h2><p class="hc-sub">Monitor all receivables, collections, and aging analysis.</p></div>
        </div>
      </div>
      <div class="filter-bar">
        <input type="text" class="form-input" placeholder="Customer" /><input type="text" class="form-input" placeholder="Invoice No." />
        <select class="form-select"><option>All Statuses</option><option>Open</option><option>Closed</option></select>
        <button class="btn btn-primary">Search</button><button class="btn btn-outline">Reset</button>
      </div>
      <div class="data-card"><table class="data-table">
        <thead><tr><th>Invoice No.</th><th>Customer</th><th>Due Date</th><th class="num">Amount</th><th class="num">Outstanding</th><th>Status</th><th>Action</th></tr></thead>
        <tbody>
          <tr v-for="r in rows" :key="r.id" class="data-row">
            <td class="mono">{{ r.no }}</td><td>{{ r.cust }}</td><td>{{ r.due }}</td><td class="num mono">{{ r.amt }}</td><td class="num mono">{{ r.out }}</td>
            <td><span class="stag" :class="sc(r.st)">{{ r.st }}</span></td>
            <td><a class="link" @click="$router.push('/finance/receivable/'+r.id)">View Details</a></td>
          </tr>
        </tbody>
      </table></div>
    </div>
  </MainLayout>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import MainLayout from '@/layout/MainLayout.vue'
import axios from 'axios'

interface R{id:string;no:string;cust:string;due:string;amt:string;out:string;st:string}
const rows = ref<R[]>([])

async function fetchData() {
  try {
    const [openRes, closedRes] = await Promise.all([
      axios.get("/api/v1/finance/ar/open"),
      axios.get("/api/v1/finance/ar/closed")
    ])
    
    const openItems = openRes.data.success ? openRes.data.data.items.map((i: any) => ({
      id: i.open_ar_id,
      no: i.invoice_id,
      cust: i.invoice?.payer || 'Unknown',
      due: i.due_date,
      amt: i.receivable_amount ? `¥${parseFloat(i.receivable_amount).toLocaleString()}` : '¥0.00',
      out: `¥${(parseFloat(i.receivable_amount) - parseFloat(i.received_amount)).toLocaleString()}`,
      st: 'Open'
    })) : []

    const closedItems = closedRes.data.success ? closedRes.data.data.items.map((i: any) => ({
      id: i.closed_ar_id,
      no: i.invoice_id,
      cust: i.invoice?.payer || 'Unknown',
      due: i.closed_time?.split('T')[0] || 'N/A',
      amt: i.receivable_amount ? `¥${parseFloat(i.receivable_amount).toLocaleString()}` : '¥0.00',
      out: '¥0.00',
      st: 'Closed'
    })) : []

    rows.value = [...openItems, ...closedItems]
  } catch (err) {
    console.error("Fetch AR failed:", err)
  }
}

onMounted(fetchData)

function sc(s:string){const m:Record<string,string>={'Open':'s-open','Closed':'s-done'};return m[s]||''}
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
.s-done{background:rgba(67,104,80,0.12);color:#2d4a38;}
.link{color:#436850;cursor:pointer;font-weight:600;font-size:12px;}.link:hover{text-decoration:underline;}
.btn{display:inline-flex;align-items:center;gap:6px;padding:9px 20px;font-size:13px;font-weight:600;border-radius:8px;cursor:pointer;transition:all 0.2s;font-family:inherit;}
.btn-primary{background:linear-gradient(135deg,#436850,#365440);color:#FBFADA;border:none;}.btn-primary:hover{transform:translateY(-1px);}
.btn-outline{background:none;color:rgba(18,55,42,0.5);border:1px solid rgba(173,188,159,0.35);}.btn-outline:hover{border-color:rgba(18,55,42,0.3);color:#12372A;}
</style>