import { defineStore } from 'pinia'
import { ref } from 'vue'

import {
  sendChatMessage,
  type NavigationTarget,
} from '@/api/modules/assistant'

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  navigation?: NavigationTarget | null
  suggestions?: string[]
  isError?: boolean
}

const WELCOME: ChatMessage = {
  role: 'assistant',
  content:
    "Hi! I'm the HAKIMI assistant. Ask me where to find a page, what a feature does, or how the sales workflow fits together.",
  suggestions: [
    'Where can I see unpaid receivables?',
    'What is the order-to-cash process?',
    'Where do I create a sales order?',
  ],
}

export const useAssistantStore = defineStore('assistant', () => {
  const isOpen = ref(false)
  const loading = ref(false)
  const messages = ref<ChatMessage[]>([{ ...WELCOME }])

  function open() {
    isOpen.value = true
  }

  function close() {
    isOpen.value = false
  }

  function toggle() {
    isOpen.value = !isOpen.value
  }

  function reset() {
    messages.value = [{ ...WELCOME }]
  }

  async function ask(question: string, currentPath?: string) {
    const text = question.trim()
    if (!text || loading.value) return

    messages.value.push({ role: 'user', content: text })
    loading.value = true
    try {
      const history = messages.value
        .filter((m) => !m.isError && m !== messages.value[0])
        .slice(0, -1) // exclude the question just pushed; it goes in `message`
        .slice(-10)
        .map((m) => ({ role: m.role, content: m.content }))

      const reply = await sendChatMessage({
        message: text,
        history,
        currentPath,
      })

      messages.value.push({
        role: 'assistant',
        content: reply.reply,
        navigation: reply.navigation,
        suggestions: reply.suggestions,
      })
    } catch (err: any) {
      messages.value.push({
        role: 'assistant',
        content: err?.message || 'The assistant is unavailable right now. Please try again later.',
        isError: true,
      })
    } finally {
      loading.value = false
    }
  }

  return { isOpen, loading, messages, open, close, toggle, reset, ask }
})
