# Stripe Restricted API Key Setup for VidCraft AI

## 🎯 **Step-by-Step Setup Guide**

### **1. Access Stripe Dashboard**
- Go to https://dashboard.stripe.com
- Navigate to **Developers** → **API Keys**
- Click **"Create restricted key"**

### **2. Key Configuration**
- **Key name**: `VidCraft AI Production Key`
- **Description**: `Payment processing for VidCraft AI video generation platform`

### **3. Required Permissions (Check These)**

#### **✅ CORE RESOURCES (Required)**

**Customers**
- ✅ **Read** - View customer information
- ✅ **Write** - Create and update customer records
- *Why needed: Manage user accounts and billing profiles*

**Payment Intents**
- ✅ **Read** - View payment status and details
- ✅ **Write** - Create and confirm payments
- *Why needed: Process one-time payments for credits*

**Subscriptions**
- ✅ **Read** - View subscription details and status
- ✅ **Write** - Create, update, and cancel subscriptions
- *Why needed: Manage monthly/yearly subscription plans*

**Invoices**
- ✅ **Read** - View invoice details
- ✅ **Write** - Create and update invoices
- *Why needed: Generate bills and manage billing cycles*

**Products**
- ✅ **Read** - View product information
- *Why needed: Access subscription plan details*

**Prices**
- ✅ **Read** - View pricing information
- *Why needed: Get current pricing for plans and credits*

#### **✅ BILLING & USAGE (Required)**

**Usage Records**
- ✅ **Write** - Record usage for metered billing
- *Why needed: Track video generation usage for billing*

**Payment Methods**
- ✅ **Read** - View saved payment methods
- ✅ **Write** - Save and update payment methods
- *Why needed: Manage customer payment methods*

#### **✅ WEBHOOKS (Required)**

**Webhook Endpoints**
- ✅ **Read** - View webhook configuration
- *Why needed: Receive payment and subscription events*

#### **✅ PROMOTIONAL (Optional but Recommended)**

**Coupons**
- ✅ **Read** - View available coupons and discounts
- *Why needed: Apply promotional codes and discounts*

**Promotion Codes**
- ✅ **Read** - View promotion code details
- *Why needed: Validate and apply promo codes*

### **4. ❌ PERMISSIONS TO EXCLUDE (For Security)**

**❌ Account** - Not needed (account management)
**❌ Application Fees** - Not needed (marketplace features)
**❌ Balance** - Not needed (account balance access)
**❌ Balance Transactions** - Not needed (transaction history)
**❌ Charges** - Not needed (legacy payment API)
**❌ Disputes** - Not needed (chargeback management)
**❌ Events** - Not needed (event log access)
**❌ Files** - Not needed (file uploads)
**❌ Payouts** - Not needed (money transfers)
**❌ Refunds** - Not needed (we'll handle via dashboard)
**❌ Reviews** - Not needed (fraud reviews)
**❌ Sources** - Not needed (legacy payment methods)
**❌ Tokens** - Not needed (tokenization)
**❌ Transfers** - Not needed (marketplace transfers)

### **5. Final Checklist**

Before creating the key, verify you have:

#### **✅ Core Payment Processing**
- [x] Customers (Read/Write)
- [x] Payment Intents (Read/Write)
- [x] Payment Methods (Read/Write)

#### **✅ Subscription Management**
- [x] Subscriptions (Read/Write)
- [x] Invoices (Read/Write)
- [x] Products (Read)
- [x] Prices (Read)

#### **✅ Usage & Billing**
- [x] Usage Records (Write)

#### **✅ Webhooks & Events**
- [x] Webhook Endpoints (Read)

#### **✅ Promotions (Optional)**
- [x] Coupons (Read)
- [x] Promotion Codes (Read)

### **6. Create the Key**
- Click **"Create restricted key"**
- **Copy the key immediately** (starts with `rk_test_` or `rk_live_`)
- **Store it securely** - you won't be able to see it again

### **7. Test the Key**
Once you provide the key, I'll test it with these operations:
- Create a test customer
- Create a test product/price
- Set up a test payment intent
- Verify webhook endpoint access

## 🔒 **Security Benefits**

With this restricted key:
- ✅ Can process payments and manage subscriptions
- ✅ Can track usage and generate invoices
- ❌ Cannot access your account balance
- ❌ Cannot create payouts or transfers
- ❌ Cannot modify critical account settings
- ❌ Cannot access sensitive financial data

## 🚀 **Ready to Implement**

Once you create the key with these permissions, I'll:
1. Set up the complete payment system
2. Create subscription plans (Free, Pro, Enterprise)
3. Implement credit purchase system
4. Set up webhook handlers
5. Test all payment flows

**This key will have exactly the permissions needed - no more, no less!**

