# Stripe API Key Security Guide for VidCraft AI

## 🔐 **Recommended: Use Restricted API Key**

For production applications like VidCraft AI, you should use a **restricted API key** for enhanced security.

## **Regular vs Restricted API Keys**

### **Regular API Key (Full Access)**
- **Format**: `sk_test_...` or `sk_live_...`
- **Access**: Full access to all Stripe resources and operations
- **Risk**: If compromised, attacker has complete control over your Stripe account
- **Use case**: Development, testing, or when you need full API access

### **Restricted API Key (Recommended)**
- **Format**: `rk_test_...` or `rk_live_...`
- **Access**: Limited to specific resources and operations you define
- **Risk**: If compromised, damage is limited to allowed operations only
- **Use case**: Production applications with specific needs

## **For VidCraft AI, You Need These Permissions:**

### **Core Resources:**
✅ **Customers** - Read/Write (manage user accounts)
✅ **Payment Intents** - Read/Write (process payments)
✅ **Subscriptions** - Read/Write (manage subscriptions)
✅ **Invoices** - Read/Write (billing management)
✅ **Products** - Read (subscription plans)
✅ **Prices** - Read (pricing information)
✅ **Webhook Endpoints** - Read (webhook management)

### **Optional Resources:**
✅ **Payment Methods** - Read/Write (saved cards)
✅ **Coupons** - Read (discount codes)
✅ **Usage Records** - Write (usage-based billing)

### **NOT Needed (Exclude for Security):**
❌ **Account** - Not needed
❌ **Application Fees** - Not needed
❌ **Balance** - Not needed
❌ **Disputes** - Not needed
❌ **Payouts** - Not needed
❌ **Transfers** - Not needed

## **How to Create Restricted API Key:**

1. **Go to Stripe Dashboard** → Developers → API Keys
2. **Click "Create restricted key"**
3. **Set permissions** as listed above
4. **Name it**: "VidCraft AI Production Key"
5. **Copy the key** (starts with `rk_`)

## **Security Benefits:**

### **Principle of Least Privilege**
- Only access what the application actually needs
- Reduces attack surface if key is compromised
- Easier to audit and monitor usage

### **Compliance & Auditing**
- Better for SOC 2, PCI compliance
- Clear audit trail of what operations are allowed
- Easier to track and monitor API usage

### **Risk Mitigation**
- If key is leaked, attacker can't:
  - Access your account balance
  - Create payouts to themselves
  - Modify webhook endpoints
  - Access sensitive account data

## **Implementation in VidCraft AI:**

```python
# Environment variable (same for both key types)
STRIPE_SECRET_KEY = "rk_test_..." # Restricted key
# or
STRIPE_SECRET_KEY = "sk_test_..." # Regular key

# Usage is identical in code
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
```

## **Recommendation for VidCraft AI:**

### **For Development/Testing:**
- Use **regular test key** (`sk_test_...`) for easier development
- Full access makes debugging and testing simpler

### **For Production:**
- Use **restricted live key** (`rk_live_...`) with minimal permissions
- Only the permissions listed above
- Better security and compliance

## **Migration Strategy:**

1. **Start with regular key** for initial development and testing
2. **Test with restricted key** before production deployment
3. **Deploy with restricted key** for production
4. **Monitor and adjust** permissions if needed

## **Bottom Line:**

**Use restricted API key for production** - it's a security best practice that costs nothing but provides significant protection. For our initial development and testing, either type works, but I'll design the system to work with restricted keys from the start.

Would you like me to proceed with either type? I can implement the payment system to work with both, and you can upgrade to restricted keys when you're ready for production.

