import React, { useState, useEffect } from 'react';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import '../App.css';

const Analytics = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState(30);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    fetchDashboardData();
  }, [timeRange]);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      // For demo purposes, we'll use mock data since we need admin access
      const mockData = generateMockData();
      setDashboardData(mockData);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const generateMockData = () => {
    const days = timeRange;
    const userGrowth = [];
    const revenueTrend = [];
    const videoTrend = [];
    
    for (let i = days; i >= 0; i--) {
      const date = new Date();
      date.setDate(date.getDate() - i);
      const dateStr = date.toISOString().split('T')[0];
      
      userGrowth.push({
        date: dateStr,
        new_users: Math.floor(Math.random() * 20) + 5,
        active_users: Math.floor(Math.random() * 100) + 50,
        total_users: 1000 + (days - i) * 10
      });
      
      revenueTrend.push({
        date: dateStr,
        revenue: Math.floor(Math.random() * 1000) + 500,
        subscriptions: Math.floor(Math.random() * 10) + 2,
        credits: Math.floor(Math.random() * 300) + 100
      });
      
      videoTrend.push({
        date: dateStr,
        videos: Math.floor(Math.random() * 200) + 100,
        credits_used: Math.floor(Math.random() * 500) + 200,
        avg_duration: Math.floor(Math.random() * 20) + 10
      });
    }

    return {
      overview: {
        total_users: 2547,
        total_videos: 15623,
        total_revenue: 45230.50,
        active_sessions: 127
      },
      user_growth: userGrowth,
      revenue_trend: revenueTrend,
      video_trend: videoTrend,
      top_templates: [
        { name: 'Product Launch', usage: 1250 },
        { name: 'Social Media Promo', usage: 980 },
        { name: 'Educational Explainer', usage: 756 },
        { name: 'Customer Testimonial', usage: 634 },
        { name: 'Event Invitation', usage: 523 }
      ],
      model_usage: [
        { name: 'Kling AI', value: 35, color: '#8884d8' },
        { name: 'Runway', value: 28, color: '#82ca9d' },
        { name: 'Veo2', value: 22, color: '#ffc658' },
        { name: 'Luma', value: 15, color: '#ff7300' }
      ]
    };
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(value);
  };

  const formatNumber = (value) => {
    return new Intl.NumberFormat('en-US').format(value);
  };

  if (loading) {
    return (
      <div className="analytics-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading analytics...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="analytics-container">
      <div className="analytics-header">
        <h1>Analytics Dashboard</h1>
        <div className="time-range-selector">
          <select 
            value={timeRange} 
            onChange={(e) => setTimeRange(parseInt(e.target.value))}
            className="time-range-select"
          >
            <option value={7}>Last 7 days</option>
            <option value={30}>Last 30 days</option>
            <option value={90}>Last 90 days</option>
          </select>
        </div>
      </div>

      <div className="analytics-tabs">
        <button 
          className={`tab-button ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button 
          className={`tab-button ${activeTab === 'users' ? 'active' : ''}`}
          onClick={() => setActiveTab('users')}
        >
          Users
        </button>
        <button 
          className={`tab-button ${activeTab === 'revenue' ? 'active' : ''}`}
          onClick={() => setActiveTab('revenue')}
        >
          Revenue
        </button>
        <button 
          className={`tab-button ${activeTab === 'content' ? 'active' : ''}`}
          onClick={() => setActiveTab('content')}
        >
          Content
        </button>
      </div>

      {activeTab === 'overview' && (
        <div className="analytics-content">
          {/* Key Metrics */}
          <div className="metrics-grid">
            <div className="metric-card">
              <div className="metric-icon">👥</div>
              <div className="metric-content">
                <h3>Total Users</h3>
                <p className="metric-value">{formatNumber(dashboardData.overview.total_users)}</p>
                <span className="metric-change positive">+12.5%</span>
              </div>
            </div>
            <div className="metric-card">
              <div className="metric-icon">🎬</div>
              <div className="metric-content">
                <h3>Videos Generated</h3>
                <p className="metric-value">{formatNumber(dashboardData.overview.total_videos)}</p>
                <span className="metric-change positive">+8.3%</span>
              </div>
            </div>
            <div className="metric-card">
              <div className="metric-icon">💰</div>
              <div className="metric-content">
                <h3>Total Revenue</h3>
                <p className="metric-value">{formatCurrency(dashboardData.overview.total_revenue)}</p>
                <span className="metric-change positive">+15.7%</span>
              </div>
            </div>
            <div className="metric-card">
              <div className="metric-icon">⚡</div>
              <div className="metric-content">
                <h3>Active Sessions</h3>
                <p className="metric-value">{formatNumber(dashboardData.overview.active_sessions)}</p>
                <span className="metric-change neutral">Real-time</span>
              </div>
            </div>
          </div>

          {/* Charts */}
          <div className="charts-grid">
            <div className="chart-card">
              <h3>User Growth</h3>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={dashboardData.user_growth}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Area type="monotone" dataKey="new_users" stackId="1" stroke="#8884d8" fill="#8884d8" />
                  <Area type="monotone" dataKey="active_users" stackId="1" stroke="#82ca9d" fill="#82ca9d" />
                </AreaChart>
              </ResponsiveContainer>
            </div>

            <div className="chart-card">
              <h3>Revenue Trend</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={dashboardData.revenue_trend}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip formatter={(value) => formatCurrency(value)} />
                  <Legend />
                  <Line type="monotone" dataKey="revenue" stroke="#8884d8" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </div>

            <div className="chart-card">
              <h3>Video Generation</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={dashboardData.video_trend}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="videos" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="chart-card">
              <h3>AI Model Usage</h3>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={dashboardData.model_usage}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {dashboardData.model_usage.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Top Templates */}
          <div className="chart-card">
            <h3>Top Templates</h3>
            <div className="template-list">
              {dashboardData.top_templates.map((template, index) => (
                <div key={index} className="template-item">
                  <span className="template-rank">#{index + 1}</span>
                  <span className="template-name">{template.name}</span>
                  <span className="template-usage">{formatNumber(template.usage)} uses</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {activeTab === 'users' && (
        <div className="analytics-content">
          <div className="chart-card">
            <h3>User Registration Trend</h3>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={dashboardData.user_growth}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="new_users" stroke="#8884d8" strokeWidth={2} />
                <Line type="monotone" dataKey="active_users" stroke="#82ca9d" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {activeTab === 'revenue' && (
        <div className="analytics-content">
          <div className="chart-card">
            <h3>Revenue Analysis</h3>
            <ResponsiveContainer width="100%" height={400}>
              <AreaChart data={dashboardData.revenue_trend}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip formatter={(value) => formatCurrency(value)} />
                <Legend />
                <Area type="monotone" dataKey="revenue" stroke="#8884d8" fill="#8884d8" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {activeTab === 'content' && (
        <div className="analytics-content">
          <div className="charts-grid">
            <div className="chart-card">
              <h3>Video Generation Trend</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={dashboardData.video_trend}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="videos" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="chart-card">
              <h3>AI Model Distribution</h3>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={dashboardData.model_usage}
                    cx="50%"
                    cy="50%"
                    outerRadius={100}
                    fill="#8884d8"
                    dataKey="value"
                    label={({ name, value }) => `${name}: ${value}%`}
                  >
                    {dashboardData.model_usage.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Analytics;

