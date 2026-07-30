<template>
  <MainLayout>
    <div class="page">
      <div class="header-card">
        <div class="hc-left">
          <div class="hc-icon"><svg viewBox="0 0 24 24" width="22" height="22"><rect x="2" y="5" width="20" height="13" rx="2" fill="none" stroke="#436850" stroke-width="1.8"/><path d="M6 5V3M18 5V3M2 11h20M7 16h3" fill="none" stroke="#436850" stroke-width="1.5" stroke-linecap="round"/></svg></div>
          <div class="hc-text"><h2 class="hc-title">Delivery List</h2><p class="hc-sub">View and manage all delivery orders.</p></div>
        </div>
      </div>
      <div class="filter-bar">
        <input type="text" class="form-input" placeholder="Delivery No." /><input type="text" class="form-input" placeholder="Sales Order" />
        <input type="text" class="form-input" placeholder="Customer" />
        <select class="form-select"><option>All Statuses</option><option>OPEN</option><option>PGI_DONE</option></select>
        <button class="btn btn-primary">Search</button><button class="btn btn-outline">Reset</button>
      </div>
      <div class="data-card">
        <table class="data-table">
          <thead><tr><th>Delivery No.</th><th>Sales Order</th><th>Customer</th><th>GI Date</th><th>Status</th><th>Action</th></tr></thead>
          <tbody>
            <tr v-for="r in rows" :key="r.id" class="data-row">
              <td class="mono">{{ r.no }}</td><td class="mono">{{ r.so }}</td><td>{{ r.cust }}</td><td>{{ r.date }}</td>
              <td><span class="stag" :class="sc(r.st)">{{ r.st }}</span></td>
              <td>
                <a class="link" @click="viewDetail(r.id)">View</a>
                <span class="divider" v-if="r.st === 'OPEN'">|</span>
                <a class="link" v-if="r.st === 'OPEN'" @click="handlePGI(r.id)">Post Goods Issue</a>
                <span class="divider" v-if="r.st === 'PGI_DONE'">|</span>
                <a class="link" v-if="r.st === 'PGI_DONE'" @click="createInvoice(r.id)">Create Invoice</a>
              </td>
            </tr>
            <tr v-if="rows.length === 0"><td colspan="6" style="text-align:center;padding:40px;color:#999;">No deliveries found.</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </MainLayout>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import MainLayout from '@/layout/MainLayout.vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
interface R{id:string;no:string;so:string;cust:string;date:string;st:string}
const rows = ref<R[]>([])

async function fetchData() {
  try {
    const res = await axios.get("/api/v1/logistics/deliveries")
    if (res.data.success) {
      rows.value = res.data.data.items.map((i: any) => ({
        id: i.delivery_id,
        no: i.delivery_id,
        so: i.sales_order_id,
        cust: i.ship_to_party,
        date: i.actual_gi_date?.split('T')[0] || i.planned_gi_date || 'N/A',
        st: i.delivery_status
      }))
    }
  } catch (err) {
    console.error("Fetch deliveries failed:", err)
  }
}

onMounted(fetchData)

function sc(s:string){const m:Record<string,string>={'PGI_DONE':'s-done','OPEN':'s-proc','CANCELLED':'s-cancel'};return m[s]||''}
function viewDetail(id:string){alert("Viewing delivery "+id+" details")}
async function handlePGI(id:string) {
  if (confirm(`Post Goods Issue for delivery ${id}? This will reduce inventory and lock the delivery.`)) {
    try {
      const res = await axios.post(`/api/v1/logistics/deliveries/${id}/pgi`)
      if (res.data.success) {
        alert("Goods Issue posted successfully!")
        fetchData()
      }
    } catch (err: any) {
      alert("PGI failed: " + (err.response?.data?.detail || err.message))
    }
  }
}
async function createInvoice(id:string) {
  if (confirm(`Create invoice for delivery ${id}?`)) {
    try {
      const res = await axios.post(`/api/v1/finance/invoices/from-delivery/${id}`)
      if (res.data.success) {
        alert(`Invoice ${res.data.data.invoice_id} created successfully!`)
        router.push("/finance/invoice")
      }
    } catch (err: any) {
      alert("Failed to create invoice: " + (err.response?.data?.detail || err.message))
    }
  }
}
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
.data-table td{padding:11px 14px;border-bottom:1px solid rgba(173,188,159,0.08);color:#12372A;}
.data-row:hover{background:rgba(67,104,80,0.025);}
.mono{font-family:'SF Mono',Consolas,monospace;font-size:12px;}
.stag{font-size:11px;font-weight:600;padding:4px 10px;border-radius:6px;}
.s-done{background:rgba(67,104,80,0.1);color:#436850;}
.s-proc{background:rgba(240,173,78,0.12);color:#c98a20;}
.s-cancel{background:rgba(217,83,79,0.08);color:#c94a45;}
.link{color:#436850;cursor:pointer;font-weight:600;font-size:12px;}
.link:hover{text-decoration:underline;}
.divider{margin:0 8px;color:rgba(18,55,42,0.15);font-size:12px;}
.btn{display:inline-flex;align-items:center;gap:6px;padding:9px 20px;font-size:13px;font-weight:600;border-radius:8px;cursor:pointer;transition:all 0.2s;font-family:inherit;}
.btn-primary{background:linear-gradient(135deg,#436850,#365440);color:#FBFADA;border:none;}
.btn-primary:hover{transform:translateY(-1px);}
.btn-outline{background:none;color:rgba(18,55,42,0.5);border:1px solid rgba(173,188,159,0.35);}
.btn-outline:hover{border-color:rgba(18,55,42,0.3);color:#12372A;}
</style>