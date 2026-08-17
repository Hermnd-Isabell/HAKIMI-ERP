<template>
  <header class="topbar">
    <div class="topbar-left">
      <h1 class="page-title">{{ pageTitle }}</h1>
    </div>
    <div class="topbar-right">
      <div class="global-search" ref="searchContainer">
        <svg class="search-icon" viewBox="0 0 20 20" width="16" height="16">
          <circle cx="9" cy="9" r="5.5" fill="none" stroke="currentColor" stroke-width="1.5"/>
          <path d="M13 13l4 4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <input
          type="text"
          v-model="searchQuery"
          @focus="showResults = true"
          @keydown.down.prevent="moveHighlight(1)"
          @keydown.up.prevent="moveHighlight(-1)"
          @keydown.enter="selectHighlighted"
          @keydown.esc="closeSearch"
          placeholder="Search pages and modules..."
          class="search-input"
        />
        <kbd class="search-kbd">Ctrl+K</kbd>
        <transition name="dropdown">
          <div class="search-dropdown" v-if="showResults && searchQuery">
            <div v-if="filteredPages.length === 0" class="no-results">
              No pages found for "{{ searchQuery }}"
            </div>
            <div v-else>
              <div class="dropdown-section-label">Pages</div>
              <div
                v-for="(page, index) in filteredPages"
                :key="page.path"
                class="search-result-item"
                :class="{ active: index === highlightIndex }"
                @mouseenter="highlightIndex = index"
                @click="navigateTo(page.path)"
              >
                <svg class="result-icon" viewBox="0 0 20 20" width="16" height="16" v-html="page.icon"></svg>
                <div class="result-content">
                  <span class="result-label" v-html="highlightText(page.label, searchQuery)"></span>
                  <span class="result-category">{{ page.category }}</span>
                </div>
                <svg class="result-arrow" viewBox="0 0 16 16" width="12" height="12">
                  <path d="M5 3l5 5-5 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
            </div>
          </div>
        </transition>
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
      <div ref="userMenuContainer" class="user-area" title="Account menu" @click.stop="toggleUserMenu">
        <div class="user-avatar">{{ authStore.initials || 'H' }}</div>
        <div class="user-info">
          <span class="user-name">{{ authStore.displayName }}</span>
          <span class="user-role">{{ authStore.user?.role || 'User' }}</span>
        </div>
        <svg viewBox="0 0 20 20" width="15" height="15" class="user-chevron" :class="{ open: userMenuVisible }">
          <path d="M7 13l-4-3 4-3M3 10h8M13 15l4-5-4-5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <transition name="user-menu">
          <div v-if="userMenuVisible" class="user-menu" @click.stop>
            <div class="user-menu-header">
              <div class="user-menu-avatar">{{ authStore.initials || 'H' }}</div>
              <div class="user-menu-meta">
                <span class="user-menu-name">{{ authStore.displayName }}</span>
                <span class="user-menu-account">@{{ authStore.user?.username || 'account' }}</span>
              </div>
            </div>
            <div class="user-menu-details">
              <div class="user-menu-detail-row">
                <span class="detail-label">Email</span>
                <span class="detail-value">{{ authStore.user?.email || '?' }}</span>
              </div>
              <div class="user-menu-detail-row">
                <span class="detail-label">Role</span>
                <span class="role-chip">{{ authStore.user?.role || 'User' }}</span>
              </div>
              <div class="user-menu-detail-row">
                <span class="detail-label">Status</span>
                <span class="status-chip" :class="{ inactive: authStore.user && !authStore.user.isActive }">
                  {{ authStore.user?.isActive === false ? 'Inactive' : 'Active' }}
                </span>
              </div>
            </div>
            <button type="button" class="logout-btn" @click="handleLogout">
              <svg viewBox="0 0 20 20" width="16" height="16">
                <path d="M8 17H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h3M13 14l3-4-3-4M11 10h5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              Sign out
            </button>
          </div>
        </transition>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const pageTitle = computed(() => (route.meta.title as string) || 'Dashboard')

// --- Search Index ---
interface SearchablePage {
  path: string
  label: string
  category: string
  icon: string
  keywords: string[]
}

const searchIndex: SearchablePage[] = [
  // Home
  {
    path: '/',
    label: 'Home / Dashboard',
    category: 'Overview',
    icon: '<path d="M3 10l7-7 7 7M5 8v7a1 1 0 0 0 1 1h3v-4h2v4h3a1 1 0 0 0 1-1V8" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
    keywords: ['home', 'dashboard', 'overview', 'main', 'start', 'homepage'],
  },
  // Customer Management
  {
    path: '/customer/bp',
    label: 'Business Partner',
    category: 'Customer Management',
    icon: '<circle cx="10" cy="7" r="2.5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M4 17c0-3.3 2.7-6 6-6s6 2.7 6 6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>',
    keywords: ['customer', 'business partner', 'bp', 'client', 'master data', 'partner'],
  },
  {
    path: '/customer/material',
    label: 'Material Master',
    category: 'Customer Management',
    icon: '<rect x="2" y="2" width="7" height="7" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.5"/><rect x="11" y="2" width="7" height="7" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.5"/><rect x="2" y="11" width="7" height="7" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.5"/><rect x="11" y="11" width="7" height="7" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.5"/>',
    keywords: ['material', 'product', 'item', 'master data', 'material master', 'sku'],
  },
  {
    path: '/customer/product',
    label: 'Product',
    category: 'Customer Management',
    icon: '<path d="M10 2l6 4v8l-6 4-6-4V6l6-4z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/><path d="M10 6v8M4 8l6 4 6-4" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>',
    keywords: ['product', 'product catalog', 'product list'],
  },
  {
    path: '/customer/pricing',
    label: 'Pricing Conditions',
    category: 'Customer Management',
    icon: '<circle cx="10" cy="10" r="7" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M10 6v4l3 2" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
    keywords: ['pricing', 'price', 'pricing conditions', 'cost', 'price list', 'discount'],
  },
  {
    path: '/customer/salesorg',
    label: 'Sales Organization',
    category: 'Customer Management',
    icon: '<path d="M3 17V7a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M7 9h6M7 13h4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>',
    keywords: ['sales organization', 'sales org', 'org', 'organization', 'sales area'],
  },
  // Sales Management
  {
    path: '/sales/inquiry',
    label: 'Inquiry Management',
    category: 'Sales Management',
    icon: '<path d="M6 3h8l4 4v10a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M14 3v4h4M7 10h6M7 14h4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>',
    keywords: ['inquiry', 'inquiry management', 'sales inquiry', 'rfq', 'request', 'quote request'],
  },
  {
    path: '/sales/quotation',
    label: 'Quotation Management',
    category: 'Sales Management',
    icon: '<path d="M5 3h10l4 4v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M13 3v4h4M7 11l2 2 4-4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
    keywords: ['quotation', 'quote', 'quotation management', 'bid', 'offer', 'proposal'],
  },
  {
    path: '/sales/orders',
    label: 'Sales Orders',
    category: 'Sales Management',
    icon: '<path d="M4 4h3l1 5h7l2-5h2M7 14a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm7 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
    keywords: ['order', 'sales order', 'orders', 'so', 'sales', 'order management'],
  },
  // Delivery Management
  {
    path: '/delivery/list',
    label: 'Delivery List',
    category: 'Delivery Management',
    icon: '<rect x="2" y="3" width="16" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M2 8h16M6 13h2" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>',
    keywords: ['delivery', 'delivery list', 'shipment', 'ship', 'outbound', 'dispatch', 'logistics'],
  },
  {
    path: '/delivery/monitor',
    label: 'Status Monitoring',
    category: 'Delivery Management',
    icon: '<rect x="2" y="2" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M6 14l3-4 2 2 3-5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
    keywords: ['monitor', 'status', 'tracking', 'delivery status', 'shipment tracking', 'logistics monitor'],
  },
  // Financial Management
  {
    path: '/finance/invoice',
    label: 'Invoice Management',
    category: 'Financial Management',
    icon: '<rect x="2" y="4" width="16" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M2 8h16M6 12h3" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>',
    keywords: ['invoice', 'billing', 'invoice management', 'bill', 'ar invoice', 'finance invoice'],
  },
  {
    path: '/finance/receivables',
    label: 'Receivables Management',
    category: 'Financial Management',
    icon: '<circle cx="10" cy="10" r="8" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M6 10h8M10 6v8" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>',
    keywords: ['receivable', 'ar', 'receivables management', 'account receivable', 'finance receivable', 'collection'],
  },
  {
    path: '/finance/unpaid',
    label: 'Unpaid Receivables',
    category: 'Financial Management',
    icon: '<circle cx="10" cy="10" r="8" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M10 6v4l-3 3" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
    keywords: ['unpaid', 'unpaid receivable', 'overdue', 'outstanding', 'pending payment', 'finance unpaid'],
  },
  // Report
  {
    path: '/report',
    label: 'Report Query',
    category: 'Report',
    icon: '<rect x="2" y="2" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M6 14l3-4 2 2 3-5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
    keywords: ['report', 'query', 'report query', 'analytics', 'statistics', 'data report'],
  },
  // Settings
  {
    path: '/settings',
    label: 'System Settings',
    category: 'Settings',
    icon: '<circle cx="10" cy="10" r="3" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M10 2v2M10 16v2M2 10h2M16 10h2M4.9 4.9l1.4 1.4M13.7 13.7l1.4 1.4M4.9 15.1l1.4-1.4M13.7 6.3l1.4-1.4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>',
    keywords: ['settings', 'system settings', 'config', 'configuration', 'system', 'preferences'],
  },
]

// --- Search Logic ---
const searchQuery = ref('')
const showResults = ref(false)
const highlightIndex = ref(-1)
const searchContainer = ref<HTMLElement | null>(null)
const userMenuContainer = ref<HTMLElement | null>(null)
const userMenuVisible = ref(false)

const filteredPages = computed(() => {
  const q = searchQuery.value.toLowerCase().trim()
  if (!q) return []
  return searchIndex.filter(page => {
    const labelMatch = page.label.toLowerCase().includes(q)
    const categoryMatch = page.category.toLowerCase().includes(q)
    const keywordMatch = page.keywords.some(k => k.toLowerCase().includes(q))
    return labelMatch || categoryMatch || keywordMatch
  })
})

function highlightText(text: string, query: string): string {
  const escaped = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  return text.replace(new RegExp(`(${escaped})`, 'gi'), '<mark>$1</mark>')
}

function moveHighlight(direction: number) {
  if (filteredPages.value.length === 0) return
  highlightIndex.value += direction
  if (highlightIndex.value < 0) highlightIndex.value = filteredPages.value.length - 1
  if (highlightIndex.value >= filteredPages.value.length) highlightIndex.value = 0
}

function selectHighlighted() {
  if (highlightIndex.value >= 0 && highlightIndex.value < filteredPages.value.length) {
    navigateTo(filteredPages.value[highlightIndex.value].path)
  }
}

function navigateTo(path: string) {
  searchQuery.value = ''
  showResults.value = false
  highlightIndex.value = -1
  closeUserMenu()
  router.push(path)
}

function toggleUserMenu() {
  userMenuVisible.value = !userMenuVisible.value
  if (userMenuVisible.value) closeSearch()
}

function closeUserMenu() {
  userMenuVisible.value = false
}

async function handleLogout() {
  closeUserMenu()
  await authStore.logout()
  await router.replace('/login')
}

function closeSearch() {
  showResults.value = false
  searchQuery.value = ''
  highlightIndex.value = -1
}

// Close dropdowns when clicking outside
function handleClickOutside(e: MouseEvent) {
  const target = e.target as Node
  if (searchContainer.value && !searchContainer.value.contains(target)) {
    closeSearch()
  }
  if (userMenuContainer.value && !userMenuContainer.value.contains(target)) {
    closeUserMenu()
  }
}

// Ctrl+K shortcut and Escape handling
function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') {
    closeSearch()
    closeUserMenu()
    return
  }
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault()
    const input = searchContainer.value?.querySelector('.search-input') as HTMLInputElement
    if (input) {
      input.focus()
      input.select()
    }
  }
}

watch(() => route.fullPath, () => {
  closeSearch()
  closeUserMenu()
})

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('keydown', handleKeydown)
})
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
  position: relative;
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

/* Search Dropdown */
.search-dropdown {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  right: 0;
  background: #fff;
  border: 1px solid rgba(173, 188, 159, 0.35);
  border-radius: 12px;
  box-shadow: 0 8px 28px rgba(18, 55, 42, 0.14);
  z-index: 10000;
  overflow: hidden;
  max-height: 400px;
  overflow-y: auto;
}
.dropdown-section-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: rgba(18, 55, 42, 0.4);
  padding: 10px 16px 4px;
}
.no-results {
  padding: 20px 16px;
  text-align: center;
  font-size: 13px;
  color: rgba(18, 55, 42, 0.4);
}
.search-result-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  cursor: pointer;
  transition: background-color 0.15s;
}
.search-result-item:hover, .search-result-item.active {
  background: rgba(173, 188, 159, 0.18);
}
.result-icon {
  color: rgba(18, 55, 42, 0.4);
  flex-shrink: 0;
}
.search-result-item.active .result-icon, .search-result-item:hover .result-icon {
  color: #436850;
}
.result-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1px;
  min-width: 0;
}
.result-label {
  font-size: 13px;
  color: #12372A;
  font-weight: 500;
}
.result-label :deep(mark) {
  background: rgba(67, 104, 80, 0.15);
  color: #436850;
  border-radius: 2px;
  padding: 0 1px;
  font-weight: 700;
}
.result-category {
  font-size: 11px;
  color: rgba(18, 55, 42, 0.35);
}
.result-arrow {
  color: rgba(18, 55, 42, 0.2);
  flex-shrink: 0;
  transition: color 0.15s;
}
.search-result-item.active .result-arrow, .search-result-item:hover .result-arrow {
  color: #436850;
}

/* Dropdown transition */
.dropdown-enter-active { transition: all 0.2s ease; }
.dropdown-leave-active { transition: all 0.15s ease; }
.dropdown-enter-from, .dropdown-leave-to {
  opacity: 0;
  transform: translateY(-6px);
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
  position: relative;
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
.user-chevron {
  color: rgba(18, 55, 42, 0.3);
  transition: transform 0.2s;
}
.user-chevron.open { transform: rotate(180deg); }

/* User profile dropdown */
.user-menu {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  width: 300px;
  background: #fffdf4;
  border: 1px solid rgba(173, 188, 159, 0.35);
  border-radius: 16px;
  box-shadow: 0 16px 44px rgba(18, 55, 42, 0.18);
  z-index: 10000;
  overflow: hidden;
}
.user-menu-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 18px 18px 14px;
  background: linear-gradient(135deg, #436850, #365440);
}
.user-menu-avatar {
  width: 46px;
  height: 46px;
  border-radius: 50%;
  background: rgba(251, 250, 218, 0.16);
  color: #FBFADA;
  font-size: 16px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  letter-spacing: 1px;
  border: 1px solid rgba(251, 250, 218, 0.28);
  flex-shrink: 0;
}
.user-menu-meta {
  display: flex;
  flex-direction: column;
  gap: 3px;
  min-width: 0;
}
.user-menu-name {
  color: #FBFADA;
  font-size: 15px;
  font-weight: 700;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.user-menu-account {
  color: rgba(251, 250, 218, 0.7);
  font-size: 12px;
}
.user-menu-details {
  padding: 8px 18px;
}
.user-menu-detail-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  padding: 10px 0;
  border-bottom: 1px solid rgba(173, 188, 159, 0.18);
}
.user-menu-detail-row:last-child { border-bottom: none; }
.detail-label {
  color: rgba(18, 55, 42, 0.45);
  font-size: 12px;
  font-weight: 600;
}
.detail-value {
  color: #12372A;
  font-size: 12px;
  text-align: right;
  overflow-wrap: anywhere;
  max-width: 180px;
}
.role-chip,
.status-chip {
  font-size: 11px;
  font-weight: 700;
  padding: 3px 9px;
  border-radius: 999px;
  white-space: nowrap;
}
.role-chip {
  background: rgba(67, 104, 80, 0.14);
  color: #436850;
}
.status-chip {
  background: rgba(67, 104, 80, 0.14);
  color: #436850;
}
.status-chip.inactive {
  background: rgba(217, 83, 79, 0.12);
  color: #D9534F;
}
.logout-btn {
  width: calc(100% - 24px);
  margin: 4px 12px 12px;
  height: 40px;
  border: 1px solid rgba(217, 83, 79, 0.22);
  border-radius: 9px;
  background: rgba(217, 83, 79, 0.06);
  color: #C0392B;
  font-size: 13px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.18s;
}
.logout-btn:hover {
  background: #D9534F;
  border-color: #D9534F;
  color: #fff;
}

/* User dropdown transition */
.user-menu-enter-active { transition: all 0.2s ease; }
.user-menu-leave-active { transition: all 0.15s ease; }
.user-menu-enter-from, .user-menu-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
