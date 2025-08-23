from flask import Blueprint, request, jsonify
import stripe
import os
from datetime import datetime, timedelta
import json

from ..models.user import User, db
from ..models.subscription import SubscriptionPlan, Payment, UsageLog
from ..routes.auth_enhanced import verify_jwt_token, log_user_action

payments_bp = Blueprint('payments', __name__)

# Initialize Stripe
stripe.api_key = "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"

def get_authenticated_user():
    """Get authenticated user from JWT token"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    user_id = verify_jwt_token(token)
    
    if not user_id:
        return None
    
    return User.query.get(user_id)

@payments_bp.route('/subscription-plans', methods=['GET'])
def get_subscription_plans():
    """Get available subscription plans"""
    try:
        plans = SubscriptionPlan.query.filter_by(is_active=True).all()
        
        # If no plans exist, create default plans
        if not plans:
            plans = create_default_subscription_plans()
        
        return jsonify({
            'success': True,
            'data': {
                'plans': [plan.to_dict() for plan in plans]
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get subscription plans: {str(e)}'
        }), 500

def create_default_subscription_plans():
    """Create default subscription plans with realistic Pollo AI pricing"""
    try:
        # Create Stripe products and prices first
        
        # Starter Plan (No Free Tier - AI costs money!)
        try:
            starter_product = stripe.Product.create(
                name='VidCraft AI Starter',
                description='Essential video generation for small projects'
            )
            
            starter_price = stripe.Price.create(
                product=starter_product.id,
                unit_amount=3900,  # $39.00
                currency='usd',
                recurring={'interval': 'month'}
            )
            
            starter_plan = SubscriptionPlan(
                name='Starter',
                tier='starter',
                stripe_price_id=starter_price.id,
                price_monthly=39.0,
                price_yearly=390.0,  # 2 months free
                credits_included=50,  # ~25 videos with budget models
                features=[
                    '50 credits per month',
                    'Budget AI models (Luma, PixVerse)',
                    'HD quality videos',
                    'Email support',
                    'Up to 10 second videos'
                ],
                max_videos_per_month=50,
                max_duration_seconds=10,
                priority_support=False,
                api_access=False,
                custom_branding=False
            )
        except Exception as e:
            print(f"Error creating Starter plan in Stripe: {e}")
            starter_plan = SubscriptionPlan(
                name='Starter',
                tier='starter',
                price_monthly=39.0,
                price_yearly=390.0,
                credits_included=50,
                features=[
                    '50 credits per month',
                    'Budget AI models (Luma, PixVerse)',
                    'HD quality videos',
                    'Email support',
                    'Up to 10 second videos'
                ],
                max_videos_per_month=50,
                max_duration_seconds=10,
                priority_support=False,
                api_access=False,
                custom_branding=False
            )
        
        # Pro Plan
        try:
            pro_product = stripe.Product.create(
                name='VidCraft AI Pro',
                description='Professional video generation with premium features'
            )
            
            pro_price = stripe.Price.create(
                product=pro_product.id,
                unit_amount=8900,  # $89.00
                currency='usd',
                recurring={'interval': 'month'}
            )
            
            pro_plan = SubscriptionPlan(
                name='Pro',
                tier='pro',
                stripe_price_id=pro_price.id,
                price_monthly=89.0,
                price_yearly=890.0,  # 2 months free
                credits_included=100,  # ~50-100 videos depending on model
                features=[
                    '100 credits per month',
                    'Most AI models (Kling, Runway, Veo2, Luma)',
                    '4K quality videos',
                    'Priority support',
                    'Custom branding',
                    'Up to 30 second videos'
                ],
                max_videos_per_month=100,
                max_duration_seconds=30,
                priority_support=True,
                api_access=False,
                custom_branding=True
            )
        except Exception as e:
            print(f"Error creating Pro plan in Stripe: {e}")
            pro_plan = SubscriptionPlan(
                name='Pro',
                tier='pro',
                price_monthly=89.0,
                price_yearly=890.0,
                credits_included=100,
                features=[
                    '100 credits per month',
                    'Most AI models (Kling, Runway, Veo2, Luma)',
                    '4K quality videos',
                    'Priority support',
                    'Custom branding',
                    'Up to 30 second videos'
                ],
                max_videos_per_month=100,
                max_duration_seconds=30,
                priority_support=True,
                api_access=False,
                custom_branding=True
            )
        
        # Business Plan
        try:
            business_product = stripe.Product.create(
                name='VidCraft AI Business',
                description='Business video generation with advanced features'
            )
            
            business_price = stripe.Price.create(
                product=business_product.id,
                unit_amount=19900,  # $199.00
                currency='usd',
                recurring={'interval': 'month'}
            )
            
            business_plan = SubscriptionPlan(
                name='Business',
                tier='business',
                stripe_price_id=business_price.id,
                price_monthly=199.0,
                price_yearly=1990.0,  # 2 months free
                credits_included=200,  # ~100-200 videos depending on model
                features=[
                    '200 credits per month',
                    'All AI models including premium (Kling 2.1 Master)',
                    '4K quality videos',
                    'Priority support',
                    'Custom branding',
                    'API access',
                    'Bulk generation',
                    'Up to 60 second videos'
                ],
                max_videos_per_month=200,
                max_duration_seconds=60,
                priority_support=True,
                api_access=True,
                custom_branding=True
            )
        except Exception as e:
            print(f"Error creating Business plan in Stripe: {e}")
            business_plan = SubscriptionPlan(
                name='Business',
                tier='business',
                price_monthly=199.0,
                price_yearly=1990.0,
                credits_included=200,
                features=[
                    '200 credits per month',
                    'All AI models including premium (Kling 2.1 Master)',
                    '4K quality videos',
                    'Priority support',
                    'Custom branding',
                    'API access',
                    'Bulk generation',
                    'Up to 60 second videos'
                ],
                max_videos_per_month=200,
                max_duration_seconds=60,
                priority_support=True,
                api_access=True,
                custom_branding=True
            )
        
        # Enterprise Plan
        try:
            enterprise_product = stripe.Product.create(
                name='VidCraft AI Enterprise',
                description='Enterprise video generation with unlimited features'
            )
            
            enterprise_price = stripe.Price.create(
                product=enterprise_product.id,
                unit_amount=49900,  # $499.00
                currency='usd',
                recurring={'interval': 'month'}
            )
            
            enterprise_plan = SubscriptionPlan(
                name='Enterprise',
                tier='enterprise',
                stripe_price_id=enterprise_price.id,
                price_monthly=499.0,
                price_yearly=4990.0,  # 2 months free
                credits_included=500,  # ~250-500 videos depending on model
                features=[
                    '500 credits per month',
                    'All premium AI models including Kling 2.1 Master',
                    '4K quality videos',
                    'Dedicated support manager',
                    'White-label solution',
                    'Advanced API access',
                    'Custom integrations',
                    'Analytics dashboard',
                    'Unlimited video length'
                ],
                max_videos_per_month=500,
                max_duration_seconds=120,
                priority_support=True,
                api_access=True,
                custom_branding=True
            )
        except Exception as e:
            print(f"Error creating Enterprise plan in Stripe: {e}")
            enterprise_plan = SubscriptionPlan(
                name='Enterprise',
                tier='enterprise',
                price_monthly=499.0,
                price_yearly=4990.0,
                credits_included=500,
                features=[
                    '500 credits per month',
                    'All premium AI models including Kling 2.1 Master',
                    '4K quality videos',
                    'Dedicated support manager',
                    'White-label solution',
                    'Advanced API access',
                    'Custom integrations',
                    'Analytics dashboard',
                    'Unlimited video length'
                ],
                max_videos_per_month=500,
                max_duration_seconds=120,
                priority_support=True,
                api_access=True,
                custom_branding=True
            )
        
        # Save plans to database
        db.session.add(starter_plan)
        db.session.add(pro_plan)
        db.session.add(business_plan)
        db.session.add(enterprise_plan)
        db.session.commit()
        
        return [starter_plan, pro_plan, business_plan, enterprise_plan]
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating default subscription plans: {e}")
        return []

@payments_bp.route('/create-customer', methods=['POST'])
def create_customer():
    """Create Stripe customer for user"""
    try:
        user = get_authenticated_user()
        if not user:
            return jsonify({
                'success': False,
                'message': 'Authentication required'
            }), 401
        
        # Check if customer already exists
        if user.stripe_customer_id:
            return jsonify({
                'success': True,
                'data': {
                    'customer_id': user.stripe_customer_id
                }
            }), 200
        
        # Create Stripe customer
        customer = stripe.Customer.create(
            email=user.email,
            name=user.get_full_name(),
            metadata={
                'user_id': user.id,
                'platform': 'vidcraft_ai'
            }
        )
        
        # Update user with customer ID
        user.stripe_customer_id = customer.id
        db.session.commit()
        
        # Log customer creation
        log_user_action(user.id, 'stripe_customer_created', {
            'customer_id': customer.id
        })
        
        return jsonify({
            'success': True,
            'data': {
                'customer_id': customer.id
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to create customer: {str(e)}'
        }), 500

@payments_bp.route('/create-subscription', methods=['POST'])
def create_subscription():
    """Create subscription for user"""
    try:
        user = get_authenticated_user()
        if not user:
            return jsonify({
                'success': False,
                'message': 'Authentication required'
            }), 401
        
        data = request.get_json()
        plan_id = data.get('plan_id')
        payment_method_id = data.get('payment_method_id')
        
        if not plan_id:
            return jsonify({
                'success': False,
                'message': 'Plan ID is required'
            }), 400
        
        # Get subscription plan
        plan = SubscriptionPlan.query.get(plan_id)
        if not plan or not plan.is_active:
            return jsonify({
                'success': False,
                'message': 'Invalid subscription plan'
            }), 400
        
        # Free plan doesn't require Stripe subscription
        if plan.tier == 'free':
            user.subscription_tier = 'free'
            user.subscription_status = 'active'
            user.credits_remaining = plan.credits_included
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Free plan activated',
                'data': {
                    'subscription_tier': 'free'
                }
            }), 200
        
        # Ensure customer exists
        if not user.stripe_customer_id:
            customer = stripe.Customer.create(
                email=user.email,
                name=user.get_full_name(),
                metadata={
                    'user_id': user.id,
                    'platform': 'vidcraft_ai'
                }
            )
            user.stripe_customer_id = customer.id
            db.session.commit()
        
        # Attach payment method to customer
        if payment_method_id:
            stripe.PaymentMethod.attach(
                payment_method_id,
                customer=user.stripe_customer_id
            )
            
            # Set as default payment method
            stripe.Customer.modify(
                user.stripe_customer_id,
                invoice_settings={
                    'default_payment_method': payment_method_id
                }
            )
        
        # Create subscription
        subscription = stripe.Subscription.create(
            customer=user.stripe_customer_id,
            items=[{
                'price': plan.stripe_price_id
            }],
            payment_behavior='default_incomplete',
            expand=['latest_invoice.payment_intent'],
            metadata={
                'user_id': user.id,
                'plan_tier': plan.tier
            }
        )
        
        # Update user subscription info
        user.stripe_subscription_id = subscription.id
        user.subscription_tier = plan.tier
        user.subscription_status = subscription.status
        user.credits_remaining += plan.credits_included
        db.session.commit()
        
        # Log subscription creation
        log_user_action(user.id, 'subscription_created', {
            'plan_tier': plan.tier,
            'subscription_id': subscription.id,
            'amount': plan.price_monthly
        })
        
        return jsonify({
            'success': True,
            'data': {
                'subscription': {
                    'id': subscription.id,
                    'status': subscription.status,
                    'client_secret': subscription.latest_invoice.payment_intent.client_secret if subscription.latest_invoice.payment_intent else None
                }
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to create subscription: {str(e)}'
        }), 500

@payments_bp.route('/purchase-credits', methods=['POST'])
def purchase_credits():
    """Purchase additional credits"""
    try:
        user = get_authenticated_user()
        if not user:
            return jsonify({
                'success': False,
                'message': 'Authentication required'
            }), 401
        
        data = request.get_json()
        credits_amount = data.get('credits', 0)
        
        if credits_amount <= 0:
            return jsonify({
                'success': False,
                'message': 'Invalid credits amount'
            }), 400
        
        # Credit pricing: $0.10 per credit
        amount_cents = int(credits_amount * 10)  # $0.10 per credit in cents
        
        # Ensure customer exists
        if not user.stripe_customer_id:
            customer = stripe.Customer.create(
                email=user.email,
                name=user.get_full_name(),
                metadata={
                    'user_id': user.id,
                    'platform': 'vidcraft_ai'
                }
            )
            user.stripe_customer_id = customer.id
            db.session.commit()
        
        # Create payment intent
        payment_intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency='usd',
            customer=user.stripe_customer_id,
            description=f'Purchase {credits_amount} credits for VidCraft AI',
            metadata={
                'user_id': user.id,
                'credits_amount': credits_amount,
                'type': 'credit_purchase'
            }
        )
        
        # Create payment record
        payment = Payment(
            user_id=user.id,
            stripe_payment_intent_id=payment_intent.id,
            amount=amount_cents / 100,  # Convert back to dollars
            currency='USD',
            status='pending',
            payment_type='credits',
            credits_purchased=credits_amount,
            description=f'Purchase {credits_amount} credits'
        )
        
        db.session.add(payment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'payment_intent': {
                    'id': payment_intent.id,
                    'client_secret': payment_intent.client_secret,
                    'amount': amount_cents,
                    'credits': credits_amount
                }
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to create payment: {str(e)}'
        }), 500

@payments_bp.route('/billing-history', methods=['GET'])
def get_billing_history():
    """Get user's billing history"""
    try:
        user = get_authenticated_user()
        if not user:
            return jsonify({
                'success': False,
                'message': 'Authentication required'
            }), 401
        
        # Get payments from database
        payments = Payment.query.filter_by(user_id=user.id).order_by(Payment.created_at.desc()).limit(50).all()
        
        return jsonify({
            'success': True,
            'data': {
                'payments': [payment.to_dict() for payment in payments],
                'total_spent': user.total_spent,
                'credits_purchased': user.credits_purchased
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get billing history: {str(e)}'
        }), 500

@payments_bp.route('/subscription-status', methods=['GET'])
def get_subscription_status():
    """Get user's current subscription status"""
    try:
        user = get_authenticated_user()
        if not user:
            return jsonify({
                'success': False,
                'message': 'Authentication required'
            }), 401
        
        subscription_data = {
            'tier': user.subscription_tier,
            'status': user.subscription_status,
            'credits_remaining': user.credits_remaining,
            'expires_at': user.subscription_expires.isoformat() if user.subscription_expires else None
        }
        
        # Get Stripe subscription details if exists
        if user.stripe_subscription_id:
            try:
                subscription = stripe.Subscription.retrieve(user.stripe_subscription_id)
                subscription_data.update({
                    'stripe_status': subscription.status,
                    'current_period_end': datetime.fromtimestamp(subscription.current_period_end).isoformat(),
                    'cancel_at_period_end': subscription.cancel_at_period_end
                })
            except Exception as e:
                print(f"Error retrieving Stripe subscription: {e}")
        
        return jsonify({
            'success': True,
            'data': {
                'subscription': subscription_data
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get subscription status: {str(e)}'
        }), 500

@payments_bp.route('/cancel-subscription', methods=['POST'])
def cancel_subscription():
    """Cancel user's subscription"""
    try:
        user = get_authenticated_user()
        if not user:
            return jsonify({
                'success': False,
                'message': 'Authentication required'
            }), 401
        
        if not user.stripe_subscription_id:
            return jsonify({
                'success': False,
                'message': 'No active subscription found'
            }), 400
        
        # Cancel subscription at period end
        subscription = stripe.Subscription.modify(
            user.stripe_subscription_id,
            cancel_at_period_end=True
        )
        
        # Log cancellation
        log_user_action(user.id, 'subscription_cancelled', {
            'subscription_id': user.stripe_subscription_id,
            'cancel_at_period_end': True
        })
        
        return jsonify({
            'success': True,
            'message': 'Subscription will be cancelled at the end of the current period',
            'data': {
                'cancel_at_period_end': subscription.cancel_at_period_end,
                'current_period_end': datetime.fromtimestamp(subscription.current_period_end).isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to cancel subscription: {str(e)}'
        }), 500

@payments_bp.route('/webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhooks"""
    try:
        payload = request.get_data()
        sig_header = request.headers.get('Stripe-Signature')
        
        # For demo purposes, we'll process without signature verification
        # In production, you should verify the webhook signature
        
        event = json.loads(payload)
        
        # Handle different event types
        if event['type'] == 'payment_intent.succeeded':
            handle_payment_succeeded(event['data']['object'])
        elif event['type'] == 'invoice.payment_succeeded':
            handle_subscription_payment_succeeded(event['data']['object'])
        elif event['type'] == 'customer.subscription.updated':
            handle_subscription_updated(event['data']['object'])
        elif event['type'] == 'customer.subscription.deleted':
            handle_subscription_deleted(event['data']['object'])
        
        return jsonify({'success': True}), 200
        
    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({'success': False}), 400

def handle_payment_succeeded(payment_intent):
    """Handle successful payment for credit purchases"""
    try:
        user_id = payment_intent['metadata'].get('user_id')
        credits_amount = int(payment_intent['metadata'].get('credits_amount', 0))
        
        if user_id and credits_amount > 0:
            user = User.query.get(user_id)
            if user:
                # Add credits to user account
                user.add_credits(credits_amount)
                user.total_spent += payment_intent['amount'] / 100
                
                # Update payment record
                payment = Payment.query.filter_by(
                    stripe_payment_intent_id=payment_intent['id']
                ).first()
                
                if payment:
                    payment.status = 'succeeded'
                
                db.session.commit()
                
                # Log successful payment
                log_user_action(user_id, 'credits_purchased', {
                    'credits_amount': credits_amount,
                    'amount': payment_intent['amount'] / 100
                })
                
    except Exception as e:
        print(f"Error handling payment succeeded: {e}")

def handle_subscription_payment_succeeded(invoice):
    """Handle successful subscription payment"""
    try:
        customer_id = invoice['customer']
        user = User.query.filter_by(stripe_customer_id=customer_id).first()
        
        if user:
            # Get subscription details
            subscription_id = invoice['subscription']
            subscription = stripe.Subscription.retrieve(subscription_id)
            
            # Update user subscription status
            user.subscription_status = 'active'
            user.subscription_expires = datetime.fromtimestamp(subscription.current_period_end)
            
            # Add monthly credits based on plan
            plan = SubscriptionPlan.query.filter_by(
                stripe_price_id=subscription['items']['data'][0]['price']['id']
            ).first()
            
            if plan:
                user.credits_remaining += plan.credits_included
            
            db.session.commit()
            
            # Log subscription payment
            log_user_action(user.id, 'subscription_payment_succeeded', {
                'subscription_id': subscription_id,
                'amount': invoice['amount_paid'] / 100
            })
            
    except Exception as e:
        print(f"Error handling subscription payment: {e}")

def handle_subscription_updated(subscription):
    """Handle subscription updates"""
    try:
        customer_id = subscription['customer']
        user = User.query.filter_by(stripe_customer_id=customer_id).first()
        
        if user:
            user.subscription_status = subscription['status']
            db.session.commit()
            
    except Exception as e:
        print(f"Error handling subscription update: {e}")

def handle_subscription_deleted(subscription):
    """Handle subscription cancellation"""
    try:
        customer_id = subscription['customer']
        user = User.query.filter_by(stripe_customer_id=customer_id).first()
        
        if user:
            user.subscription_tier = 'free'
            user.subscription_status = 'cancelled'
            user.stripe_subscription_id = None
            db.session.commit()
            
            # Log subscription cancellation
            log_user_action(user.id, 'subscription_cancelled', {
                'subscription_id': subscription['id']
            })
            
    except Exception as e:
        print(f"Error handling subscription deletion: {e}")

