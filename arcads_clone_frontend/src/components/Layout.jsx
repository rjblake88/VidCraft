import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { 
  Video, 
  Users, 
  Mic, 
  Settings, 
  CreditCard, 
  LogOut, 
  Menu,
  X,
  Sparkles,
  Play,
  BarChart3
} from 'lucide-react'
import '../App.css'

const Layout = ({ children, currentPage, onNavigate, user, onLogout }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const navigation = [
    { name: 'Dashboard', icon: Video, page: 'dashboard' },
    { name: 'Create Video', icon: Play, page: 'create' },
    ...(user?.is_admin ? [{ name: 'Analytics', icon: BarChart3, page: 'analytics' }] : []),
    { name: 'Templates', icon: Users, page: 'templates' },
    { name: 'AI Actors', icon: Users, page: 'actors' },
    { name: 'Voice Library', icon: Mic, page: 'voices' },
    { name: 'Settings', icon: Settings, page: 'settings' },
    { name: 'Billing', icon: CreditCard, page: 'billing' },
  ]
  return (
    <div className="min-h-screen bg-background">
      {/* Mobile sidebar backdrop */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black/50 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`
        fixed inset-y-0 left-0 z-50 w-64 bg-card border-r border-border transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        <div className="flex items-center justify-between h-16 px-6 border-b border-border">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 gradient-bg rounded-lg flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold text-foreground">VidCraft AI</span>
          </div>
          <Button
            variant="ghost"
            size="sm"
            className="lg:hidden"
            onClick={() => setSidebarOpen(false)}
          >
            <X className="w-5 h-5" />
          </Button>
        </div>

        <nav className="flex-1 px-4 py-6 space-y-2">
          {navigation.map((item) => {
            const Icon = item.icon
            return (
              <Button
                key={item.name}
                variant={currentPage === item.page ? "default" : "ghost"}
                className={`w-full justify-start ${
                  currentPage === item.page 
                    ? 'bg-primary text-primary-foreground' 
                    : 'text-muted-foreground hover:text-foreground hover:bg-accent'
                }`}
                onClick={() => {
                  onNavigate(item.page)
                  setSidebarOpen(false)
                }}
              >
                <Icon className="w-5 h-5 mr-3" />
                {item.name}
              </Button>
            )
          })}
        </nav>

        <div className="p-4 border-t border-border">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-10 h-10 bg-gradient-to-r from-primary to-secondary rounded-full flex items-center justify-center">
              <span className="text-sm font-medium text-white">
                {user?.name ? user.name.split(' ').map(n => n[0]).join('').toUpperCase() : 'U'}
              </span>
            </div>
            <div>
              <p className="text-sm font-medium text-foreground">
                {user?.name || 'User'}
              </p>
              <p className="text-xs text-muted-foreground">
                {user?.subscription || 'Free'} Plan • {user?.credits || 0} credits
              </p>
            </div>
          </div>
          <Button 
            variant="ghost" 
            className="w-full justify-start text-muted-foreground"
            onClick={onLogout}
          >
            <LogOut className="w-4 h-4 mr-3" />
            Sign Out
          </Button>
        </div>
      </div>

      {/* Main content */}
      <div className="lg:pl-64">
        {/* Page content */}
        <main className="min-h-screen">
          {children}
        </main>
      </div>
    </div>
  )
}

export default Layout

