import pandas as pd
import numpy as np
import re
from typing import List, Dict, Tuple
from collections import Counter
import logging

class StockAnalyzer:
    def __init__(self):
        self.stock_keywords = {
            '반도체': ['삼성전자', 'SK하이닉스', '지니틱스', '라닉스', '와이씨켐', '샘씨엔에스', '저스템', '케이엔제이'],
            '금융': ['SK증권', '한화손해보험', 'KB금융', '신한지주', '하나금융지주'],
            '우주항공': ['한화에어로스페이스', '항공우주', '스페이스X', '아르테미스'],
            '조선': ['삼성중공업', '현대중공업', '대선조선', '한국조선해양'],
            '2차전지': ['LG에너지솔루션', '삼성SDI', 'SK온', '에코프로', '포스코퓨처엠'],
            '바이오': ['삼성바이오로직스', '셀트리온', 'SK바이오팜', 'LG화학'],
            '자율주행': ['현대차', '기아', '네이버', '카카오'],
            'AI': ['네이버', '카카오', '삼성전자', 'SK하이닉스']
        }
        
        self.positive_words = [
            '상승', '급등', '오름', '강세', '호황', '실적개선', '수주', '기대감', '수혜', 
            '돌파', '신고가', '상승세', '매수세', '긍정적', '전망', '목표가', '상향'
        ]
        
        self.negative_words = [
            '하락', '급락', '약세', '부진', '실적악화', '손실', '위험', '하락세', 
            '매도세', '부정적', '하향', '조정', '하락장'
        ]

    def analyze_news_sentiment(self, news_list: List[Dict]) -> Dict:
        """뉴스 감성 분석"""
        sentiment_scores = {}
        
        for news in news_list:
            title = news.get('title', '')
            content = news.get('content', '')
            text = f"{title} {content}"
            
            # 긍정/부정 단어 카운트
            positive_count = sum(1 for word in self.positive_words if word in text)
            negative_count = sum(1 for word in self.negative_words if word in text)
            
            # 감성 점수 계산
            total_words = positive_count + negative_count
            if total_words > 0:
                sentiment_score = (positive_count - negative_count) / total_words
            else:
                sentiment_score = 0
                
            sentiment_scores[news['title']] = sentiment_score
            
        return sentiment_scores

    def extract_stock_mentions(self, news_list: List[Dict]) -> Dict[str, int]:
        """뉴스에서 주식 언급 횟수 추출"""
        stock_mentions = Counter()
        
        for news in news_list:
            title = news.get('title', '')
            content = news.get('content', '')
            text = f"{title} {content}"
            
            # 각 섹터별 주식 언급 확인
            for sector, stocks in self.stock_keywords.items():
                for stock in stocks:
                    if stock in text:
                        stock_mentions[stock] += 1
                        
        return dict(stock_mentions)

    def calculate_stock_scores(self, news_list: List[Dict], stock_mentions: Dict[str, int]) -> Dict[str, float]:
        """주식별 상승 가능성 점수 계산"""
        stock_scores = {}
        
        # 뉴스 감성 분석
        sentiment_scores = self.analyze_news_sentiment(news_list)
        
        # 각 주식에 대한 점수 계산
        for stock, mention_count in stock_mentions.items():
            if mention_count == 0:
                continue
                
            # 기본 점수: 언급 횟수
            base_score = mention_count * 10
            
            # 감성 점수 추가
            sentiment_bonus = 0
            for news in news_list:
                if stock in f"{news.get('title', '')} {news.get('content', '')}":
                    sentiment_bonus += sentiment_scores.get(news['title'], 0) * 5
            
            # 섹터 가중치
            sector_weight = self._get_sector_weight(stock)
            
            # 최종 점수
            final_score = (base_score + sentiment_bonus) * sector_weight
            stock_scores[stock] = final_score
            
        return stock_scores

    def _get_sector_weight(self, stock: str) -> float:
        """섹터별 가중치 부여"""
        sector_weights = {
            '반도체': 1.2,      # 현재 가장 핫한 섹터
            'AI': 1.15,         # AI 테마
            '금융': 1.1,        # 정책 수혜 기대
            '우주항공': 1.25,   # 이벤트 기대감
            '2차전지': 1.0,     # 안정적
            '바이오': 0.9,      # 변동성 큼
            '조선': 1.05,       # 장기 호황
            '자율주행': 1.1     # 미래 성장성
        }
        
        for sector, stocks in self.stock_keywords.items():
            if stock in stocks:
                return sector_weights.get(sector, 1.0)
                
        return 1.0

    def rank_stocks(self, stock_scores: Dict[str, float]) -> List[Tuple[str, float, str]]:
        """주식 랭킹 생성"""
        # 점수 기준 정렬
        ranked_stocks = sorted(stock_scores.items(), key=lambda x: x[1], reverse=True)
        
        # 랭킹 결과 생성
        results = []
        for rank, (stock, score) in enumerate(ranked_stocks[:10], 1):
            reason = self._generate_ranking_reason(stock, score)
            results.append((stock, score, reason))
            
        return results

    def _generate_ranking_reason(self, stock: str, score: float) -> str:
        """랭킹 선정 이유 생성"""
        reasons = []
        
        # 섹터 확인
        for sector, stocks in self.stock_keywords.items():
            if stock in stocks:
                reasons.append(f"{sector} 섹터 소속")
                break
        
        # 점수 기반 이유
        if score > 50:
            reasons.append("매우 강력한 상승 모멘텀")
        elif score > 30:
            reasons.append("강력한 상승 기대감")
        elif score > 20:
            reasons.append("상승 가능성 높음")
        else:
            reasons.append("일반적 상승 기대")
            
        # 구체적인 이유 추가
        if '반도체' in stock or '삼성전자' in stock or 'SK하이닉스' in stock:
            reasons.append("실적 발표 기대감")
        elif '금융' in stock or '증권' in stock or '보험' in stock:
            reasons.append("정책 수혜 기대")
        elif '우주' in stock or '항공' in stock:
            reasons.append("이벤트 촉매재")
            
        return ", ".join(reasons)

    def analyze_market_trends(self, news_list: List[Dict]) -> Dict:
        """시장 동향 분석"""
        trend_analysis = {
            'hot_sectors': [],
            'market_sentiment': 'neutral',
            'key_events': []
        }
        
        # 핫 섹터 분석
        sector_mentions = Counter()
        for news in news_list:
            text = f"{news.get('title', '')} {news.get('content', '')}"
            for sector, stocks in self.stock_keywords.items():
                if any(stock in text for stock in stocks):
                    sector_mentions[sector] += 1
                    
        trend_analysis['hot_sectors'] = [sector for sector, count in sector_mentions.most_common(3)]
        
        # 시장 심리 분석
        sentiment_scores = self.analyze_news_sentiment(news_list)
        avg_sentiment = np.mean(list(sentiment_scores.values())) if sentiment_scores else 0
        
        if avg_sentiment > 0.2:
            trend_analysis['market_sentiment'] = 'bullish'
        elif avg_sentiment < -0.2:
            trend_analysis['market_sentiment'] = 'bearish'
        else:
            trend_analysis['market_sentiment'] = 'neutral'
            
        return trend_analysis