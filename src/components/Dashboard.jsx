import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { 
  Plus, 
  Play, 
  MoreHorizontal, 
  Clock, 
  CheckCircle, 
  AlertCircle,
  TrendingUp,
  Video,
  Users,
  Zap
} from 'lucide-react'
import '../App.css'

const Dashboard = ({ onNavigate, user }) => {
  const [projects, setProjects] = useState([]);
  const [stats, setStats] = useState({
    totalVideos: 0,
    creditsUsed: 0,
    activeProjects: 0,
    successRate: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // For alpha testing, show empty state for new users
      // Real API calls would go here
      
      // Show user's actual subscription data
      const userStats = {
        totalVideos: 0, // Will be populated from real API
        creditsUsed: user?.subscription?.credits_used || 0,
        activeProjects: 0,
        successRate: 100.0
      };
      
      setStats(userStats);
      setProjects([]); // Empty for new users
      
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-4 h-4 text-green-600" />
      case 'processing':
        return <Clock className="w-4 h-4 text-yellow-600" />
      case 'draft':
        return <AlertCircle className="w-4 h-4 text-gray-600" />
      default:
        return null
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800'
      case 'processing':
        return 'bg-yellow-100 text-yellow-800'
      case 'draft':
        return 'bg-gray-100 text-gray-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  // Dynamic stats cards based on real user data
  const statsCards = [
    {
      title: "Total Videos",
      value: stats.totalVideos.toString(),
      change: stats.totalVideos > 0 ? "+100%" : "0%",
      icon: Video,
      color: "text-blue-600"
    },
    {
      title: "Credits Used",
      value: stats.creditsUsed.toString(),
      change: stats.creditsUsed > 0 ? `${stats.creditsUsed} used` : "0 used",
      icon: Zap,
      color: "text-purple-600"
    },
    {
      title: "Active Projects",
      value: stats.activeProjects.toString(),
      change: stats.activeProjects > 0 ? `+${stats.activeProjects}` : "0",
      icon: Users,
      color: "text-green-600"
    },
    {
      title: "Success Rate",
      value: `${stats.successRate}%`,
      change: stats.totalVideos > 0 ? "+100%" : "Perfect!",
      icon: TrendingUp,
      color: "text-orange-600"
    }
  ]

  return (
    <div className="p-6 space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Dashboard</h1>
          <p className="text-muted-foreground">Welcome back! Here's what's happening with your projects.</p>
        </div>
        <Button 
          className="gradient-bg text-white hover:opacity-90"
          onClick={() => onNavigate('create')}
        >
          <Plus className="w-4 h-4 mr-2" />
          Create Video
        </Button>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {statsCards.map((stat, index) => {
          const Icon = stat.icon
          return (
            <Card key={index} className="video-card-hover">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">{stat.title}</p>
                    <p className="text-2xl font-bold text-foreground">{stat.value}</p>
                    <p className="text-xs text-green-600 flex items-center mt-1">
                      <TrendingUp className="w-3 h-3 mr-1" />
                      {stat.change}
                    </p>
                  </div>
                  <div className={`p-3 rounded-lg bg-muted ${stat.color}`}>
                    <Icon className="w-6 h-6" />
                  </div>
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      {/* Recent Projects */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Recent Projects</CardTitle>
              <CardDescription>Your latest video generation projects</CardDescription>
            </div>
            <Button variant="outline" size="sm">
              View All
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          {projects.length === 0 ? (
            <div className="text-center py-12">
              <Video className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-foreground mb-2">No projects yet</h3>
              <p className="text-muted-foreground mb-4">Create your first AI-generated video to get started!</p>
              <Button 
                className="gradient-bg text-white hover:opacity-90"
                onClick={() => onNavigate('create')}
              >
                <Plus className="w-4 h-4 mr-2" />
                Create Your First Video
              </Button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {projects.map((project) => (
                <Card key={project.id} className="video-card-hover cursor-pointer">
                  <div className="relative">
                    <div className="aspect-video bg-muted rounded-t-lg flex items-center justify-center">
                      <Play className="w-12 h-12 text-muted-foreground" />
                    </div>
                    <div className="absolute top-2 right-2">
                      <Badge variant="secondary" className="text-xs">
                        {project.model}
                      </Badge>
                    </div>
                    <div className="absolute bottom-2 right-2">
                      <Badge variant="outline" className="text-xs bg-black/50 text-white border-white/20">
                        {project.duration}
                      </Badge>
                    </div>
                  </div>
                  <CardContent className="p-4">
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="font-semibold text-foreground line-clamp-1">{project.name}</h3>
                      <Button variant="ghost" size="sm" className="h-6 w-6 p-0">
                        <MoreHorizontal className="w-4 h-4" />
                      </Button>
                    </div>
                    <p className="text-sm text-muted-foreground mb-3 line-clamp-2">{project.description}</p>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        {getStatusIcon(project.status)}
                        <Badge className={`text-xs ${getStatusColor(project.status)}`}>
                          {project.status}
                        </Badge>
                      </div>
                      <span className="text-xs text-muted-foreground">{project.createdAt}</span>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="video-card-hover cursor-pointer" onClick={() => onNavigate('create')}>
          <CardContent className="p-4 text-center">
            <div className="w-10 h-10 gradient-bg rounded-lg flex items-center justify-center mx-auto mb-3">
              <Plus className="w-5 h-5 text-white" />
            </div>
            <h3 className="font-semibold text-foreground mb-2">Create New Video</h3>
            <p className="text-sm text-muted-foreground">Start a new video project with AI generation</p>
          </CardContent>
        </Card>

        <Card className="video-card-hover cursor-pointer" onClick={() => onNavigate('actors')}>
          <CardContent className="p-4 text-center">
            <div className="w-10 h-10 bg-secondary rounded-lg flex items-center justify-center mx-auto mb-3">
              <Users className="w-5 h-5 text-secondary-foreground" />
            </div>
            <h3 className="font-semibold text-foreground mb-2">Browse AI Actors</h3>
            <p className="text-sm text-muted-foreground">Explore our library of AI-generated actors</p>
          </CardContent>
        </Card>

        <Card className="video-card-hover cursor-pointer" onClick={() => onNavigate('voices')}>
          <CardContent className="p-4 text-center">
            <div className="w-10 h-10 bg-accent rounded-lg flex items-center justify-center mx-auto mb-3">
              <Zap className="w-5 h-5 text-accent-foreground" />
            </div>
            <h3 className="font-semibold text-foreground mb-2">Voice Library</h3>
            <p className="text-sm text-muted-foreground">Access premium voices and create custom clones</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default Dashboard

