import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Slider } from '@/components/ui/slider.jsx'
import { 
  Play, 
  Pause, 
  RotateCcw, 
  Download, 
  Settings, 
  Wand2,
  Clock,
  Zap,
  Star,
  Users,
  Mic,
  CheckCircle,
  AlertCircle
} from 'lucide-react'
import apiService from '../services/api.js'
import '../App.css'

const VideoCreator = () => {
  const [script, setScript] = useState('')
  const [selectedModel, setSelectedModel] = useState('')
  const [selectedActor, setSelectedActor] = useState('')
  const [selectedVoice, setSelectedVoice] = useState('')
  const [duration, setDuration] = useState([8])
  const [isGenerating, setIsGenerating] = useState(false)
  const [generationStatus, setGenerationStatus] = useState('')
  const [videoResult, setVideoResult] = useState(null)
  const [error, setError] = useState('')

  // Data from API
  const [models, setModels] = useState([])
  const [actors, setActors] = useState([])
  const [voices, setVoices] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadInitialData()
  }, [])

  const loadInitialData = async () => {
    try {
      setLoading(true)
      
      // Load models from API
      const modelsResponse = await apiService.getVideoModels()
      if (modelsResponse.success) {
        setModels(modelsResponse.data.models)
      }

      // Load actors from API
      const actorsResponse = await apiService.getActors()
      if (actorsResponse.success) {
        setActors(actorsResponse.data.actors)
      }

      // Load voices from API
      const voicesResponse = await apiService.getVoices()
      if (voicesResponse.success) {
        setVoices(voicesResponse.data.voices)
      }

    } catch (error) {
      console.error('Failed to load initial data:', error)
      setError('Failed to load data. Please refresh the page.')
    } finally {
      setLoading(false)
    }
  }

  const handleGenerate = async () => {
    if (!script || !selectedModel || !selectedActor || !selectedVoice) {
      setError('Please fill in all required fields')
      return
    }

    try {
      setIsGenerating(true)
      setError('')
      setGenerationStatus('Initializing video generation...')

      const videoData = {
        script,
        model_id: selectedModel,
        actor_id: selectedActor,
        voice_id: selectedVoice,
        duration: duration[0],
        settings: {
          quality: 'high',
          aspect_ratio: '16:9'
        }
      }

      const response = await apiService.generateVideo(videoData)
      
      if (response.success) {
        const videoId = response.data.video_id
        setGenerationStatus('Video generation started...')
        
        // Poll for status updates
        pollVideoStatus(videoId)
      } else {
        throw new Error(response.message || 'Failed to start video generation')
      }

    } catch (error) {
      console.error('Video generation failed:', error)
      setError(error.message || 'Failed to generate video')
      setIsGenerating(false)
      setGenerationStatus('')
    }
  }

  const pollVideoStatus = async (videoId) => {
    const pollInterval = setInterval(async () => {
      try {
        const statusResponse = await apiService.getVideoStatus(videoId)
        
        if (statusResponse.success) {
          const status = statusResponse.data.status
          setGenerationStatus(statusResponse.data.message || `Status: ${status}`)
          
          if (status === 'completed') {
            clearInterval(pollInterval)
            const resultResponse = await apiService.getVideoResult(videoId)
            
            if (resultResponse.success) {
              setVideoResult(resultResponse.data)
              setGenerationStatus('Video generation completed!')
            }
            setIsGenerating(false)
          } else if (status === 'failed') {
            clearInterval(pollInterval)
            setError('Video generation failed')
            setIsGenerating(false)
            setGenerationStatus('')
          }
        }
      } catch (error) {
        console.error('Failed to check video status:', error)
        clearInterval(pollInterval)
        setError('Failed to check generation status')
        setIsGenerating(false)
        setGenerationStatus('')
      }
    }, 3000) // Poll every 3 seconds

    // Stop polling after 10 minutes
    setTimeout(() => {
      clearInterval(pollInterval)
      if (isGenerating) {
        setError('Video generation timed out')
        setIsGenerating(false)
        setGenerationStatus('')
      }
    }, 600000)
  }

  const calculateCredits = () => {
    const model = models.find(m => m.id === selectedModel)
    if (!model) return 0
    return Math.round(duration[0] * model.credits_per_second)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading video creation tools...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Create Video</h1>
          <p className="text-muted-foreground">Generate professional videos with AI in minutes</p>
        </div>
        <div className="flex items-center space-x-2">
          <Badge variant="outline" className="text-sm">
            <Zap className="w-3 h-3 mr-1" />
            150 credits remaining
          </Badge>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="p-4 bg-destructive/10 border border-destructive/20 rounded-lg flex items-center">
          <AlertCircle className="w-5 h-5 text-destructive mr-2" />
          <span className="text-destructive">{error}</span>
        </div>
      )}

      {/* Generation Status */}
      {generationStatus && (
        <div className="p-4 bg-primary/10 border border-primary/20 rounded-lg flex items-center">
          <div className="w-4 h-4 border-2 border-primary border-t-transparent rounded-full animate-spin mr-2"></div>
          <span className="text-primary">{generationStatus}</span>
        </div>
      )}

      {/* Success Message */}
      {videoResult && (
        <div className="p-4 bg-green-50 border border-green-200 rounded-lg flex items-center">
          <CheckCircle className="w-5 h-5 text-green-600 mr-2" />
          <span className="text-green-800">Video generated successfully!</span>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Panel - Script & Settings */}
        <div className="lg:col-span-1 space-y-6">
          {/* Script Input */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Wand2 className="w-5 h-5 mr-2" />
                Script
              </CardTitle>
              <CardDescription>Write your video script or let AI help you</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Textarea
                placeholder="Enter your video script here... For example: 'Welcome to our amazing summer collection! Discover the latest trends in fashion with our premium quality clothing designed for comfort and style.'"
                value={script}
                onChange={(e) => setScript(e.target.value)}
                className="min-h-[120px] resize-none"
              />
              <div className="flex justify-between items-center text-sm text-muted-foreground">
                <span>{script.length} characters</span>
                <Button variant="outline" size="sm">
                  <Wand2 className="w-3 h-3 mr-1" />
                  AI Enhance
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Model Selection */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Settings className="w-5 h-5 mr-2" />
                AI Model
              </CardTitle>
              <CardDescription>Choose the best model for your needs</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Select value={selectedModel} onValueChange={setSelectedModel}>
                <SelectTrigger>
                  <SelectValue placeholder="Select AI model" />
                </SelectTrigger>
                <SelectContent>
                  {models.map((model) => (
                    <SelectItem key={model.id} value={model.id}>
                      <div className="flex items-center justify-between w-full">
                        <div>
                          <div className="font-medium">{model.name}</div>
                          <div className="text-xs text-muted-foreground">{model.provider}</div>
                        </div>
                        <div className="flex items-center space-x-2 ml-4">
                          <div className="flex items-center">
                            <Star className="w-3 h-3 text-yellow-500 mr-1" />
                            <span className="text-xs">{model.quality_rating}</span>
                          </div>
                          <Badge variant="outline" className="text-xs">
                            {model.credits_per_second}x credits
                          </Badge>
                        </div>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              
              {selectedModel && (
                <div className="p-3 bg-muted rounded-lg">
                  {(() => {
                    const model = models.find(m => m.id === selectedModel)
                    return (
                      <div className="space-y-2">
                        <div className="flex items-center justify-between text-sm">
                          <span className="flex items-center">
                            <Clock className="w-3 h-3 mr-1" />
                            Generation time
                          </span>
                          <span>{model.estimated_time}</span>
                        </div>
                        <div className="flex flex-wrap gap-1">
                          {model.features.map((feature, index) => (
                            <Badge key={index} variant="secondary" className="text-xs">
                              {feature}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    )
                  })()}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Duration */}
          <Card>
            <CardHeader>
              <CardTitle>Duration</CardTitle>
              <CardDescription>Set video length (seconds)</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <Slider
                  value={duration}
                  onValueChange={setDuration}
                  max={10}
                  min={3}
                  step={1}
                  className="w-full"
                />
                <div className="flex justify-between text-sm text-muted-foreground">
                  <span>3s</span>
                  <span className="font-medium">{duration[0]}s</span>
                  <span>10s</span>
                </div>
                <div className="text-center">
                  <Badge variant="outline">
                    {calculateCredits()} credits required
                  </Badge>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Center Panel - Preview */}
        <div className="lg:col-span-1">
          <Card className="h-full">
            <CardHeader>
              <CardTitle>Preview</CardTitle>
              <CardDescription>Video preview will appear here</CardDescription>
            </CardHeader>
            <CardContent className="flex-1">
              <div className="aspect-video bg-muted rounded-lg flex items-center justify-center mb-4">
                {videoResult ? (
                  <div className="text-center">
                    <video 
                      controls 
                      className="w-full h-full rounded-lg"
                      src={videoResult.video_url}
                    >
                      Your browser does not support the video tag.
                    </video>
                  </div>
                ) : isGenerating ? (
                  <div className="text-center">
                    <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                    <p className="text-sm text-muted-foreground">Generating video...</p>
                  </div>
                ) : (
                  <div className="text-center">
                    <Play className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
                    <p className="text-sm text-muted-foreground">Preview will appear after generation</p>
                  </div>
                )}
              </div>
              
              <div className="flex items-center justify-center space-x-2">
                <Button variant="outline" size="sm" disabled={isGenerating || !videoResult}>
                  <RotateCcw className="w-4 h-4" />
                </Button>
                <Button variant="outline" size="sm" disabled={isGenerating || !videoResult}>
                  <Play className="w-4 h-4" />
                </Button>
                <Button variant="outline" size="sm" disabled={isGenerating || !videoResult}>
                  <Pause className="w-4 h-4" />
                </Button>
                <Button variant="outline" size="sm" disabled={isGenerating || !videoResult}>
                  <Download className="w-4 h-4" />
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Right Panel - Actor & Voice */}
        <div className="lg:col-span-1 space-y-6">
          {/* Actor Selection */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Users className="w-5 h-5 mr-2" />
                AI Actor
              </CardTitle>
              <CardDescription>Choose your video presenter</CardDescription>
            </CardHeader>
            <CardContent>
              <Select value={selectedActor} onValueChange={setSelectedActor}>
                <SelectTrigger>
                  <SelectValue placeholder="Select AI actor" />
                </SelectTrigger>
                <SelectContent>
                  {actors.map((actor) => (
                    <SelectItem key={actor.id} value={actor.id}>
                      <div className="flex items-center justify-between w-full">
                        <div>
                          <div className="font-medium">{actor.name}</div>
                          <div className="text-xs text-muted-foreground">{actor.style}</div>
                        </div>
                        <div className="flex space-x-1 ml-4">
                          <Badge variant="outline" className="text-xs">{actor.gender}</Badge>
                          <Badge variant="outline" className="text-xs">{actor.age_range}</Badge>
                        </div>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              
              {selectedActor && (
                <div className="mt-3 p-3 bg-muted rounded-lg">
                  <div className="aspect-square bg-background rounded-lg flex items-center justify-center mb-2">
                    <Users className="w-8 h-8 text-muted-foreground" />
                  </div>
                  <p className="text-xs text-center text-muted-foreground">Actor preview</p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Voice Selection */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Mic className="w-5 h-5 mr-2" />
                Voice
              </CardTitle>
              <CardDescription>Select voice for narration</CardDescription>
            </CardHeader>
            <CardContent>
              <Select value={selectedVoice} onValueChange={setSelectedVoice}>
                <SelectTrigger>
                  <SelectValue placeholder="Select voice" />
                </SelectTrigger>
                <SelectContent>
                  {voices.map((voice) => (
                    <SelectItem key={voice.id} value={voice.id}>
                      <div className="flex items-center justify-between w-full">
                        <div>
                          <div className="font-medium">{voice.name}</div>
                          <div className="text-xs text-muted-foreground">{voice.accent}</div>
                        </div>
                        <Badge variant="outline" className="text-xs ml-4">{voice.gender}</Badge>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              
              {selectedVoice && (
                <div className="mt-3">
                  <Button variant="outline" size="sm" className="w-full">
                    <Play className="w-3 h-3 mr-1" />
                    Preview Voice
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Generate Button */}
          <Card>
            <CardContent className="p-6">
              <Button 
                className="w-full gradient-bg text-white hover:opacity-90"
                size="lg"
                onClick={handleGenerate}
                disabled={!script || !selectedModel || !selectedActor || !selectedVoice || isGenerating}
              >
                {isGenerating ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                    Generating...
                  </>
                ) : (
                  <>
                    <Wand2 className="w-4 h-4 mr-2" />
                    Generate Video
                  </>
                )}
              </Button>
              
              <div className="mt-4 text-center text-sm text-muted-foreground">
                <p>Estimated time: 2-3 minutes</p>
                <p>Cost: {calculateCredits()} credits</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default VideoCreator

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Create Video</h1>
          <p className="text-muted-foreground">Generate professional videos with AI in minutes</p>
        </div>
        <div className="flex items-center space-x-2">
          <Badge variant="outline" className="text-sm">
            <Zap className="w-3 h-3 mr-1" />
            150 credits remaining
          </Badge>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Panel - Script & Settings */}
        <div className="lg:col-span-1 space-y-6">
          {/* Script Input */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Wand2 className="w-5 h-5 mr-2" />
                Script
              </CardTitle>
              <CardDescription>Write your video script or let AI help you</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Textarea
                placeholder="Enter your video script here... For example: 'Welcome to our amazing summer collection! Discover the latest trends in fashion with our premium quality clothing designed for comfort and style.'"
                value={script}
                onChange={(e) => setScript(e.target.value)}
                className="min-h-[120px] resize-none"
              />
              <div className="flex justify-between items-center text-sm text-muted-foreground">
                <span>{script.length} characters</span>
                <Button variant="outline" size="sm">
                  <Wand2 className="w-3 h-3 mr-1" />
                  AI Enhance
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Model Selection */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Settings className="w-5 h-5 mr-2" />
                AI Model
              </CardTitle>
              <CardDescription>Choose the best model for your needs</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Select value={selectedModel} onValueChange={setSelectedModel}>
                <SelectTrigger>
                  <SelectValue placeholder="Select AI model" />
                </SelectTrigger>
                <SelectContent>
                  {models.map((model) => (
                    <SelectItem key={model.id} value={model.id}>
                      <div className="flex items-center justify-between w-full">
                        <div>
                          <div className="font-medium">{model.name}</div>
                          <div className="text-xs text-muted-foreground">{model.provider}</div>
                        </div>
                        <div className="flex items-center space-x-2 ml-4">
                          <div className="flex items-center">
                            <Star className="w-3 h-3 text-yellow-500 mr-1" />
                            <span className="text-xs">{model.quality}</span>
                          </div>
                          <Badge variant="outline" className="text-xs">
                            {model.credits}x credits
                          </Badge>
                        </div>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              
              {selectedModel && (
                <div className="p-3 bg-muted rounded-lg">
                  {(() => {
                    const model = models.find(m => m.id === selectedModel)
                    return (
                      <div className="space-y-2">
                        <div className="flex items-center justify-between text-sm">
                          <span className="flex items-center">
                            <Clock className="w-3 h-3 mr-1" />
                            Generation time
                          </span>
                          <span>{model.speed}</span>
                        </div>
                        <div className="flex flex-wrap gap-1">
                          {model.features.map((feature, index) => (
                            <Badge key={index} variant="secondary" className="text-xs">
                              {feature}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    )
                  })()}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Duration */}
          <Card>
            <CardHeader>
              <CardTitle>Duration</CardTitle>
              <CardDescription>Set video length (seconds)</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <Slider
                  value={duration}
                  onValueChange={setDuration}
                  max={10}
                  min={3}
                  step={1}
                  className="w-full"
                />
                <div className="flex justify-between text-sm text-muted-foreground">
                  <span>3s</span>
                  <span className="font-medium">{duration[0]}s</span>
                  <span>10s</span>
                </div>
                <div className="text-center">
                  <Badge variant="outline">
                    {calculateCredits()} credits required
                  </Badge>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Center Panel - Preview */}
        <div className="lg:col-span-1">
          <Card className="h-full">
            <CardHeader>
              <CardTitle>Preview</CardTitle>
              <CardDescription>Video preview will appear here</CardDescription>
            </CardHeader>
            <CardContent className="flex-1">
              <div className="aspect-video bg-muted rounded-lg flex items-center justify-center mb-4">
                {isGenerating ? (
                  <div className="text-center">
                    <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                    <p className="text-sm text-muted-foreground">Generating video...</p>
                  </div>
                ) : (
                  <div className="text-center">
                    <Play className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
                    <p className="text-sm text-muted-foreground">Preview will appear after generation</p>
                  </div>
                )}
              </div>
              
              <div className="flex items-center justify-center space-x-2">
                <Button variant="outline" size="sm" disabled={isGenerating}>
                  <RotateCcw className="w-4 h-4" />
                </Button>
                <Button variant="outline" size="sm" disabled={isGenerating}>
                  <Play className="w-4 h-4" />
                </Button>
                <Button variant="outline" size="sm" disabled={isGenerating}>
                  <Pause className="w-4 h-4" />
                </Button>
                <Button variant="outline" size="sm" disabled={isGenerating}>
                  <Download className="w-4 h-4" />
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Right Panel - Actor & Voice */}
        <div className="lg:col-span-1 space-y-6">
          {/* Actor Selection */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Users className="w-5 h-5 mr-2" />
                AI Actor
              </CardTitle>
              <CardDescription>Choose your video presenter</CardDescription>
            </CardHeader>
            <CardContent>
              <Select value={selectedActor} onValueChange={setSelectedActor}>
                <SelectTrigger>
                  <SelectValue placeholder="Select AI actor" />
                </SelectTrigger>
                <SelectContent>
                  {actors.map((actor) => (
                    <SelectItem key={actor.id} value={actor.id}>
                      <div className="flex items-center justify-between w-full">
                        <div>
                          <div className="font-medium">{actor.name}</div>
                          <div className="text-xs text-muted-foreground">{actor.style}</div>
                        </div>
                        <div className="flex space-x-1 ml-4">
                          <Badge variant="outline" className="text-xs">{actor.gender}</Badge>
                          <Badge variant="outline" className="text-xs">{actor.age}</Badge>
                        </div>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              
              {selectedActor && (
                <div className="mt-3 p-3 bg-muted rounded-lg">
                  <div className="aspect-square bg-background rounded-lg flex items-center justify-center mb-2">
                    <Users className="w-8 h-8 text-muted-foreground" />
                  </div>
                  <p className="text-xs text-center text-muted-foreground">Actor preview</p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Voice Selection */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Mic className="w-5 h-5 mr-2" />
                Voice
              </CardTitle>
              <CardDescription>Select voice for narration</CardDescription>
            </CardHeader>
            <CardContent>
              <Select value={selectedVoice} onValueChange={setSelectedVoice}>
                <SelectTrigger>
                  <SelectValue placeholder="Select voice" />
                </SelectTrigger>
                <SelectContent>
                  {voices.map((voice) => (
                    <SelectItem key={voice.id} value={voice.id}>
                      <div className="flex items-center justify-between w-full">
                        <div>
                          <div className="font-medium">{voice.name}</div>
                          <div className="text-xs text-muted-foreground">{voice.accent}</div>
                        </div>
                        <Badge variant="outline" className="text-xs ml-4">{voice.gender}</Badge>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              
              {selectedVoice && (
                <div className="mt-3">
                  <Button variant="outline" size="sm" className="w-full">
                    <Play className="w-3 h-3 mr-1" />
                    Preview Voice
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Generate Button */}
          <Card>
            <CardContent className="p-6">
              <Button 
                className="w-full gradient-bg text-white hover:opacity-90"
                size="lg"
                onClick={handleGenerate}
                disabled={!script || !selectedModel || !selectedActor || !selectedVoice || isGenerating}
              >
                {isGenerating ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                    Generating...
                  </>
                ) : (
                  <>
                    <Wand2 className="w-4 h-4 mr-2" />
                    Generate Video
                  </>
                )}
              </Button>
              
              <div className="mt-4 text-center text-sm text-muted-foreground">
                <p>Estimated time: 2-3 minutes</p>
                <p>Cost: {calculateCredits()} credits</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default VideoCreator

