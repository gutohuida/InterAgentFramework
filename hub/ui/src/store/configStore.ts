import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface ConfigState {
  apiKey: string
  hubUrl: string
  projectId: string
  isConfigured: boolean
  _hasHydrated: boolean
  setConfig: (apiKey: string, hubUrl: string, projectId: string) => void
  clearConfig: () => void
  setHasHydrated: (v: boolean) => void
}

export const useConfigStore = create<ConfigState>()(
  persist(
    (set) => ({
      apiKey: '',
      hubUrl: 'http://localhost:8000',
      projectId: 'proj-default',
      isConfigured: false,
      _hasHydrated: false,
      setConfig: (apiKey, hubUrl, projectId) =>
        set({ apiKey, hubUrl, projectId, isConfigured: !!apiKey }),
      clearConfig: () =>
        set({ apiKey: '', hubUrl: 'http://localhost:8000', projectId: 'proj-default', isConfigured: false }),
      setHasHydrated: (v) => set({ _hasHydrated: v }),
    }),
    {
      name: 'agentweave-config',
      onRehydrateStorage: () => (state) => {
        state?.setHasHydrated(true)
      },
    }
  )
)
