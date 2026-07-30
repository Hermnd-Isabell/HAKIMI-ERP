<template>
  <MainLayout>
    <div class="page">
      <div class="header-card">
        <div class="hc-left">
          <div class="hc-icon"><svg viewBox="0 0 24 24" width="22" height="22"><path d="M3 8l1.7-4.3A1 1 0 0 1 5.6 3h12.8a1 1 0 0 1 .9.7L21 8M5 8v11a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8" fill="none" stroke="#436850" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M10 12h4" fill="none" stroke="#436850" stroke-width="1.5" stroke-linecap="round"/></svg></div>
          <div class="hc-text"><h2 class="hc-title">Inquiry Management</h2><p class="hc-sub">Track and manage customer inquiries, convert to quotations.</p></div>
        </div>
        <div class="hc-right">
          <button class="btn btn-primary" @click="showCreate = true">
            <svg viewBox="0 0 24 24" width="16" height="16" style="margin-right: 4px;"><path d="M12 5v14M5 12h14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
            Create Inquiry
          </button>
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
              <td>
                <a class="link" @click="viewDetail(r.id)">View</a>
                <span class="divider">|</span>
                <a class="link" v-if="r.st === 'OPEN'" @click="convertToQuotation(r.id)">Convert to Quote</a>
              </td>
            </tr>
            <tr v-if="rows.length === 0"><td colspan="7" style="text-align:center;padding:40px;color:#999;">No inquiries found.</td></tr>
          </tbody>
        </table>
        <div class="table-footer">
          <span class="tf-total">Total {{ rows.length }} items</span>
          <div class="pager"><button class="pg-btn active">1</button></div>
        </div>
      </div>
    </div>

    <!-- Create Modal -->
    <div v-if="showCreate" class="modal-mask">
      <div class="modal-container modal-lg">
        <div class="modal-header"><h3>Create New Inquiry</h3><button class="close-btn" @click="showCreate=false">&times;</button></div>
        <div class="modal-body">
          <div class="form-grid">
            <div class="form-group"><label class="fl required">Customer (BP)</label>
              <select class="form-select" v-model="form.customerId">
                <option v-for="p in partners" :key="p.bp_id" :value="p.bp_id">{{ p.bp_id }} - {{ p.bp_name }}</option>
              </select>
            </div>
            <div class="form-group"><label class="fl">Customer Reference</label><input type="text" class="form-input" v-model="form.customerReference" /></div>
            
            <div class="form-group"><label class="fl">Validity From</label><input type="date" class="form-input" v-model="form.validFrom" /></div>
            <div class="form-group"><label class="fl">Validity To</label><input type="date" class="form-input" v-model="form.validTo" /></div>
            
            <div class="form-group"><label class="fl">Req. Deliv. Date</label><input type="date" class="form-input" v-model="form.requestedDeliveryDate" /></div>
            <div class="form-group"><label class="fl">Sales Org</label><input type="text" class="form-input" v-model="form.salesOrg" /></div>
          </div>

          <div class="divider">Material Details</div>
          
          <div class="form-grid">
            <div class="form-group"><label class="fl required">Material</label>
              <select class="form-select" v-model="form.materialId">
                <option v-for="m in materials" :key="m.material_id" :value="m.material_id">{{ m.material_id }} - {{ m.material_name }}</option>
              </select>
            </div>
            <div class="form-group"><label class="fl">Item Description</label><input type="text" class="form-input" v-model="form.itemDescription" /></div>
            <div class="form-group"><label class="fl required">Quantity</label><input type="number" class="form-input" v-model="form.quantity" /></div>
            <div class="form-group"><label class="fl">Expected Value</label><input type="number" class="form-input" v-model="form.expectedValue" /></div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-outline" @click="showCreate=false">Cancel</button>
          <button class="btn btn-primary" @click="handleSave">Create Inquiry</button>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue"
import MainLayout from "@/layout/MainLayout.vue"
import axios from "axios"
import { useRouter } from "vue-router"

const router = useRouter()
interface R{id:string;no:string;cust:string;date:string;mat:string;qty:string;st:string}
const rows = ref<R[]>([])

// Create form state
const showCreate = ref(false)
const form = reactive({
  customerId: '',
  materialId: '',
  quantity: 1,
  type: 'IN',
  validFrom: new Date().toISOString().split('T')[0],
  validTo: '',
  requestedDeliveryDate: '',
  customerReference: '',
  salesOrg: '1000',
  distributionChannel: '10',
  division: '00',
  itemDescription: '',
  expectedValue: 0
})

const partners = ref<any[]>([])
const materials = ref<any[]>([])

async function fetchData() {
  try {
    const [inqRes, bpRes, matRes] = await Promise.all([
      axios.get("/api/v1/sales/inquiries"),
      axios.get("/api/v1/master/partners/"),
      axios.get("/api/v1/master/materials/")
    ])
    
    if (inqRes.data.success) {
      rows.value = inqRes.data.data.items.map((i: any) => ({
        id: i.inquiry_id,
        no: i.inquiry_id,
        cust: i.customer_id,
        date: i.created_time?.split('T')[0] || 'N/A',
        mat: i.items?.[0]?.material_id || 'N/A',
        qty: i.items?.[0]?.order_quantity || '0',
        st: i.status
      }))
    }
    if (bpRes.data.success) partners.value = bpRes.data.data.items
    if (matRes.data.success) materials.value = matRes.data.data.items
  } catch (err) {
    console.error("Fetch error:", err)
  }
}

onMounted(fetchData)

async function handleSave() {
  try {
    const payload = {
      inquiry_id: `INQ${Math.floor(Math.random() * 1000000).toString().padStart(6, '0')}`,
      inquiry_type: form.type,
      customer_id: form.customerId,
      customer_reference: form.customerReference,
      valid_from: form.validFrom || null,
      valid_to: form.validTo || null,
      requested_delivery_date: form.requestedDeliveryDate || null,
      sales_org: form.salesOrg,
      distribution_channel: form.distributionChannel,
      division: form.division,
      status: 'OPEN',
      items: [
        {
          inquiry_item_id: `II${Math.floor(Math.random() * 1000000)}`,
          item_no: 10,
          material_id: form.materialId,
          item_description: form.itemDescription,
          order_quantity: form.quantity,
          expected_order_value: form.expectedValue,
          sales_unit: 'PC'
        }
      ]
    }
    const res = await axios.post("/api/v1/sales/inquiries", payload)
    if (res.data.success) {
      alert("Inquiry created!")
      showCreate.value = false
      fetchData()
    }
  } catch (err: any) {
    alert("Save failed: " + (err.response?.data?.detail || err.message))
  }
}

function sc(s:string){const m:Record<string,string>={"OPEN":"s-open","CLOSED":"s-done","CANCELLED":"s-cancel"};return m[s]||""}
function viewDetail(id:string){alert("Viewing inquiry "+id+" details")}
function convertToQuotation(id:string) {
  router.push({ path: '/sales/quotation/new', query: { ref: id } })
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
.divider{margin:0 8px;color:rgba(18,55,42,0.15);font-size:12px;}
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

/* Modal CSS */
.modal-mask {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(18, 55, 42, 0.4); backdrop-filter: blur(4px);
  display: flex; align-items: center; justify-content: center; z-index: 1000;
}
.modal-container {
  background: #FBFADA; width: 480px; border-radius: 16px; padding: 24px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.1); border: 1px solid rgba(173,188,159,0.3);
}
.modal-lg { width: 720px; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.divider { margin: 20px 0 10px; padding-bottom: 5px; border-bottom: 1px solid rgba(173,188,159,0.2); font-size: 12px; font-weight: 700; color: #436850; text-transform: uppercase; }
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.modal-header h3 { color: #12372A; margin: 0; font-size: 18px; }
.close-btn { background: none; border: none; font-size: 24px; cursor: pointer; color: #999; }
.modal-body { display: flex; flex-direction: column; gap: 16px; }
.modal-footer { margin-top: 24px; display: flex; justify-content: flex-end; gap: 12px; }
.fl.required::after { content: " *"; color: #D9534F; }
</style>
