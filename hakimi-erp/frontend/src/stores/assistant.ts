import { defineStore } from 'pinia'
import { ref } from 'vue'

import {
  sendChatMessage,
  type ChatStep,
  type NavigationTarget,
} from '@/api/modules/assistant'

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  navigation?: NavigationTarget | null
  suggestions?: string[]
  steps?: ChatStep[]
  isError?: boolean
}

const WELCOME: ChatMessage = {
  role: 'assistant',
  content:
    "Hi! I'm the HAKIMI order-to-cash assistant. Give me a sales order number and I'll run it from picking all the way to settlement — or guide you step by step.",
  suggestions: [
    '把 SO00104 从拣配一路跑到平帐',
    '先给 SO00105 拣 50 件',
    '随便挑一笔开放订单跑全流程',
  ],
}

function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms))
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

      if (reply.steps && reply.steps.length > 0) {
        // Scripted demo flow: reveal the execution steps one by one so the
        // assistant looks like an agent working through tool calls.
        messages.value.push({
          role: 'assistant',
          content: '',
          navigation: null,
          suggestions: [],
          steps: [],
        })
        const live = messages.value[messages.value.length - 1]
        for (const step of reply.steps) {
          await sleep(650)
          live.steps!.push(step)
        }
        await sleep(350)
        live.content = reply.reply
        live.navigation = reply.navigation
        live.suggestions = reply.suggestions
      } else {
        messages.value.push({
          role: 'assistant',
          content: reply.reply,
          navigation: reply.navigation,
          suggestions: reply.suggestions,
        })
      }
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
