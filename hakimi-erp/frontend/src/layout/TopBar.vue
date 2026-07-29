<template>
  <header class="topbar">
    <div class="topbar-left">
      <h1 class="page-title">{{ pageTitle }}</h1>
    </div>
    <div class="topbar-right">
      <div class="global-search">
        <svg class="search-icon" viewBox="0 0 20 20" width="16" height="16">
          <circle cx="9" cy="9" r="5.5" fill="none" stroke="currentColor" stroke-width="1.5"/>
          <path d="M13 13l4 4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <input type="text" placeholder="Search orders, invoices, customers..." class="search-input" />
        <kbd class="search-kbd">Ctrl+K</kbd>
      </div>
      <button class="topbar-btn" title="Notifications">
        <svg viewBox="0 0 20 20" width="19" height="19">
          <path d="M8 3a5 5 0 0 0-5 5v3l-1 2h16l-1-2V8a5 5 0 0 0-5-5M8 3V2a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v1" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M9 17a1.5 1.5 0 0 0 2.5 1" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <span class="badge">3</span>
      </button>
      <button class="topbar-btn" title="Help">
        <svg viewBox="0 0 20 20" width="19" height="19">
          <circle cx="10" cy="10" r="8" fill="none" stroke="currentColor" stroke-width="1.5"/>
          <path d="M7.5 8a2.5 2.5 0 0 1 4.2-1.8c.8.7.8 2 .1 2.8l-.8.8V11" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <circle cx="10" cy="14" r="0.75" fill="currentColor"/>
        </svg>
      </button>
      <div class="user-area">
        <div class="user-avatar">SA</div>
        <div class="user-info">
          <span class="user-name">Sales Admin</span>
          <span class="user-role">Administrator</span>
        </div>
        <svg viewBox="0 0 20 20" width="14" height="14" class="user-chevron">
          <path d="M6 8l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const pageTitle = computed(() => (route.meta.title as string) || 'Dashboard')
</script>

<style scoped>
.topbar {
  height: 56px;
  background-color: #FBFADA;
  border-bottom: 1px solid rgba(173, 188, 159, 0.3);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 28px;
  flex-shrink: 0;
}
.topbar-left { display: flex; align-items: center; }
.page-title { font-size: 20px; font-weight: 700; color: #12372A; margin: 0; letter-spacing: -0.3px; }
.topbar-right { display: flex; align-items: center; gap: 8px; }

.global-search {
  display: flex;
  align-items: center;
  background: rgba(173, 188, 159, 0.15);
  border: 1px solid rgba(173, 188, 159, 0.3);
  border-radius: 10px;
  padding: 7px 14px;
  gap: 8px;
  min-width: 300px;
  transition: all 0.2s;
}
.global-search:focus-within {
  border-color: #436850;
  background: #fff;
  box-shadow: 0 0 0 3px rgba(67, 104, 80, 0.08);
}
.search-icon { color: rgba(18, 55, 42, 0.3); flex-shrink: 0; }
.search-input {
  border: none;
  background: transparent;
  font-size: 13px;
  color: #12372A;
  outline: none;
  flex: 1;
  font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif;
}
.search-input::placeholder { color: rgba(18, 55, 42, 0.3); }
.search-kbd {
  font-size: 10px;
  background: rgba(173, 188, 159, 0.25);
  border-radius: 4px;
  padding: 2px 7px;
  color: rgba(18, 55, 42, 0.4);
  font-family: 'SF Mono', Consolas, monospace;
  letter-spacing: 0.5px;
}

.topbar-btn {
  position: relative;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  color: rgba(18, 55, 42, 0.45);
  transition: all 0.2s;
}
.topbar-btn:hover { background: rgba(173, 188, 159, 0.25); color: #12372A; }
.badge {
  position: absolute;
  top: 3px;
  right: 3px;
  background: #D9534F;
  color: #fff;
  font-size: 10px;
  min-width: 17px;
  height: 17px;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  padding: 0 4px;
  border: 2px solid #FBFADA;
}

.user-area {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 4px 10px 4px 6px;
  border-radius: 10px;
  transition: background-color 0.2s;
  margin-left: 4px;
}
.user-area:hover { background: rgba(173, 188, 159, 0.2); }
.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #436850, #2d4a38);
  color: #FBFADA;
  font-size: 12px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  letter-spacing: 1px;
}
.user-info { display: flex; flex-direction: column; line-height: 1.2; }
.user-name { font-size: 13px; color: #12372A; font-weight: 600; }
.user-role { font-size: 11px; color: rgba(18, 55, 42, 0.45); }
.user-chevron { color: rgba(18, 55, 42, 0.3); }
</style>