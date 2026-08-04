<template>
  <router-view />
</template>

<script setup lang="ts">
</script>

<style>
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  height: 100%;
  overflow: hidden;
}

body {
  font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif;
  font-size: 13px;
  color: #12372A;
  background: linear-gradient(135deg, #FBFADA 0%, #f5f3d8 100%);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  height: 100%;
}

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(173, 188, 159, 0.45); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(173, 188, 159, 0.7); }

::selection {
  background-color: rgba(67, 104, 80, 0.18);
  color: #12372A;
}

/* Toast - fixed bottom bar style per UX spec */
.hakimi-toast-bottom.el-message {
  top: auto !important;
  bottom: 24px !important;
  left: 50% !important;
  transform: translateX(-50%) !important;
  min-width: 320px;
  max-width: 560px;
  padding: 12px 18px;
  border-radius: 8px;
  background: #12372A;
  border: 1px solid rgba(67, 104, 80, 0.3);
  box-shadow: 0 6px 24px rgba(18, 55, 42, 0.22);
}

.hakimi-toast-bottom.el-message .el-message__content {
  color: #FBFADA;
  font-size: 13px;
  font-weight: 500;
}

.hakimi-toast-bottom.el-message .el-message__icon {
  color: #FBFADA;
}

.hakimi-toast-bottom.el-message--success {
  background: #436850;
  border-color: rgba(67, 104, 80, 0.5);
}

.hakimi-toast-bottom.el-message--error {
  background: #D9534F;
  border-color: rgba(217, 83, 79, 0.5);
}

.hakimi-toast-bottom.el-message--warning {
  background: #F0AD4E;
  border-color: rgba(240, 173, 78, 0.5);
}

.hakimi-confirm-dialog .el-message-box__title {
  color: #12372A;
}

.hakimi-alert-dialog .el-message-box__title {
  color: #12372A;
}
</style>