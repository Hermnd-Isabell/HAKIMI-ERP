<template>
  <div class="page-container">
    <!-- Header -->
    <div class="page-header">
      <h2 class="page-title">{{ isEdit ? 'Edit' : 'Create' }} Inquiry</h2>
      <button class="exit-btn" @click="handleExit">
        <svg viewBox="0 0 20 20" width="16" height="16">
          <path d="M6 6l8 8M14 6l-8 8" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
        </svg>
        Exit
      </button>
    </div>

    <!-- Main Form Area -->
    <div class="form-card">
      <div class="form-row form-row-3">
        <div class="form-group">
          <label class="form-label">Inquiry No.</label>
          <input type="text" class="form-input" v-model="form.inquiryId" placeholder="Auto-generated if empty" :disabled="isEdit" />
        </div>
        <div class="form-group">
          <label class="form-label required">Inquiry Type</label>
          <select class="form-select" v-model="form.inquiryType">
            <option value="IN">Inquiry (IN)</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label required">Customer (BP)</label>
          <div class="input-with-f4">
            <select class="form-select" v-model="form.customerId">
              <option value="">-- Select Customer --</option>
              <option v-for="p in partners" :key="p.bpId" :value="p.bpId">{{ p.bpId }} - {{ p.bpName }}</option>
            </select>
            <button class="f4-trigger" @click="openF4('customer')">
              <svg viewBox="0 0 20 20" width="14" height="14">
                <circle cx="9" cy="9" r="5.5" fill="none" stroke="currentColor" stroke-width="1.5"/>
                <path d="M13 13l4 4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Tabs -->
    <div class="form-card form-card-tabs">
      <div class="tab-bar">
        <button
          v-for="tab in tabs" :key="tab.key"
          class="tab-btn" :class="{ active: activeTab === tab.key }"
          @click="activeTab = tab.key"
        >{{ tab.label }}</button>
      </div>

      <!-- Sales Tab -->
      <div class="tab-content" v-show="activeTab === 'sales'">
        <div class="form-grid-3">
          <div class="form-group">
            <label class="form-label">Sales Org</label>
            <input type="text" class="form-input" v-model="form.salesOrg" />
          </div>
          <div class="form-group">
            <label class="form-label">Dist. Channel</label>
            <input type="text" class="form-input" v-model="form.distributionChannel" />
          </div>
          <div class="form-group">
            <label class="form-label">Division</label>
            <input type="text" class="form-input" v-model="form.division" />
          </div>
          <div class="form-group">
            <label class="form-label">Sales Office</label>
            <input type="text" class="form-input" v-model="form.salesOffice" />
          </div>
          <div class="form-group">
            <label class="form-label">Sales Group</label>
            <input type="text" class="form-input" v-model="form.salesGroup" />
          </div>
          <div class="form-group">
            <label class="form-label">Currency</label>
            <input type="text" class="form-input" v-model="form.currency" />
          </div>
        </div>
      </div>

      <!-- Material Details Tab -->
      <div class="tab-content" v-show="activeTab === 'material'">
        <div class="form-grid-2">
          <div class="form-group">
            <label class="form-label required">Material</label>
            <div class="input-with-f4">
              <select class="form-select" v-model="itemForm.materialId">
                <option value="">-- Select Material --</option>
                <option v-for="m in materials" :key="m.materialId" :value="m.materialId">{{ m.materialId }} - {{ m.materialName }}</option>
              </select>
              <button class="f4-trigger" @click="openF4('material')">
                <svg viewBox="0 0 20 20" width="14" height="14">
                  <circle cx="9" cy="9" r="5.5" fill="none" stroke="currentColor" stroke-width="1.5"/>
                  <path d="M13 13l4 4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
              </button>
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Item Description</label>
            <input type="text" class="form-input" v-model="itemForm.itemDescription" />
          </div>
          <div class="form-group">
            <label class="form-label required">Quantity</label>
            <div class="input-with-unit">
              <input type="number" class="form-input" v-model="itemForm.orderQuantity" />
              <span class="input-unit">PC</span>
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Expected Value</label>
            <input type="number" class="form-input" v-model="itemForm.expectedOrderValue" />
          </div>
        </div>
      </div>

      <!-- Dates/Shipping Tab -->
      <div class="tab-content" v-show="activeTab === 'shipping'">
        <div class="form-grid-3">
          <div class="form-group">
            <label class="form-label">Valid From</label>
            <input type="date" class="form-input" v-model="form.validFrom" />
          </div>
          <div class="form-group">
            <label class="form-label">Valid To</label>
            <input type="date" class="form-input" v-model="form.validTo" />
          </div>
          <div class="form-group">
            <label class="form-label">Req. Deliv. Date</label>
            <input type="date" class="form-input" v-model="form.requestedDeliveryDate" />
          </div>
          <div class="form-group">
            <label class="form-label">Delivering Plant</label>
            <input type="text" class="form-input" v-model="form.deliveringPlant" />
          </div>
          <div class="form-group">
            <label class="form-label">Incoterms</label>
            <input type="text" class="form-input" v-model="form.incoterms" />
          </div>
          <div class="form-group">
            <label class="form-label">Payment Terms</label>
            <input type="text" class="form-input" v-model="form.paymentTerms" />
          </div>
        </div>
      </div>

      <div class="tab-content tab-placeholder" v-show="!['sales','material','shipping'].includes(activeTab)">
        <p>{{ activeTabLabel }} &mdash; content to be developed</p>
      </div>
    </div>

    <!-- Action Bar -->
    <div class="action-bar">
      <div class="action-left">
        <button class="btn btn-primary" @click="handleSave" :disabled="saving">
          <svg viewBox="0 0 20 20" width="16" height="16">
            <path d="M4 16V4a1 1 0 0 1 1-1h8l4 4v9a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1z" fill="none" stroke="currentColor" stroke-width="1.5"/>
            <path d="M13 3v4h4M7 12h6M7 15h4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          {{ saving ? 'Saving...' : 'Save' }}
        </button>
        <button class="btn btn-secondary" @click="handleSaveContinue" :disabled="saving" v-if="!isEdit">
          Save &amp; Continue
        </button>
        <button class="btn btn-outline" @click="convertToQuote" v-if="isEdit && form.status === 'OPEN'">
          Convert to Quote
        </button>
      </div>
      <button class="btn btn-border" @click="handleExit" :disabled="saving">Cancel</button>
    </div>

    <!-- Recent Inquiries -->
    <div class="form-card" style="margin-top: 30px;">
      <h3 class="block-title">Recent Inquiries</h3>
      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Customer</th>
            <th>Date</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="inq in recentInquiries" :key="inq.inquiryId">
            <td class="mono">{{ inq.inquiryId }}</td>
            <td>{{ inq.customerId }}</td>
            <td>{{ inq.createdTime?.split('T')[0] }}</td>
            <td><span class="status-tag">{{ inq.status }}</span></td>
            <td><a class="link-btn" @click="loadInquiry(inq.inquiryId)">Edit</a></td>
          </tr>
        </tbody>
      </table>
    </div>

    <F4SearchModal v-model:visible="showF4" :type="f4Type" @select="onF4Select" />
    <SuccessModal v-model:visible="successVisible" :message="successMsg" @confirm="onSuccessConfirm" />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import F4SearchModal from '@/components/F4SearchModal.vue'
import SuccessModal from '@/components/SuccessModal.vue'
import { alert } from '@/utils/toast'
import { fetchInquiries, fetchInquiryById, createInquiry, updateInquiry, fetchPartners, fetchMaterials } from '@/api'

const router = useRouter()
const route = useRoute()

const loading = ref(false)
const saving = ref(false)
const isEdit = computed(() => !!route.params.id && route.params.id !== 'new')
const activeTab = ref('sales')
const showF4 = ref(false)
const f4Type = ref('partner')
const f4Field = ref('')

const successVisible = ref(false)
const successMsg = ref('')

const partners = ref<any[]>([])
const materials = ref<any[]>([])
const recentInquiries = ref<any[]>([])

const tabs = [
  { key: 'sales', label: 'Sales Data' },
  { key: 'material', label: 'Material Details' },
  { key: 'shipping', label: 'Shipping & Dates' },
  { key: 'texts', label: 'Texts/Notes' },
  { key: 'partners', label: 'Partners' },
]

const activeTabLabel = computed(() => tabs.find(t => t.key === activeTab.value)?.label || '')

const form = reactive({
  inquiryId: '',
  inquiryType: 'IN',
  customerId: '',
  salesOrg: '1000',
  distributionChannel: '10',
  division: '00',
  salesOffice: '100',
  salesGroup: '10',
  currency: 'CNY',
  validFrom: new Date().toISOString().split('T')[0],
  validTo: '',
  requestedDeliveryDate: '',
  deliveringPlant: '1000',
  incoterms: 'EXW',
  paymentTerms: 'Z001',
  status: 'OPEN'
})

const itemForm = reactive({
  materialId: '',
  itemDescription: '',
  orderQuantity: 1,
  expectedOrderValue: 0
})

async function loadMasters() {
  const [bpRes, matRes, inqRes] = await Promise.all([
    fetchPartners({ pageSize: 1000 }),
    fetchMaterials({ pageSize: 1000 }),
    fetchInquiries({ pageSize: 5 })
  ])
  partners.value = bpRes.items || []
  materials.value = matRes.items || []
  recentInquiries.value = inqRes.items || []
}

async function loadInquiry(id: string) {
  loading.value = true
  try {
    const data = await fetchInquiryById(id)
    Object.assign(form, data)
    if (data.items && data.items.length > 0) {
      Object.assign(itemForm, data.items[0])
    }
  } catch (err: any) {
    alert('Failed to load inquiry: ' + err.message)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await loadMasters()
  if (isEdit.value) {
    await loadInquiry(route.params.id as string)
  }
})

async function handleSave() {
  if (!form.customerId || !itemForm.materialId) {
    alert('Please fill in required fields: Customer and Material')
    return
  }
  saving.value = true
  try {
    const cleanForm = Object.fromEntries(
      Object.entries(form).map(([k, v]) => [k, v === '' ? null : v])
    )
    const payload = {
      ...cleanForm,
      inquiryId: form.inquiryId || `INQ${Math.floor(Math.random() * 1000000).toString().padStart(6, '0')}`,
      items: [
        {
          inquiryItemId: `II${Math.floor(Math.random() * 1000000)}`,
          itemNo: 10,
          ...itemForm,
          salesUnit: 'PC'
        }
      ]
    }
    
    if (isEdit.value) {
      await updateInquiry(form.inquiryId, payload)
      successMsg.value = `Inquiry ${form.inquiryId} updated successfully!`
    } else {
      await createInquiry(payload)
      successMsg.value = `Inquiry ${payload.inquiryId} created successfully!`
    }
    successVisible.value = true
  } catch (err: any) {
    alert('Save failed: ' + err.message)
  } finally {
    saving.value = false
  }
}

function handleSaveContinue() {
  handleSave()
}

function onSuccessConfirm() {
  successVisible.value = false
  if (!isEdit.value) {
    router.push('/sales/inquiry')
  }
}

function handleExit() {
  router.push('/sales/inquiry')
}

function convertToQuote() {
  router.push({ path: '/sales/quotation/new', query: { ref: form.inquiryId } })
}

function openF4(field: string) {
  f4Field.value = field
  f4Type.value = field === 'material' ? 'material' : 'partner'
  showF4.value = true
}

function onF4Select(item: any) {
  if (f4Field.value === 'customer') {
    form.customerId = item.bpId
  } else if (f4Field.value === 'material') {
    itemForm.materialId = item.materialId
  }
  showF4.value = false
}
</script>

<style scoped>
.page-container { padding: 32px 40px; max-width: 1200px; margin: 0 auto; }
.page-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px; }
.page-title { font-size: 20px; font-weight: 700; color: #12372A; margin: 0; }
.exit-btn { display: inline-flex; align-items: center; gap: 6px; background: none; border: 1px solid rgba(173,188,159,0.4); border-radius: 8px; padding: 8px 18px; font-size: 13px; color: rgba(18,55,42,0.6); cursor: pointer; transition: all 0.2s; font-family: inherit; }
.exit-btn:hover { border-color: #D9534F; color: #D9534F; background: rgba(217,83,79,0.04); }

.form-card { background: linear-gradient(145deg, #fdfce8, #f7f5d1); border-radius: 14px; padding: 24px; margin-bottom: 20px; border: 1px solid rgba(173, 188, 159, 0.18); box-shadow: 0 2px 6px rgba(173, 188, 159, 0.12); }
.form-card-tabs { padding-top: 0; overflow: hidden; }

.form-row { display: grid; gap: 18px; margin-bottom: 16px; }
.form-row-3 { grid-template-columns: 1fr 1fr 1fr; }
.form-grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; padding: 20px 0; }
.form-grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; padding: 20px 0; }

.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-label { font-size: 12px; font-weight: 600; color: rgba(18, 55, 42, 0.7); letter-spacing: 0.3px; }
.form-label.required::after { content: ' *'; color: #D9534F; font-weight: 700; }
.form-input, .form-select { height: 38px; border: 1px solid rgba(173,188,159,0.4); border-radius: 8px; padding: 0 12px; font-size: 13px; color: #12372A; background: rgba(251, 250, 218, 0.4); font-family: inherit; transition: all 0.2s; outline: none; width: 100%; }
.form-input:focus, .form-select:focus { border-color: #436850; box-shadow: 0 0 0 3px rgba(67, 104, 80, 0.08); background: #fff; }

.input-with-f4 { position: relative; display: flex; gap: 4px; }
.f4-trigger { width: 38px; height: 38px; border: 1px solid rgba(173,188,159,0.4); border-radius: 8px; background: rgba(251, 250, 218, 0.4); cursor: pointer; display: flex; align-items: center; justify-content: center; color: rgba(18,55,42,0.5); }
.f4-trigger:hover { border-color: #436850; color: #436850; background: #fff; }

.input-with-unit { position: relative; display: flex; }
.input-unit { display: flex; align-items: center; padding: 0 12px; background: rgba(173,188,159,0.1); border: 1px solid rgba(173,188,159,0.4); border-left: none; border-radius: 0 8px 8px 0; font-size: 12px; font-weight: 600; color: #436850; }
.input-with-unit .form-input { border-radius: 8px 0 0 8px; }

.tab-bar { display: flex; gap: 0; border-bottom: 1px solid rgba(173,188,159,0.3); margin: 0 -24px; padding: 0 24px; background: rgba(251, 250, 218, 0.3); border-radius: 14px 14px 0 0; }
.tab-btn { padding: 12px 18px; font-size: 12px; font-weight: 500; color: rgba(18, 55, 42, 0.5); background: none; border: none; border-bottom: 2px solid transparent; cursor: pointer; transition: all 0.2s; font-family: inherit; white-space: nowrap; }
.tab-btn.active { color: #436850; font-weight: 600; border-bottom-color: #436850; background: linear-gradient(to bottom, transparent, rgba(67, 104, 80, 0.04)); }

.tab-content { padding-top: 22px; }
.tab-placeholder { display: flex; align-items: center; justify-content: center; min-height: 120px; color: rgba(18,55,42,0.2); font-size: 14px; }

.action-bar { display: flex; align-items: center; justify-content: space-between; padding: 18px 24px; background: linear-gradient(145deg, #fdfce8, #f7f5d1); border-radius: 14px; border: 1px solid rgba(173, 188, 159, 0.18); box-shadow: 0 2px 6px rgba(173, 188, 159, 0.12); }
.action-left { display: flex; gap: 12px; }
.btn { display: inline-flex; align-items: center; gap: 8px; padding: 11px 24px; font-size: 13px; font-weight: 600; border-radius: 8px; cursor: pointer; transition: all 0.2s; font-family: inherit; }
.btn-primary { background: linear-gradient(135deg, #436850, #365440); color: #FBFADA; border: none; }
.btn-secondary { background: none; color: #436850; border: 1px solid #436850; }
.btn-border { background: none; color: rgba(18,55,42,0.5); border: 1px solid rgba(173,188,159,0.4); }

.block-title { font-size: 13px; font-weight: 700; color: #436850; margin-bottom: 14px; display: flex; align-items: center; gap: 8px; }
.block-title::before { content: ''; width: 4px; height: 14px; background: #436850; border-radius: 2px; display: inline-block; }

.data-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.data-table th { text-align: left; padding: 12px; font-size: 11px; color: rgba(18, 55, 42, 0.4); text-transform: uppercase; border-bottom: 1px solid rgba(173,188,159,0.2); }
.data-table td { padding: 12px; color: #12372A; border-bottom: 1px solid rgba(173,188,159,0.08); }
.mono { font-family: monospace; }
.status-tag { background: rgba(67, 104, 80, 0.1); color: #436850; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; }
.link-btn { color: #436850; cursor: pointer; font-weight: 600; }
.link-btn:hover { text-decoration: underline; }
</style>
