import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button.jsx';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx';
import { Badge } from '@/components/ui/badge.jsx';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx';
import { 
  CreditCard, 
  Check, 
  Star, 
  Zap, 
  Crown, 
  Calendar,
  DollarSign,
  Download,
  ArrowUpRight
} from 'lucide-react';
import apiService from '../services/api.js';
import '../App.css';

const Billing = () => {
  const [subscriptionPlans, setSubscriptionPlans] = useState([]);
  const [currentSubscription, setCurrentSubscription] = useState(null);
  const [billingHistory, setBillingHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [processingPayment, setProcessingPayment] = useState(false);

  useEffect(() => {
    fetchBillingData();
  }, []);

  const fetchBillingData = async () => {
    try {
      setLoading(true);
      
      // Updated realistic pricing based on Pollo AI costs
      const mockPlans = [
        {
          id: 'starter',
          name: 'Starter',
          price: 39,
          interval: 'month',
          credits: 50,
          features: [
            '50 video credits per month',
            'Budget AI models (Luma, PixVerse)',
            'HD quality exports',
            'Email support',
            'Up to 10 second videos'
          ],
          popular: false,
          icon: <Zap className="w-6 h-6" />
        },
        {
          id: 'pro',
          name: 'Pro',
          price: 89,
          interval: 'month',
          credits: 100,
          features: [
            '100 video credits per month',
            'Most AI models (Kling, Runway, Veo2, Luma)',
            '4K quality exports',
            'Priority support',
            'Custom branding',
            'Up to 30 second videos'
          ],
          popular: true,
          icon: <Star className="w-6 h-6" />
        },
        {
          id: 'business',
          name: 'Business',
          price: 199,
          interval: 'month',
          credits: 200,
          features: [
            '200 video credits per month',
            'All AI models including premium (Kling 2.1 Master)',
            '4K quality exports',
            'Priority support',
            'Custom branding',
            'API access',
            'Bulk generation',
            'Up to 60 second videos'
          ],
          popular: false,
          icon: <Crown className="w-6 h-6" />
        },
        {
          id: 'enterprise',
          name: 'Enterprise',
          price: 499,
          interval: 'month',
          credits: 500,
          features: [
            '500 video credits per month',
            'All premium AI models including Kling 2.1 Master',
            '4K quality exports',
            'Dedicated support manager',
            'White-label solution',
            'Advanced API access',
            'Custom integrations',
            'Analytics dashboard',
            'Unlimited video length'
          ],
          popular: false,
          icon: <Crown className="w-6 h-6" />
        }
      ];

      const mockCurrentSubscription = {
        id: 'sub_123',
        plan: 'pro',
        status: 'active',
        current_period_start: '2024-01-01',
        current_period_end: '2024-02-01',
        credits_used: 67,
        credits_remaining: 33
      };

      const mockBillingHistory = [
        {
          id: 'inv_001',
          date: '2024-01-01',
          amount: 89.00,
          status: 'paid',
          description: 'Pro Plan - Monthly',
          invoice_url: '#'
        },
        {
          id: 'inv_002',
          date: '2023-12-01',
          amount: 89.00,
          status: 'paid',
          description: 'Pro Plan - Monthly',
          invoice_url: '#'
        },
        {
          id: 'inv_003',
          date: '2023-11-15',
          amount: 25.00,
          status: 'paid',
          description: 'Additional Credits (25)',
          invoice_url: '#'
        }
      ];

      setSubscriptionPlans(mockPlans);
      setCurrentSubscription(mockCurrentSubscription);
      setBillingHistory(mockBillingHistory);
    } catch (error) {
      console.error('Error fetching billing data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubscribe = async (planId) => {
    setProcessingPayment(true);
    
    try {
      // Demo subscription flow
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Update current subscription
      setCurrentSubscription({
        ...currentSubscription,
        plan: planId,
        status: 'active'
      });
      
      alert(`Successfully subscribed to ${planId} plan!`);
    } catch (error) {
      alert('Payment failed. Please try again.');
    } finally {
      setProcessingPayment(false);
    }
  };

  const handlePurchaseCredits = async (amount) => {
    setProcessingPayment(true);
    
    try {
      // Demo credit purchase
      await new Promise(resolve => setTimeout(resolve, 1500));
      alert(`Successfully purchased ${amount} credits!`);
    } catch (error) {
      alert('Purchase failed. Please try again.');
    } finally {
      setProcessingPayment(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
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
          <h1 className="text-3xl font-bold text-foreground">Billing & Subscription</h1>
          <p className="text-muted-foreground">Manage your subscription and billing information</p>
        </div>
      </div>

      <Tabs defaultValue="subscription" className="space-y-6">
        <TabsList>
          <TabsTrigger value="subscription">Subscription</TabsTrigger>
          <TabsTrigger value="credits">Credits</TabsTrigger>
          <TabsTrigger value="history">Billing History</TabsTrigger>
        </TabsList>

        <TabsContent value="subscription" className="space-y-6">
          {/* Current Subscription */}
          {currentSubscription && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Crown className="h-5 w-5 text-primary" />
                  Current Subscription
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between">
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <h3 className="text-xl font-semibold capitalize">{currentSubscription.plan} Plan</h3>
                      <Badge variant={currentSubscription.status === 'active' ? 'default' : 'secondary'}>
                        {currentSubscription.status}
                      </Badge>
                    </div>
                    <p className="text-muted-foreground">
                      Next billing: {formatDate(currentSubscription.current_period_end)}
                    </p>
                    <div className="mt-4">
                      <div className="flex items-center gap-4 text-sm">
                        <span>Credits used: {currentSubscription.credits_used}</span>
                        <span>Remaining: {currentSubscription.credits_remaining}</span>
                      </div>
                      <div className="w-full bg-secondary rounded-full h-2 mt-2">
                        <div 
                          className="bg-primary h-2 rounded-full" 
                          style={{ 
                            width: `${(currentSubscription.credits_used / (currentSubscription.credits_used + currentSubscription.credits_remaining)) * 100}%` 
                          }}
                        ></div>
                      </div>
                    </div>
                  </div>
                  <Button variant="outline">
                    Manage Subscription
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Subscription Plans */}
          <div>
            <h2 className="text-2xl font-bold mb-4">Choose Your Plan</h2>
            <div className="grid md:grid-cols-3 gap-6">
              {subscriptionPlans.map((plan) => (
                <Card key={plan.id} className={`relative ${plan.popular ? 'border-primary shadow-lg' : ''}`}>
                  {plan.popular && (
                    <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                      <Badge className="bg-primary text-primary-foreground">
                        <Star className="h-3 w-3 mr-1" />
                        Most Popular
                      </Badge>
                    </div>
                  )}
                  
                  <CardHeader className="text-center">
                    <div className="mx-auto mb-4 p-3 rounded-full bg-primary/10 w-fit">
                      {plan.id === 'free' && <Zap className="h-6 w-6 text-primary" />}
                      {plan.id === 'pro' && <Star className="h-6 w-6 text-primary" />}
                      {plan.id === 'enterprise' && <Crown className="h-6 w-6 text-primary" />}
                    </div>
                    <CardTitle className="text-xl">{plan.name}</CardTitle>
                    <div className="text-3xl font-bold">
                      {formatCurrency(plan.price)}
                      <span className="text-sm font-normal text-muted-foreground">/{plan.interval}</span>
                    </div>
                    <CardDescription>{plan.credits} video credits included</CardDescription>
                  </CardHeader>
                  
                  <CardContent className="space-y-4">
                    <ul className="space-y-2">
                      {plan.features.map((feature, index) => (
                        <li key={index} className="flex items-center gap-2 text-sm">
                          <Check className="h-4 w-4 text-green-500" />
                          {feature}
                        </li>
                      ))}
                    </ul>
                    
                    <Button 
                      className="w-full" 
                      variant={plan.popular ? "default" : "outline"}
                      onClick={() => handleSubscribe(plan.id)}
                      disabled={processingPayment || currentSubscription?.plan === plan.id}
                    >
                      {processingPayment ? 'Processing...' : 
                       currentSubscription?.plan === plan.id ? 'Current Plan' : 
                       plan.price === 0 ? 'Get Started' : 'Subscribe'}
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </TabsContent>

        <TabsContent value="credits" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Zap className="h-5 w-5 text-primary" />
                Purchase Additional Credits
              </CardTitle>
              <CardDescription>
                Need more credits? Purchase additional credits at $0.10 each
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-3 gap-4">
                {[
                  { amount: 100, price: 10, bonus: 0 },
                  { amount: 250, price: 22.5, bonus: 25 },
                  { amount: 500, price: 40, bonus: 100 }
                ].map((package_) => (
                  <Card key={package_.amount} className="text-center">
                    <CardContent className="pt-6">
                      <div className="text-2xl font-bold">{package_.amount + package_.bonus}</div>
                      <div className="text-sm text-muted-foreground mb-2">
                        {package_.amount} credits {package_.bonus > 0 && `+ ${package_.bonus} bonus`}
                      </div>
                      <div className="text-xl font-semibold mb-4">{formatCurrency(package_.price)}</div>
                      <Button 
                        className="w-full" 
                        onClick={() => handlePurchaseCredits(package_.amount + package_.bonus)}
                        disabled={processingPayment}
                      >
                        {processingPayment ? 'Processing...' : 'Purchase'}
                      </Button>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="history" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Calendar className="h-5 w-5 text-primary" />
                Billing History
              </CardTitle>
              <CardDescription>
                View and download your past invoices
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {billingHistory.map((invoice) => (
                  <div key={invoice.id} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center gap-4">
                      <div className="p-2 bg-primary/10 rounded-full">
                        <DollarSign className="h-4 w-4 text-primary" />
                      </div>
                      <div>
                        <div className="font-medium">{invoice.description}</div>
                        <div className="text-sm text-muted-foreground">
                          {formatDate(invoice.date)}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
                      <div className="text-right">
                        <div className="font-semibold">{formatCurrency(invoice.amount)}</div>
                        <Badge variant={invoice.status === 'paid' ? 'default' : 'secondary'}>
                          {invoice.status}
                        </Badge>
                      </div>
                      <Button variant="ghost" size="sm">
                        <Download className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Billing;

