import axios from 'axios';

// Prefer value from Vite env during development, fall back to production URL
const API_BASE_URL =
  (import.meta?.env?.VITE_API_BASE_URL) ||
  'https://9yhyi3c8539k.manus.space/api';

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add auth token to requests if available
    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('authToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  // Authentication methods
  async login(credentials) {
    try {
      const response = await this.client.post('/auth/v2/login', credentials);
      return response.data;
    } catch (error) {
      return { success: false, message: error.response?.data?.message || 'Login failed' };
    }
  }

  async register(userData) {
    try {
      const response = await this.client.post('/auth/v2/register', userData);
      return response.data;
    } catch (error) {
      return { success: false, message: error.response?.data?.message || 'Registration failed' };
    }
  }

  async logout() {
    try {
      await this.client.post('/auth/v2/logout');
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      return { success: true };
    } catch (error) {
      return { success: false, message: 'Logout failed' };
    }
  }

  // Video generation methods
  async getModels() {
    try {
      const response = await this.client.get('/videos/models');
      return response.data;
    } catch (error) {
      console.error('Error fetching models:', error);
      return [];
    }
  }

  async generateVideo(videoData) {
    try {
      const response = await this.client.post('/videos/generate', videoData);
      return response.data;
    } catch (error) {
      console.error('Error generating video:', error);
      throw error;
    }
  }

  async getVideoStatus(videoId) {
    try {
      const response = await this.client.get(`/videos/${videoId}/status`);
      return response.data;
    } catch (error) {
      console.error('Error getting video status:', error);
      throw error;
    }
  }

  // Actor methods
  async getActors() {
    try {
      const response = await this.client.get('/actors/');
      return response.data;
    } catch (error) {
      console.error('Error fetching actors:', error);
      return [];
    }
  }

  // Voice methods
  async getVoices() {
    try {
      const response = await this.client.get('/voices/');
      return response.data;
    } catch (error) {
      console.error('Error fetching voices:', error);
      return [];
    }
  }

  // Payment methods
  async getSubscriptionPlans() {
    try {
      const response = await this.client.get('/payments/subscription-plans');
      return response.data;
    } catch (error) {
      console.error('Error fetching subscription plans:', error);
      return [];
    }
  }

  async createSubscription(planId) {
    try {
      const response = await this.client.post('/payments/create-subscription', { plan_id: planId });
      return response.data;
    } catch (error) {
      console.error('Error creating subscription:', error);
      throw error;
    }
  }

  async purchaseCredits(amount) {
    try {
      const response = await this.client.post('/payments/purchase-credits', { amount });
      return response.data;
    } catch (error) {
      console.error('Error purchasing credits:', error);
      throw error;
    }
  }

  async getBillingHistory() {
    try {
      const response = await this.client.get('/payments/billing-history');
      return response.data;
    } catch (error) {
      console.error('Error fetching billing history:', error);
      return [];
    }
  }

  // Content methods
  async getTemplates() {
    try {
      const response = await this.client.get('/content/templates');
      return response.data;
    } catch (error) {
      console.error('Error fetching templates:', error);
      return [];
    }
  }

  async getAssets() {
    try {
      const response = await this.client.get('/content/assets');
      return response.data;
    } catch (error) {
      console.error('Error fetching assets:', error);
      return [];
    }
  }

  async getCategories() {
    try {
      const response = await this.client.get('/content/categories');
      return response.data;
    } catch (error) {
      console.error('Error fetching categories:', error);
      return [];
    }
  }

  // Analytics methods
  async getDashboardData() {
    try {
      const response = await this.client.get('/analytics/dashboard');
      return response.data;
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      return null;
    }
  }

  async trackEvent(eventData) {
    try {
      const response = await this.client.post('/analytics/track', eventData);
      return response.data;
    } catch (error) {
      console.error('Error tracking event:', error);
      return null;
    }
  }
}

const apiService = new ApiService();
export default apiService;

