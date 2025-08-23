// API service for connecting frontend to backend
import axios from 'axios'

const API_BASE_URL = 'https://9yhyi3c8539k.manus.space/api'

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000, // 30 seconds timeout
    })

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response.data,
      (error) => {
        console.error('API Error:', error)
        if (error.response) {
          throw new Error(error.response.data.message || 'API request failed')
        } else if (error.request) {
          throw new Error('Network error - please check your connection')
        } else {
          throw new Error('Request failed')
        }
      }
    )
  }

  // Authentication
  async login(email, password) {
    return this.client.post('/auth/login', { email, password })
  }

  async register(userData) {
    return this.client.post('/auth/register', userData)
  }

  // Video generation
  async getVideoModels() {
    return this.client.get('/videos/models')
  }

  async generateVideo(videoData) {
    return this.client.post('/videos/generate', videoData)
  }

  async getVideoStatus(videoId) {
    return this.client.get(`/videos/${videoId}/status`)
  }

  async getVideoResult(videoId) {
    return this.client.get(`/videos/${videoId}`)
  }

  // Projects
  async getProjects() {
    return this.client.get('/projects')
  }

  async createProject(projectData) {
    return this.client.post('/projects', projectData)
  }

  async updateProject(projectId, projectData) {
    return this.client.put(`/projects/${projectId}`, projectData)
  }

  async deleteProject(projectId) {
    return this.client.delete(`/projects/${projectId}`)
  }

  // AI Actors
  async getActors() {
    return this.client.get('/actors')
  }

  async getActor(actorId) {
    return this.client.get(`/actors/${actorId}`)
  }

  // Voices
  async getVoices() {
    return this.client.get('/voices')
  }

  async generateVoice(voiceData) {
    return this.client.post('/voices/generate', voiceData)
  }

  async cloneVoice(voiceData) {
    return this.client.post('/voices/clone', voiceData)
  }

  // User
  async getUserProfile() {
    return this.client.get('/users/profile')
  }

  async updateUserProfile(userData) {
    return this.client.put('/users/profile', userData)
  }

  async getUserCredits() {
    return this.client.get('/users/credits')
  }
}

export default new ApiService()

