import { create } from 'zustand'

const STORAGE_KEY = 'agentweave-config'

interface StoredConfig {
  apiKey: string
  hubUrl: string
  projectId: string
}

function loadFromStorage(): StoredConfig {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) return JSON.parse(raw) as StoredConfig
  } catch {}
  return { apiKey: '', hubUrl: 'http://localhost:8000', projectId: 'proj-default' }
}

function saveToStorage(config: StoredConfig) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(config))
  } catch {}
}

interface ConfigState extends StoredConfig {
  isConfigured: boolean
  setConfig: (apiKey: string, hubUrl: string, projectId: string) => void
  clearConfig: () => void
}

const initial = loadFromStorage()

export const useConfigStore = create<ConfigState>()((set) => ({
  ...initial,
  isConfigured: !!initial.apiKey,
  setConfig: (apiKey, hubUrl, projectId) => {
    saveToStorage({ apiKey, hubUrl, projectId })
    set({ apiKey, hubUrl, projectId, isConfigured: !!apiKey })
  },
  clearConfig: () => {
    localStorage.removeItem(STORAGE_KEY)
    set({ apiKey: '', hubUrl: 'http://localhost:8000', projectId: 'proj-default', isConfigured: false })
  },
}))
