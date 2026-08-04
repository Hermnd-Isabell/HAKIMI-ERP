<template>
  <MainLayout>
    <div class="page">
      <div class="header-card">
        <div class="hc-left">
          <div class="hc-icon"><svg viewBox="0 0 24 24" width="22" height="22"><rect x="2" y="3" width="20" height="17" rx="2" fill="none" stroke="#436850" stroke-width="1.8"/><path d="M2 9h20M7 3v3M17 3v3M8 13h3M8 16h5" fill="none" stroke="#436850" stroke-width="1.5" stroke-linecap="round"/></svg></div>
          <div class="hc-text"><h2 class="hc-title">Sales Organization</h2><p class="hc-sub">Configure sales org structure, distribution channels, and divisions.</p></div>
        </div>
      </div>
      <div v-if="loading" class="loading-msg">Loading sales organizations...</div>
      <div v-else-if="error" class="error-msg">{{ error }}</div>
      <div v-else class="data-card"><table class="dt">
        <thead><tr><th>Sales Org</th><th>Description</th><th>Dist. Channel</th><th>Division</th><th>Currency</th><th>Country</th><th>Status</th></tr></thead>
        <tbody>
          <tr v-for="r in rows" :key="r.sales_org_id + '-' + r.distribution_channel + '-' + r.division" class="dr">
            <td class="mono">{{ r.sales_org_id }}</td><td>{{ r.description }}</td><td class="mono">{{ r.distribution_channel }}</td><td class="mono">{{ r.division }}</td><td>{{ r.currency }}</td><td>{{ r.country }}</td>
            <td><span class="stag s-done">{{ r.status }}</span></td>
          </tr>
        </tbody>
      </table></div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import MainLayout from '@/layout/MainLayout.vue'
import axios from 'axios'
const rows = ref<any[]>([])
const loading = ref(true)
const error = ref('')
onMounted(async () => {
  try {
    const res = await axios.get('/api/v1/master/materials/sales-organizations', { params: { page_size: 50 } })
    rows.value = res.data.data.items || []
  } catch (e: any) { error.value = e.message || 'Failed to load sales organizations' }
  finally { loading.value = false }
})
</script>

<style scoped>
.page{padding:28px 36px;max-width:1100px;margin:0 auto;}
.header-card{display:flex;align-items:center;background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:16px;padding:20px 24px;border:1px solid rgba(173,188,159,0.18);box-shadow:0 2px 8px rgba(173,188,159,0.12);margin-bottom:20px;}
.hc-left{display:flex;align-items:center;gap:14px;}
.hc-icon{width:44px;height:44px;border-radius:12px;background:rgba(67,104,80,0.08);display:flex;align-items:center;justify-content:center;}
.hc-title{font-size:18px;font-weight:800;color:#12372A;margin:0;}
.hc-sub{font-size:12px;color:rgba(18,55,42,0.45);margin:2px 0 0;}
.loading-msg,.error-msg{text-align:center;padding:40px;color:rgba(18,55,42,0.4);font-size:14px;}
.error-msg{color:#D9534F;}
.data-card{background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:14px;border:1px solid rgba(173,188,159,0.15);box-shadow:0 2px 6px rgba(173,188,159,0.1);overflow:hidden;}
.dt{width:100%;border-collapse:collapse;font-size:13px;}
.dt th{text-align:left;padding:12px 14px;font-size:10px;font-weight:700;color:rgba(18,55,42,0.45);text-transform:uppercase;letter-spacing:0.8px;background:rgba(173,188,159,0.08);border-bottom:1px solid rgba(173,188,159,0.2);}
.dt td{padding:11px 14px;border-bottom:1px solid rgba(173,188,159,0.08);color:#12372A;}
.dr:hover{background:rgba(67,104,80,0.025);}
.mono{font-family:'SF Mono',Consolas,monospace;font-size:12px;}
.stag{font-size:10px;font-weight:600;padding:3px 8px;border-radius:5px;}
.s-done{background:rgba(67,104,80,0.1);color:#436850;}
</style>
