#!/usr/bin/env python3
"""
Facebook Forex & Market News Automation
Automatically posts bilingual (English/Tamil) market news to Facebook
Scheduled 3x daily: 06:00, 15:00, 21:00 IST
"""

import os
import requests
import feedparser
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Environment variables
FACEBOOK_PAGE_ID = os.getenv('FACEBOOK_PAGE_ID')
FACEBOOK_PAGE_TOKEN = os.getenv('FACEBOOK_PAGE_TOKEN')
GOOGLE_SHEETS_ID = os.getenv('GOOGLE_SHEETS_ID')
GOOGLE_CREDENTIALS_JSON = os.getenv('GOOGLE_CREDENTIALS_JSON')

# RSS Feed URLs
RSS_FEEDS = [
    'https://feeds.bloomberg.com/markets/forex.rss',
    'https://feeds.economictimes.indiatimes.com/etMarkets/marketstory.cms?feedtype=rss',
    'https://feeds.forexfactory.com/calendar.xml'
]

class FacebookNewsAutomation:
    def __init__(self):
        self.fb_api_url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/feed"
        self.sheets_service = self._init_sheets_service()
        self.translation_cache = {}
    
    def _init_sheets_service(self):
        """Initialize Google Sheets API"""
        try:
            creds_dict = json.loads(GOOGLE_CREDENTIALS_JSON)
            creds = Credentials.from_service_account_info(
                creds_dict,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            return build('sheets', 'v4', credentials=creds)
        except Exception as e:
            logger.error(f"Failed to init Sheets service: {e}")
            return None
    
    def fetch_news(self):
        """Fetch latest news from RSS feeds"""
        news_items = []
        for feed_url in RSS_FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:3]:  # Get top 3 from each feed
                    news_items.append({
                        'title': entry.get('title', 'No title'),
                        'link': entry.get('link', ''),
                        'summary': entry.get('summary', '')[:200],
                        'source': feed.feed.get('title', 'Unknown')
                    })
            except Exception as e:
                logger.error(f"Error fetching {feed_url}: {e}")
        
        return news_items[:5]  # Limit to top 5 news items
    
    def translate_to_tamil(self, text):
        """Translate text to Tamil using MyMemory API (Free)"""
        if text in self.translation_cache:
            return self.translation_cache[text]
        
        try:
            url = "https://api.mymemory.translated.net/get"
            params = {
                'q': text,
                'langpair': 'en|ta'
            }
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data['responseStatus'] == 200:
                    tamil_text = data['responseData']['translatedText']
                    self.translation_cache[text] = tamil_text
                    return tamil_text
        except Exception as e:
            logger.error(f"Translation error: {e}")
        
        return text
    
    def format_post(self, news_item):
        """Format news item into English and Tamil posts"""
        title = news_item['title'][:100]
        link = news_item['link']
        source = news_item['source']
        
        # English post
        english_post = f"""📰 MARKET UPDATE

{title}

Source: {source}
🔗 Read more: {link}

#Forex #Markets #Trading #ForexNews #MarketAnalysis
"""
        
        # Tamil post
        tamil_title = self.translate_to_tamil(title)
        tamil_post = f"""📰 மக்ளுந்தங்க வற்ஜபப்ப u

{tamil_title}

Source: {source}
🔗 {link}

#வற்ஜபப்ப #சர்ந்தகங்கள் #வற்ஜய஼நர்பம்
"""
        
        return english_post, tamil_post
    
    def post_to_facebook(self, message):
        """Post message to Facebook Page"""
        try:
            payload = {
                'message': message,
                'access_token': FACEBOOK_PAGE_TOKEN
            }
            response = requests.post(self.fb_api_url, data=payload, timeout=10)
            
            if response.status_code == 200:
                post_id = response.json().get('id')
                logger.info(f"Posted to Facebook: {post_id}")
                return post_id
            else:
                logger.error(f"Facebook API error: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error posting to Facebook: {e}")
            return None
    
    def log_to_sheets(self, post_data):
        """Log post details to Google Sheets"""
        if not self.sheets_service or not GOOGLE_SHEETS_ID:
            return
        
        try:
            values = [[
                datetime.now().isoformat(),
                post_data['title'],
                post_data['language'],
                post_data['post_id'],
                post_data['status'],
                post_data.get('error', '')
            ]]
            
            self.sheets_service.spreadsheets().values().append(
                spreadsheetId=GOOGLE_SHEETS_ID,
                range='Sheet1!A:F',
                valueInputOption='USER_ENTERED',
                body={'values': values}
            ).execute()
            
            logger.info("Logged to Google Sheets")
        except Exception as e:
            logger.error(f"Error logging to Sheets: {e}")
    
    def run(self):
        """Main execution function"""
        logger.info("Starting Facebook News Automation")
        
        try:
            # Fetch news
            news_items = self.fetch_news()
            logger.info(f"Fetched {len(news_items)} news items")
            
            if not news_items:
                logger.warning("No news items found")
                return
            
            # Post first item in both languages
            news = news_items[0]
            english_post, tamil_post = self.format_post(news)
            
            # Post English
            en_post_id = self.post_to_facebook(english_post)
            self.log_to_sheets({
                'title': news['title'],
                'language': 'English',
                'post_id': en_post_id or 'ERROR',
                'status': 'SUCCESS' if en_post_id else 'FAILED'
            })
            
            # Post Tamil
            ta_post_id = self.post_to_facebook(tamil_post)
            self.log_to_sheets({
                'title': news['title'],
                'language': 'Tamil',
                'post_id': ta_post_id or 'ERROR',
                'status': 'SUCCESS' if ta_post_id else 'FAILED'
            })
            
            logger.info("Automation completed successfully")
            
        except Exception as e:
            logger.error(f"Automation error: {e}")
            self.log_to_sheets({
                'title': 'ERROR',
                'language': 'N/A',
                'post_id': 'N/A',
                'status': 'FAILED',
                'error': str(e)
            })

if __name__ == '__main__':
    automation = FacebookNewsAutomation()
    automation.run()
