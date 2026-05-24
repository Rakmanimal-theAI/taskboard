import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
    id: number
    name: string
    email: string
}

interface AuthStore {
    token: string | null
    user: User | null
    setToken: (token: string) => void
    setUser: (user: User) => void
    logout: () => void
}

const useAuthStore = create<AuthStore>()(
    persist<AuthStore>(
        (set) => ({
            token: null,
            user: null,
            setToken: (new_token) => set({ token: new_token }),
            setUser: (new_user) => set({user: new_user}),
            logout: () => set({ token: null, user: null }),
        }),
        { name: 'auth-storage' }
    )
)

export default useAuthStore
