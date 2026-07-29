<template>
  <MainLayout>
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
          <div class="form-group"><label class="fl">Material No.</label><div class="ir">Auto-generated</div></div>
          <div class="form-group"><label class="fl required">Material Type</label>
            <div class="input-with-f4-inline"><select class="fs" v-model="form.matType"><option>FERT - Finished Product</option><option>ROH - Raw Material</option><option>HAWA - Trading Goods</option><option>HALB - Semi-Finished</option></select><button class="f4-trigger-sm" @click="openF4(`matType`)" title="F4 Search"><svg viewBox="0 0 20 20" width="12" height="12"><circle cx="8" cy="8" r="5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M12 12l5 5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button></div>
          </div>
          <div class="form-group"><label class="fl required">Industry Sector</label>
            <div class="input-with-f4-inline"><select class="fs" v-model="form.industry"><option>M - Mechanical Engineering</option><option>C - Chemical Industry</option><option>E - Electrical</option></select><button class="f4-trigger-sm" @click="openF4(`industry`)" title="F4 Search"><svg viewBox="0 0 20 20" width="12" height="12"><circle cx="8" cy="8" r="5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M12 12l5 5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button></div>
          </div>
          <div class="form-group"><label class="fl required">Base UoM</label><select class="fs" v-model="form.uom"><option>EA - Each</option><option>KG - Kilogram</option><option>M - Meter</option><option>L - Liter</option></select></div>
        </div>
      </div>

      <div class="form-card form-card-tabs">
        <div class="tab-bar">
          <button v-for="t in tabs" :key="t" class="tab-btn" :class="{active:active===t}" @click="active=t">{{ t }}</button>
        </div>
        <div class="tab-content" v-show="active===`Basic Data`">
          <fieldset class="fb"><legend class="bt">General Data</legend>
            <div class="form-row form-row-4">
              <div class="form-group"><label class="fl required">Material Desc.</label><input class="fi" v-model="form.desc" placeholder="e.g. Industrial Sensor X200" /></div>
              <div class="form-group"><label class="fl">Old Material No.</label><input class="fi" v-model="form.oldNo" placeholder="Legacy system ID" /></div>
              <div class="form-group"><label class="fl">Material Group</label>
                <div class="input-with-f4-inline"><select class="fs" v-model="form.matGroup"><option>01 - Electronics</option><option>02 - Mechanical</option></select><button class="f4-trigger-sm" @click="openF4(`matGroup`)" title="F4 Search"><svg viewBox="0 0 20 20" width="12" height="12"><circle cx="8" cy="8" r="5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M12 12l5 5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button></div>
              </div>
              <div class="form-group"><label class="fl">Division</label><select class="fs" v-model="form.division"><option>10 - Standard</option><option>20 - Special</option></select></div>
            </div>
          </fieldset>
          <fieldset class="fb"><legend class="bt">Dimensions</legend>
            <div class="form-row form-row-4">
              <div class="form-group"><label class="fl">Gross Weight</label><div class="iu"><input class="fi" v-model="form.grossWt" placeholder="0.000" /><span class="uu">KG</span></div></div>
              <div class="form-group"><label class="fl">Net Weight</label><div class="iu"><input class="fi" v-model="form.netWt" placeholder="0.000" /><span class="uu">KG</span></div></div>
              <div class="form-group"><label class="fl">Weight Unit</label><select class="fs"><option>KG</option><option>LB</option></select></div>
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
            <tr v-for="m in mats" :key="m.id" class="dr"><td class="mono">{{ m.id }}</td><td>{{ m.desc }}</td><td>{{ m.type }}</td><td>{{ m.uom }}</td><td>{{ m.grp }}</td><td><span class="stag s-done">{{ m.st }}</span></td><td><a class="link" @click="viewDetail(m.id)">Edit</a></td></tr>
          </tbody>
        </table>
      </div>

      <div class="action-bar">
        <button class="btn btn-primary" @click="saveMaterial">Save</button>
        <button class="btn btn-secondary" @click="alert(`Material saved. Continue editing?`);">Save &amp; Continue</button>
        <button class="btn btn-outline" @click="$router.push(`/`)">Cancel</button>
      </div>
    </div>

    <F4SearchModal :visible="f4Visible" :title="f4Title" @update:visible="f4Visible=$event" @confirm="onF4Confirm" />
  </MainLayout>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue"
import MainLayout from "@/layout/MainLayout.vue"
import F4SearchModal from "@/components/F4SearchModal.vue"

const active=ref("Basic Data")
const tabs=["Basic Data","Sales Data","Purchasing","MRP","Accounting","Storage","Quality"]

const form=reactive({
  matType:"FERT - Finished Product",
  industry:"M - Mechanical Engineering",
  uom:"EA - Each",
  desc:"",
  oldNo:"",
  matGroup:"01 - Electronics",
  division:"10 - Standard",
  grossWt:"",
  netWt:"",
  volume:"",
})

const mats=[{id:"DXTR1026",desc:"Industrial Sensor Module X200",type:"FERT",uom:"EA",grp:"Electronics",st:"Active"},{id:"CABL4400",desc:"Fiber Optic Cable 50m",type:"HAWA",uom:"M",grp:"Electronics",st:"Active"},{id:"BRKT220",desc:"Mounting Bracket Set",type:"FERT",uom:"EA",grp:"Mechanical",st:"Active"},{id:"FG-1001",desc:"Mountain Bike Frame",type:"FERT",uom:"EA",grp:"Mechanical",st:"Active"},{id:"SP-7780",desc:"Brake Assembly Kit",type:"HALB",uom:"EA",grp:"Mechanical",st:"Inactive"}]

// F4 Search
const f4Visible=ref(false)
const f4Title=ref("Search Help")
function openF4(ctx:string){
  const titles:Record<string,string>={matType:"Material Type (1)",industry:"Industry Sector (1)",matGroup:"Material Group (1)"}
  f4Title.value=titles[ctx]||"Search Help (1)"
  f4Visible.value=true
}
function onF4Confirm(idx:number){f4Visible.value=false;alert(`F4 selection confirmed at index ${idx}`)}

function saveMaterial(){alert("Material saved successfully!")}
function viewDetail(id:string){alert(`Editing material ${id}`)}
</script>

<style scoped>
.page{padding:28px 36px;max-width:1200px;margin:0 auto;}
.header-card{display:flex;align-items:center;background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:16px;padding:20px 24px;border:1px solid rgba(173,188,159,0.18);box-shadow:0 2px 8px rgba(173,188,159,0.12);margin-bottom:20px;}
.hc-left{display:flex;align-items:center;gap:14px;}
.hc-icon{width:44px;height:44px;border-radius:12px;background:rgba(67,104,80,0.08);display:flex;align-items:center;justify-content:center;}
.hc-title{font-size:18px;font-weight:800;color:#12372A;margin:0;}
.hc-sub{font-size:12px;color:rgba(18,55,42,0.45);margin:2px 0 0;}

.form-card{background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:14px;padding:20px;border:1px solid rgba(173,188,159,0.15);box-shadow:0 2px 6px rgba(173,188,159,0.1);margin-bottom:16px;}
.form-card-tabs{padding-top:0;overflow:hidden;}
.form-row{display:grid;gap:18px;margin-bottom:14px;}
.form-row-4{grid-template-columns:1fr 1fr 1fr 1fr;}
.form-group{display:flex;flex-direction:column;gap:6px;}
.fl{font-size:11px;font-weight:600;color:rgba(18,55,42,0.55);text-transform:uppercase;letter-spacing:0.5px;}
.fl.required::after{content:" *";color:#D9534F;}
.fi,.fs{height:36px;border:1px solid rgba(173,188,159,0.4);border-radius:8px;padding:0 12px;font-size:13px;color:#12372A;background:rgba(251,250,218,0.4);font-family:inherit;outline:none;width:100%;}
.fi:focus,.fs:focus{border-color:#436850;box-shadow:0 0 0 3px rgba(67,104,80,0.06);}
.fs{cursor:pointer;appearance:none;background-image:url("data:image/svg+xml,%3Csvg viewBox=\"0 0 20 20\" width=\"12\" height=\"12\" xmlns=\"http://www.w3.org/2000/svg\"%3E%3Cpath d=\"M5 7l5 5 5-5\" fill=\"none\" stroke=\"%2312372A\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\" opacity=\"0.4\"/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 10px center;padding-right:32px;}
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

.data-card{background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:14px;padding:18px;border:1px solid rgba(173,188,159,0.15);box-shadow:0 2px 6px rgba(173,188,159,0.1);margin-bottom:18px;}
.sc-title{font-size:13px;font-weight:700;color:#436850;margin:0 0 14px;}
.dt{width:100%;border-collapse:collapse;font-size:13px;}
.dt th{text-align:left;padding:9px 12px;font-size:10px;font-weight:700;color:rgba(18,55,42,0.4);text-transform:uppercase;letter-spacing:0.5px;border-bottom:1px solid rgba(173,188,159,0.2);}
.dt td{padding:9px 12px;border-bottom:1px solid rgba(173,188,159,0.07);color:#12372A;}
.dr:hover{background:rgba(67,104,80,0.025);}
.mono{font-family:"SF Mono",Consolas,monospace;font-size:12px;}
.stag{font-size:10px;font-weight:600;padding:3px 8px;border-radius:5px;}
.s-done{background:rgba(67,104,80,0.1);color:#436850;}
.link{color:#436850;cursor:pointer;font-weight:600;font-size:12px;}
.link:hover{text-decoration:underline;}

.action-bar{display:flex;gap:12px;padding:16px 0;}
.btn{display:inline-flex;align-items:center;gap:6px;padding:10px 22px;font-size:13px;font-weight:600;border-radius:8px;cursor:pointer;transition:all 0.2s;font-family:inherit;}
.btn-primary{background:linear-gradient(135deg,#436850,#365440);color:#FBFADA;border:none;box-shadow:0 2px 8px rgba(67,104,80,0.25);}
.btn-primary:hover{transform:translateY(-1px);}
.btn-secondary{background:rgba(173,188,159,0.2);color:#436850;border:1px solid rgba(173,188,159,0.35);}
.btn-secondary:hover{background:rgba(173,188,159,0.3);}
.btn-outline{background:none;color:rgba(18,55,42,0.5);border:1px solid rgba(173,188,159,0.35);}
.btn-outline:hover{border-color:rgba(18,55,42,0.3);color:#12372A;}
</style>
