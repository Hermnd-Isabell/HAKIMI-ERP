<template>
  <div class="page">
    <div class="header-card">
        <div class="hc-left">
          <div class="hc-icon"><svg viewBox="0 0 24 24" width="22" height="22"><rect x="3" y="3" width="8" height="8" rx="1.5" fill="none" stroke="#436850" stroke-width="1.8"/><rect x="13" y="3" width="8" height="8" rx="1.5" fill="none" stroke="#436850" stroke-width="1.8"/><rect x="3" y="13" width="8" height="8" rx="1.5" fill="none" stroke="#436850" stroke-width="1.8"/><rect x="13" y="13" width="8" height="8" rx="1.5" fill="none" stroke="#436850" stroke-width="1.8"/></svg></div>
          <div class="hc-text"><h2 class="hc-title">Material Master</h2><p class="hc-sub">Create and manage material master records across all organizational levels.</p></div>
        </div>
      </div>

      <!-- Form with F4 Search -->
      <div class="form-card">
        <div class="form-row form-row-4">
          <div class="form-group"><label class="fl">Material No.</label><input class="fi" v-model="form.materialId" placeholder="Input ID or leave for random" /></div>
          <div class="form-group"><label class="fl required">Material Type</label>
            <div class="input-with-f4-inline"><select class="fs" v-model="form.materialType"><option value="FERT">FERT - Finished Product</option><option value="ROH">ROH - Raw Material</option><option value="HAWA">HAWA - Trading Goods</option><option value="HALB">HALB - Semi-Finished</option></select><button class="f4-trigger-sm" @click="openF4(`matType`)" title="F4 Search"><svg viewBox="0 0 20 20" width="12" height="12"><circle cx="8" cy="8" r="5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M12 12l5 5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button></div>
          </div>
          <div class="form-group"><label class="fl required">Industry Sector</label>
            <div class="input-with-f4-inline"><select class="fs" v-model="form.industrySector"><option value="M">M - Mechanical Engineering</option><option value="C">C - Chemical Industry</option><option value="E">E - Electrical</option></select><button class="f4-trigger-sm" @click="openF4(`industry`)" title="F4 Search"><svg viewBox="0 0 20 20" width="12" height="12"><circle cx="8" cy="8" r="5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M12 12l5 5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button></div>
          </div>
          <div class="form-group"><label class="fl required">Base UoM</label><select class="fs" v-model="form.baseUnit"><option value="EA">EA - Each</option><option value="KG">KG - Kilogram</option><option value="M">M - Meter</option><option value="L">L - Liter</option></select></div>
        </div>
      </div>

      <div class="form-card form-card-tabs">
        <div class="tab-bar">
          <button v-for="t in tabs" :key="t" class="tab-btn" :class="{active:active===t}" @click="active=t">{{ t }}</button>
        </div>
        <div class="tab-content" v-show="active===`Basic Data`">
          <fieldset class="fb"><legend class="bt">General Data</legend>
            <div class="form-row form-row-4">
              <div class="form-group"><label class="fl required">Material Desc.</label><input class="fi" v-model="form.materialName" placeholder="e.g. Industrial Sensor X200" /></div>
              <div class="form-group"><label class="fl">Old Material No.</label><input class="fi" v-model="form.oldMaterialNo" placeholder="Legacy system ID" /></div>
              <div class="form-group"><label class="fl">Material Group</label>
                <div class="input-with-f4-inline"><select class="fs" v-model="form.materialGroup"><option value="01">01 - Electronics</option><option value="02">02 - Mechanical</option></select><button class="f4-trigger-sm" @click="openF4(`matGroup`)" title="F4 Search"><svg viewBox="0 0 20 20" width="12" height="12"><circle cx="8" cy="8" r="5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M12 12l5 5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button></div>
              </div>
              <div class="form-group"><label class="fl">Division</label><select class="fs" v-model="form.division"><option value="10">10 - Standard</option><option value="20">20 - Special</option></select></div>
            </div>
          </fieldset>
          <fieldset class="fb"><legend class="bt">Dimensions</legend>
            <div class="form-row form-row-4">
              <div class="form-group"><label class="fl">Gross Weight</label><div class="iu"><input class="fi" v-model="form.weight" placeholder="0.000" /><span class="uu">KG</span></div></div>
              <div class="form-group"><label class="fl">Net Weight</label><div class="iu"><input class="fi" v-model="form.weight" placeholder="0.000" /><span class="uu">KG</span></div></div>
              <div class="form-group"><label class="fl">Weight Unit</label><select class="fs" v-model="form.weightUnit"><option value="KG">KG</option><option value="LB">LB</option></select></div>
              <div class="form-group"><label class="fl">Volume</label><div class="iu"><input class="fi" v-model="form.volume" placeholder="0.000" /><span class="uu">M3</span></div></div>
            </div>
          </fieldset>
        </div>
        <div class="tab-placeholder" v-show="active!==`Basic Data`"><p>{{ active }} &mdash; content to be developed</p></div>
      </div>

      <div class="data-card">
        <h3 class="sc-title">Material List</h3>
        <table class="dt"><thead><tr><th>Material</th><th>Description</th><th>Type</th><th>UoM</th><th>Group</th><th>Status</th><th>Action</th></tr></thead>
          <tbody>
            <tr v-if="loading"><td colspan="7" style="text-align:center;padding:20px;color:#999">Loading materials...</td></tr>
            <tr v-for="m in mats" :key="m.id" class="dr"><td class="mono">{{ m.id }}</td><td>{{ m.desc }}</td><td>{{ m.type }}</td><td>{{ m.uom }}</td><td>{{ m.grp }}</td><td><span class="stag s-done">{{ m.st }}</span></td><td><a class="link" @click="viewDetail(m.id)">Edit</a></td></tr>
            <tr v-if="!loading && mats.length === 0"><td colspan="7" style="text-align:center;padding:20px;color:#999">No materials found.</td></tr>
          </tbody>
        </table>
      </div>

      <div class="action-bar">
        <button class="btn btn-primary" @click="saveMaterial" :disabled="saving">{{ saving ? 'Saving...' : 'Save' }}</button>
        <button class="btn btn-secondary" @click="saveMaterial(true)">Save &amp; Continue</button>
        <button class="btn btn-outline" @click="$router.push(`/`)">Cancel</button>
      </div>

      <F4SearchModal :visible="f4Visible" :title="f4Title" @update:visible="f4Visible=$event" @confirm="onF4Confirm" />
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue"
import F4SearchModal from "@/components/F4SearchModal.vue"
import { fetchMaterials, createMaterial } from "@/api"

const active=ref("Basic Data")
const tabs=["Basic Data","Sales Data","Purchasing","MRP","Accounting","Storage","Quality"]
const loading = ref(false)
const saving = ref(false)

const form=reactive({
  materialId: "",
  materialType: "FERT",
  industrySector: "M",
  baseUnit: "EA",
  materialName: "",
  oldMaterialNo: "",
  materialGroup: "01",
  division: "10",
  weight: "",
  weightUnit: "KG",
  volume: "",
  volumeUnit: "M3",
  searchTerm: ""
})

const mats = ref<any[]>([])

async function loadMaterials() {
  loading.value = true
  try {
    const data = await fetchMaterials({ limit: 1000 })
    mats.value = (data.items || []).map((item: any) => ({
      id: item.materialId,
      desc: item.materialName,
      type: item.materialType || 'N/A',
      uom: item.baseUnit,
      grp: item.materialGroup || "N/A",
      st: "Active"
    }))
  } catch (err) {
    console.error("Failed to fetch materials:", err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadMaterials()
})

// F4 Search
const f4Visible=ref(false)
const f4Title=ref("Search Help")
function openF4(ctx:string){
  const titles:Record<string,string>={matType:"Material Type (1)",industry:"Industry Sector (1)",matGroup:"Material Group (1)"}
  f4Title.value=titles[ctx]||"Search Help (1)"
  f4Visible.value=true
}
function onF4Confirm(idx:number){f4Visible.value=false;alert(`F4 selection confirmed at index ${idx}`)}

async function saveMaterial(cont = false){
  if (!form.materialName) { alert("Please enter material description"); return }
  saving.value = true
  try {
    const payload = {
      ...form,
      materialId: form.materialId || `M${Math.floor(Math.random() * 1000000).toString().padStart(6, '0')}`,
      description: form.materialName,
      weight: parseFloat(form.weight) || 0,
      volume: parseFloat(form.volume) || 0,
      standardPrice: 0
    }
    await createMaterial(payload)
    alert("Material saved successfully!")
    if (!cont) {
      resetForm()
    }
    loadMaterials()
  } catch (err: any) {
    alert("Save failed: " + err.message)
  } finally {
    saving.value = false
  }
}

function resetForm() {
  Object.assign(form, {
    materialId: "",
    materialType: "FERT",
    industrySector: "M",
    baseUnit: "EA",
    materialName: "",
    oldMaterialNo: "",
    materialGroup: "01",
    division: "10",
    weight: "",
    weightUnit: "KG",
    volume: "",
    volumeUnit: "M3",
    searchTerm: ""
  })
}

function viewDetail(id:string){alert(`Editing material ${id}`)}
</script>

<style scoped>
.page{padding:28px 36px;max-width:1200px;margin:0 auto;}

.ir{height:36px;display:flex;align-items:center;padding:0 12px;font-size:13px;color:rgba(18,55,42,0.35);background:rgba(173,188,159,0.12);border-radius:8px;border:1px dashed rgba(173,188,159,0.3);}
.iu{display:flex;}.iu .fi{border-radius:8px 0 0 8px;flex:1;}.uu{display:flex;align-items:center;padding:0 10px;height:36px;font-size:11px;font-weight:600;color:rgba(18,55,42,0.45);background:rgba(173,188,159,0.12);border:1px solid rgba(173,188,159,0.4);border-left:none;border-radius:0 8px 8px 0;}

.input-with-f4-inline{display:flex;align-items:center;gap:3px;}
.input-with-f4-inline .fs{flex:1;}
.f4-trigger-sm{width:26px;height:26px;border:1px solid rgba(173,188,159,0.35);border-radius:5px;background:rgba(251,250,218,0.3);cursor:pointer;display:flex;align-items:center;justify-content:center;color:rgba(18,55,42,0.4);transition:all 0.2s;flex-shrink:0;}
.f4-trigger-sm:hover{border-color:#436850;color:#436850;background:rgba(67,104,80,0.06);}

.tab-bar{display:flex;gap:0;border-bottom:1px solid rgba(173,188,159,0.22);margin:0 -20px 16px;padding:0 20px;overflow-x:auto;background:rgba(251,250,218,0.15);border-radius:14px 14px 0 0;}
.tab-btn{padding:10px 14px;font-size:11px;font-weight:500;color:rgba(18,55,42,0.45);background:none;border:none;border-bottom:2px solid transparent;cursor:pointer;font-family:inherit;white-space:nowrap;transition:all 0.2s;}
.tab-btn:hover{color:#12372A;}
.tab-btn.active{color:#436850;font-weight:700;border-bottom-color:#436850;}
.tab-placeholder{display:flex;align-items:center;justify-content:center;min-height:120px;color:rgba(18,55,42,0.2);font-size:14px;}

.fb{border:none;padding:0;margin:0 0 20px;border-bottom:1px solid rgba(173,188,159,0.12);padding-bottom:16px;}
.fb:last-child{border-bottom:none;margin-bottom:0;}
.bt{font-size:12px;font-weight:700;color:#436850;display:flex;align-items:center;gap:8px;margin-bottom:12px;}
.bt::before{content:"";width:3px;height:12px;background:#436850;border-radius:2px;}

.sc-title{font-size:13px;font-weight:700;color:#436850;margin:0 0 14px;}
.link{color:#436850;cursor:pointer;font-weight:600;font-size:12px;}
.link:hover{text-decoration:underline;}

.action-bar{display:flex;gap:12px;padding:16px 0;}
</style>
