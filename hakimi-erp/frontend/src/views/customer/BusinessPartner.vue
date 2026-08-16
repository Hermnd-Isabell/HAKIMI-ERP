<template>
  <div class="bp-page">
    <!-- Header -->
    <div class="header-card">
      <div class="hc-left">
        <div class="hc-icon">
          <svg viewBox="0 0 24 24" width="22" height="22"><circle cx="12" cy="7" r="4" fill="none" stroke="#436850" stroke-width="1.8"/><path d="M4 21v-2a4 4 0 0 1 4-4h8a4 4 0 0 1 4 4v2" fill="none" stroke="#436850" stroke-width="1.8" stroke-linecap="round"/></svg>
        </div>
        <div class="hc-text">
          <h2 class="hc-title">Business Partner Master</h2>
          <p class="hc-sub">Create and manage customers and vendors across the organization.</p>
        </div>
      </div>
      <div class="hc-right">
      </div>
    </div>

    <!-- Top Form Row -->
      <div class="form-card">
        <div class="form-row form-row-3">
          <div class="form-group">
            <label class="form-label">Business Partner No.</label>
            <input type="text" class="form-input" v-model="form.bpId" placeholder="Auto-generated if empty" />
          </div>
          <div class="form-group">
            <label class="form-label">Grouping</label>
            <div class="input-with-f4-inline">
              <select class="form-select" v-model="form.grouping">
                <option value="">Select grouping</option>
                <option value="EXT">External</option>
                <option value="INT">Internal</option>
              </select>
              <button class="f4-trigger-sm" @click="openF4('grouping')" title="F4 Search">
                <svg viewBox="0 0 20 20" width="14" height="14"><circle cx="9" cy="9" r="5.5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M13 13l4 4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
              </button>
            </div>
          </div>
          <div class="form-group">
            <label class="form-label required">BP Role</label>
            <select class="form-select" v-model="form.bpRole">
              <option value="">Select role</option>
              <option value="FLCU01">Customer (FLCU01)</option>
              <option value="FLVN00">Vendor (FLVN00)</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="form-card form-card-tabs">
        <div class="tab-bar">
          <button
            v-for="tab in tabs" :key="tab.key"
            class="tab-btn" :class="{ active: activeTab === tab.key }"
            @click="switchTab(tab.key)"
          >{{ tab.label }}</button>
        </div>

        <!-- Address Tab -->
        <div class="tab-content" v-show="activeTab === 'address'">
          <fieldset class="fieldset-block">
            <legend class="block-title">Basic Information</legend>
            <div class="form-row form-row-4">
              <div class="form-group">
                <label class="form-label">Salutation</label>
                <select class="form-select" v-model="form.salutation">
                  <option value="">Select</option>
                  <option value="MR">Mr.</option>
                  <option value="MS">Ms.</option>
                  <option value="MRS">Mrs.</option>
                  <option value="DR">Dr.</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label required">Last Name</label>
                <input type="text" class="form-input" v-model="form.lastName" placeholder="Enter last name" />
              </div>
              <div class="form-group">
                <label class="form-label required">First Name</label>
                <input type="text" class="form-input" v-model="form.firstName" placeholder="Enter first name" />
              </div>
              <div class="form-group">
                <label class="form-label">Search Term</label>
                <input type="text" class="form-input" v-model="form.searchTerm" placeholder="Quick search keyword" />
              </div>
            </div>
          </fieldset>

          <fieldset class="fieldset-block">
            <legend class="block-title">Standard Address</legend>
            <div class="form-row form-row-2">
              <div class="form-group">
                <label class="form-label">Street</label>
                <input type="text" class="form-input" v-model="form.street" placeholder="Street name" />
              </div>
              <div class="form-group">
                <label class="form-label">House No.</label>
                <input type="text" class="form-input" v-model="form.houseNumber" placeholder="House number" />
              </div>
            </div>
            <div class="form-row form-row-3">
              <div class="form-group">
                <label class="form-label required">Country / Region</label>
                <select class="form-select" v-model="form.country">
                  <option value="">Select country</option>
                  <option value="CN">China</option>
                  <option value="US">United States</option>
                  <option value="DE">Germany</option>
                  <option value="JP">Japan</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label required">City</label>
                <input type="text" class="form-input" v-model="form.city" placeholder="Enter city" />
              </div>
              <div class="form-group">
                <label class="form-label required">Postal Code</label>
                <div class="input-with-indicator">
                  <input
                    type="text" class="form-input postal-input"
                    v-model="form.postalCode"
                    @input="validatePostalCode"
                    placeholder="e.g. 100080"
                  />
                  <div class="postal-indicator" v-if="form.postalCode">
                    <div class="indicator-bar" :class="postalStatus"></div>
                    <span class="indicator-label">{{ postalLabel }}</span>
                  </div>
                </div>
              </div>
            </div>
          </fieldset>
        </div>

        <!-- Address Overview Tab -->
        <div class="tab-content" v-show="activeTab === 'address_overview'">
          <div class="overview-grid">
            <div class="overview-item">
              <span class="ov-label">Main Address</span>
              <div class="ov-value">
                <p v-if="form.street || form.city">{{ form.street }} {{ form.houseNumber }}</p>
                <p v-if="form.city || form.country">{{ form.postalCode }} {{ form.city }}, {{ form.country }}</p>
                <p v-else class="text-muted">No address information entered yet.</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Identification Tab -->
        <div class="tab-content" v-show="activeTab === 'identification'">
          <fieldset class="fieldset-block">
            <legend class="block-title">Tax Numbers</legend>
            <div class="form-row form-row-2">
              <div class="form-group">
                <label class="form-label">Tax ID 1 (VAT)</label>
                <input type="text" class="form-input" v-model="form.taxId1" placeholder="Enter Tax ID" />
              </div>
              <div class="form-group">
                <label class="form-label">Tax ID 2</label>
                <input type="text" class="form-input" v-model="form.taxId2" placeholder="Enter Tax ID" />
              </div>
            </div>
          </fieldset>
          <fieldset class="fieldset-block">
            <legend class="block-title">ID Numbers</legend>
            <div class="form-row form-row-2">
              <div class="form-group">
                <label class="form-label">ID Type</label>
                <select class="form-select" v-model="form.idType">
                  <option value="">Select ID Type</option>
                  <option value="CRM001">Business Registration</option>
                  <option value="CRM002">Passport</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">ID Number</label>
                <input type="text" class="form-input" v-model="form.idNumber" />
              </div>
            </div>
          </fieldset>
        </div>

        <div class="tab-content tab-placeholder" v-show="!['address', 'address_overview', 'identification'].includes(activeTab)">
          <p>{{ activeTabLabel }} &mdash; content to be developed</p>
        </div>
      </div>

      <!-- Business Partner List -->
      <div class="form-card">
        <h3 class="block-title">Business Partner List</h3>
        <div v-if="error" class="error-msg">{{ error }}</div>
        <table class="bp-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Role</th>
              <th>Country</th>
              <th>City</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="6" class="loading-cell">Loading business partners...</td>
            </tr>
            <template v-else>
              <tr v-for="bp in partners" :key="bp.bpId" class="clickable-row" @click="editPartner(bp)">
                <td class="mono">{{ bp.bpId }}</td>
                <td>{{ bp.bpName }}</td>
                <td>{{ bp.bpRole }}</td>
                <td>{{ bp.country }}</td>
                <td>{{ bp.city }}</td>
                <td><span class="status-tag">{{ bp.status }}</span></td>
              </tr>
              <tr v-if="partners.length === 0">
                <td colspan="6" class="empty-cell">No business partners found.</td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>

      <!-- Bottom Action Bar -->
      <div class="action-bar">
        <div class="action-left">
          <button class="btn btn-primary" @click="handleSave" :disabled="saving">
            <svg viewBox="0 0 20 20" width="16" height="16">
              <path d="M4 16V4a1 1 0 0 1 1-1h8l4 4v9a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1z" fill="none" stroke="currentColor" stroke-width="1.5"/>
              <path d="M13 3v4h4M7 12h6M7 15h4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            {{ saving ? 'Saving...' : 'Save' }}
          </button>
          <button class="btn btn-secondary" @click="handleSaveContinue" :disabled="saving">
            Save &amp; Continue
          </button>
        </div>
        <button class="btn btn-border" @click="handleCancel" :disabled="saving">Cancel</button>
      </div>

      <F4SearchModal v-model:visible="showF4" @confirm="onF4Confirm" />
      <SuccessModal v-model:visible="successVisible" :message="successMsg" @confirm="handleSuccessConfirm" />
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import F4SearchModal from '@/components/F4SearchModal.vue'
import SuccessModal from '@/components/SuccessModal.vue'
import { alert } from '@/utils/toast'
import { fetchPartners, createPartner } from '@/api'

const router = useRouter()
const successVisible = ref(false)
const successMsg = ref('')
const loading = ref(false)
const saving = ref(false)
const error = ref('')
const partners = ref<any[]>([])
const activeTab = ref('address')
const postalStatus = ref('')
const postalLabel = ref('')

const form = reactive({
  bpId: '',
  grouping: '',
  bpRole: '',
  salutation: '',
  lastName: '',
  firstName: '',
  searchTerm: '',
  street: '',
  houseNumber: '',
  country: '',
  city: '',
  district: '',
  postalCode: '',
  status: 'ACTIVE'
})

const tabs = [
  { key: 'address', label: 'Address' },
  { key: 'address_overview', label: 'Address Overview' },
  { key: 'identification', label: 'Identification' },
  { key: 'control', label: 'Control Data' },
  { key: 'payment', label: 'Payment Transactions' },
  { key: 'status', label: 'Status' },
  { key: 'technical', label: 'Technical ID' },
]

const activeTabLabel = computed(() => tabs.find(t => t.key === activeTab.value)?.label || '')

async function loadPartners() {
  loading.value = true
  error.value = ''
  try {
    const data = await fetchPartners()
    partners.value = data.items || []
  } catch (err: any) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

async function handleSave() {
  // 严格检查字段，确保名字和 form reactive 中的完全一致
  if (!form.bpRole || !form.lastName || !form.firstName || !form.city || !form.country || !form.postalCode) {
    alert('Please fill in required fields: Role, Names, Country, City, Postal Code')
    return
  }
  saving.value = true
  try {
    const payload = {
      ...form,
      bpId: form.bpId || `BP${Math.floor(Math.random() * 1000000).toString().padStart(6, '0')}`,
      bpName: `${form.lastName} ${form.firstName}`.trim(),
      bpType: form.grouping === 'INT' ? 'PERS' : 'ORG'
    }
    const data = await createPartner(payload)
    successMsg.value = `Business Partner ${data.bpId} created successfully!`
    successVisible.value = true
    await loadPartners()
    resetForm()
  } catch (err: any) {
    alert('Save failed: ' + err.message)
  } finally {
    saving.value = false
  }
}

function resetForm() {
  Object.assign(form, {
    bpId: '', grouping: '', bpRole: '', salutation: '',
    lastName: '', firstName: '', searchTerm: '', street: '',
    houseNumber: '', country: '', city: '', district: '',
    postalCode: '', status: 'ACTIVE'
  })
}

function validatePostalCode() {
  const v = form.postalCode.trim()
  if (!v) { postalStatus.value = ''; postalLabel.value = ''; return }
  postalStatus.value = v.length === 6 ? 'ok' : 'error'
  postalLabel.value = v.length === 6 ? 'Available' : 'Format Error'
}

const showF4 = ref(false)
const f4Field = ref('')
function openF4(field: string) { f4Field.value = field; showF4.value = true }
function onF4Confirm() { showF4.value = false }
function switchTab(key: string) { activeTab.value = key }
function handleSuccessConfirm() { successVisible.value = false }
function handleSaveContinue() { handleSave() }
function handleCancel() { router.push('/') }
function handleExit() { router.push('/') }

function editPartner(bp: any) {
  Object.assign(form, {
    bpId: bp.bpId,
    grouping: bp.bpType === 'PERS' ? 'INT' : 'EXT',
    bpRole: bp.bpRole,
    lastName: bp.bpName?.split(' ')[0] || '',
    firstName: bp.bpName?.split(' ').slice(1).join(' ') || '',
    country: bp.country,
    city: bp.city,
    postalCode: bp.postalCode || '',
    status: bp.status || 'ACTIVE'
  })
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(loadPartners)
</script>

<style scoped>
.bp-page { padding: 32px 40px; max-width: 1200px; margin: 0 auto; }
.page-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px; }
.page-title { font-size: 20px; font-weight: 700; color: #12372A; margin: 0; }
.exit-btn { display: inline-flex; align-items: center; gap: 6px; background: none; border: 1px solid rgba(173,188,159,0.4); border-radius: 8px; padding: 8px 18px; font-size: 13px; color: rgba(18,55,42,0.6); cursor: pointer; transition: all 0.2s; font-family: inherit; }
.exit-btn:hover { border-color: #D9534F; color: #D9534F; background: rgba(217,83,79,0.04); }
.form-card { background: linear-gradient(145deg, #fdfce8, #f7f5d1); border-radius: 14px; padding: 24px; margin-bottom: 20px; border: 1px solid rgba(173, 188, 159, 0.18); box-shadow: 0 2px 6px rgba(173, 188, 159, 0.12); }
.form-card-tabs { padding-top: 0; overflow: hidden; }
.form-row { display: grid; gap: 18px; margin-bottom: 16px; }
.form-row-2 { grid-template-columns: 1fr 1fr; }
.form-row-3 { grid-template-columns: 1fr 1fr 1fr; }
.form-row-4 { grid-template-columns: 1fr 1fr 1fr 1fr; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-label { font-size: 12px; font-weight: 600; color: rgba(18, 55, 42, 0.7); letter-spacing: 0.3px; }
.form-label.required::after { content: ' *'; color: #D9534F; font-weight: 700; }
.form-input, .form-select { height: 38px; border: 1px solid rgba(173, 188, 159, 0.4); border-radius: 8px; padding: 0 12px; font-size: 13px; color: #12372A; background: rgba(251, 250, 218, 0.4); font-family: inherit; transition: all 0.2s; outline: none; width: 100%; }
.form-input:focus, .form-select:focus { border-color: #436850; box-shadow: 0 0 0 3px rgba(67, 104, 80, 0.08); background: #fff; }
.postal-input { padding-right: 80px !important; }
.form-select { cursor: pointer; appearance: none; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 20 20' width='12' height='12' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M5 7l5 5 5-5' fill='none' stroke='%2312372A' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round' opacity='0.4'/%3E%3C/svg%3E"); background-repeat: no-repeat; background-position: right 10px center; padding-right: 32px; }
.input-with-f4-inline { display: flex; align-items: center; gap: 0; }
.input-with-f4-inline .form-select { border-radius: 8px 0 0 8px; }
.f4-trigger-sm { width: 32px; height: 38px; border: 1px solid rgba(173,188,159,0.4); border-left: none; border-radius: 0 8px 8px 0; background: rgba(67,104,80,0.06); color: #436850; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.f4-trigger-sm:hover { background: rgba(67,104,80,0.12); }
.input-with-indicator { position: relative; }
.postal-indicator { position: absolute; right: 8px; top: 50%; transform: translateY(-50%); display: flex; align-items: center; gap: 6px; }
.indicator-label { font-size: 10px; font-weight: 700; color: rgba(18, 55, 42, 0.4); text-transform: uppercase; }
.indicator-bar { width: 4px; height: 16px; border-radius: 2px; transition: background 0.3s; background: rgba(173, 188, 159, 0.3); }
.indicator-bar.ok { background: #436850; }
.indicator-bar.error { background: #D9534F; }
.tab-bar { display: flex; gap: 0; border-bottom: 1px solid rgba(173, 188, 159, 0.3); margin: 0 -24px; padding: 0 24px; background: rgba(251, 250, 218, 0.3); border-radius: 14px 14px 0 0; }
.tab-btn { padding: 12px 18px; font-size: 12px; font-weight: 500; color: rgba(18, 55, 42, 0.5); background: none; border: none; border-bottom: 2px solid transparent; cursor: pointer; transition: all 0.2s; font-family: inherit; white-space: nowrap; }
.tab-btn.active { color: #436850; font-weight: 600; border-bottom-color: #436850; background: linear-gradient(to bottom, transparent, rgba(67, 104, 80, 0.04)); }
.tab-content { padding-top: 22px; }
.fieldset-block { border: none; padding: 0; margin: 0 0 22px; border-bottom: 1px solid rgba(173, 188, 159, 0.15); padding-bottom: 18px; }
.block-title { font-size: 13px; font-weight: 700; color: #436850; margin-bottom: 14px; display: flex; align-items: center; gap: 8px; }
.block-title::before { content: ''; width: 4px; height: 14px; background: #436850; border-radius: 2px; display: inline-block; }
.overview-grid { display: grid; gap: 16px; }
.overview-item { background: rgba(255, 255, 255, 0.3); padding: 16px; border-radius: 10px; border: 1px solid rgba(173, 188, 159, 0.2); }
.ov-label { font-size: 11px; font-weight: 700; color: rgba(18, 55, 42, 0.4); text-transform: uppercase; margin-bottom: 8px; display: block; }
.ov-value p { margin: 0; font-size: 14px; color: #12372A; line-height: 1.5; }
.text-muted { color: rgba(18, 55, 42, 0.4); font-style: italic; }
.action-bar { display: flex; align-items: center; justify-content: space-between; padding: 18px 24px; background: linear-gradient(145deg, #fdfce8, #f7f5d1); border-radius: 14px; border: 1px solid rgba(173, 188, 159, 0.18); box-shadow: 0 2px 6px rgba(173, 188, 159, 0.12); }
.action-left { display: flex; gap: 12px; }
.btn { display: inline-flex; align-items: center; gap: 8px; padding: 11px 24px; font-size: 13px; font-weight: 600; border-radius: 8px; cursor: pointer; transition: all 0.2s; font-family: inherit; }
.btn-primary { background: linear-gradient(135deg, #436850, #365440); color: #FBFADA; border: none; }
.bp-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
.bp-table th { text-align: left; padding: 12px; font-size: 11px; color: rgba(18, 55, 42, 0.4); text-transform: uppercase; border-bottom: 1px solid rgba(173, 188, 159, 0.2); }
.bp-table td { padding: 12px; font-size: 13px; color: #12372A; border-bottom: 1px solid rgba(173, 188, 159, 0.08); }
.clickable-row { cursor: pointer; transition: background 0.2s; }
.clickable-row:hover { background: rgba(67, 104, 80, 0.04); }
.mono { font-family: monospace; }
.status-tag { background: rgba(67, 104, 80, 0.1); color: #436850; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; }
.error-msg { color: #D9534F; font-size: 13px; padding: 10px 12px; background: rgba(217, 83, 79, 0.08); border-radius: 8px; margin-bottom: 12px; }
</style>
