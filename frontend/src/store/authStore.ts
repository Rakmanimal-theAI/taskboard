import { create } from 'zustand'

interface AuthStore {
    token: string | null
    user: string | null
    setToken: (token: string) => void
    logout: () => void
}

const useAuthStore = create<AuthStore>((set) => ({
    token: null,
    user: null,
    setToken: (new_token) => set({ token: new_token }),
    logout: () => set({ token: null, user: null }),
}))

export default useAuthStore
