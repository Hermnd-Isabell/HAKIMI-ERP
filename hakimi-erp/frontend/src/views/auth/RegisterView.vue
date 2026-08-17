<template>
  <main class="auth-page">
    <section class="auth-card">
      <div class="auth-brand">
        <div class="brand-mark">H</div>
        <div>
          <h1>Create Account</h1>
          <p>Register a new HAKIMI ERP user</p>
        </div>
      </div>

      <form class="auth-form" @submit.prevent="submit">
        <label class="field">
          <span>Username</span>
          <input v-model.trim="form.username" type="text" autocomplete="username" placeholder="At least 3 characters" />
        </label>

        <label class="field">
          <span>Email</span>
          <input v-model.trim="form.email" type="email" autocomplete="email" placeholder="name@company.com" />
        </label>

        <label class="field">
          <span>Full name</span>
          <input v-model.trim="form.fullName" type="text" autocomplete="name" placeholder="Optional" />
        </label>

        <label class="field">
          <span>Password</span>
          <input v-model="form.password" type="password" autocomplete="new-password" placeholder="At least 6 characters" />
        </label>

        <label class="field">
          <span>Confirm password</span>
          <input v-model="confirmPassword" type="password" autocomplete="new-password" placeholder="Repeat password" />
        </label>

        <button class="submit" type="submit" :disabled="loading">
          {{ loading ? 'Creating account...' : 'Create Account' }}
        </button>
      </form>

      <p class="auth-switch">
        Already have an account?
        <RouterLink to="/login">Sign in</RouterLink>
      </p>
    </section>
  </main>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'
import { toast } from '@/utils/toast'

const authStore = useAuthStore()
const router = useRouter()
const loading = ref(false)
const confirmPassword = ref('')

const form = reactive({
  username: '',
  email: '',
  fullName: '',
  password: '',
})

async function submit() {
  if (!form.username || !form.email || !form.password) {
    toast.warning('Please fill in username, email and password')
    return
  }
  if (form.password.length < 6) {
    toast.warning('Password must be at least 6 characters')
    return
  }
  if (form.password !== confirmPassword.value) {
    toast.warning('Passwords do not match')
    return
  }

  loading.value = true
  try {
    await authStore.register({
      username: form.username,
      email: form.email,
      password: form.password,
      fullName: form.fullName || undefined,
    })
    toast.success('Account created successfully')
    await router.replace('/')
  } catch (err: any) {
    toast.error(err?.message || 'Registration failed')
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
  width: 440px;
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
  gap: 15px;
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
  height: 40px;
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
