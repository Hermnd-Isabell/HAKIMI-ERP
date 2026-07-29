<template>
  <MainLayout>
    <div class="page">
      <div class="top-bar">
        <button class="back-btn" @click="$router.push('/delivery/monitor')"><svg viewBox="0 0 20 20" width="16" height="16"><path d="M12 4l-6 6 6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>Back</button>
        <div class="hc-icon"><svg viewBox="0 0 24 24" width="22" height="22"><rect x="2" y="5" width="20" height="13" rx="2" fill="none" stroke="#436850" stroke-width="1.8"/><path d="M6 5V3M18 5V3M2 11h20M7 16h3" fill="none" stroke="#436850" stroke-width="1.5" stroke-linecap="round"/></svg></div>
        <div class="top-info">
          <span class="ti-label">Delivery No.</span>
          <span class="ti-value">80000078</span>
          <span class="ti-sub">Sales Order 500000122 &middot; The Bike Zone</span>
        </div>
        <div style="margin-left:auto;display:flex;align-items:center;gap:10px;">
          <span class="stag s-transit">In Transit</span>
          <button class="btn btn-primary"><svg viewBox="0 0 20 20" width="14" height="14"><path d="M10 3v10M6 9l4 4 4-4M3 17h14" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>Download POD</button>
          <button class="btn btn-outline"><svg viewBox="0 0 20 20" width="14" height="14"><rect x="3" y="4" width="14" height="10" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M6 8h8M6 11h5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>Print</button>
        </div>
      </div>

      <div class="info-cards">
        <div class="ic"><span class="ic-label">Delivery Date</span><span class="ic-value">2026-03-15</span></div>
        <div class="ic"><span class="ic-label">Planned GI Date</span><span class="ic-value">2026-03-18</span></div>
        <div class="ic"><span class="ic-label">Carrier</span><span class="ic-value">GreenLine Freight</span></div>
        <div class="ic"><span class="ic-label">Delivered / Total</span><span class="ic-value mono">3,200 / 5,000</span></div>
      </div>

      <div class="section-card">
        <h3 class="sc-title">Delivery Progress</h3>
        <p class="sc-hint">Current milestone: shipped and moving toward customer receiving dock.</p>
        <div class="timeline">
          <div v-for="(s,i) in steps" :key="i" class="tl-step" :class="{done:s.done,cur:s.cur}">
            <div class="tl-dot"></div><div v-if="i<3" class="tl-line"></div>
            <div class="tl-info"><span class="tl-status">{{ s.label }}</span><span class="tl-time">{{ s.time }}</span></div>
          </div>
        </div>
      </div>

      <div class="two-col">
        <div class="section-card">
          <h3 class="sc-title">Shipment Information</h3>
          <div class="si-grid">
            <div class="si-item"><span class="si-label">Ship-to Address</span><span class="si-value mono">1288 Market Street<br/>San Francisco, CA 94102</span></div>
            <div class="si-item"><span class="si-label">Contact</span><span class="si-value">Emma Rodriguez<br/>+1 (415) 555-0198</span></div>
            <div class="si-item"><span class="si-label">Route</span><span class="si-value">Warehouse A → Bay Area Hub → Customer Site</span></div>
            <div class="si-item"><span class="si-label">Truck / Driver</span><span class="si-value">TRK-2048 · Daniel Wu</span></div>
            <div class="si-item"><span class="si-label">Latest GPS</span><span class="si-value">Oakland, CA <span class="gps-time">Updated 6 min ago</span></span></div>
          </div>
        </div>
        <div class="section-card">
          <h3 class="sc-title">Order Items</h3>
          <table class="data-table">
            <thead><tr><th>Material</th><th>Description</th><th class="num">Qty</th><th>Status</th></tr></thead>
            <tbody>
              <tr><td class="mono">FG-1001</td><td>Mountain Bike Frame</td><td class="num mono">1,800</td><td><span class="stag s-done">Shipped</span></td></tr>
              <tr><td class="mono">FG-1014</td><td>Road Bike Wheel Set</td><td class="num mono">900</td><td><span class="stag s-done">Shipped</span></td></tr>
              <tr><td class="mono">SP-7780</td><td>Brake Assembly Kit</td><td class="num mono">500</td><td><span class="stag s-pick">Loading</span></td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from '@/layout/MainLayout.vue'
const steps=[{label:'Created',done:true,time:'Mar 15, 08:20',cur:false},{label:'Picked',done:true,time:'Mar 15, 13:45',cur:false},{label:'Shipped',done:true,time:'Mar 16, 09:10',cur:true},{label:'Completed',done:false,time:'Pending',cur:false}]
</script>

<style scoped>
.page{padding:28px 36px;max-width:1200px;margin:0 auto;}
.top-bar{display:flex;align-items:center;gap:16px;margin-bottom:22px;flex-wrap:wrap;}
.back-btn{display:inline-flex;align-items:center;gap:6px;background:none;border:1px solid rgba(173,188,159,0.35);border-radius:8px;padding:8px 16px;font-size:13px;color:rgba(18,55,42,0.55);cursor:pointer;font-family:inherit;transition:all 0.2s;}
.back-btn:hover{border-color:#436850;color:#436850;}
.hc-icon{width:42px;height:42px;border-radius:10px;background:rgba(67,104,80,0.08);display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.top-info{display:flex;flex-direction:column;}
.ti-label{font-size:10px;color:rgba(18,55,42,0.35);text-transform:uppercase;letter-spacing:1px;font-weight:600;}
.ti-value{font-size:22px;font-weight:800;color:#12372A;font-family:'SF Mono',Consolas,monospace;}
.ti-sub{font-size:12px;color:rgba(18,55,42,0.4);}
.stag{font-size:11px;font-weight:600;padding:5px 12px;border-radius:6px;}
.s-transit{background:rgba(67,104,80,0.1);color:#436850;}
.s-done{background:rgba(67,104,80,0.1);color:#436850;}
.s-pick{background:rgba(240,173,78,0.12);color:#c98a20;}

.info-cards{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:20px;}
.ic{background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:12px;padding:16px 18px;border:1px solid rgba(173,188,159,0.15);box-shadow:0 2px 6px rgba(173,188,159,0.1);}
.ic-label{font-size:10px;color:rgba(18,55,42,0.4);font-weight:600;text-transform:uppercase;letter-spacing:0.5px;display:block;margin-bottom:6px;}
.ic-value{font-size:15px;font-weight:700;color:#12372A;}

.section-card{background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:14px;padding:22px;border:1px solid rgba(173,188,159,0.15);box-shadow:0 2px 6px rgba(173,188,159,0.1);margin-bottom:18px;}
.sc-title{font-size:14px;font-weight:700;color:#436850;margin:0 0 12px;display:flex;align-items:center;gap:8px;}
.sc-title::before{content:'';width:3px;height:13px;background:#436850;border-radius:2px;}
.sc-hint{font-size:12px;color:rgba(18,55,42,0.4);margin:0 0 18px;font-style:italic;}

.timeline{display:flex;align-items:flex-start;padding:8px 0;}
.tl-step{flex:1;position:relative;display:flex;flex-direction:column;align-items:center;}
.tl-dot{width:13px;height:13px;border-radius:50%;border:2px solid rgba(173,188,159,0.35);background:#FBFADA;z-index:1;}
.tl-step.done .tl-dot{background:#436850;border-color:#436850;}
.tl-step.cur .tl-dot{background:#436850;border-color:#436850;box-shadow:0 0 0 4px rgba(67,104,80,0.12);}
.tl-line{position:absolute;top:6px;left:50%;width:100%;height:2px;background:rgba(173,188,159,0.25);}
.tl-step.done .tl-line{background:#436850;}
.tl-info{margin-top:10px;text-align:center;}
.tl-status{font-size:11px;font-weight:600;color:rgba(18,55,42,0.45);display:block;}
.tl-step.cur .tl-status,.tl-step.done .tl-status{color:#436850;}
.tl-time{font-size:10px;color:rgba(18,55,42,0.28);display:block;margin-top:2px;}

.two-col{display:grid;grid-template-columns:1fr 1fr;gap:18px;}
.si-grid{display:flex;flex-direction:column;gap:14px;}
.si-item{display:flex;flex-direction:column;gap:2px;}
.si-label{font-size:10px;color:rgba(18,55,42,0.38);font-weight:600;text-transform:uppercase;letter-spacing:0.5px;}
.si-value{font-size:13px;color:#12372A;line-height:1.6;}
.gps-time{font-size:10px;color:rgba(18,55,42,0.25);}

.data-table{width:100%;border-collapse:collapse;font-size:13px;}
.data-table th{text-align:left;padding:9px 12px;font-size:10px;font-weight:700;color:rgba(18,55,42,0.4);text-transform:uppercase;letter-spacing:0.5px;border-bottom:1px solid rgba(173,188,159,0.2);}
.data-table th.num{text-align:right;}
.data-table td{padding:9px 12px;border-bottom:1px solid rgba(173,188,159,0.07);color:#12372A;}
.data-table td.num{text-align:right;}
.mono{font-family:'SF Mono',Consolas,monospace;font-size:12px;}

.btn{display:inline-flex;align-items:center;gap:6px;padding:9px 18px;font-size:13px;font-weight:600;border-radius:8px;cursor:pointer;transition:all 0.2s;font-family:inherit;}
.btn-primary{background:linear-gradient(135deg,#436850,#365440);color:#FBFADA;border:none;box-shadow:0 2px 8px rgba(67,104,80,0.25);}
.btn-primary:hover{transform:translateY(-1px);}
.btn-outline{background:none;color:rgba(18,55,42,0.5);border:1px solid rgba(173,188,159,0.35);}
.btn-outline:hover{border-color:#436850;color:#436850;}
</style>