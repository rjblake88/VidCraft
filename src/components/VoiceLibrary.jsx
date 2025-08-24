import React, { useState, useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button.jsx';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx';
import { Badge } from '@/components/ui/badge.jsx';
import { Input } from '@/components/ui/input.jsx';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx';
import api from '@/services/api.js';

// Base URL for backend API (used for proxying preview audio)
const API_BASE =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/+$/, '') ||
  'http://localhost:5002/api';
import { 
  Search, 
  Play, 
  Pause,
  Heart, 
  Mic,
  Volume2,
  Star,
  Clock,
  Globe,
  Zap,
  Upload,
  Plus
} from 'lucide-react';
import '../App.css';

const VoiceLibrary = () => {
  const [voices, setVoices] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [favorites, setFavorites] = useState([]);
  const [playingVoice, setPlayingVoice] = useState(null);
  const [loading, setLoading] = useState(true);
  const audioRef = useRef(null);
  const [generatingId, setGeneratingId] = useState(null); // track voice currently generating

  useEffect(() => {
    fetchVoices();
  }, []);

  const fetchVoices = async () => {
    try {
      setLoading(true);

      // Attempt to fetch from backend (ElevenLabs proxy)
      const res = await api.getVoices();
      const backendVoices = res?.data?.voices || res?.voices || [];

      if (backendVoices.length) {
        const mapped = backendVoices.map((v, idx) => ({
          id: v.id || idx,
          name: v.name || 'Voice',
          description: v.description || 'Professional AI voice',
          category: 'professional',
          gender: (v.gender || '').toLowerCase() || 'female',
          age: 'Adult',
          accent: v.accent || '',
          language: v.language || 'English',
          style: v.style || 'General',
          sample_url: v.sample_url || v.preview_audio_url || '',
          rating: 4.8,
          usage_count: v.usage_count || 0,
          duration: '',
          tags: [],
          premium: false,
          clone_available: false,
        }));
        setVoices(mapped);
      } else {
        // Mock list if backend empty/unavailable
        const mockVoices = [
        {
          id: 1,
          name: "Emma Watson",
          description: "Warm, professional female voice perfect for corporate presentations",
          category: "professional",
          gender: "female",
          age: "Adult",
          accent: "British",
          language: "English",
          style: "Professional",
          sample_url: "#",
          rating: 4.9,
          usage_count: 2150,
          duration: "0:45",
          tags: ["corporate", "warm", "clear", "trustworthy"],
          premium: false,
          clone_available: true
        },
        {
          id: 2,
          name: "David Chen",
          description: "Authoritative male narrator ideal for documentaries and training",
          category: "narrative",
          gender: "male",
          age: "Adult",
          accent: "American",
          language: "English",
          style: "Authoritative",
          sample_url: "#",
          rating: 4.8,
          usage_count: 1890,
          duration: "1:02",
          tags: ["documentary", "authoritative", "deep", "engaging"],
          premium: true,
          clone_available: true
        },
        {
          id: 3,
          name: "Sofia Rodriguez",
          description: "Energetic bilingual voice perfect for marketing and social media",
          category: "marketing",
          gender: "female",
          age: "Young Adult",
          accent: "Spanish",
          language: "Spanish/English",
          style: "Energetic",
          sample_url: "#",
          rating: 4.7,
          usage_count: 1650,
          duration: "0:38",
          tags: ["marketing", "energetic", "bilingual", "youthful"],
          premium: false,
          clone_available: false
        },
        {
          id: 4,
          name: "James Mitchell",
          description: "Friendly conversational voice ideal for tutorials and explanations",
          category: "educational",
          gender: "male",
          age: "Adult",
          accent: "Australian",
          language: "English",
          style: "Conversational",
          sample_url: "#",
          rating: 4.6,
          usage_count: 1420,
          duration: "0:52",
          tags: ["tutorial", "friendly", "clear", "approachable"],
          premium: false,
          clone_available: true
        },
        {
          id: 5,
          name: "Aria Kim",
          description: "Modern tech-savvy voice perfect for app demos and tech content",
          category: "technology",
          gender: "female",
          age: "Young Adult",
          accent: "American",
          language: "English",
          style: "Modern",
          sample_url: "#",
          rating: 4.8,
          usage_count: 1780,
          duration: "0:41",
          tags: ["technology", "modern", "clear", "innovative"],
          premium: true,
          clone_available: true
        },
        {
          id: 6,
          name: "Oliver Thompson",
          description: "Sophisticated British voice ideal for luxury brand content",
          category: "luxury",
          gender: "male",
          age: "Adult",
          accent: "British",
          language: "English",
          style: "Sophisticated",
          sample_url: "#",
          rating: 4.9,
          usage_count: 1320,
          duration: "0:55",
          tags: ["luxury", "sophisticated", "elegant", "premium"],
          premium: true,
          clone_available: false
        }
      ];

        setVoices(mockVoices);
      }
    } catch (error) {
      console.error('Error fetching voices:', error);
    } finally {
      setLoading(false);
    }
  };

  const categories = [
    { id: 'all', name: 'All Voices' },
    { id: 'professional', name: 'Professional' },
    { id: 'marketing', name: 'Marketing' },
    { id: 'educational', name: 'Educational' },
    { id: 'narrative', name: 'Narrative' },
    { id: 'technology', name: 'Technology' },
    { id: 'luxury', name: 'Luxury' }
  ];

  const filteredVoices = voices.filter(voice => {
    const matchesSearch = voice.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         voice.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         voice.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesCategory = selectedCategory === 'all' || voice.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const toggleFavorite = (voiceId) => {
    setFavorites(prev => 
      prev.includes(voiceId) 
        ? prev.filter(id => id !== voiceId)
        : [...prev, voiceId]
    );
  };

  const togglePlayback = (voiceId) => {
    const voice = voices.find(v => v.id === voiceId);
    if (!voice?.sample_url) return;

    if (!audioRef.current) {
      audioRef.current = new Audio();
      audioRef.current.onended = () => setPlayingVoice(null);
    }

    // If clicking same voice that's playing -> pause/stop
    if (playingVoice === voiceId) {
      audioRef.current.pause();
      setPlayingVoice(null);
      return;
    }

    // Start new playback
    try {
      audioRef.current.pause();
      // Use backend proxy to avoid CORS / mixed-content issues
      const proxied = `${API_BASE}/voices/preview?url=${encodeURIComponent(
        voice.sample_url
      )}`;
      audioRef.current.src = proxied;
      audioRef.current.load();
      audioRef.current.play().catch(() => {});
      setPlayingVoice(voiceId);
    } catch (e) {
      console.error('Audio playback error', e);
    }
  };

  const handleSelectVoice = async (voice) => {
    // Generate a short TTS sample so the user hears the selected voice in action
    setGeneratingId(voice.id);
    try {
      const resp = await api.generateVoice({
        text: 'This is a sample generated by VidCraft.',
        voice_id: voice.id,
      });

      if (resp?.success && resp?.data?.audio_url_absolute) {
        if (!audioRef.current) {
          audioRef.current = new Audio();
          audioRef.current.onended = () => setPlayingVoice(null);
        }
        audioRef.current.pause();
        audioRef.current.src = resp.data.audio_url_absolute;
        audioRef.current.load();
        await audioRef.current.play().catch(() => {});
        setPlayingVoice(voice.id);
      } else {
        alert(resp?.message || 'Failed to generate audio sample.');
      }
    } catch (e) {
      console.error('Voice generation error', e);
      alert('Voice generation failed. Please try again.');
    } finally {
      setGeneratingId(null);
    }
  };

  const handleCloneVoice = (voice) => {
    alert(`Voice cloning for ${voice.name} will be available soon!`);
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-muted rounded w-1/4 mb-4"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="h-48 bg-muted rounded-lg"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-foreground mb-2">Voice Library</h1>
        <p className="text-muted-foreground">Choose from our collection of professional AI voices or create custom voice clones</p>
      </div>

      {/* Tabs */}
      <Tabs defaultValue="library" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="library">Voice Library</TabsTrigger>
          <TabsTrigger value="custom">Custom Voices</TabsTrigger>
        </TabsList>
        
        <TabsContent value="library" className="space-y-6">
          {/* Search and Filters */}
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
              <Input
                placeholder="Search voices by name, style, or language..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
            <div className="flex gap-2 flex-wrap">
              {categories.map(category => (
                <Button
                  key={category.id}
                  variant={selectedCategory === category.id ? "default" : "outline"}
                  size="sm"
                  onClick={() => setSelectedCategory(category.id)}
                  className={selectedCategory === category.id ? "gradient-bg text-white" : ""}
                >
                  {category.name}
                </Button>
              ))}
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
            <Card>
              <CardContent className="p-4 text-center">
                <Mic className="w-8 h-8 text-blue-600 mx-auto mb-2" />
                <p className="text-2xl font-bold text-foreground">{voices.length}</p>
                <p className="text-sm text-muted-foreground">Total Voices</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4 text-center">
                <Globe className="w-8 h-8 text-green-600 mx-auto mb-2" />
                <p className="text-2xl font-bold text-foreground">12</p>
                <p className="text-sm text-muted-foreground">Languages</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4 text-center">
                <Star className="w-8 h-8 text-yellow-600 mx-auto mb-2" />
                <p className="text-2xl font-bold text-foreground">4.8</p>
                <p className="text-sm text-muted-foreground">Average Rating</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4 text-center">
                <Zap className="w-8 h-8 text-purple-600 mx-auto mb-2" />
                <p className="text-2xl font-bold text-foreground">{filteredVoices.length}</p>
                <p className="text-sm text-muted-foreground">Available Now</p>
              </CardContent>
            </Card>
          </div>

          {/* Voices Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {filteredVoices.map(voice => (
              <Card key={voice.id} className="video-card-hover">
                <CardContent className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <div className="w-12 h-12 bg-gradient-to-br from-purple-100 to-blue-100 rounded-full flex items-center justify-center">
                        <Volume2 className="w-6 h-6 text-purple-600" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-foreground flex items-center gap-2">
                          {voice.name}
                          {voice.premium && (
                            <Badge variant="secondary" className="text-xs">
                              Premium
                            </Badge>
                          )}
                        </h3>
                        <p className="text-sm text-muted-foreground">
                          {voice.accent} • {voice.language} • {voice.age}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="flex items-center gap-1">
                        <Star className="w-4 h-4 text-yellow-500 fill-current" />
                        <span className="text-sm font-medium">{voice.rating}</span>
                      </div>
                      <Button
                        variant="ghost"
                        size="sm"
                        className="h-8 w-8 p-0"
                        onClick={() => toggleFavorite(voice.id)}
                      >
                        <Heart 
                          className={`w-4 h-4 ${favorites.includes(voice.id) ? 'fill-red-500 text-red-500' : ''}`} 
                        />
                      </Button>
                    </div>
                  </div>
                  
                  <p className="text-sm text-muted-foreground mb-4">
                    {voice.description}
                  </p>
                  
                  <div className="flex flex-wrap gap-1 mb-4">
                    {voice.tags.map(tag => (
                      <Badge key={tag} variant="outline" className="text-xs">
                        {tag}
                      </Badge>
                    ))}
                  </div>
                  
                  <div className="flex items-center justify-between text-xs text-muted-foreground mb-4">
                    <div className="flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {voice.duration}
                    </div>
                    <div className="flex items-center gap-1">
                      <Play className="w-3 h-3" />
                      {voice.usage_count} uses
                    </div>
                    <div className="flex items-center gap-1">
                      <Mic className="w-3 h-3" />
                      {voice.style}
                    </div>
                  </div>
                  
                  <div className="flex gap-2">
                    <Button 
                      variant="outline" 
                      size="sm" 
                      className="flex-1"
                      onClick={() => togglePlayback(voice.id)}
                    >
                      {playingVoice === voice.id ? (
                        <Pause className="w-4 h-4 mr-1" />
                      ) : (
                        <Play className="w-4 h-4 mr-1" />
                      )}
                      {playingVoice === voice.id ? 'Playing...' : 'Preview'}
                    </Button>
                    <Button 
                      size="sm" 
                      className="flex-1 gradient-bg text-white hover:opacity-90"
                      onClick={() => handleSelectVoice(voice)}
                      disabled={!!generatingId}
                    >
                      {generatingId === voice.id ? 'Generating…' : 'Select'}
                    </Button>
                    {voice.clone_available && (
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => handleCloneVoice(voice)}
                      >
                        Clone
                      </Button>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {filteredVoices.length === 0 && (
            <div className="text-center py-12">
              <Mic className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-foreground mb-2">No voices found</h3>
              <p className="text-muted-foreground">Try adjusting your search or filter criteria</p>
            </div>
          )}
        </TabsContent>
        
        <TabsContent value="custom" className="space-y-6">
          <div className="text-center py-12">
            <Upload className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-foreground mb-2">Custom Voice Cloning</h3>
            <p className="text-muted-foreground mb-6 max-w-md mx-auto">
              Upload audio samples to create custom voice clones. Perfect for brand consistency and personalized content.
            </p>
            <div className="space-y-4 max-w-sm mx-auto">
              <Button className="w-full gradient-bg text-white hover:opacity-90">
                <Plus className="w-4 h-4 mr-2" />
                Create New Voice Clone
              </Button>
              <p className="text-xs text-muted-foreground">
                Requires 5-10 minutes of clear audio samples
              </p>
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default VoiceLibrary;

