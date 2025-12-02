#!/usr/bin/env python3
import os,logging
from datetime import datetime
from dotenv import load_dotenv
from src.instagram_publisher import InstagramPublisher
load_dotenv()
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger=logging.getLogger(__name__)
def publish_trading_content(image_url:str,caption:str):
    try:
        publisher=InstagramPublisher()
        logger.info(f'Publishing to Instagram...')
        success=publisher.post_image(image_url,caption)
        if success:
            logger.info('Post published successfully!')
            return True
        return False
    except Exception as e:
        logger.error(f'Error:{str(e)}')
        return False
def main():
    logger.info('Starting Instagram Auto-Poster...')
    image_url='https://images.unsplash.com/photo-1611974789855-9c2a0a7fbda1?w=1080&h=1350'
    caption='📊 Supply & Demand Analysis\n\n#Trading #TechnicalAnalysis'
    result=publish_trading_content(image_url,caption)
    exit(0 if result else 1)
if __name__=='__main__':
    main()
