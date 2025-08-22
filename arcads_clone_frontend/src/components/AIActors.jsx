import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button.jsx';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx';
import { Badge } from '@/components/ui/badge.jsx';
import { Input } from '@/components/ui/input.jsx';
import { 
  Search, 
  Filter, 
  Heart, 
  Play, 
  User,
  Star,
  Clock,
  Zap
} from 'lucide-react';
import '../App.css';

const AIActors = () => {
  const [actors, setActors] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchActors();
  }, []);

  const fetchActors = async () => {
    try {
      setLoading(true);
      
      // Professional AI actors for video generation
      const mockActors = [
        {
          id: 1,
          name: "Sarah Chen",
          description: "Professional business presenter with warm, confident delivery",
          category: "business",
          gender: "female",
          age_range: "25-35",
          accent: "American",
          style: "Professional",
          thumbnail: "/api/placeholder/300/400",
          rating: 4.9,
          usage_count: 1250,
          duration_range: "30s-2min",
          languages: ["English", "Mandarin"],
          tags: ["corporate", "professional", "warm", "confident"]
        },
        {
          id: 2,
          name: "Marcus Johnson",
          description: "Charismatic spokesperson perfect for product launches and marketing",
          category: "marketing",
          gender: "male",
          age_range: "30-40",
          accent: "British",
          style: "Charismatic",
          thumbnail: "/api/placeholder/300/400",
          rating: 4.8,
          usage_count: 980,
          duration_range: "15s-90s",
          languages: ["English"],
          tags: ["marketing", "charismatic", "energetic", "persuasive"]
        },
        {
          id: 3,
          name: "Dr. Elena Rodriguez",
          description: "Academic expert ideal for educational and training content",
          category: "education",
          gender: "female",
          age_range: "35-45",
          accent: "Spanish",
          style: "Educational",
          thumbnail: "/api/placeholder/300/400",
          rating: 4.7,
          usage_count: 750,
          duration_range: "1min-5min",
          languages: ["English", "Spanish"],
          tags: ["education", "expert", "clear", "authoritative"]
        },
        {
          id: 4,
          name: "Alex Thompson",
          description: "Tech-savvy presenter perfect for software demos and tutorials",
          category: "technology",
          gender: "non-binary",
          age_range: "25-30",
          accent: "Canadian",
          style: "Tech-friendly",
          thumbnail: "/api/placeholder/300/400",
          rating: 4.6,
          usage_count: 650,
          duration_range: "30s-3min",
          languages: ["English", "French"],
          tags: ["technology", "clear", "modern", "approachable"]
        },
        {
          id: 5,
          name: "Isabella Martinez",
          description: "Creative storyteller ideal for brand narratives and testimonials",
          category: "creative",
          gender: "female",
          age_range: "28-35",
          accent: "American",
          style: "Storyteller",
          thumbnail: "/api/placeholder/300/400",
          rating: 4.8,
          usage_count: 890,
          duration_range: "45s-2min",
          languages: ["English", "Spanish"],
          tags: ["creative", "storytelling", "emotional", "authentic"]
        },
        {
          id: 6,
          name: "James Wilson",
          description: "Authoritative news anchor style perfect for announcements",
          category: "news",
          gender: "male",
          age_range: "40-50",
          accent: "American",
          style: "Authoritative",
          thumbnail: "/api/placeholder/300/400",
          rating: 4.9,
          usage_count: 1100,
          duration_range: "20s-90s",
          languages: ["English"],
          tags: ["news", "authoritative", "clear", "trustworthy"]
        }
      ];

      setActors(mockActors);
    } catch (error) {
      console.error('Error fetching actors:', error);
    } finally {
      setLoading(false);
    }
  };

  const categories = [
    { id: 'all', name: 'All Categories' },
    { id: 'business', name: 'Business' },
    { id: 'marketing', name: 'Marketing' },
    { id: 'education', name: 'Education' },
    { id: 'technology', name: 'Technology' },
    { id: 'creative', name: 'Creative' },
    { id: 'news', name: 'News' }
  ];

  const filteredActors = actors.filter(actor => {
    const matchesSearch = actor.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         actor.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         actor.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesCategory = selectedCategory === 'all' || actor.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const toggleFavorite = (actorId) => {
    setFavorites(prev => 
      prev.includes(actorId) 
        ? prev.filter(id => id !== actorId)
        : [...prev, actorId]
    );
  };

  const handleSelectActor = (actor) => {
    // In a real app, this would pass the selected actor back to the video creator
    alert(`Selected ${actor.name} for your video!`);
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-muted rounded w-1/4 mb-4"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="h-96 bg-muted rounded-lg"></div>
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
        <h1 className="text-2xl font-bold text-foreground mb-2">AI Actors</h1>
        <p className="text-muted-foreground">Choose from our library of professional AI actors for your videos</p>
      </div>

      {/* Search and Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
          <Input
            placeholder="Search actors by name, style, or tags..."
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
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <Card>
          <CardContent className="p-4 text-center">
            <User className="w-8 h-8 text-blue-600 mx-auto mb-2" />
            <p className="text-2xl font-bold text-foreground">{actors.length}</p>
            <p className="text-sm text-muted-foreground">Total Actors</p>
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
            <p className="text-2xl font-bold text-foreground">{filteredActors.length}</p>
            <p className="text-sm text-muted-foreground">Available Now</p>
          </CardContent>
        </Card>
      </div>

      {/* Actors Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredActors.map(actor => (
          <Card key={actor.id} className="video-card-hover overflow-hidden">
            <div className="relative">
              <div className="aspect-[3/4] bg-gradient-to-br from-purple-100 to-blue-100 flex items-center justify-center">
                <User className="w-16 h-16 text-muted-foreground" />
              </div>
              <div className="absolute top-2 right-2 flex gap-2">
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-8 w-8 p-0 bg-black/50 hover:bg-black/70 text-white"
                  onClick={() => toggleFavorite(actor.id)}
                >
                  <Heart 
                    className={`w-4 h-4 ${favorites.includes(actor.id) ? 'fill-red-500 text-red-500' : ''}`} 
                  />
                </Button>
              </div>
              <div className="absolute bottom-2 left-2">
                <Badge variant="secondary" className="text-xs">
                  {actor.style}
                </Badge>
              </div>
            </div>
            
            <CardContent className="p-4">
              <div className="flex items-start justify-between mb-2">
                <div>
                  <h3 className="font-semibold text-foreground">{actor.name}</h3>
                  <p className="text-sm text-muted-foreground">{actor.accent} • {actor.age_range}</p>
                </div>
                <div className="flex items-center gap-1">
                  <Star className="w-4 h-4 text-yellow-500 fill-current" />
                  <span className="text-sm font-medium">{actor.rating}</span>
                </div>
              </div>
              
              <p className="text-sm text-muted-foreground mb-3 line-clamp-2">
                {actor.description}
              </p>
              
              <div className="flex flex-wrap gap-1 mb-3">
                {actor.tags.slice(0, 3).map(tag => (
                  <Badge key={tag} variant="outline" className="text-xs">
                    {tag}
                  </Badge>
                ))}
              </div>
              
              <div className="flex items-center justify-between text-xs text-muted-foreground mb-3">
                <div className="flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  {actor.duration_range}
                </div>
                <div className="flex items-center gap-1">
                  <Play className="w-3 h-3" />
                  {actor.usage_count} uses
                </div>
              </div>
              
              <div className="flex gap-2">
                <Button 
                  variant="outline" 
                  size="sm" 
                  className="flex-1"
                  onClick={() => alert(`Preview of ${actor.name} coming soon!`)}
                >
                  <Play className="w-4 h-4 mr-1" />
                  Preview
                </Button>
                <Button 
                  size="sm" 
                  className="flex-1 gradient-bg text-white hover:opacity-90"
                  onClick={() => handleSelectActor(actor)}
                >
                  Select
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredActors.length === 0 && (
        <div className="text-center py-12">
          <User className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-foreground mb-2">No actors found</h3>
          <p className="text-muted-foreground">Try adjusting your search or filter criteria</p>
        </div>
      )}
    </div>
  );
};

export default AIActors;

