import React, { useState } from 'react'
import { useAuth } from './hooks/useAuth'
import { LoginForm } from './components/LoginForm'
import { Dashboard } from './components/Dashboard'

function App() {
  const { user, loading, signIn, signUp, signOut } = useAuth()
  const [authLoading, setAuthLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleAuth = async (email: string, password: string, isSignUp: boolean) => {
    setAuthLoading(true)
    setError(null)

    try {
      const { error } = isSignUp 
        ? await signUp(email, password)
        : await signIn(email, password)

      if (error) {
        if (error.message.includes('Invalid login credentials')) {
          setError('Email ou senha incorretos')
        } else if (error.message.includes('User already registered')) {
          setError('Este email já está cadastrado. Tente fazer login.')
        } else if (error.message.includes('Password should be at least 6 characters')) {
          setError('A senha deve ter pelo menos 6 caracteres')
        } else {
          setError(error.message)
        }
      } else if (isSignUp) {
        setError('Conta criada com sucesso! Você já está logado.')
      }
    } catch (err) {
      setError('Erro inesperado. Tente novamente.')
    } finally {
      setAuthLoading(false)
    }
  }

  const handleSignOut = async () => {
    const { error } = await signOut()
    if (error) {
      setError('Erro ao sair. Tente novamente.')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="bg-white rounded-2xl shadow-xl p-8 flex flex-col items-center gap-4">
          <div className="w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-gray-600">Carregando...</p>
        </div>
      </div>
    )
  }

  if (user) {
    return <Dashboard user={user} onSignOut={handleSignOut} />
  }

  return (
    <LoginForm 
      onSubmit={handleAuth} 
      loading={authLoading} 
      error={error} 
    />
  )
}

export default App