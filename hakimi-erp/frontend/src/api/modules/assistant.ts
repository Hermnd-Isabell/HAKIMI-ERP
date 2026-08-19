import { post } from '../request'

const BASE = '/api/v1/assistant'

export interface ChatHistoryItem {
  role: 'user' | 'assistant'
  content: string
}

export interface NavigationTarget {
  label: string
  route: string
}

export interface ChatStep {
  icon: string
  text: string
}

export interface ChatReply {
  reply: string
  navigation: NavigationTarget | null
  suggestions: string[]
  steps: ChatStep[]
}

export function sendChatMessage(payload: {
  message: string
  history: ChatHistoryItem[]
  currentPath?: string
}) {
  // LLM responses are slower than normal CRUD calls; allow a longer timeout.
  return post<ChatReply>(`${BASE}/chat`, payload, { timeout: 90000 })
}
