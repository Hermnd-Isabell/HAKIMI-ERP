<template>
  <MainLayout>
    <div class="page">
      <div class="top-bar">
        <button class="back-btn" @click="$router.push('/finance/unpaid')"><svg viewBox="0 0 20 20" width="16" height="16"><path d="M12 4l-6 6 6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>Back</button>
        <div class="hc-icon"><svg viewBox="0 0 24 24" width="22" height="22"><circle cx="12" cy="12" r="10" fill="none" stroke="#436850" stroke-width="1.8"/><path d="M7 14l3 3 7-7" fill="none" stroke="#436850" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
        <div class="top-info">
          <span class="ti-label">Invoice No.</span><span class="ti-value mono">INV-2026-00086</span>
          <span class="ti-sub">The Bike Zone &middot; Sales Order 500000120 &middot; Due 2026-02-28</span>
        </div>
        <div style="margin-left:auto;display:flex;align-items:center;gap:10px;">
          <span class="stag s-overdue">Overdue</span>
          <button class="btn btn-primary">Collect</button>
          <button class="btn btn-outline">Export</button>
        </div>
      </div>

      <div class="info-cards">
        <div class="ic"><span class="ic-label">Invoice Amount</span><span class="ic-value">$85,000.00</span></div>
        <div class="ic"><span class="ic-label">Received Amount</span><span class="ic-value">$20,000.00</span></div>
        <div class="ic ic-danger"><span class="ic-label">Unpaid Amount</span><span class="ic-value ic-red">$65,000.00</span></div>
        <div class="ic ic-warn"><span class="ic-label">Days Overdue</span><span class="ic-value ic-amber">139 days</span></div>
      </div>

      <div class="section-card">
        <h3 class="sc-title">Collection Progress</h3>
        <p class="sc-hint">Current stage: overdue notice sent, waiting for customer payment confirmation.</p>
        <div class="timeline">
          <div v-for="(s,i) in steps" :key="i" class="tl-step" :class="{done:s.done,cur:s.cur,alert:s.alert}">
            <div class="tl-dot"></div><div v-if="i<3" class="tl-line"></div>
            <div class="tl-info"><span class="tl-status">{{ s.label }}</span><span class="tl-time">{{ s.time }}</span></div>
          </div>
        </div>
      </div>

      <div class="two-col">
        <div class="section-card">
          <h3 class="sc-title">Customer &amp; Terms</h3>
          <div class="si-grid">
            <div class="si-item"><span class="si-label">Customer</span><span class="si-value">The Bike Zone</span></div>
            <div class="si-item"><span class="si-label">Contact</span><span class="si-value">Emma Rodriguez · finance@bikezone.example</span></div>
            <div class="si-item"><span class="si-label">Payment Terms</span><span class="si-value">Net 30</span></div>
            <div class="si-item"><span class="si-label">Credit Limit</span><span class="si-value mono">$250,000.00</span></div>
            <div class="si-item"><span class="si-label">Risk Level</span><span class="si-value"><span class="risk-tag medium">Medium</span></span></div>
          </div>
        </div>
        <div class="section-card">
          <h3 class="sc-title">Payment History</h3>
          <table class="data-table">
            <thead><tr><th>Date</th><th>Method</th><th class="num">Amount</th><th>Reference</th></tr></thead>
            <tbody>
              <tr><td>2026-02-12</td><td>Bank Transfer</td><td class="num mono">$20,000.00</td><td class="mono">PAY-20418</td></tr>
              <tr><td colspan="2" class="pending-row">Pending</td><td class="num mono" style="color:#D9534F">$65,000.00</td><td class="mono"><span class="stag s-overdue">Overdue</span></td></tr>
            </tbody>
          </table>
          <div class="ratio-bar-wrap"><span class="ratio-label">Collection ratio</span><div class="ratio-bar"><div class="ratio-fill" style="width:24%"></div></div><span class="ratio-pct">24%</span></div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from '@/layout/MainLayout.vue'
const steps=[{label:'Invoice Issued',done:true,time:'Jan 28, 2026',cur:false,alert:false},{label:'Partially Paid',done:true,time:'Feb 12, 2026',cur:false,alert:false},{label:'Overdue Notice',done:false,time:'Mar 01, 09:10',cur:true,alert:true},{label:'Closed',done:false,time:'Pending',cur:false,alert:false}]
</script>

<style scoped>
.page{padding:28px 36px;max-width:1200px;margin:0 auto;}
.top-bar{display:flex;align-items:center;gap:16px;margin-bottom:22px;flex-wrap:wrap;}
.back-btn{display:inline-flex;align-items:center;gap:6px;background:none;border:1px solid rgba(173,188,159,0.35);border-radius:8px;padding:8px 16px;font-size:13px;color:rgba(18,55,42,0.55);cursor:pointer;font-family:inherit;transition:all 0.2s;}
.back-btn:hover{border-color:#436850;color:#436850;}
.hc-icon{width:42px;height:42px;border-radius:10px;background:rgba(67,104,80,0.08);display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.top-info{display:flex;flex-direction:column;}
.ti-label{font-size:10px;color:rgba(18,55,42,0.35);text-transform:uppercase;letter-spacing:1px;font-weight:600;}
.ti-value{font-size:22px;font-weight:800;color:#12372A;}
.ti-sub{font-size:12px;color:rgba(18,55,42,0.4);}
.stag{font-size:11px;font-weight:600;padding:5px 12px;border-radius:6px;}
.s-overdue{background:rgba(217,83,79,0.1);color:#D9534F;}

.info-cards{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:20px;}
.ic{background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:12px;padding:16px 18px;border:1px solid rgba(173,188,159,0.15);box-shadow:0 2px 6px rgba(173,188,159,0.1);}
.ic-danger{border-left:3px solid #D9534F;}
.ic-warn{border-left:3px solid #F0AD4E;}
.ic-label{font-size:10px;color:rgba(18,55,42,0.4);font-weight:600;text-transform:uppercase;letter-spacing:0.5px;display:block;margin-bottom:6px;}
.ic-value{font-size:15px;font-weight:700;color:#12372A;font-family:'SF Mono',Consolas,monospace;}
.ic-red{color:#D9534F;}
.ic-amber{color:#c98a20;}

.section-card{background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:14px;padding:22px;border:1px solid rgba(173,188,159,0.15);box-shadow:0 2px 6px rgba(173,188,159,0.1);margin-bottom:18px;}
.sc-title{font-size:14px;font-weight:700;color:#436850;margin:0 0 12px;display:flex;align-items:center;gap:8px;}
.sc-title::before{content:'';width:3px;height:13px;background:#436850;border-radius:2px;}
.sc-hint{font-size:12px;color:rgba(18,55,42,0.4);margin:0 0 18px;font-style:italic;}

.timeline{display:flex;align-items:flex-start;padding:8px 0;}
.tl-step{flex:1;position:relative;display:flex;flex-direction:column;align-items:center;}
.tl-dot{width:13px;height:13px;border-radius:50%;border:2px solid rgba(173,188,159,0.35);background:#FBFADA;z-index:1;}
.tl-step.done .tl-dot{background:#436850;border-color:#436850;}
.tl-step.cur .tl-dot{background:#436850;border-color:#436850;box-shadow:0 0 0 4px rgba(67,104,80,0.12);}
.tl-step.alert .tl-dot{background:#D9534F;border-color:#D9534F;box-shadow:0 0 0 4px rgba(217,83,79,0.12);}
.tl-line{position:absolute;top:6px;left:50%;width:100%;height:2px;background:rgba(173,188,159,0.25);}
.tl-step.done .tl-line{background:#436850;}
.tl-info{margin-top:10px;text-align:center;}
.tl-status{font-size:11px;font-weight:600;color:rgba(18,55,42,0.45);display:block;}
.tl-step.cur .tl-status,.tl-step.done .tl-status{color:#436850;}
.tl-step.alert .tl-status{color:#D9534F;}
.tl-time{font-size:10px;color:rgba(18,55,42,0.28);display:block;margin-top:2px;}

.two-col{display:grid;grid-template-columns:1fr 1fr;gap:18px;}
.si-grid{display:flex;flex-direction:column;gap:14px;}
.si-item{display:flex;flex-direction:column;gap:2px;}
.si-label{font-size:10px;color:rgba(18,55,42,0.38);font-weight:600;text-transform:uppercase;letter-spacing:0.5px;}
.si-value{font-size:13px;color:#12372A;line-height:1.6;}
.risk-tag{font-size:11px;font-weight:600;padding:3px 10px;border-radius:6px;}
.risk-tag.medium{background:rgba(240,173,78,0.15);color:#c98a20;}

.data-table{width:100%;border-collapse:collapse;font-size:13px;}
.data-table th{text-align:left;padding:9px 12px;font-size:10px;font-weight:700;color:rgba(18,55,42,0.4);text-transform:uppercase;letter-spacing:0.5px;border-bottom:1px solid rgba(173,188,159,0.2);}
.data-table th.num{text-align:right;}
.data-table td{padding:9px 12px;border-bottom:1px solid rgba(173,188,159,0.07);color:#12372A;}
.data-table td.num{text-align:right;}
.pending-row{color:#D9534F;font-weight:600;}

.ratio-bar-wrap{display:flex;align-items:center;gap:10px;margin-top:16px;}
.ratio-label{font-size:11px;color:rgba(18,55,42,0.4);white-space:nowrap;}
.ratio-bar{flex:1;height:7px;background:rgba(173,188,159,0.2);border-radius:4px;overflow:hidden;}
.ratio-fill{height:100%;background:#436850;border-radius:4px;}
.ratio-pct{font-size:13px;font-weight:700;color:#12372A;}
.mono{font-family:'SF Mono',Consolas,monospace;font-size:12px;}

.btn{display:inline-flex;align-items:center;gap:6px;padding:9px 18px;font-size:13px;font-weight:600;border-radius:8px;cursor:pointer;transition:all 0.2s;font-family:inherit;}
.btn-primary{background:linear-gradient(135deg,#436850,#365440);color:#FBFADA;border:none;box-shadow:0 2px 8px rgba(67,104,80,0.25);}
.btn-primary:hover{transform:translateY(-1px);}
.btn-outline{background:none;color:rgba(18,55,42,0.5);border:1px solid rgba(173,188,159,0.35);}
.btn-outline:hover{border-color:#436850;color:#436850;}
</style>