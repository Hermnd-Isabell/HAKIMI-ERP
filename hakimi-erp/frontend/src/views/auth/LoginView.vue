<template>
  <main class="auth-page">
    <section class="auth-card">
      <div class="auth-brand">
        <div class="brand-mark">H</div>
        <div>
          <h1>HAKIMI ERP</h1>
          <p>Sign in to continue</p>
        </div>
      </div>

      <form class="auth-form" @submit.prevent="submit">
        <label class="field">
          <span>Account</span>
          <input v-model.trim="form.account" type="text" autocomplete="username" placeholder="Username or email" />
        </label>

        <label class="field">
          <span>Password</span>
          <input v-model="form.password" type="password" autocomplete="current-password" placeholder="Enter password" />
        </label>

        <label class="remember">
          <input v-model="form.rememberMe" type="checkbox" />
          <span>Remember login state</span>
        </label>

        <button class="submit" type="submit" :disabled="loading">
          {{ loading ? 'Signing in...' : 'Sign In' }}
        </button>
      </form>

      <p class="auth-switch">
        Don't have an account?
        <RouterLink to="/register">Create one</RouterLink>
      </p>
    </section>
  </main>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'
import { toast } from '@/utils/toast'

const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()
const loading = ref(false)

const form = reactive({
  account: '',
  password: '',
  rememberMe: true,
})

async function submit() {
  if (!form.account || !form.password) {
    toast.warning('Please enter account and password')
    return
  }

  loading.value = true
  try {
    await authStore.login({
      account: form.account,
      password: form.password,
      rememberMe: form.rememberMe,
    })
    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/'
    await router.replace(redirect)
  } catch (err: any) {
    toast.error(err?.message || 'Login failed')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px;
  background:
    radial-gradient(circle at 20% 20%, rgba(67, 104, 80, 0.12), transparent 34%),
    linear-gradient(135deg, #FBFADA 0%, #f4f0cf 100%);
}

.auth-card {
  width: 420px;
  background: linear-gradient(145deg, #fdfce8, #f7f5d1);
  border: 1px solid rgba(173, 188, 159, 0.28);
  border-radius: 22px;
  box-shadow: 0 24px 70px rgba(18, 55, 42, 0.16);
  padding: 34px 34px 26px;
}

.auth-brand {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 26px;
}

.brand-mark {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: linear-gradient(135deg, #436850, #2d4a38);
  color: #FBFADA;
  font-size: 24px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
}

.auth-brand h1 {
  margin: 0;
  color: #12372A;
  font-size: 20px;
  letter-spacing: 0.5px;
}

.auth-brand p {
  margin: 2px 0 0;
  color: rgba(18, 55, 42, 0.48);
  font-size: 13px;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 7px;
}

.field span {
  color: rgba(18, 55, 42, 0.58);
  font-size: 12px;
  font-weight: 700;
}

.field input {
  height: 42px;
  border: 1px solid rgba(173, 188, 159, 0.45);
  border-radius: 9px;
  padding: 0 13px;
  color: #12372A;
  background: rgba(251, 250, 218, 0.55);
  outline: none;
  font-family: inherit;
  font-size: 14px;
}

.field input:focus {
  border-color: #436850;
  background: #fff;
  box-shadow: 0 0 0 3px rgba(67, 104, 80, 0.08);
}

.remember {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(18, 55, 42, 0.62);
  font-size: 13px;
  cursor: pointer;
  user-select: none;
}

.remember input {
  width: 16px;
  height: 16px;
  accent-color: #436850;
}

.submit {
  height: 44px;
  border: none;
  border-radius: 10px;
  background: linear-gradient(135deg, #436850, #365440);
  color: #FBFADA;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 8px 20px rgba(67, 104, 80, 0.22);
  transition: all 0.2s;
  font-family: inherit;
}

.submit:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 10px 24px rgba(67, 104, 80, 0.3);
}

.submit:disabled {
  cursor: not-allowed;
  opacity: 0.62;
}

.auth-switch {
  margin: 22px 0 0;
  text-align: center;
  color: rgba(18, 55, 42, 0.55);
  font-size: 13px;
}

.auth-switch a {
  color: #436850;
  font-weight: 700;
  text-decoration: none;
}

.auth-switch a:hover {
  text-decoration: underline;
}
</style>
