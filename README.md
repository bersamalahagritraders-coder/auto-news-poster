# auto-news-poster

Automated Instagram posting for trading analysis and news content using Instagram Graph API v19.0.

## Overview

This project automates the posting of trading analysis and news content to Instagram Business accounts using the Instagram Graph API. The solution uses GitHub Actions for scheduled automated posting at 9:00 AM IST daily, with the flexibility for manual triggering.

## Features

- **Scheduled Posting**: Automatically posts content at 9:00 AM IST (3:30 AM UTC) daily
- **Manual Trigger**: Ability to manually trigger posts via GitHub Actions
- **Image Publishing**: Supports image uploads with captions
- **Error Handling**: Robust error handling with retry logic
- **Insights Tracking**: Retrieve post insights and analytics
- **Containerization**: Creates and publishes media containers before posting
- **CI/CD Integration**: Complete GitHub Actions workflow for automation

## Prerequisites

### Before Setup

1. **Facebook Developer Account**: Create one at [developers.facebook.com](https://developers.facebook.com)
2. **Facebook App**: Create an app for Instagram Graph API access
3. **Instagram Business Account**: Convert your Instagram account to a Business account
4. **Python 3.11+**: For local testing

### Required Credentials

- Instagram Business Account ID
- Instagram Page Access Token (with `instagram_basic`, `instagram_content_publish` permissions)

## Setup Instructions

### 1. Facebook Developer Setup

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app (select "Other" as the app type)
3. Add the Instagram Graph API product
4. Get your App ID and App Secret

### 2. Convert Instagram to Business Account

1. Open Instagram settings on the account you want to automate
2. Go to "Account" → "Switch to Professional Account"
3. Choose "Business" as the account type
4. Get your Instagram Business Account ID from your profile settings

### 3. Generate Access Token

1. In your Facebook App, generate a Page Access Token:
   - Go to Settings → Basic → Get tokens
   - Ensure tokens have these permissions:
     - `instagram_basic`
     - `instagram_content_publish`
     - `pages_manage_metadata`

### 4. Configure Environment Variables

1. Copy `.env.example` to `.env` (local only):
   ```bash
   cp .env.example .env
   ```

2. Fill in your credentials in `.env`:
   ```
   INSTAGRAM_BUSINESS_ACCOUNT_ID=your_business_account_id
   INSTAGRAM_PAGE_ACCESS_TOKEN=your_page_access_token
   ```

3. **Important**: Never commit `.env` to GitHub (it's in `.gitignore`)

### 5. GitHub Secrets Configuration

1. Go to your repository Settings → Secrets and Variables → Actions
2. Add these secrets:
   - `INSTAGRAM_BUSINESS_ACCOUNT_ID`: Your business account ID
   - `INSTAGRAM_PAGE_ACCESS_TOKEN`: Your page access token

### 6. Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run the posting script
python auto_post.py
```

## Project Structure

```
auto-news-poster/
├── .github/
│   └── workflows/
│       └── post-instagram.yml      # GitHub Actions workflow
├── src/
│   ├── __init__.py
│   └── instagram_publisher.py      # Instagram API wrapper
├── auto_post.py                    # Main orchestrator script
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
├── LICENSE                         # MIT License
└── README.md                       # This file
```

## File Descriptions

### `auto_post.py`
Main entry point that orchestrates the Instagram posting workflow:
- Loads environment variables
- Initializes the Instagram publisher
- Handles posting logic
- Error handling and logging

### `src/instagram_publisher.py`
Instagram Graph API wrapper class with methods for:
- `create_image_container()`: Prepares image for upload
- `publish_media()`: Publishes the container
- `post_image()`: Complete flow for posting images
- `get_insights()`: Retrieves post analytics

### `.github/workflows/post-instagram.yml`
GitHub Actions workflow that:
- Runs on schedule (9:00 AM IST daily)
- Supports manual workflow dispatch
- Checks out repository code
- Sets up Python environment
- Installs dependencies
- Executes the posting script

## Usage

### Scheduled Posts
Posts automatically every day at 9:00 AM IST. The workflow runs based on the cron schedule:
```yaml
cron: '30 3 * * *'  # 3:30 AM UTC = 9:00 AM IST
```

### Manual Posts
1. Go to your repository → Actions
2. Select "Instagram Post Automation" workflow
3. Click "Run workflow"
4. Select the branch and click "Run workflow"

## Dependencies

- `requests` - HTTP requests for API calls
- `python-dotenv` - Environment variable management
- `python-dateutil` - Date parsing and utilities

See `requirements.txt` for specific versions.

## API Reference

### Instagram Publisher Class

#### Initialization
```python
from src.instagram_publisher import InstagramPublisher

publisher = InstagramPublisher(
    account_id="YOUR_ACCOUNT_ID",
    access_token="YOUR_ACCESS_TOKEN"
)
```

#### Methods

**`create_image_container(image_url, caption)`**
- Creates a media container for the image
- Returns container ID

**`publish_media(creation_id)`**
- Publishes the container
- Returns media ID

**`post_image(image_url, caption)`**
- Complete workflow: create container → publish
- Returns True if successful

**`get_insights(media_id)`**
- Retrieves analytics for a post
- Returns insights dictionary

## Error Handling

The application includes:
- Automatic retry logic for API failures
- Comprehensive error logging
- Graceful error messages
- Request validation

## Troubleshooting

### Token Expired
- Regenerate access token in Facebook App
- Update GitHub Secrets

### "Invalid Access Token" Error
- Verify token has correct permissions
- Check account ID is correct
- Regenerate token if needed

### Posts Not Publishing
- Check GitHub Actions logs
- Verify GitHub Secrets are configured
- Test locally with `python auto_post.py`
- Check Instagram Business account is active

### API Rate Limiting
- Instagram limits API requests
- Adjust posting frequency if needed
- Check rate limit in response headers

## Security Considerations

1. **Never commit credentials** to repository
2. Use GitHub Secrets for sensitive data
3. Regularly rotate access tokens
4. Review permissions on tokens
5. Use environment variables, never hardcode credentials
6. Keep dependencies updated

## Logging

The application logs to stdout with timestamps and severity levels:
- INFO: General information
- ERROR: Error messages with details

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review GitHub Actions logs
3. Verify credentials in GitHub Secrets
4. Test locally before relying on scheduled posts

## References

- [Instagram Graph API Documentation](https://developers.facebook.com/docs/instagram-api)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Cron Syntax Reference](https://crontab.guru/)

## Roadmap

- [ ] Support for carousel posts
- [ ] Video posting support
- [ ] Scheduled content queue
- [ ] Instagram Stories support
- [ ] Post scheduling UI
- [ ] Analytics dashboard

---

**Last Updated**: 2024
**Status**: Active Development
