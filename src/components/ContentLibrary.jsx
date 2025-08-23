import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button.jsx';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx';
import { Badge } from '@/components/ui/badge.jsx';
import { Input } from '@/components/ui/input.jsx';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx';
import { 
  Search, 
  Filter, 
  Heart, 
  Play, 
  Download, 
  Eye,
  Star,
  Clock,
  Users,
  Image,
  Music,
  Video
} from 'lucide-react';
import apiService from '../services/api.js';
import '../App.css';

const ContentLibrary = () => {
  const [templates, setTemplates] = useState([]);
  const [assets, setAssets] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [favorites, setFavorites] = useState(new Set());

  useEffect(() => {
    fetchContentData();
  }, []);

  const fetchContentData = async () => {
    try {
      setLoading(true);
      
      // For demo purposes, using mock data
      const mockTemplates = [
        {
          id: 1,
          title: 'Product Launch Announcement',
          description: 'Professional product launch video template with modern animations',
          category: 'marketing',
          subcategory: 'product',
          thumbnail: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=300&h=200&fit=crop',
          duration: 30,
          difficulty: 'beginner',
          usage_count: 1250,
          rating: 4.8,
          tags: ['product', 'launch', 'marketing', 'business'],
          script_template: 'Introducing our revolutionary new product...',
          created_at: '2024-01-15'
        },
        {
          id: 2,
          title: 'Social Media Promo',
          description: 'Eye-catching social media promotional video template',
          category: 'social',
          subcategory: 'promotion',
          thumbnail: 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=300&h=200&fit=crop',
          duration: 15,
          difficulty: 'beginner',
          usage_count: 980,
          rating: 4.6,
          tags: ['social', 'promo', 'instagram', 'tiktok'],
          script_template: 'Don\'t miss out on this amazing offer...',
          created_at: '2024-01-10'
        },
        {
          id: 3,
          title: 'Educational Explainer',
          description: 'Clear and engaging educational content template',
          category: 'education',
          subcategory: 'explainer',
          thumbnail: 'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=300&h=200&fit=crop',
          duration: 60,
          difficulty: 'intermediate',
          usage_count: 756,
          rating: 4.9,
          tags: ['education', 'explainer', 'tutorial', 'learning'],
          script_template: 'Today we\'ll learn about...',
          created_at: '2024-01-08'
        },
        {
          id: 4,
          title: 'Customer Testimonial',
          description: 'Authentic customer testimonial video template',
          category: 'testimonial',
          subcategory: 'customer',
          thumbnail: 'https://images.unsplash.com/photo-1556761175-b413da4baf72?w=300&h=200&fit=crop',
          duration: 45,
          difficulty: 'beginner',
          usage_count: 634,
          rating: 4.7,
          tags: ['testimonial', 'customer', 'review', 'trust'],
          script_template: 'I\'ve been using this product for...',
          created_at: '2024-01-05'
        }
      ];

      const mockAssets = [
        {
          id: 1,
          name: 'Modern Office Background',
          type: 'image',
          category: 'backgrounds',
          url: 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=400&h=300&fit=crop',
          thumbnail: 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=200&h=150&fit=crop',
          size: '2.4 MB',
          dimensions: '1920x1080',
          license: 'royalty-free',
          tags: ['office', 'modern', 'business', 'professional']
        },
        {
          id: 2,
          name: 'Corporate Music Track',
          type: 'audio',
          category: 'music',
          url: '#',
          thumbnail: 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=200&h=150&fit=crop',
          size: '3.2 MB',
          duration: '2:30',
          license: 'royalty-free',
          tags: ['corporate', 'upbeat', 'motivational', 'background']
        },
        {
          id: 3,
          name: 'Product Showcase Video',
          type: 'video',
          category: 'footage',
          url: '#',
          thumbnail: 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=200&h=150&fit=crop',
          size: '15.6 MB',
          duration: '0:30',
          license: 'premium',
          tags: ['product', 'showcase', 'commercial', 'professional']
        },
        {
          id: 4,
          name: 'Abstract Gradient Background',
          type: 'image',
          category: 'backgrounds',
          url: 'https://images.unsplash.com/photo-1557672172-298e090bd0f1?w=400&h=300&fit=crop',
          thumbnail: 'https://images.unsplash.com/photo-1557672172-298e090bd0f1?w=200&h=150&fit=crop',
          size: '1.8 MB',
          dimensions: '1920x1080',
          license: 'royalty-free',
          tags: ['abstract', 'gradient', 'colorful', 'modern']
        }
      ];

      const mockCategories = [
        { id: 'all', name: 'All Categories', count: 4 },
        { id: 'marketing', name: 'Marketing', count: 1 },
        { id: 'social', name: 'Social Media', count: 1 },
        { id: 'education', name: 'Education', count: 1 },
        { id: 'testimonial', name: 'Testimonials', count: 1 }
      ];

      setTemplates(mockTemplates);
      setAssets(mockAssets);
      setCategories(mockCategories);
    } catch (error) {
      console.error('Error fetching content data:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleFavorite = (id, type) => {
    const key = `${type}-${id}`;
    const newFavorites = new Set(favorites);
    if (newFavorites.has(key)) {
      newFavorites.delete(key);
    } else {
      newFavorites.add(key);
    }
    setFavorites(newFavorites);
  };

  const filteredTemplates = templates.filter(template => {
    const matchesSearch = template.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         template.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         template.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesCategory = selectedCategory === 'all' || template.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const filteredAssets = assets.filter(asset => {
    const matchesSearch = asset.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         asset.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
    return matchesSearch;
  });

  const getAssetIcon = (type) => {
    switch (type) {
      case 'image': return <Image className="h-4 w-4" />;
      case 'audio': return <Music className="h-4 w-4" />;
      case 'video': return <Video className="h-4 w-4" />;
      default: return <Image className="h-4 w-4" />;
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Content Library</h1>
          <p className="text-muted-foreground">Browse templates and assets for your video projects</p>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search templates and assets..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        <div className="flex gap-2">
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="px-3 py-2 border border-input bg-background rounded-md text-sm"
          >
            {categories.map(category => (
              <option key={category.id} value={category.id}>
                {category.name} ({category.count})
              </option>
            ))}
          </select>
          <Button variant="outline" size="sm">
            <Filter className="h-4 w-4 mr-2" />
            Filters
          </Button>
        </div>
      </div>

      <Tabs defaultValue="templates" className="space-y-6">
        <TabsList>
          <TabsTrigger value="templates">Templates ({filteredTemplates.length})</TabsTrigger>
          <TabsTrigger value="assets">Assets ({filteredAssets.length})</TabsTrigger>
          <TabsTrigger value="favorites">Favorites</TabsTrigger>
        </TabsList>

        <TabsContent value="templates" className="space-y-6">
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredTemplates.map((template) => (
              <Card key={template.id} className="group hover:shadow-lg transition-shadow">
                <div className="relative">
                  <img
                    src={template.thumbnail}
                    alt={template.title}
                    className="w-full h-48 object-cover rounded-t-lg"
                  />
                  <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity rounded-t-lg flex items-center justify-center">
                    <Button size="sm" className="mr-2">
                      <Play className="h-4 w-4 mr-2" />
                      Preview
                    </Button>
                    <Button size="sm" variant="outline">
                      <Eye className="h-4 w-4" />
                    </Button>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="absolute top-2 right-2 bg-white/80 hover:bg-white"
                    onClick={() => toggleFavorite(template.id, 'template')}
                  >
                    <Heart 
                      className={`h-4 w-4 ${favorites.has(`template-${template.id}`) ? 'fill-red-500 text-red-500' : ''}`} 
                    />
                  </Button>
                  <div className="absolute top-2 left-2">
                    <Badge variant="secondary" className="text-xs">
                      {template.difficulty}
                    </Badge>
                  </div>
                </div>
                
                <CardHeader className="pb-2">
                  <div className="flex items-start justify-between">
                    <CardTitle className="text-lg line-clamp-1">{template.title}</CardTitle>
                    <div className="flex items-center gap-1 text-sm text-muted-foreground">
                      <Star className="h-3 w-3 fill-yellow-400 text-yellow-400" />
                      {template.rating}
                    </div>
                  </div>
                  <CardDescription className="line-clamp-2">
                    {template.description}
                  </CardDescription>
                </CardHeader>
                
                <CardContent className="pt-0">
                  <div className="flex items-center justify-between text-sm text-muted-foreground mb-3">
                    <div className="flex items-center gap-1">
                      <Clock className="h-3 w-3" />
                      {template.duration}s
                    </div>
                    <div className="flex items-center gap-1">
                      <Users className="h-3 w-3" />
                      {template.usage_count.toLocaleString()}
                    </div>
                  </div>
                  
                  <div className="flex flex-wrap gap-1 mb-3">
                    {template.tags.slice(0, 3).map(tag => (
                      <Badge key={tag} variant="outline" className="text-xs">
                        {tag}
                      </Badge>
                    ))}
                  </div>
                  
                  <Button className="w-full">
                    Use Template
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="assets" className="space-y-6">
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
            {filteredAssets.map((asset) => (
              <Card key={asset.id} className="group hover:shadow-lg transition-shadow">
                <div className="relative">
                  <img
                    src={asset.thumbnail}
                    alt={asset.name}
                    className="w-full h-32 object-cover rounded-t-lg"
                  />
                  <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity rounded-t-lg flex items-center justify-center">
                    <Button size="sm" className="mr-2">
                      <Download className="h-4 w-4 mr-2" />
                      Download
                    </Button>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="absolute top-2 right-2 bg-white/80 hover:bg-white"
                    onClick={() => toggleFavorite(asset.id, 'asset')}
                  >
                    <Heart 
                      className={`h-4 w-4 ${favorites.has(`asset-${asset.id}`) ? 'fill-red-500 text-red-500' : ''}`} 
                    />
                  </Button>
                  <div className="absolute top-2 left-2">
                    <Badge variant="secondary" className="text-xs flex items-center gap-1">
                      {getAssetIcon(asset.type)}
                      {asset.type}
                    </Badge>
                  </div>
                </div>
                
                <CardContent className="p-3">
                  <h3 className="font-medium text-sm line-clamp-1 mb-1">{asset.name}</h3>
                  <div className="text-xs text-muted-foreground space-y-1">
                    <div>{asset.size}</div>
                    {asset.dimensions && <div>{asset.dimensions}</div>}
                    {asset.duration && <div>{asset.duration}</div>}
                    <Badge variant="outline" className="text-xs">
                      {asset.license}
                    </Badge>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="favorites" className="space-y-6">
          <div className="text-center py-12">
            <Heart className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-xl font-semibold mb-2">No favorites yet</h3>
            <p className="text-muted-foreground">
              Start adding templates and assets to your favorites to see them here
            </p>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default ContentLibrary;

