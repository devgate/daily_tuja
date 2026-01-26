import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import re
from typing import List, Dict, Tuple, Optional
import logging
import yfinance as yf
import random

class NewsCollector:
    def __init__(self):
        self.news_sources = [
            'https://finance.naver.com/',
            'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101',
            'https://www.hankyung.com/economic',
            'https://www.mk.co.kr/news/economy/',
            'https://www.asiae.co.kr/list/economy'
        ]
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def collect_financial_news(self) -> List[Dict]:
        """금융 뉴스 수집 (실제 웹크롤링 대신 샘플 데이터 제공)"""
        # 실제 환경에서는 웹크롤링 구현 필요
        # 현재는 샘플 데이터로 대체
        return self._create_sample_news()
    
    def _create_sample_news(self) -> List[Dict]:
        """샘플 뉴스 데이터 생성"""
        sample_news = [
            {
                'title': '삼성전자, 다음 주 실적 발표 기대감에 시간외 상승',
                'link': 'https://finance.naver.com/news/mainnews.naver?articleId=12345',
                'source': '네이버금융',
                'date': '2026.01.26',
                'content': '삼성전자가 다음 주 실적 발표를 앞두고 시간외 거래에서 강세를 보이고 있습니다. 반도체 업황 개선 기대감이 커지면서 낙수효과가 기대됩니다. 시장의 관심이 집중되고 있습니다.'
            },
            {
                'title': '지니틱스, 시스템반도체 설계 분야에서 급등',
                'link': 'https://finance.naver.com/news/mainnews.naver?articleId=12346',
                'source': '머니투데이',
                'date': '2026.01.26',
                'content': '지니틱스가 웨어러블용 터치IC 설계 분야에서 주목받고 있습니다. 실적 시즌 기대감으로 매수세가 몰리고 있습니다. 기술력에 대한 평가가 긍정적입니다.'
            },
            {
                'title': 'SK증권, 자사주 소각 의무화 정책에 긍정적 반응',
                'link': 'https://finance.naver.com/news/mainnews.naver?articleId=12347',
                'source': '아시아경제',
                'date': '2026.01.26',
                'content': '정부의 3차 상법개정 추진에 따라 SK증권이 긍정적인 반응을 보이고 있습니다. 주주환원정책 강화 기대감이 높습니다. 금융 sector 전반에 좋은 영향을 줄 것으로 전망됩니다.'
            },
            {
                'title': '한화에어로스페이스, 아르테미스 프로젝트 기대감 상승',
                'link': 'https://finance.naver.com/news/mainnews.naver?articleId=12348',
                'source': '네이버금융',
                'date': '2026.01.26',
                'content': '한화에어로스페이스가 2월 아르테미스 발사를 앞두고 투자자들의 관심을 받고 있습니다. 우주항공 산업 본격화가 기대됩니다. 정부의 지원 정책도 긍정적입니다.'
            },
            {
                'title': 'SK하이닉스, HBM4 품질 승인 소식에 강세',
                'link': 'https://finance.naver.com/news/mainnews.naver?articleId=12349',
                'source': '머니투데이',
                'date': '2026.01.26',
                'content': 'SK하이닉스가 HBM4 품질 승정 관련 긍정적인 소식으로 상승하고 있습니다. AI 인프라 확대 수혜가 기대됩니다. 반도체 주가 전체에 긍정적인 영향을 줄 것입니다.'
            },
            {
                'title': '현대차그룹, 휴머노이드 로봇 아틀라스 양산 계획 발표',
                'link': 'https://finance.naver.com/news/mainnews.naver?articleId=12350',
                'source': '한국경제',
                'date': '2026.01.26',
                'content': '현대차그룹이 휴머노이드 로봇 아틀라스의 연 3만 대 생산 체계 구축 계획을 발표했습니다. 피지컬 AI 산업화 본격 진입에 대한 기대감이 커지고 있습니다.'
            },
            {
                'title': 'LG에너지솔루션, 배터리 기술 개발 가속화로 상승',
                'link': 'https://finance.naver.com/news/mainnews.naver?articleId=12351',
                'source': '조선일보',
                'date': '2026.01.26',
                'content': 'LG에너지솔루션이 차세대 배터리 기술 개발을 가속화하고 있습니다. 2차전지 sector 전반에 좋은 영향을 줄 것으로 보입니다. 북미 전기차 시장 확대도 긍정적입니다.'
            },
            {
                'title': 'KB금융, 금리 안정화로 실적 개선 기대감 증가',
                'link': 'https://finance.naver.com/news/mainnews.naver?articleId=12352',
                'source': '매일경제',
                'date': '2026.01.26',
                'content': 'KB금융이 금리 안정화로 실적 개선 기대감이 증가하고 있습니다. 금융주 전반에 매수세가 몰리고 있습니다. 주주환원정책도 긍정적으로 평가됩니다.'
            },
            {
                'title': '네이버, AI 기술 고도화로 주목받아',
                'link': 'https://finance.naver.com/news/mainnews.naver?articleId=12353',
                'source': '전자신문',
                'date': '2026.01.26',
                'content': '네이버가 AI 기술 고도화로 투자자들의 주목을 받고 있습니다. 클라우드 사업도 순항하고 있어 성장성이 높습니다. AI 플랫폼 확대가 기대됩니다.'
            },
            {
                'title': '삼성중공업, 조선업 장기 호황 사이클 수혜',
                'link': 'https://finance.naver.com/news/mainnews.naver?articleId=12354',
                'source': '한겨례',
                'date': '2026.01.26',
                'content': '삼성중공업이 조선업 장기 호황 사이클의 수혜를 받고 있습니다. 수주 잔고가 풍부하고 선가 상승도 이어지고 있습니다. 업황 개선이 지속될 전망입니다.'
            }
        ]
        
        # 무작위로 5-10개 선택하여 반환
        selected_count = random.randint(5, min(10, len(sample_news)))
        return random.sample(sample_news, selected_count)

    def _scrape_naver_finance(self) -> List[Dict]:
        """네이버 금융 뉴스 스크래핑"""
        news_list = []
        try:
            url = 'https://finance.naver.com/news/mainnews.naver'
            response = self.session.get(url, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            articles = soup.find_all('li', class_='block1')
            for article in articles[:20]:  # 상위 20개
                title_element = article.find('a', class_='articleTitle')
                if title_element:
                    title = title_element.get_text(strip=True)
                    href = title_element.get('href')
                    if href:
                        link = f"https://finance.naver.com{href}"
                    else:
                        continue
                    
                    # 날짜 추출
                    date_element = article.find('span', class_='date')
                    date = date_element.get_text(strip=True) if date_element else ''
                    
                    news_list.append({
                        'title': title,
                        'link': link,
                        'source': '네이버금융',
                        'date': date,
                        'content': self._extract_article_content(link)
                    })
                    
        except Exception as e:
            logging.error(f"네이버 금융 뉴스 수집 오류: {e}")
            
        return news_list

    def _scrape_moneytoday(self) -> List[Dict]:
        """머니투데이 뉴스 스크래핑"""
        news_list = []
        try:
            url = 'https://news.mt.co.kr/mtview.php?no=2026012609134672146'
            response = self.session.get(url, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 실제 구현에서는 머니투데이 메인 페이지에서 최신 뉴스 링크를 가져와야 함
            # 여기서는 예시로 간단한 구조만 표시
            
        except Exception as e:
            logging.error(f"머니투데이 뉴스 수집 오류: {e}")
            
        return news_list

    def _scrape_asiae(self) -> List[Dict]:
        """아시아경제 뉴스 스크래핑"""
        news_list = []
        try:
            url = 'https://www.asiae.co.kr/list/economy'
            response = self.session.get(url, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 실제 구현에서는 아시아경제 구조에 맞게 스크래핑
            
        except Exception as e:
            logging.error(f"아시아경제 뉴스 수집 오류: {e}")
            
        return news_list

    def _extract_article_content(self, url: str) -> str:
        """기사 본문 추출"""
        try:
            response = self.session.get(url, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 네이버 뉴스 본문 선택자
            content = soup.find('div', class_='newsct_article') or \
                     soup.find('div', id='articleBody') or \
                     soup.find('div', class_='articleBody')
                     
            return content.get_text(strip=True) if content else ''
            
        except Exception as e:
            logging.error(f"기사 본문 추출 오류: {e}")
            return ''

    def collect_stock_data(self) -> Dict:
        """주식 시장 데이터 수집"""
        try:
            # KOSPI, KOSDAQ 데이터
            kospi = yf.Ticker('^KS11')
            kosdaq = yf.Ticker('^KQ11')
            
            return {
                'kospi': {
                    'current': kospi.history(period='1d')['Close'].iloc[-1],
                    'change': kospi.history(period='1d')['Close'].pct_change().iloc[-1] * 100
                },
                'kosdaq': {
                    'current': kosdaq.history(period='1d')['Close'].iloc[-1],
                    'change': kosdaq.history(period='1d')['Close'].pct_change().iloc[-1] * 100
                }
            }
        except Exception as e:
            logging.error(f"주식 데이터 수집 오류: {e}")
            return {}