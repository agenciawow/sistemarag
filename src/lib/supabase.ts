import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

// Create a mock client when environment variables are missing
const createMockClient = () => ({
  auth: {
    signUp: () => Promise.reject(new Error('Please connect to Supabase first')),
    signInWithPassword: () => Promise.reject(new Error('Please connect to Supabase first')),
    signOut: () => Promise.reject(new Error('Please connect to Supabase first')),
    getSession: () => Promise.resolve({ data: { session: null }, error: null }),
    onAuthStateChange: () => ({ data: { subscription: { unsubscribe: () => {} } } })
  },
  from: () => ({
    select: () => Promise.reject(new Error('Please connect to Supabase first')),
    insert: () => Promise.reject(new Error('Please connect to Supabase first')),
    update: () => Promise.reject(new Error('Please connect to Supabase first')),
    delete: () => Promise.reject(new Error('Please connect to Supabase first'))
  })
})

export const supabase = (!supabaseUrl || !supabaseAnonKey) 
  ? createMockClient()
  : createClient(supabaseUrl, supabaseAnonKey, {
      auth: {
        autoRefreshToken: true,
        persistSession: true,
        detectSessionInUrl: true
      }
    })

export const isSupabaseConfigured = !!(supabaseUrl && supabaseAnonKey)