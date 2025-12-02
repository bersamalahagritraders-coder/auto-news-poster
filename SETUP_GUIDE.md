# Facebook Forex News Automation - Setup Guide

## Quick Start (3 Steps)

### Step 1: Get Your Tokens (5 minutes)

**Facebook Page Token:**
1. Go to [Meta for Developers](https://developers.facebook.com)
2. Create or select your app
3. Add "Facebook Login" and "Pages" products
4. Go to Settings → Basic, copy your App ID
5. Go to Tools → Graph API Explorer
6. Select your app, then select your Facebook Page
7. Get a user access token with `pages_manage_posts, pages_read_engagement` permissions
8. Exchange for long-lived token using the token tool (lasts ~60 days)
9. Copy the long-lived `PAGE_TOKEN` and your `PAGE_ID`

**Google Sheets (Optional - for logging):**
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable "Google Sheets API"
4. Create a Service Account credential (JSON key)
5. Copy the entire JSON and your Sheets ID

### Step 2: Add GitHub Secrets (3 minutes)

1. Go to your repo → Settings → Secrets and variables → Actions
2. Click "New repository secret" and add:
   - `FACEBOOK_PAGE_ID`: Your Facebook Page ID
   - `FACEBOOK_PAGE_TOKEN`: Your long-lived page token
   - `GOOGLE_SHEETS_ID`: (Optional) Your Google Sheets ID
   - `GOOGLE_CREDENTIALS_JSON`: (Optional) Your Google service account JSON

### Step 3: Enable GitHub Actions (1 minute)

1. Go to your repo → Actions → Workflows
2. Find "Facebook Forex News Automation" workflow
3. Click "Enable workflow"
4. It will run automatically at: **06:00 IST, 15:00 IST, 21:00 IST** (3x daily)
5. Manual trigger: Go to Actions tab → select workflow → click "Run workflow"

---

## What Gets Posted

✅ **English posts** with market news, forex rates, and trading analysis  
✅ **Tamil posts** with auto-translated content and Tamil hashtags  
✅ **Logging** to Google Sheets (timestamp, status, post ID)  
✅ **Error handling** with retry logic  

---

## Files Explained

- `auto_post.py` - Main automation script (RSS → Facebook → Sheets)
- `.github/workflows/post-facebook.yml` - GitHub Actions scheduler (3x daily)
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variable template
- `SETUP_GUIDE.md` - This file

---

## Cost Breakdown

| Component | Cost |
|-----------|------|
| Facebook Page | FREE |
| Graph API (100 posts/month) | FREE |
| GitHub Actions (300 tasks/month) | FREE |
| RSS Feeds | FREE |
| Translation (MyMemory API) | FREE |
| **TOTAL** | **₹0** |

---

## How It Works

1. **Fetch** → Pulls latest news from Forex Factory, Bloomberg, Economic Times RSS feeds
2. **Translate** → Auto-translates to Tamil using free MyMemory API
3. **Format** → Creates bilingual posts with emojis and hashtags
4. **Post** → Posts to Facebook using Graph API
5. **Log** → Records post details in Google Sheets (optional)

---

## Troubleshooting

**Posts not appearing?**
- Check GitHub Actions logs (Actions tab → workflow → latest run)
- Verify FACEBOOK_PAGE_TOKEN is long-lived (not user token)
- Ensure page has public access

**Translation not working?**
- MyMemory API is free but has rate limits (~500 requests/day)
- Falls back to original text if translation fails

**Google Sheets logging fails?**
- This is OPTIONAL - automation works without it
- Check Service Account has Editor permission on the Sheet

---

## Next Steps

- Monitor posts daily (check Facebook Page)
- Review Google Sheets logs weekly
- Refresh long-lived token every 60 days (automated workflow can help)
- Scale to Instagram/Twitter by forking workflows

---

**Created for:** Automated Forex market news posting (faceless, zero-cost)  
**Languages:** English + Tamil  
**Schedule:** 06:00, 15:00, 21:00 IST (Daily)  
**Status:** Production-ready ✅
