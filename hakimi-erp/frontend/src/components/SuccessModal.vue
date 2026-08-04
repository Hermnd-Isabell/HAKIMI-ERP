<template>
  <Teleport to="body">
    <div class="modal-overlay" v-if="visible" @click.self="close">
      <div class="sm-card">
        <div class="sm-top">
          <div class="sm-check-circle">
            <svg viewBox="0 0 32 32" width="24" height="24"><path d="M8 16l6 6 10-10" fill="none" stroke="#FBFADA" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </div>
          <h3 class="sm-title">{{ title }}</h3>
        </div>
        <div class="sm-divider"></div>
        <div class="sm-body">
          <div class="sm-doc-wrap">
            <svg viewBox="0 0 36 36" width="36" height="36"><rect x="6" y="4" width="22" height="27" rx="3" fill="none" stroke="#436850" stroke-width="1.6"/><path d="M16 4v6h-6M14 16h10M14 20h8M14 24h6" fill="none" stroke="#436850" stroke-width="1.3" stroke-linecap="round"/></svg>
            <div class="sm-doc-badge"><svg viewBox="0 0 14 14" width="8" height="8"><path d="M3 7l3 3 5-5" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
          </div>
          <div class="sm-msg">
            <p class="sm-line1">{{ message }}</p>
            <p class="sm-line2" v-if="subtitle">{{ subtitle }}</p>
          </div>
        </div>
        <div class="sm-footer">
          <button class="btn btn-secondary" @click="close">{{ displayLabel }}</button>
          <button class="btn btn-primary" @click="confirm">{{ actionLabel }}</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  visible?: boolean
  title?: string
  message?: string
  subtitle?: string
  actionLabel?: string
  displayLabel?: string
}>(), {
  visible: false,
  title: 'Success',
  message: 'Operation completed successfully',
  subtitle: '',
  actionLabel: 'OK',
  displayLabel: 'Display'
})
const emit = defineEmits<{
  'update:visible': [v: boolean]
  confirm: []
}>()
function close() { emit('update:visible', false) }
function confirm() { emit('confirm'); emit('update:visible', false) }
</script>

<style scoped>
.modal-overlay{position:fixed;inset:0;background:rgba(18,55,42,0.3);backdrop-filter:blur(4px);display:flex;align-items:center;justify-content:center;z-index:2000;}
.sm-card{width:460px;background:linear-gradient(145deg,#fdfce8,#f7f5d1);border-radius:18px;box-shadow:0 20px 60px rgba(18,55,42,0.22);border:1px solid rgba(173,188,159,0.2);overflow:hidden;}
.sm-top{display:flex;align-items:center;gap:14px;padding:24px 28px 16px;}
.sm-check-circle{width:44px;height:44px;border-radius:50%;background:#436850;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.sm-title{font-size:22px;font-weight:800;color:#436850;margin:0;}
.sm-divider{height:2px;background:rgba(67,104,80,0.12);margin:0 28px;}
.sm-body{display:flex;align-items:center;gap:18px;padding:20px 28px;}
.sm-doc-wrap{position:relative;flex-shrink:0;}
.sm-doc-badge{position:absolute;bottom:-3px;right:-3px;width:18px;height:18px;border-radius:50%;background:#436850;display:flex;align-items:center;justify-content:center;border:2px solid #FBFADA;}
.sm-msg{display:flex;flex-direction:column;gap:2px;}
.sm-line1{font-size:14px;font-weight:600;color:#12372A;margin:0;}
.sm-line2{font-size:14px;color:rgba(18,55,42,0.55);margin:0;}
.sm-footer{display:flex;justify-content:flex-end;gap:10px;padding:14px 28px;background:rgba(251,250,218,0.25);border-top:1px solid rgba(173,188,159,0.1);}
.btn{display:inline-flex;align-items:center;gap:6px;padding:10px 24px;font-size:13px;font-weight:600;border-radius:8px;cursor:pointer;transition:all 0.2s;font-family:inherit;}
.btn-primary{background:#436850;color:#FBFADA;border:none;}
.btn-primary:hover{background:#365440;}
.btn-secondary{background:rgba(173,188,159,0.2);color:#436850;border:1px solid rgba(173,188,159,0.3);}
.btn-secondary:hover{background:rgba(173,188,159,0.3);}
</style>
