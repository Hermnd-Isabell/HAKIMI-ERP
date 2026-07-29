<template>
  <footer class="footer-bar">
    <span class="footer-text">HAKIMI ERP &mdash; SAP SD Simplified System</span>
    <span class="footer-divider">&middot;</span>
    <span class="footer-text">v1.0</span>
    <span class="footer-divider">&middot;</span>
    <span class="footer-text">&copy; 2026</span>
  </footer>
</template>

<style scoped>
.footer-bar {
  height: 40px;
  background-color: #FBFADA;
  border-top: 1px solid rgba(173, 188, 159, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  flex-shrink: 0;
}
.footer-text {
  font-size: 11px;
  color: rgba(18, 55, 42, 0.35);
  font-weight: 500;
  letter-spacing: 0.3px;
}
.footer-divider {
  color: rgba(18, 55, 42, 0.15);
  font-size: 14px;
}
</style>