import pandas as pd
import numpy as np
import re
from typing import List, Dict, Tuple
from collections import Counter
import logging

class StockAnalyzer:
    def __init__(self):
        self.stock_keywords = {
            '반도체': ['삼성전자', 'SK하이닉스', '지니틱스', '라닉스', '와이씨켐', '샘씨엔에스', '저스템', '케이엔제이', '한미반도체', 'DB하이텍', '이노션', '아이씨케이', 'HBM4', 'HBM', 'TSMC', 'NVIDIA', 'AMD', 'Broadcom', 'Qualcomm', 'TSM'],
            '금융': ['SK증권', '한화손해보험', 'KB금융', '신한지주', '하나금융지주', '미래에셋증권', '키움증권', 'KB증권', 'Fed', 'Federal Reserve'],
            '우주항공': ['한화에어로스페이스', '항공우주', '스페이스X', '아르테미스', '한국항공우주', '항공우주산업', 'NASA', 'SpaceX'],
            '조선': ['삼성중공업', '현대중공업', '대선조선', '한국조선해양', '현대삼호중공업'],
            '2차전지': ['LG에너지솔루션', '삼성SDI', 'SK온', '에코프로', '포스코퓨처엠', '포스코DX', 'LG화학', '삼성전자', 'Tesla', 'CATL'],
            '바이오': ['삼성바이오로직스', '셀트리온', 'SK바이오팜', 'LG화학', '한국백신', '유진바이오', '녹십자', '케이씨씨', '보령', 'Pfizer', 'Moderna'],
            '자율주행': ['현대차', '기아', '네이버', '카카오', 'KT', 'LG이노텍', '모바일리언', 'Tesla', 'Waymo'],
            'AI': ['네이버', '카카오', '삼성전자', 'SK하이닉스', 'LG', 'KT', '더존비즈온', '비젠트로', 'OpenAI', 'ChatGPT', 'Anthropic'],
            '로봇': ['현대로보틱스', '로보스타', '네오텍', '유비온', '티로보틱스', '알체라', '스타일럽', '두산로보틱스', '한국로봇산업진흥원', 'Boston Dynamics', 'Tesla Bot'],
            '전력': ['한국전력', '한수원', 'GS에너지', 'E1', 'SK가스', '삼성엔지니어링', '포스코건설', 'NextEra', 'Duke Energy'],
            '방산': ['한화에어로스페이스', 'LIG넥스원', '현대로템', '한국항공우주', '삼성탈레스', 'KAI', 'Lockheed Martin', 'Boeing'],
            '글로벌테크': ['Apple', 'Microsoft', 'Google', 'Alphabet', 'Amazon', 'Meta', 'Facebook', 'TSMC', 'NVIDIA', 'AMD', 'Broadcom']
        }
        
        self.positive_words = [
            '상승', '급등', '오름', '강세', '호황', '실적개선', '수주', '기대감', '수혜', 
            '돌파', '신고가', '상승세', '매수세', '긍정적', '전망', '목표가', '상향',
            '양산', '승인', '독주', '압도적', '성장성', '고도화', '가속화', '확대',
            '호조', '반등', '상향', '투자의견', '매수', '매수강도', '외국인매수',
            '기관매수', '순매수', '인수', '합병', 'M&A', '실적', '흑자전환',
            '원팀', 'One-Team', 'TSMC', '엔비디아', 'AI', 'HBM4', '양산', 'record', 'blockbuster', 'surge', 'rally',
            'growth', 'expansion', 'investment', 'partnership', 'innovation', 'breakthrough', 'momentum', 'bullish', 'resilience', 'recovery'
        ]
        
        self.negative_words = [
            '하락', '급락', '약세', '부진', '실적악화', '손실', '위험', '하락세', 
            '매도세', '부정적', '하향', '조정', '하락장', '외국인매도', '기관매도',
            '순매도', '적자', '실적부진', '공백', '리스크', '과열', '버블',
            '부족', '지연', '실패', '감산', '수요둔화', 'decline', 'drop', 'fall', 'bearish', 'uncertainty', 'concern', 'warning', 'shrink', 'margin pressure'
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
        """주식별 상승 가능성 점수 계산 (글로벌 데이터 반영)"""
        stock_scores = {}
        
        # 뉴스 감성 분석
        sentiment_scores = self.analyze_news_sentiment(news_list)
        
        # 글로벌 주요 이벤트 감지
        global_topics = self._detect_global_topics(news_list)
        
        # 동적 섹터 가중치 계산
        dynamic_weights = self.get_dynamic_sector_weights(global_topics)
        
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
            
            # 글로벌 연관성 보너스
            global_bonus = self._calculate_global_impact(stock, global_topics)
            
            # 동적 섹터 가중치
            sector_weight = self._get_sector_weight(stock, dynamic_weights)
            
            # 최종 점수
            final_score = (base_score + sentiment_bonus + global_bonus) * sector_weight
            stock_scores[stock] = final_score
            
        return stock_scores

    def _detect_global_topics(self, news_list: List[Dict]) -> Dict[str, bool]:
        """글로벌 주요 이벤트 감지"""
        topics = {
            'tsmc_earnings': False,
            'nvidia_earnings': False,
            'openAI_titan': False,
            'fed_announcement': False,
            'record_quarter': False,
            'ai_boom': False,
            'global_tech_surge': False
        }
        
        all_text = ' '.join([f"{news.get('title', '')} {news.get('content', '')}" for news in news_list]).lower()
        
        if 'tsmc' in all_text and ('earnings' in all_text or 'record' in all_text):
            topics['tsmc_earnings'] = True
        if 'nvidia' in all_text and ('earnings' in all_text or 'revenue' in all_text):
            topics['nvidia_earnings'] = True
        if 'openai' in all_text and 'titan' in all_text:
            topics['openai_titan'] = True
        if 'fed' in all_text or 'federal reserve' in all_text:
            topics['fed_announcement'] = True
        if 'record' in all_text and ('quarter' in all_text or 'earnings' in all_text):
            topics['record_quarter'] = True
        if 'ai' in all_text and ('demand' in all_text or 'boom' in all_text):
            topics['ai_boom'] = True
        if 'surge' in all_text or 'rally' in all_text:
            topics['global_tech_surge'] = True
            
        return topics

    def _calculate_global_impact(self, stock: str, global_topics: Dict[str, bool]) -> float:
        """글로벌 이벤트의 종목별 영향력 계산"""
        impact = 0
        
        # TSMC 연관 종목들
        if global_topics['tsmc_earnings'] and stock in ['삼성전자', 'SK하이닉스', 'TSMC']:
            impact += 15
        
        # NVIDIA 연관 종목들
        if global_topics['nvidia_earnings'] and stock in ['NVIDIA', 'SK하이닉스', 'Broadcom']:
            impact += 12
        
        # OpenAI Titan 칩 발표
        if global_topics['openai_titan'] and stock in ['TSMC', 'Broadcom', 'NVIDIA']:
            impact += 10
        
        # Fed 발표
        if global_topics['fed_announcement'] and stock in ['SK증권', 'KB금융', '미래에셋증권']:
            impact += 8
        
        # AI 붐
        if global_topics['ai_boom'] and stock in ['NVIDIA', '삼성전자', 'TSMC', 'OpenAI']:
            impact += 10
        
        # 글로벌 테크 서지
        if global_topics['global_tech_surge'] and stock in ['Apple', 'Microsoft', 'Google', 'Meta']:
            impact += 8
            
        return impact

    def get_dynamic_sector_weights(self, global_topics: Dict[str, bool]) -> Dict[str, float]:
        """글로벌 이벤트에 따른 동적 섹터 가중치 계산"""
        base_weights = {
            '반도체': 1.4,      # TSMC 실적 폭발, 글로벌 AI 칩 수요 과열
            'AI': 1.35,         # OpenAI Titan 칩 발표, AI 플랫폼 확장
            '로봇': 1.3,       # 피지컬 AI, 휴머노이드 부상
            '우주항공': 1.25,   # 아르테미스, 우주경제 기대
            '글로벌테크': 1.3,  # 미국 빅테크 실적 호조
            '금융': 1.1,        # Fed 정책 불확실성으로 가중치 하향
            '방산': 1.2,        # 지정학적 리스크 증가
            '조선': 1.2,        # 장기 호황 사이클 지속
            '전력': 1.1,        # AI 데이터센터 전력 수요
            '2차전지': 1.05,    # 미국 IRA 정책 수혜
            '바이오': 0.95,     # 일시적 조정
            '자율주행': 1.15    # 로봇과 시너지
        }
        
        # TSMC 실적 발표 시 반도체 가중치 증가
        if global_topics['tsmc_earnings']:
            base_weights['반도체'] += 0.3
            
        # Fed 발표 시 금융 가중치 조정
        if global_topics['fed_announcement']:
            base_weights['금융'] += 0.15
            
        # AI 붐 시 관련 섹터 가중치 증가
        if global_topics['ai_boom']:
            base_weights['AI'] += 0.2
            base_weights['글로벌테크'] += 0.2
            
        return base_weights

    def _get_sector_weight(self, stock: str, dynamic_weights: Dict[str, float]) -> float:
        """동적 섹터 가중치 반환"""
        if dynamic_weights:
            for sector, stocks in self.stock_keywords.items():
                if stock in stocks:
                    return dynamic_weights.get(sector, 1.0)
                    
        # 기본 가중치 (이전 로직)
        sector_weights = {
            '반도체': 1.4,      # TSMC 실적 폭발, 글로벌 AI 칩 수요 과열
            'AI': 1.35,         # OpenAI Titan 칩 발표, AI 플랫폼 확장
            '로봇': 1.3,       # 피지컬 AI, 휴머노이드 부상
            '우주항공': 1.25,   # 아르테미스, 우주경제 기대
            '글로벌테크': 1.3,  # 미국 빅테크 실적 호조
            '금융': 1.1,        # Fed 정책 불확실성으로 가중치 하향
            '방산': 1.2,        # 지정학적 리스크 증가
            '조선': 1.2,        # 장기 호황 사이클 지속
            '전력': 1.1,        # AI 데이터센터 전력 수요
            '2차전지': 1.05,    # 미국 IRA 정책 수혜
            '바이오': 0.95,     # 일시적 조정
            '자율주행': 1.15    # 로봇과 시너지
        }
        
        for sector, stocks in self.stock_keywords.items():
            if stock in stocks:
                return sector_weights.get(sector, 1.0)
                
        return 1.0

    def _get_sector_weight_static(self, stock: str) -> float:
        """섹터별 가중치 부여"""
        sector_weights = {
            '반도체': 1.4,      # TSMC 실적 폭발, 글로벌 AI 칩 수요 과열
            'AI': 1.35,         # OpenAI Titan 칩 발표, AI 플랫폼 확장
            '로봇': 1.3,       # 피지컬 AI, 휴머노이드 부상
            '우주항공': 1.25,   # 아르테미스, 우주경제 기대
            '글로벌테크': 1.3,  # 미국 빅테크 실적 호조
            '금융': 1.1,        # Fed 정책 불확실성으로 가중치 하향
            '방산': 1.2,        # 지정학적 리스크 증가
            '조선': 1.2,        # 장기 호황 사이클 지속
            '전력': 1.1,        # AI 데이터센터 전력 수요
            '2차전지': 1.05,    # 미국 IRA 정책 수혜
            '바이오': 0.95,     # 일시적 조정
            '자율주행': 1.15    # 로봇과 시너지
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
            
        # 구체적인 이유 추가 (최신 외부 데이터 기반)
        if 'TSMC' in stock or '하이닉스' in stock:
            reasons.append("TSMC 실적 폭발 + 글로벌 AI 칩 수요 과열")
        elif 'HBM4' in stock:
            reasons.append("HBM4 양산 돌입 기대감")
        elif '삼성전자' in stock:
            reasons.append("글로벌 AI 반도체 리더 + 실적 기대감")
        elif 'NVIDIA' in stock:
            reasons.append("AI 칩 수익성 우려 vs 수요 증가 복합")
        elif 'OpenAI' in stock:
            reasons.append("Titan 칩 발표 + 독립 AI 칩 생태계 구축")
        elif 'Broadcom' in stock:
            reasons.append("AI 인프라 확대 + 맞춤형 실리콘 수혜")
        elif '금융' in stock or '증권' in stock or '보험' in stock or 'Fed' in stock:
            reasons.append("Fed 정책 불확실성 vs 금융 주주환원 정책")
        elif '우주' in stock or '항공' in stock or '아르테미스' in stock:
            reasons.append("아르테미스 프로젝트 + 글로벌 우주산업 성장")
        elif '로봇' in stock or '휴머노이드' in stock:
            reasons.append("피지컬 AI 시대 본격화 + 산업화 가속")
        elif '조선' in stock:
            reasons.append("글로벌 조선업 호황 + 수주 잔고 풍부")
        elif 'AI' in stock or '네이버' in stock or '카카오' in stock:
            reasons.append("글로벌 AI 투자 확대 + 플랫폼 경쟁력")
        elif '전력' in stock:
            reasons.append("AI 데이터센터 글로벌 전력 수요 급증")
        elif '방산' in stock:
            reasons.append("지정학적 리스크 증가 + 글로벌 방산 수요")
        elif '글로벌테크' in stock:
            reasons.append("미국 빅테크 실적 호조 + 글로벌 영향력")
            
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