<template>
  <div class="page">
    <div class="header-card">
        <div class="hc-left">
          <div class="hc-icon"><svg viewBox="0 0 24 24" width="22" height="22"><path d="M12 2l7 4.5v9L12 20l-7-4.5v-9L12 2z" fill="none" stroke="#436850" stroke-width="1.8" stroke-linejoin="round"/><path d="M12 7v8M5 9l7 4 7-4" fill="none" stroke="#436850" stroke-width="1.3" stroke-linecap="round"/></svg></div>
          <div class="hc-text"><h2 class="hc-title">Product Catalog</h2><p class="hc-sub">Browse and manage product listings with pricing and availability.</p></div>
        </div>
      </div>
      <div v-if="loading" class="loading-msg">Loading products...</div>
      <div v-else-if="error" class="error-msg">{{ error }}</div>
      <div v-else class="data-card"><table class="dt">
        <thead><tr><th>Product ID</th><th>Name</th><th>Category</th><th class="num">Unit Price</th><th>UoM</th><th class="num">Stock</th><th>Status</th></tr></thead>
        <tbody>
          <tr v-for="p in products" :key="p.materialId" class="dr">
            <td class="mono">{{ p.materialId }}</td><td>{{ p.materialName }}</td><td>{{ p.category || '-' }}</td><td class="num mono">{{ p.standardPrice }}</td><td>{{ p.baseUnit }}</td><td class="num mono">{{ p.stockQuantity }}</td>
            <td><span class="stag" :class="p.status==='ACTIVE'?'s-done':'s-warn'">{{ p.status === 'ACTIVE' ? 'Available' : 'Inactive' }}</span></td>
          </tr>
        </tbody>
      </table>    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchMaterials } from '@/api'

const products = ref<any[]>([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const data = await fetchMaterials({ pageSize: 50 })
    products.value = data.items || []
  } catch (e: any) { error.value = e.message || 'Failed to load products' }
  finally { loading.value = false }
})
</script>

<style scoped>
.page{padding:28px 36px;max-width:1200px;margin:0 auto;}
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
.dt th.num{text-align:right;}
.dt td{padding:11px 14px;border-bottom:1px solid rgba(173,188,159,0.08);color:#12372A;}
.dt td.num{text-align:right;}
.dr:hover{background:rgba(67,104,80,0.025);}
.mono{font-family:'SF Mono',Consolas,monospace;font-size:12px;}
.stag{font-size:10px;font-weight:600;padding:3px 8px;border-radius:5px;}
.s-done{background:rgba(67,104,80,0.1);color:#436850;}
.s-warn{background:rgba(217,83,79,0.08);color:#c94a45;}
</style>
