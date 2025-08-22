import { useState, useEffect } from 'react'
import Layout from './components/Layout.jsx'
import Dashboard from './components/Dashboard.jsx'
import VideoCreator from './components/VideoCreator.jsx'
import Analytics from './components/Analytics.jsx'
import Auth from './components/Auth.jsx'
import Billing from './components/Billing.jsx'
import ContentLibrary from './components/ContentLibrary.jsx'
import AIActors from './components/AIActors.jsx'
import VoiceLibrary from './components/VoiceLibrary.jsx'
import Settings from './components/Settings.jsx'
import './App.css'

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard')
  const [user, setUser] = useState(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check for existing authentication
    const token = localStorage.getItem('authToken')
    const userData = localStorage.getItem('user')
    
    if (token && userData) {
      try {
        const parsedUser = JSON.parse(userData)
        setUser(parsedUser)
        setIsAuthenticated(true)
      } catch (error) {
        console.error('Error parsing user data:', error)
        localStorage.removeItem('authToken')
        localStorage.removeItem('user')
      }
    }
    
    setLoading(false)
  }, [])

  const handleAuthSuccess = (userData) => {
    setUser(userData)
    setIsAuthenticated(true)
  }

  const handleLogout = () => {
    localStorage.removeItem('authToken')
    localStorage.removeItem('user')
    setUser(null)
    setIsAuthenticated(false)
    setCurrentPage('dashboard')
  }

  const handleNavigate = (page) => {
    setCurrentPage(page)
  }

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard onNavigate={handleNavigate} />
      case 'create':
        return <VideoCreator />
      case 'analytics':
        return <Analytics />
      case 'actors':
        return <AIActors />
      case 'voices':
        return <VoiceLibrary />
      case 'templates':
        return <ContentLibrary />
      case 'settings':
        return <Settings user={user} onUserUpdate={setUser} />
      case 'billing':
        return <Billing />
      default:
        return <Dashboard onNavigate={handleNavigate} />
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return <Auth onAuthSuccess={handleAuthSuccess} />
  }

  return (
    <Layout 
      currentPage={currentPage} 
      onNavigate={handleNavigate}
      user={user}
      onLogout={handleLogout}
    >
      {renderPage()}
    </Layout>
  )
}

export default App
