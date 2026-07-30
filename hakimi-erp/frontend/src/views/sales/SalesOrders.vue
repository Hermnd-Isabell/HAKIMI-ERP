<template>
  <MainLayout>
    <div class="page">
      <div class="header-card">
        <div class="hc-left">
          <div class="hc-icon"><svg viewBox="0 0 24 24" width="22" height="22"><path d="M4 4h3l1 5h7l2-5h2M7 14a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm7 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4z" fill="none" stroke="#436850" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
          <div class="hc-text"><h2 class="hc-title">Sales Orders</h2><p class="hc-sub">Manage and track all sales orders across the organization.</p></div>
        </div>
        <div class="hc-right">
          <button class="btn btn-primary" @click="showCreate = true">
            <svg viewBox="0 0 24 24" width="16" height="16" style="margin-right: 4px;"><path d="M12 5v14M5 12h14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
            Create Order
          </button>
        </div>
      </div>

      <div class="filter-bar">
        <input type="text" class="form-input" placeholder="Order No." />
        <input type="text" class="form-input" placeholder="Customer Name" />
        <select class="form-select"><option>All Statuses</option><option>Open</option><option>In Process</option><option>Completed</option><option>Cancelled</option></select>
        <button class="btn btn-primary">Search</button>
        <button class="btn btn-outline">Reset</button>
      </div>

      <div class="data-card">
        <table class="data-table">
          <thead><tr><th>Order No.</th><th>Customer</th><th>Order Date</th><th class="num">Net Value</th><th>Status</th><th>Action</th></tr></thead>
          <tbody>
            <tr v-for="r in rows" :key="r.id" class="data-row">
              <td class="mono">{{ r.no }}</td><td>{{ r.cust }}</td><td>{{ r.date }}</td><td class="num mono">{{ r.val }}</td>
              <td><span class="stag" :class="sc(r.st)">{{ r.st }}</span></td>
              <td>
                <a class="link" @click="viewDetail(r.id)">View</a>
                <span class="divider" v-if="r.st === 'OPEN'">|</span>
                <a class="link" v-if="r.st === 'OPEN'" @click="convertToDelivery(r.id)">Convert to Delivery</a>
              </td>
            </tr>
            <tr v-if="rows.length === 0"><td colspan="6" style="text-align:center;padding:40px;color:#999;">No orders found.</td></tr>
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
        <div class="modal-header"><h3>Create New Sales Order</h3><button class="close-btn" @click="showCreate=false">&times;</button></div>
        <div class="modal-body">
          <div class="hdr-info-row" v-if="quotationId">
            <span class="info-tag">Ref Quotation: {{ quotationId }}</span>
          </div>
          <div class="form-grid">
            <div class="form-group"><label class="fl required">Customer (BP)</label>
              <select class="form-select" v-model="form.customerId">
                <option v-for="p in partners" :key="p.bp_id" :value="p.bp_id">{{ p.bp_id }} - {{ p.bp_name }}</option>
              </select>
            </div>
            <div class="form-group"><label class="fl">Customer Reference</label><input type="text" class="form-input" v-model="form.customerReference" /></div>
            
            <div class="form-group"><label class="fl">Req. Deliv. Date</label><input type="date" class="form-input" v-model="form.requestedDeliveryDate" /></div>
            <div class="form-group"><label class="fl">Pricing Date</label><input type="date" class="form-input" v-model="form.pricingDate" /></div>
            
            <div class="form-group"><label class="fl">Ship. Condition</label><input type="text" class="form-input" v-model="form.shippingCondition" /></div>
            <div class="form-group"><label class="fl">Deliv. Priority</label><input type="text" class="form-input" v-model="form.deliveryPriority" /></div>
          </div>

          <div class="divider">Material Details</div>
          
          <div class="form-grid">
            <div class="form-group"><label class="fl required">Material</label>
              <select class="form-select" v-model="form.materialId">
                <option v-for="m in materials" :key="m.material_id" :value="m.material_id">{{ m.material_id }} - {{ m.material_name }}</option>
              </select>
            </div>
            <div class="form-group"><label class="fl">Item Category</label><input type="text" class="form-input" v-model="form.itemCategory" /></div>
            <div class="form-group"><label class="fl required">Quantity</label><input type="number" class="form-input" v-model="form.quantity" /></div>
            <div class="form-group"><label class="fl">Plant</label><input type="text" class="form-input" v-model="form.plant" /></div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-outline" @click="showCreate=false">Cancel</button>
          <button class="btn btn-primary" @click="handleSave">Create Order</button>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue"
import MainLayout from "@/layout/MainLayout.vue"
import axios from "axios"
import { useRoute, useRouter } from "vue-router"

const route = useRoute()
const router = useRouter()
interface R{id:string;no:string;cust:string;date:string;val:string;st:string}
const rows = ref<R[]>([])

// Create form state
const showCreate = ref(false)
const quotationId = ref("")
const form = reactive({
  customerId: '',
  materialId: '',
  quantity: 1,
  type: 'OR',
  customerReference: '',
  requestedDeliveryDate: '',
  pricingDate: new Date().toISOString().split('T')[0],
  shippingCondition: '01',
  deliveryPriority: '02',
  itemCategory: 'TAN',
  plant: '1000'
})

const partners = ref<any[]>([])
const materials = ref<any[]>([])

async function fetchQuotationRef(id: string) {
  try {
    const res = await axios.get(`/api/v1/sales/quotations/${id}`)
    if (res.data.success) {
      const q = res.data.data
      quotationId.value = q.quotation_id
      form.customerId = q.customer_id
      if (q.items && q.items.length > 0) {
        const item = q.items[0]
        form.materialId = item.material_id
        form.quantity = item.order_quantity
      }
      showCreate.value = true
    }
  } catch (err) {
    console.error("Fetch quotation ref failed:", err)
  }
}

async function fetchData() {
  try {
    const [soRes, bpRes, matRes] = await Promise.all([
      axios.get("/api/v1/sales/orders"),
      axios.get("/api/v1/master/partners/"),
      axios.get("/api/v1/master/materials/")
    ])
    
    if (soRes.data.success) {
      rows.value = soRes.data.data.items.map((i: any) => ({
        id: i.sales_order_id,
        no: i.sales_order_id,
        cust: i.customer_id,
        date: i.created_time?.split('T')[0] || 'N/A',
        val: i.net_value ? `¥${i.net_value.toLocaleString()}` : '¥0.00',
        st: i.status
      }))
    }
    if (bpRes.data.success) partners.value = bpRes.data.data.items
    if (matRes.data.success) materials.value = matRes.data.data.items
  } catch (err) {
    console.error("Fetch error:", err)
  }
}

onMounted(() => {
  fetchData()
  const refQuo = route.query.ref as string
  if (refQuo) {
    fetchQuotationRef(refQuo)
  }
})

async function handleSave() {
  try {
    const payload = {
      sales_order_id: `SO${Math.floor(Math.random() * 1000000).toString().padStart(6, '0')}`,
      quotation_id: quotationId.value || null,
      order_type: form.type,
      customer_id: form.customerId,
      customer_reference: form.customerReference,
      requested_delivery_date: form.requestedDeliveryDate || null,
      pricing_date: form.pricingDate || null,
      shipping_condition: form.shippingCondition,
      delivery_priority: form.deliveryPriority,
      status: 'OPEN',
      items: [
        {
          so_item_id: `SOI${Math.floor(Math.random() * 1000000)}`,
          item_no: 10,
          material_id: form.materialId,
          item_category: form.itemCategory,
          order_quantity: form.quantity,
          plant: form.plant,
          sales_unit: 'PC'
        }
      ]
    }
    const res = await axios.post("/api/v1/sales/orders", payload)
    if (res.data.success) {
      alert("Sales Order created!")
      showCreate.value = false
      fetchData()
    }
  } catch (err: any) {
    alert("Save failed: " + (err.response?.data?.detail || err.message))
  }
}

function sc(s:string){const m:Record<string,string>={"OPEN":"s-open","IN_PROCESS":"s-proc","COMPLETED":"s-done","CANCELLED":"s-cancel"};return m[s]||""}
function viewDetail(id:string){alert("Viewing order "+id+" details")}
async function convertToDelivery(id:string) {
  if (confirm(`Create delivery for order ${id}?`)) {
    try {
      const res = await axios.post(`/api/v1/logistics/deliveries/from-so/${id}`)
      if (res.data.success) {
        alert(`Delivery ${res.data.data.delivery_id} created successfully!`)
        router.push("/delivery/list")
      }
    } catch (err: any) {
      alert("Failed to create delivery: " + (err.response?.data?.detail || err.message))
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
.form-input,.form-select{height:38px;border:1px solid rgba(173,188,159,0.4);border-radius:8px;padding:0 12px;font-size:13px;color:#12372A;background:rgba(251,250,218,0.35);font-family:inherit;outline:none;min-width:140px;transition:all 0.2s;}
.form-input:focus,.form-select:focus{border-color:#436850;box-shadow:0 0 0 3px rgba(67,104,80,0.06);}
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
.s-proc{background:rgba(240,173,78,0.12);color:#c98a20;}
.s-done{background:rgba(67,104,80,0.12);color:#2d4a38;}
.s-cancel{background:rgba(217,83,79,0.08);color:#c94a45;}
.link{color:#436850;cursor:pointer;font-weight:600;font-size:12px;}
.link:hover{text-decoration:underline;}
.divider{margin:0 8px;color:rgba(18,55,42,0.15);font-size:12px;}
.table-footer{display:flex;align-items:center;justify-content:space-between;padding:12px 16px;border-top:1px solid rgba(173,188,159,0.15);}

/* Modal & Form Styles */
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
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.modal-header h3 { color: #12372A; margin: 0; font-size: 18px; }
.close-btn { background: none; border: none; font-size: 24px; cursor: pointer; color: #999; }
.modal-body { display: flex; flex-direction: column; gap: 16px; }
.modal-footer { margin-top: 24px; display: flex; justify-content: flex-end; gap: 12px; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.divider { margin: 20px 0 10px; padding-bottom: 5px; border-bottom: 1px solid rgba(173,188,159,0.2); font-size: 12px; font-weight: 700; color: #436850; text-transform: uppercase; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.fl { font-size: 12px; font-weight: 600; color: #12372A; opacity: 0.7; }
.fl.required::after { content: " *"; color: #D9534F; }

.hdr-info-row{display:flex;gap:12px;margin-bottom:12px;padding-bottom:10px;border-bottom:1px solid rgba(173,188,159,0.1);}
.info-tag{font-size:11px;font-weight:700;background:rgba(67,104,80,0.08);color:#436850;padding:4px 10px;border-radius:6px;border:1px solid rgba(67,104,80,0.1);}

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