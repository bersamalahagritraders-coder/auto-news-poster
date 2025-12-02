#!/usr/bin/env python3
import requests,logging,os
from typing import Dict,Optional,List
from dotenv import load_dotenv
load_dotenv()
logger=logging.getLogger(__name__)
class InstagramPublisher:
    def __init__(self):
        self.token=os.getenv('INSTAGRAM_PAGE_ACCESS_TOKEN')
        self.account_id=os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
        self.api_version=os.getenv('GRAPH_API_VERSION','v19.0')
        self.base_url=f'https://graph.instagram.com/{self.api_version}'
        self.timeout=int(os.getenv('REQUEST_TIMEOUT','30'))
        if not self.token or not self.account_id:
            raise ValueError('Missing INSTAGRAM credentials')
    def _api_call(self,method:str,endpoint:str,data:Optional[Dict]=None,retry:int=0)->Dict:
        url=f'{self.base_url}{endpoint}'
        headers={'Authorization':f'Bearer {self.token}'}
        try:
            if method=='POST':
                r=requests.post(url,json=data,headers=headers,timeout=self.timeout)
            else:
                r=requests.get(url,params=data,headers=headers,timeout=self.timeout)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            logger.error(f'API Error:{str(e)}')
            return {'error':str(e)}
    def create_image_container(self,image_url:str,caption:str)->Optional[str]:
        payload={'image_url':image_url,'caption':caption,'media_type':'IMAGE'}
        result=self._api_call('POST',f'/{self.account_id}/media',payload)
        if 'id' in result:
            logger.info(f'Container created:{result["id"]}')
            return result['id']
        return None
    def publish_media(self,creation_id:str)->Optional[str]:
        payload={'creation_id':creation_id}
        result=self._api_call('POST',f'/{self.account_id}/media_publish',payload)
        if 'id' in result:
            logger.info(f'Published:{result["id"]}')
            return result['id']
        return None
    def post_image(self,image_url:str,caption:str)->bool:
        container_id=self.create_image_container(image_url,caption)
        if container_id:
            return self.publish_media(container_id) is not None
        return False
    def get_insights(self)->Dict:
        params={'metric':'impressions,reach,profile_views,follower_count'}
        return self._api_call('GET',f'/{self.account_id}/insights',params)
