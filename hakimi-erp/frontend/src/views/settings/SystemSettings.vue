<template>
  <MainLayout>
    <div class="page">
      <div class="header-card">
        <div class="hc-left">
          <div class="hc-icon"><svg viewBox="0 0 24 24" width="22" height="22"><circle cx="12" cy="12" r="3" fill="none" stroke="#436850" stroke-width="1.8"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" fill="none" stroke="#436850" stroke-width="1.8"/></svg></div>
          <div class="hc-text"><h2 class="hc-title">System Settings</h2><p class="hc-sub">Configure global system parameters and preferences.</p></div>
        </div>
      </div>

      <div class="settings-grid">
        <div class="settings-card">
          <h3 class="sc-title">Company Information</h3>
          <div class="form-row form-row-2">
            <div class="form-group">
              <label class="form-label">Company Name</label>
              <input type="text" class="form-input" v-model="settings.companyName" placeholder="HAKIMI Corporation" />
            </div>
            <div class="form-group">
              <label class="form-label">Short Name</label>
              <input type="text" class="form-input" v-model="settings.shortName" placeholder="HAKIMI" />
            </div>
          </div>
          <div class="form-row form-row-2">
            <div class="form-group">
              <label class="form-label">Tax ID / VAT No.</label>
              <input type="text" class="form-input" v-model="settings.taxId" placeholder="Enter tax identification number" />
            </div>
            <div class="form-group">
              <label class="form-label">Registration No.</label>
              <input type="text" class="form-input" v-model="settings.regNo" placeholder="Enter registration number" />
            </div>
          </div>
        </div>

        <div class="settings-card">
          <h3 class="sc-title">Regional Settings</h3>
          <div class="form-row form-row-2">
            <div class="form-group">
              <label class="form-label">Default Currency</label>
              <select class="form-select" v-model="settings.currency">
                <option value="USD">USD - US Dollar</option>
                <option value="EUR">EUR - Euro</option>
                <option value="CNY">CNY - Chinese Yuan</option>
                <option value="JPY">JPY - Japanese Yen</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Date Format</label>
              <select class="form-select" v-model="settings.dateFormat">
                <option value="YYYY-MM-DD">YYYY-MM-DD (ISO)</option>
                <option value="DD/MM/YYYY">DD/MM/YYYY (EU)</option>
                <option value="MM/DD/YYYY">MM/DD/YYYY (US)</option>
              </select>
            </div>
          </div>
          <div class="form-row form-row-2">
            <div class="form-group">
              <label class="form-label">Language</label>
              <select class="form-select" v-model="settings.language">
                <option value="en">English</option>
                <option value="zh">中文 (Chinese)</option>
                <option value="de">Deutsch (German)</option>
                <option value="ja">日本語 (Japanese)</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Timezone</label>
              <select class="form-select" v-model="settings.timezone">
                <option value="Asia/Shanghai">Asia/Shanghai (UTC+8)</option>
                <option value="America/New_York">America/New_York (UTC-5)</option>
                <option value="Europe/Berlin">Europe/Berlin (UTC+1)</option>
                <option value="Asia/Tokyo">Asia/Tokyo (UTC+9)</option>
              </select>
            </div>
          </div>
        </div>

        <div class="settings-card">
          <h3 class="sc-title">Document Numbering</h3>
          <div class="form-row form-row-2">
            <div class="form-group">
              <label class="form-label">Sales Order Prefix</label>
              <input type="text" class="form-input" v-model="settings.soPrefix" placeholder="SO" />
            </div>
            <div class="form-group">
              <label class="form-label">Quotation Prefix</label>
              <input type="text" class="form-input" v-model="settings.qtPrefix" placeholder="QT" />
            </div>
          </div>
          <div class="form-row form-row-2">
            <div class="form-group">
              <label class="form-label">Invoice Prefix</label>
              <input type="text" class="form-input" v-model="settings.invPrefix" placeholder="INV" />
            </div>
            <div class="form-group">
              <label class="form-label">Delivery Prefix</label>
              <input type="text" class="form-input" v-model="settings.dlPrefix" placeholder="DL" />
            </div>
          </div>
        </div>

        <div class="settings-card">
          <h3 class="sc-title">System Preferences</h3>
          <div class="form-row form-row-2">
            <div class="form-group">
              <label class="form-label">Session Timeout (minutes)</label>
              <input type="number" class="form-input" v-model="settings.sessionTimeout" min="5" max="480" />
            </div>
            <div class="form-group">
              <label class="form-label">Rows per Page</label>
              <select class="form-select" v-model="settings.rowsPerPage">
                <option value="20">20</option>
                <option value="50">50</option>
                <option value="100">100</option>
              </select>
            </div>
          </div>
          <div class="form-row form-row-2">
            <div class="form-group">
              <label class="form-label">Decimal Places</label>
              <select class="form-select" v-model="settings.decimalPlaces">
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Theme</label>
              <select class="form-select" v-model="settings.theme">
                <option value="light">Light</option>
                <option value="dark">Dark</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <div class="action-bar">
        <div class="action-left">
          <button class="btn btn-primary" @click="saveSettings">Save Settings</button>
          <button class="btn btn-secondary" @click="resetSettings">Reset</button>
        </div>
        <span class="action-status" v-if="saved">✓ Settings saved successfully!</span>
      </div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue"
import MainLayout from "@/layout/MainLayout.vue"

const saved = ref(false)

const settings = reactive({
  companyName:"HAKIMI Corporation",
  shortName:"HAKIMI",
  taxId:"TAX-2026-001",
  regNo:"REG-HAK-2026",
  currency:"CNY",
  dateFormat:"YYYY-MM-DD",
  language:"en",
  timezone:"Asia/Shanghai",
  soPrefix:"SO",
  qtPrefix:"QT",
  invPrefix:"INV",
  dlPrefix:"DL",
  sessionTimeout:30,
  rowsPerPage:"50",
  decimalPlaces:"2",
  theme:"light",
})

function saveSettings(){
  saved.value=true
  setTimeout(()=>saved.value=false,3000)
}
function resetSettings(){
  if(confirm("Reset all settings to defaults?")){
    settings.companyName="HAKIMI Corporation";settings.shortName="HAKIMI"
    settings.taxId="TAX-2026-001";settings.regNo="REG-HAK-2026"
    settings.currency="CNY";settings.dateFormat="YYYY-MM-DD"
    settings.language="en";settings.timezone="Asia/Shanghai"
    settings.soPrefix="SO";settings.qtPrefix="QT"
    settings.invPrefix="INV";settings.dlPrefix="DL"
    settings.sessionTimeout=30;settings.rowsPerPage="50"
    settings.decimalPlaces="2";settings.theme="light"
  }
}
</script>

<style scoped>
.page{padding:28px 36px;max-width:1000px;margin:0 auto;}
.header-card{display:flex;align-items:center;background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:16px;padding:20px 24px;border:1px solid rgba(173,188,159,0.18);box-shadow:0 2px 8px rgba(173,188,159,0.12);margin-bottom:20px;}
.hc-left{display:flex;align-items:center;gap:14px;}
.hc-icon{width:44px;height:44px;border-radius:12px;background:rgba(67,104,80,0.08);display:flex;align-items:center;justify-content:center;}
.hc-title{font-size:18px;font-weight:800;color:#12372A;margin:0;}
.hc-sub{font-size:12px;color:rgba(18,55,42,0.45);margin:2px 0 0;}

.settings-grid{display:flex;flex-direction:column;gap:16px;margin-bottom:20px;}
.settings-card{background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:14px;padding:22px 24px;border:1px solid rgba(173,188,159,0.15);box-shadow:0 2px 6px rgba(173,188,159,0.08);}
.sc-title{font-size:14px;font-weight:700;color:#436850;margin:0 0 16px;padding-bottom:10px;border-bottom:1px solid rgba(173,188,159,0.2);display:flex;align-items:center;gap:8px;}
.sc-title::before{content:"";width:3px;height:14px;background:#436850;border-radius:2px;}

.form-row{display:grid;gap:14px;margin-bottom:14px;}
.form-row:last-child{margin-bottom:0;}
.form-row-2{grid-template-columns:1fr 1fr;}
.form-group{display:flex;flex-direction:column;gap:6px;}
.form-label{font-size:12px;font-weight:600;color:rgba(18,55,42,0.55);}
.form-input,.form-select{height:38px;border:1px solid rgba(173,188,159,0.4);border-radius:8px;padding:0 12px;font-size:13px;color:#12372A;background:rgba(251,250,218,0.35);font-family:inherit;outline:none;transition:all 0.2s;}
.form-input:focus,.form-select:focus{border-color:#436850;box-shadow:0 0 0 3px rgba(67,104,80,0.06);}
.form-select{cursor:pointer;appearance:none;background-image:url("data:image/svg+xml,%3Csvg viewBox=\"0 0 20 20\" width=\"12\" height=\"12\" xmlns=\"http://www.w3.org/2000/svg\"%3E%3Cpath d=\"M5 7l5 5 5-5\" fill=\"none\" stroke=\"%2312372A\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\" opacity=\"0.4\"/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 10px center;padding-right:32px;}

.action-bar{display:flex;align-items:center;justify-content:space-between;padding:18px 24px;background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:14px;border:1px solid rgba(173,188,159,0.18);box-shadow:0 2px 6px rgba(173,188,159,0.12);}
.action-left{display:flex;gap:12px;}
.action-status{font-size:13px;color:#436850;font-weight:600;}
.btn{display:inline-flex;align-items:center;gap:8px;padding:11px 24px;font-size:13px;font-weight:600;border-radius:8px;cursor:pointer;transition:all 0.2s;font-family:inherit;}
.btn-primary{background:linear-gradient(135deg,#436850,#365440);color:#FBFADA;border:none;box-shadow:0 2px 8px rgba(67,104,80,0.25);}
.btn-primary:hover{transform:translateY(-1px);box-shadow:0 4px 16px rgba(67,104,80,0.3);}
.btn-secondary{background:rgba(173,188,159,0.2);color:#436850;border:1px solid rgba(173,188,159,0.35);}
.btn-secondary:hover{background:rgba(173,188,159,0.3);}
</style>
