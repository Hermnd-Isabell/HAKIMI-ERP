<template>
  <Teleport to="body">
    <div class="modal-overlay" v-if="visible" @click.self="close">
      <div class="f4-modal">
        <div class="f4-header">
          <h3 class="f4-title">{{ title }}</h3>
          <button class="f4-close" @click="close"><svg viewBox="0 0 20 20" width="16" height="16"><path d="M6 6l8 8M14 6l-8 8" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg></button>
        </div>
        <div class="f4-body">
          <div class="f4-section-label">Restrictions</div>
          <div class="f4-search-row">
            <button class="f4-tool-btn" title="Search"><svg viewBox="0 0 20 20" width="14" height="14"><circle cx="9" cy="9" r="5.5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M13 13l4 4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
            <button class="f4-tool-btn" title="Advanced Search"><svg viewBox="0 0 20 20" width="14" height="14"><circle cx="9" cy="9" r="5.5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M13 13l4 4M9 5v8M5 9h8" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg></button>
            <select class="f4-search-select"><option>Search Relationship Category</option></select>
          </div>
          <div class="f4-table-wrap">
            <table class="f4-table">
              <thead><tr><th class="radio-col"></th><th>RelCat</th><th>Direction</th><th>Description</th></tr></thead>
              <tbody>
                <tr v-for="(r,i) in rows" :key="i" class="f4-row" :class="{selected:sel===i}" @click="sel=i">
                  <td class="radio-col"><span class="radio-dot" :class="{on:sel===i}"></span></td>
                  <td class="mono">{{ r.cat }}</td><td>{{ r.dir }}</td><td>{{ r.desc }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="f4-count">{{ rows.length }} Entries found</div>
        </div>
        <div class="f4-footer">
          <div class="f4-foot-left">
            <button class="f4-foot-btn" title="Search"><svg viewBox="0 0 20 20" width="13" height="13"><circle cx="9" cy="9" r="5.5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M13 13l4 4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
            <button class="f4-foot-btn" title="Move"><svg viewBox="0 0 20 20" width="13" height="13"><path d="M7 5l3-3 3 3M7 15l3 3 3-3M3 9h14" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
          </div>
          <div class="f4-foot-right">
            <button class="f4-foot-btn confirm" @click="confirm"><svg viewBox="0 0 20 20" width="14" height="14"><path d="M5 11l4 4 7-7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
            <button class="f4-foot-btn" title="Print"><svg viewBox="0 0 20 20" width="13" height="13"><rect x="3" y="4" width="14" height="10" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M6 8h8M6 11h5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg></button>
            <button class="f4-foot-btn cancel" @click="close"><svg viewBox="0 0 20 20" width="14" height="14"><path d="M6 6l8 8M14 6l-8 8" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg></button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref } from 'vue'
const props=withDefaults(defineProps<{visible?:boolean;title?:string}>(),{visible:false,title:'Relationship Category (1)'})
const emit=defineEmits<{'update:visible':[v:boolean];confirm:[idx:number]}>()
const sel=ref(0)
const rows=[
  {cat:'BBP002',dir:'->',desc:'Has the Invoicing Party'},
  {cat:'BUR001',dir:'->',desc:'Has Contact Person'},
  {cat:'BUR002',dir:'->',desc:'Has Activity Partner'},
  {cat:'BUR004',dir:'<->',desc:'Is Married To'},
  {cat:'BUR006',dir:'<->',desc:'Is Identical To'},
  {cat:'BUR010',dir:'->',desc:'Has the Employee'},
  {cat:'BUR013',dir:'->',desc:'Is Replaced By'},
  {cat:'BUR020',dir:'->',desc:'Has Department'},
  {cat:'BUR023',dir:'<->',desc:'Is Related To'},
  {cat:'CRMH04',dir:'->',desc:'Has the Bill-To Party'},
  {cat:'EWM001',dir:'->',desc:'Has the Dock Appointment Scheduling Planner'},
  {cat:'FS0030',dir:'->',desc:'Borrower Entity Member'},
  {cat:'BBP003',dir:'<->',desc:'Is Business Partner Of'},
  {cat:'BBP005',dir:'->',desc:'Has the Contact Person'},
  {cat:'BUR030',dir:'<->',desc:'Is Subsidiary Of'},
  {cat:'BUR035',dir:'->',desc:'Has Legal Representative'},
  {cat:'CRMH01',dir:'->',desc:'Has the Ship-To Party'},
  {cat:'CRMH02',dir:'->',desc:'Has the Payer'},
  {cat:'FS0001',dir:'->',desc:'Has Credit Account'},
  {cat:'FS0015',dir:'->',desc:'Loan Guarantor'},
]
function close(){emit('update:visible',false)}
function confirm(){emit('confirm',sel.value);emit('update:visible',false)}
</script>

<style scoped>
.modal-overlay{position:fixed;inset:0;background:rgba(18,55,42,0.3);backdrop-filter:blur(4px);display:flex;align-items:center;justify-content:center;z-index:2000;}
.f4-modal{width:720px;max-height:82vh;background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:18px;box-shadow:0 20px 60px rgba(18,55,42,0.22);border:1px solid rgba(173,188,159,0.2);display:flex;flex-direction:column;overflow:hidden;}
.f4-header{display:flex;align-items:center;justify-content:space-between;padding:18px 24px;border-bottom:1px solid rgba(173,188,159,0.18);}
.f4-title{font-size:16px;font-weight:700;color:#12372A;margin:0;}
.f4-close{background:none;border:none;color:rgba(18,55,42,0.35);cursor:pointer;padding:4px;border-radius:6px;transition:all 0.2s;display:flex;}
.f4-close:hover{background:rgba(217,83,79,0.08);color:#D9534F;}

.f4-body{flex:1;overflow-y:auto;padding:18px 24px;}
.f4-section-label{font-size:11px;font-weight:700;color:rgba(18,55,42,0.5);text-transform:uppercase;letter-spacing:0.8px;margin-bottom:10px;display:flex;align-items:center;gap:6px;}
.f4-section-label::before{content:'';width:3px;height:11px;background:#436850;border-radius:2px;}

.f4-search-row{display:flex;gap:6px;margin-bottom:16px;}
.f4-tool-btn{width:34px;height:34px;border:1px solid rgba(173,188,159,0.3);border-radius:7px;background:rgba(251,250,218,0.3);cursor:pointer;display:flex;align-items:center;justify-content:center;color:rgba(18,55,42,0.4);transition:all 0.2s;}
.f4-tool-btn:hover{border-color:#436850;color:#436850;}
.f4-search-select{flex:1;height:34px;border:1px solid rgba(173,188,159,0.4);border-radius:7px;padding:0 12px;font-size:12px;color:#12372A;background:rgba(251,250,218,0.3);font-family:inherit;outline:none;}

.f4-table-wrap{max-height:340px;overflow-y:auto;border:1px solid rgba(173,188,159,0.12);border-radius:8px;}
.f4-table-wrap::-webkit-scrollbar{width:4px;}
.f4-table-wrap::-webkit-scrollbar-thumb{background:rgba(173,188,159,0.4);border-radius:2px;}
.f4-table{width:100%;border-collapse:collapse;font-size:13px;}
.f4-table th{text-align:left;padding:10px 14px;font-size:10px;font-weight:700;color:rgba(18,55,42,0.4);text-transform:uppercase;letter-spacing:0.5px;border-bottom:1px solid rgba(173,188,159,0.15);background:rgba(173,188,159,0.06);position:sticky;top:0;}
.f4-table td{padding:9px 14px;border-bottom:1px solid rgba(173,188,159,0.06);color:#12372A;}
.radio-col{width:44px;text-align:center;}
.radio-dot{width:16px;height:16px;border-radius:50%;border:2px solid rgba(173,188,159,0.4);display:inline-block;transition:all 0.2s;}
.radio-dot.on{border-color:#436850;background:#436850;box-shadow:inset 0 0 0 4px #FBFADA;}
.f4-row{cursor:pointer;transition:background 0.15s;}
.f4-row:hover{background:rgba(67,104,80,0.03);}
.f4-row.selected{background:rgba(67,104,80,0.06);}
.f4-count{font-size:11px;color:rgba(18,55,42,0.3);margin-top:10px;}
.mono{font-family:'SF Mono',Consolas,monospace;font-size:12px;}

.f4-footer{display:flex;align-items:center;justify-content:space-between;padding:12px 24px;border-top:1px solid rgba(173,188,159,0.15);background:rgba(251,250,218,0.2);}
.f4-foot-left,.f4-foot-right{display:flex;gap:6px;}
.f4-foot-btn{width:34px;height:34px;border:1px solid rgba(173,188,159,0.25);border-radius:7px;background:rgba(251,250,218,0.3);cursor:pointer;display:flex;align-items:center;justify-content:center;color:rgba(18,55,42,0.4);transition:all 0.2s;}
.f4-foot-btn:hover{border-color:#436850;color:#436850;}
.f4-foot-btn.confirm{background:#436850;color:#FBFADA;border-color:#436850;width:38px;height:38px;border-radius:8px;}
.f4-foot-btn.confirm:hover{background:#365440;}
.f4-foot-btn.cancel:hover{background:rgba(217,83,79,0.08);color:#D9534F;border-color:#D9534F;}
</style>