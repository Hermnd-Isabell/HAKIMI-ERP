<template>
  <MainLayout>
    <div class="page">
      <div class="header-card">
        <div class="hc-left">
          <div class="hc-icon">
            <svg viewBox="0 0 24 24" width="22" height="22">
              <path d="M5 3h10l4 4v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z" fill="none" stroke="#436850" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M13 3v4h4M7 11l2 2 4-4" fill="none" stroke="#436850" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="hc-text">
            <h2 class="hc-title">Quotation Management</h2>
            <p class="hc-sub">Manage customer quotes and convert them to sales orders.</p>
          </div>
        </div>
        <div class="hc-right">
          <button class="btn btn-primary" @click="$router.push('/sales/quotation/new')">
            <svg viewBox="0 0 24 24" width="16" height="16" style="margin-right: 4px;">
              <path d="M12 5v14M5 12h14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            Create Quotation
          </button>
        </div>
      </div>

      <div class="filter-bar">
        <input type="text" class="form-input" placeholder="Quotation No." />
        <input type="text" class="form-input" placeholder="Customer" />
        <select class="form-select">
          <option>All Statuses</option>
          <option>Open</option>
          <option>Closed</option>
        </select>
        <button class="btn btn-primary">Search</button>
        <button class="btn btn-outline">Reset</button>
      </div>

      <div class="data-card">
        <table class="data-table">
          <thead>
            <tr>
              <th>Quotation No.</th>
              <th>Ref Inquiry</th>
              <th>Customer</th>
              <th>Valid Until</th>
              <th class="num">Net Value</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="r in rows" :key="r.id" class="data-row">
              <td class="mono">{{ r.no }}</td>
              <td class="mono">{{ r.refInq || '-' }}</td>
              <td>{{ r.cust }}</td>
              <td>{{ r.validTo }}</td>
              <td class="num mono">{{ r.val }}</td>
              <td><span class="stag" :class="sc(r.st)">{{ r.st }}</span></td>
              <td>
                <a class="link" @click="viewDetail(r.id)">View</a>
                <span class="divider" v-if="r.st === 'OPEN'">|</span>
                <a class="link" v-if="r.st === 'OPEN'" @click="convertToOrder(r.id)">Convert to Order</a>
              </td>
            </tr>
            <tr v-if="rows.length === 0">
              <td colspan="7" style="text-align:center;padding:40px;color:#999;">No quotations found.</td>
            </tr>
          </tbody>
        </table>
        <div class="table-footer">
          <span class="tf-total">Total {{ rows.length }} items</span>
          <div class="pager">
            <button class="pg-btn active">1</button>
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue"
import MainLayout from "@/layout/MainLayout.vue"
import axios from "axios"
import { useRouter } from "vue-router"

const router = useRouter()

interface R {
  id: string
  no: string
  refInq: string | null
  cust: string
  validTo: string
  val: string
  st: string
}

const rows = ref<R[]>([])

async function fetchQuotations() {
  try {
    const res = await axios.get("/api/v1/sales/quotations")
    if (res.data.success) {
      rows.value = res.data.data.items.map((q: any) => ({
        id: q.quotation_id,
        no: q.quotation_id,
        refInq: q.inquiry_id,
        cust: q.customer_id,
        validTo: q.valid_to || 'N/A',
        val: q.net_value ? `¥${q.net_value.toLocaleString()}` : '¥0.00',
        st: q.status
      }))
    }
  } catch (err) {
    console.error("Fetch quotations failed:", err)
  }
}

onMounted(fetchQuotations)

function sc(s: string) {
  const m: Record<string, string> = {
    "OPEN": "s-open",
    "CLOSED": "s-done",
    "CANCELLED": "s-cancel"
  }
  return m[s] || ""
}

function viewDetail(id: string) {
  router.push(`/sales/quotation/${id}`)
}

function convertToOrder(id: string) {
  router.push({ path: '/sales/orders', query: { ref: id } })
}
</script>

<style scoped>
.page { padding: 28px 36px; max-width: 1200px; margin: 0 auto; }
.header-card { display: flex; align-items: center; background: linear-gradient(145deg, #fdfce8, #f7f5d1); border-radius: 16px; padding: 20px 24px; border: 1px solid rgba(173,188,159,0.18); box-shadow: 0 2px 8px rgba(173,188,159,0.12); margin-bottom: 20px; }
.hc-left { display: flex; align-items: center; gap: 14px; }
.hc-icon { width: 44px; height: 44px; border-radius: 12px; background: rgba(67,104,80,0.08); display: flex; align-items: center; justify-content: center; }
.hc-title { font-size: 18px; font-weight: 800; color: #12372A; margin: 0; }
.hc-sub { font-size: 12px; color: rgba(18,55,42,0.45); margin: 2px 0 0; }
.filter-bar { display: flex; gap: 10px; margin-bottom: 16px; align-items: center; flex-wrap: wrap; }
.form-input, .form-select { height: 38px; border: 1px solid rgba(173,188,159,0.4); border-radius: 8px; padding: 0 12px; font-size: 13px; color: #12372A; background: rgba(251,250,218,0.35); font-family: inherit; outline: none; min-width: 140px; transition: all 0.2s; }
.data-card { background: linear-gradient(145deg, #fdfce8, #f7f5d1); border-radius: 14px; border: 1px solid rgba(173,188,159,0.15); box-shadow: 0 2px 6px rgba(173,188,159,0.1); overflow: hidden; }
.data-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.data-table th { text-align: left; padding: 12px 14px; font-size: 10px; font-weight: 700; color: rgba(18,55,42,0.45); text-transform: uppercase; letter-spacing: 0.8px; background: rgba(173,188,159,0.08); border-bottom: 1px solid rgba(173,188,159,0.2); }
.data-table th.num { text-align: right; }
.data-table td { padding: 11px 14px; border-bottom: 1px solid rgba(173,188,159,0.08); color: #12372A; }
.data-table td.num { text-align: right; }
.data-row:hover { background: rgba(67,104,80,0.025); }
.mono { font-family: "SF Mono", Consolas, monospace; font-size: 12px; }
.stag { font-size: 11px; font-weight: 600; padding: 4px 10px; border-radius: 6px; }
.s-open { background: rgba(67,104,80,0.1); color: #436850; }
.s-done { background: rgba(67,104,80,0.12); color: #2d4a38; }
.s-cancel { background: rgba(217,83,79,0.08); color: #c94a45; }
.link { color: #436850; cursor: pointer; font-weight: 600; font-size: 12px; }
.link:hover { text-decoration: underline; }
.divider { margin: 0 8px; color: rgba(18, 55, 42, 0.15); font-size: 12px; }
.table-footer { display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; border-top: 1px solid rgba(173,188,159,0.15); }
.tf-total { font-size: 12px; color: rgba(18,55,42,0.4); }
.btn { display: inline-flex; align-items: center; gap: 6px; padding: 9px 20px; font-size: 13px; font-weight: 600; border-radius: 8px; cursor: pointer; transition: all 0.2s; font-family: inherit; }
.btn-primary { background: linear-gradient(135deg, #436850, #365440); color: #FBFADA; border: none; }
.btn-outline { background: none; color: rgba(18,55,42,0.5); border: 1px solid rgba(173,188,159,0.35); }
.pg-btn { min-width: 30px; height: 30px; border: 1px solid rgba(173,188,159,0.25); border-radius: 6px; background: rgba(251,250,218,0.3); font-size: 12px; color: #12372A; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.pg-btn.active { background: #436850; color: #FBFADA; border-color: #436850; }
</style>
