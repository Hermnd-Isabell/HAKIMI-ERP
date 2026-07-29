<template>
  <div class="indicator-card" :style="{ '--accent': color }">
    <div class="card-top">
      <div class="card-icon-wrap">
        <svg viewBox="0 0 20 20" width="17" height="17" v-html="icon"></svg>
      </div>
      <span class="card-change" :class="changeType">
        <svg viewBox="0 0 16 16" width="11" height="11">
          <path v-if="changeType === 'up'" d="M4 10l4-4 4 4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path v-else d="M4 6l4 4 4-4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        {{ change }}
      </span>
    </div>
    <div class="card-value">{{ value }}</div>
    <div class="card-footer">
      <span class="card-title">{{ title }}</span>
      <span class="card-compare">{{ comparison }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string; value: string; change: string
  changeType: 'up' | 'down'; comparison: string; color: string; icon: string
}>()
</script>

<style scoped>
.indicator-card {
  --accent: #436850;
  background: linear-gradient(145deg, #fdfce8, #f7f5d1);
  border-radius: 16px;
  padding: 18px 20px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow:
    0 2px 4px rgba(173, 188, 159, 0.18),
    0 6px 16px rgba(173, 188, 159, 0.12),
    inset 0 1px 0 rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(173, 188, 159, 0.18);
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.indicator-card:hover {
  transform: translateY(-4px);
  box-shadow:
    0 4px 8px rgba(173, 188, 159, 0.25),
    0 12px 28px rgba(173, 188, 159, 0.18),
    inset 0 1px 0 rgba(255, 255, 255, 0.7);
  border-color: color-mix(in srgb, var(--accent) 30%, transparent);
}

.card-top { display: flex; align-items: center; justify-content: space-between; }
.card-icon-wrap {
  width: 32px; height: 32px; border-radius: 10px;
  background: linear-gradient(135deg, color-mix(in srgb, var(--accent) 8%, transparent), color-mix(in srgb, var(--accent) 14%, transparent));
  display: flex; align-items: center; justify-content: center; color: var(--accent);
  box-shadow: inset 0 1px 2px rgba(255,255,255,0.5), 0 1px 3px rgba(0,0,0,0.04);
}
.card-change {
  font-size: 11px; font-weight: 700; display: inline-flex; align-items: center; gap: 2px;
  padding: 3px 8px; border-radius: 6px;
}
.card-change.up { color: #3d6b48; background: rgba(67, 104, 80, 0.07); }
.card-change.down { color: #c94a45; background: rgba(217, 83, 79, 0.06); }

.card-value {
  font-size: 26px; font-weight: 800; color: #12372A;
  font-family: 'SF Mono', 'Consolas', 'JetBrains Mono', monospace;
  letter-spacing: -0.5px; line-height: 1;
}
.card-footer { display: flex; align-items: center; justify-content: space-between; }
.card-title { font-size: 12px; color: rgba(18, 55, 42, 0.45); font-weight: 500; }
.card-compare { font-size: 10px; color: rgba(18, 55, 42, 0.25); }
</style>