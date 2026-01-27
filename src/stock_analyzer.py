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
        
        # 새로운 기술/영역 이슈 감지 키워드
        self.emerging_tech_keywords = {
            'AI전력': ['AI 전력', '데이터센터 전력', '전력전쟁', 'AI 인프라', '가스터빈', '액침냉각', '전력수요', '전력부족', 'shortage', 'AI power'],
            '차세대AI': ['초거대AI', 'AGI', '일반인공지능', '휴머노이드', '피지컬AI', 'AI 에이전트', 'autonomous AI'],
            '에너지혁신': ['원자력', '소형모듈원자로', 'SMR', '수소에너지', 'ESS', '전력저장', '재생에너지'],
            '우주경제': ['우주경제', '우주산업', '위성인터넷', '스페이스X', '아르테미스', '우주관광'],
            '차세대반도체': ['양자컴퓨터', '광자반도체', '뉴로모픽', 'HBM4', '3나노', 'GAA'],
            '생명공학': ['유전자편집', 'CRISPR', 'mRNA', '바이오시밀러', '세포치료'],
            '블록체인Web3': ['Web3', '탈중심화', 'NFT', '메타버스', '디지털자산']
        }
        
        # 영향력 있는 인물/기관 키워드 (10대 기구+인물 포함)
        self.influential_entities = {
            # 주식 시장 영향력 10대 기구
            '미국연방준비제도': ['Fed', '연방준비제도', '연준', 'Federal Reserve', '제롬 파월', 'Powell', '기준금리'],
            '미국증권거래위원회': ['SEC', '미국증권거래위원회', 'U.S. Securities', '규제', '상장'],
            '석유수출국기구': ['OPEC', '석유수출국기구', 'OPEC+', '원유', '석유감산'],
            '한국은행': ['한국은행', 'Bank of Korea', '이창용', 'Rhee Chang-yong', '기준금리', '통화정책'],
            '블랙록': ['블랙록', 'BlackRock', 'ETF', 'iShares', '래리 핑크', 'Larry Fink'],
            '유럽중앙은행': ['ECB', '유럽중앙은행', 'European Central Bank', '크리스틴 라가르드', 'Lagarde'],
            '일본은행': ['BOJ', '일본은행', 'Bank of Japan', '우에다 가즈오', 'Kazuo Ueda', '엔화'],
            'MSCI': ['MSCI', '모건스탠리 캐피탈 인터내셔널', 'Morgan Stanley', '지수', '인덱스'],
            '국제통화기금': ['IMF', '국제통화기금', 'International Monetary Fund', '재닛 옐런', 'Yellen'],
            '금융위원회': ['금융위원회', 'FSC', '금융감독원', 'FSS', '한국 금융당국'],
            
            # 주식 시장 영향력 10대 인물
            '제롬파월': ['제롬 파월', 'Powell', 'Fed 의장', '연준 의장'],
            '재닛옐런': ['재닛 옐런', 'Yellen', '재무장관', '미 재무장관'],
            '젠슨황': ['젠슨 황', 'Jensen Huang', '젠슨 황', 'NVIDIA CEO', '엔비디아'],
            '일론머스크': ['일론 머스크', '머스크', 'Elon Musk', '테슬라', '스페이스X', 'X', '도지코인'],
            '워런버핏': ['워런 버핏', 'Warren Buffett', '버크셔 해서웨이', 'Berkshire', '투자의 전설'],
            '크리스틴라가르드': ['크리스틴 라가르드', 'Lagarde', 'ECB 총재', '유럽중앙은행 총재'],
            '우에다가즈오': ['우에다 가즈오', 'Kazuo Ueda', 'BOJ 총재', '일본은행 총재'],
            '이창용': ['이창용', 'Rhee Chang-yong', '한국은행 총재'],
            '제이미다이먼': ['제이미 다이먼', 'Jamie Dimon', 'JP모건', 'JPMorgan', '은행'],
            '팀쿡': ['팀 쿡', 'Tim Cook', '애플', 'Apple', '아이폰', '맥북', 'CEO'],
            '이재명': ['이재명', '대통령', '윤석열', '정부', '청와대', '대통령실'],
            
            # 기타 주요 기업
            '구글': ['순다르피차이', '구글', 'Google', '알파벳', 'Alphabet'],
            '마이크로소프트': ['나델라', '마이크로소프트', 'Microsoft', '윈도우'],
            '아마존': ['베조스', '아마존', 'Amazon', 'AWS'],
            '메타': ['자커버그', '메타', 'Meta', '페이스북', '인스타그램']
        }
        
        # 국가별 주식 분류
        self.korean_stocks = [
            '삼성전자', 'SK하이닉스', '지니틱스', '라닉스', '와이씨켐', '샘씨엔에스', '저스템', '케이엔제이', 
            '한미반도체', 'DB하이텍', '이노션', '아이씨케이', 'SK증권', '한화손해보험', 'KB금융', '신한지주', 
            '하나금융지주', '미래에셋증권', '키움증권', 'KB증권', '한화에어로스페이스', '항공우주', '한국항공우주', 
            '항공우주산업', '삼성중공업', '현대중공업', '대선조선', '한국조선해양', '현대삼호중공업', 'LG에너지솔루션', 
            '삼성SDI', 'SK온', '에코프로', '포스코퓨처엠', '포스코DX', 'LG화학', '삼성바이오로직스', '셀트리온', 
            'SK바이오팜', '한국백신', '유진바이오', '녹십자', '케이씨씨', '보령', '현대차', '기아', '네이버', 
            '카카오', 'KT', 'LG이노텍', '모바일리언', 'LG', '더존비즈온', '비젠트로', '현대로보틱스', '로보스타', 
            '네오텍', '유비온', '티로보틱스', '알체라', '스타일럽', '두산로보틱스', '한국로봇산업진흥원', '한국전력', 
            '한수원', 'GS에너지', 'E1', 'SK가스', '삼성엔지니어링', '포스코건설', 'LIG넥스원', '현대로템', 
            '삼성탈레스', 'KAI'
        ]
        
        self.us_stocks = [
            'TSMC', 'NVIDIA', 'AMD', 'Broadcom', 'Qualcomm', 'TSM', 'Tesla', 'CATL', 'Pfizer', 'Moderna', 
            'Waymo', 'OpenAI', 'ChatGPT', 'Anthropic', 'Boston Dynamics', 'Tesla Bot', 'NextEra', 'Duke Energy', 
            'Lockheed Martin', 'Boeing', 'Apple', 'Microsoft', 'Google', 'Alphabet', 'Amazon', 'Meta', 'Facebook',
            'SpaceX', 'NASA', 'Fed', 'Federal Reserve', 'IMF'
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
        if global_topics.get('tsmc_earnings'):
            base_weights['반도체'] += 0.3
            
        # Fed 발표 시 금융 가중치 조정
        if global_topics.get('fed_announcement'):
            base_weights['금융'] += 0.15
            
        # AI 붐 시 관련 섹터 가중치 증가
        if global_topics.get('ai_boom'):
            base_weights['AI'] += 0.2
            base_weights['글로벌테크'] += 0.2
            
        return base_weights
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

    def _analyze_global_sentiment(self, global_market_data: Dict) -> Dict:
        """글로벌 시장 심리 분석 (stock_analyzer에 추가)"""
        try:
            sp500_change = global_market_data.get('sp500', {}).get('change', 0)
            nasdaq_change = global_market_data.get('nasdaq', {}).get('change', 0)
            semicon_change = global_market_data.get('semiconductor_etf', {}).get('change', 0)
            
            # 글로벌 시장 종합 심리
            avg_change = (sp500_change + nasdaq_change) / 2
            
            if avg_change > 1.0 and semicon_change > 2.0:
                sentiment = 'VERY_BULLISH'
            elif avg_change > 0.5:
                sentiment = 'BULLISH'
            elif avg_change < -0.5:
                sentiment = 'BEARISH'
            else:
                sentiment = 'NEUTRAL'
                
            return {
                'sentiment': sentiment,
                'sp500_change': sp500_change,
                'nasdaq_change': nasdaq_change,
                'semicon_change': semicon_change,
                'avg_change': avg_change
            }
                
        except Exception as e:
            logging.error(f"글로벌 시장 심리 분석 오류: {e}")
            return {
                'sentiment': 'NEUTRAL',
                'sp500_change': 0.5,
                'nasdaq_change': 1.2,
                'semicon_change': 2.1,
                'avg_change': 0.8
            }

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
    
    def classify_stock_region(self, stock: str) -> str:
        """주식의 국가 분류 (한국/미국/기타)"""
        if stock in self.korean_stocks:
            return "한국"
        elif stock in self.us_stocks:
            return "미국"
        else:
            # 섹터별 추가 분류
            if stock in ['HBM4', 'HBM']:  # 기술 용어는 한국 반도체 관련
                return "한국"
            elif stock in ['IMF', 'SpaceX']:  # 미국 기관
                return "미국"
            else:
                return "기타"
    
    def predict_declining_stocks(self, news_list: List[Dict], stock_mentions: Dict[str, int]) -> List[Tuple[str, float, str]]:
        """하락 예측 주식 분석 (부정적 뉴스 기반)"""
        declining_stocks = []
        
        # 뉴스 감성 분석
        for news in news_list:
            title = news.get('title', '')
            content = news.get('content', '')
            text = f"{title} {content}"
            
            # 부정적 단어 카운트
            negative_count = sum(1 for word in self.negative_words if word in text)
            
            # 각 섹터별 주식 확인 (부정적 뉴스에 언급된 주식)
            for sector, stocks in self.stock_keywords.items():
                for stock in stocks:
                    if stock in text and stock in stock_mentions:
                        # 부정적 뉴스 강도 계산
                        negative_score = negative_count * 10
                        
                        # 섹터별 위험도 추가
                        sector_risk = {
                            '금융': 15,  # Fed 정책 리스크
                            '2차전지': 12,  # 수요 둔화 우려
                            '바이오': 10,  # 규제 리스크
                            '자율주행': 8,  # 기술 지연 리스크
                            '조선': 6,  # 경기 민감
                            '전력': 5,  # 정책 리스크
                        }.get(sector, 3)
                        
                        total_risk_score = negative_score + sector_risk
                        
                        # 일정 점수 이상이면 하락 예측에 추가
                        if total_risk_score >= 20:
                            reason = f"{sector} 섹터, 부정적 뉴스 강도: {negative_score}, 섹터 위험도: {sector_risk}"
                            declining_stocks.append((stock, total_risk_score, reason))
        
        # 점수순 정렬 및 중복 제거
        unique_declining = {}
        for stock, score, reason in declining_stocks:
            if stock not in unique_declining or score > unique_declining[stock][0]:
                unique_declining[stock] = (score, reason)
        
        # 상위 5개 하락 예측 주식 반환
        sorted_declining = sorted(unique_declining.items(), key=lambda x: x[1][0], reverse=True)[:5]
        return [(stock, score, reason) for stock, (score, reason) in sorted_declining]
    
    def detect_emerging_trends(self, news_list: List[Dict]) -> Dict:
        """새로운 기술/영역 이슈 감지 (AI 전력, 일론머스크 효과 등)"""
        emerging_trends = {
            'hot_technologies': [],
            'influential_mentions': [],
            'trend_signals': []
        }
        
        tech_counts = Counter()
        entity_counts = Counter()
        trend_signals = []
        
        for news in news_list:
            title = news.get('title', '')
            content = news.get('content', '')
            text = f"{title} {content}".lower()
            
            # 새로운 기술 키워드 감지
            for tech_category, keywords in self.emerging_tech_keywords.items():
                for keyword in keywords:
                    if keyword.lower() in text:
                        tech_counts[tech_category] += 1
                        
                        # 구체적인 시그널 감지
                        if tech_category == 'AI전력' and any(word in text for word in ['급성장', '폭증', '부족', '전쟁', '수요급증']):
                            trend_signals.append({
                                'trend': 'AI전력인프라',
                                'signal': 'AI 전력 수요 급증',
                                'impact': 'HIGH',
                                'related_stocks': ['가스터빈', '액침냉각', '원자력', 'ESS'],
                                'reason': 'AI 데이터센터 전력 수요가 예상을 초과하며 인프라 투자 확대'
                            })
            
            # 영향력 있는 인물/기관 언급 감지
            for entity, keywords in self.influential_entities.items():
                for keyword in keywords:
                    if keyword.lower() in text:
                        entity_counts[entity] += 1
                        
                        # 일론 머스크 효과 감지
                        if entity == '일론머스크' and any(word in text for word in ['언급', '영향', '효과', '상승', '급등']):
                            trend_signals.append({
                                'trend': '머스크효과',
                                'signal': '일론 머스크 언급으로 주가 영향',
                                'impact': 'MEDIUM',
                                'related_stocks': ['테슬라', '스페이스X', '관련주'],
                                'reason': '일론 머스크의 언급으로 관련 주식 변동성 예상'
                            })
        
        # 핫 기술 분류 (상위 5개)
        top_techs = tech_counts.most_common(5)
        for tech, count in top_techs:
            if count >= 2:  # 2회 이상 언급된 경우만
                emerging_trends['hot_technologies'].append({
                    'technology': tech,
                    'mention_count': count,
                    'significance': 'HIGH' if count >= 4 else 'MEDIUM'
                })
        
        # 영향력 있는 인물/기관 분류 (상위 5개)
        top_entities = entity_counts.most_common(5)
        for entity, count in top_entities:
            if count >= 2:
                emerging_trends['influential_mentions'].append({
                    'entity': entity,
                    'mention_count': count,
                    'significance': 'HIGH' if count >= 4 else 'MEDIUM'
                })
        
        # 트렌드 시그널 정렬 (영향력 순)
        emerging_trends['trend_signals'] = sorted(
            trend_signals, 
            key=lambda x: {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}[x['impact']], 
            reverse=True
        )[:3]
        
        return emerging_trends
    
    def analyze_influential_impact(self, news_list: List[Dict]) -> Dict:
        """영향력 있는 기관/인물의 시장 영향 분석"""
        impact_analysis = {
            'high_impact_entities': [],
            'entity_signals': [],
            'market_impact_forecast': []
        }
        
        entity_mentions = Counter()
        impact_signals = []
        
        for news in news_list:
            title = news.get('title', '')
            content = news.get('content', '')
            text = f"{title} {content}".lower()
            
            # 영향력 기관/인물 언급 감지
            for entity, keywords in self.influential_entities.items():
                for keyword in keywords:
                    if keyword.lower() in text:
                        entity_mentions[entity] += 1
                        
                        # 고영향력 시그널 감지
                        if entity in ['미국연방준비제도', '한국은행', '제롬파월', '이창용']:
                            if any(word in text for word in ['기준금리', '인상', '인하', '통화정책', 'FOMC', '긴축', '완화']):
                                impact_signals.append({
                                    'entity': entity,
                                    'signal': '중앙은행 정책 발언',
                                    'impact': 'CRITICAL',
                                    'market_effect': '전체 시장 변동성',
                                    'related_sectors': ['금융', '반도체', '수출', '부동산'],
                                    'expected_move': '±2~5%'
                                })
                        
                        elif entity in ['일론머스크', '젠슨황']:
                            if any(word in text for word in ['발표', '언급', '상승', '급등', '혁신']):
                                impact_signals.append({
                                    'entity': entity,
                                    'signal': f'{entity} 주요 발언/발표',
                                    'impact': 'HIGH',
                                    'market_effect': '관련주 직접 영향',
                                    'related_sectors': ['AI', '반도체', '전기차', '우주'],
                                    'expected_move': '±5~15%'
                                })
                        
                        elif entity == '이재명':
                            if any(word in text for word in ['정책', '발표', '국회', '법안', '규제', '지원', '투자']):
                                impact_signals.append({
                                    'entity': entity,
                                    'signal': '대통령 정책 발표',
                                    'impact': 'HIGH',
                                    'market_effect': '정책 수혜/규제 섹터 영향',
                                    'related_sectors': ['부동산', '건설', '금융', '에너지', '제조업'],
                                    'expected_move': '±3~8%'
                                })
                        
                        elif entity in ['블랙록', 'MSCI']:
                            if any(word in text for word in ['ETF', '인덱스', '리밸런싱', '편입']):
                                impact_signals.append({
                                    'entity': entity,
                                    'signal': '대형 자금 움직임',
                                    'impact': 'HIGH',
                                    'market_effect': '대규모 자금 이동',
                                    'related_sectors': ['전체 섹터'],
                                    'expected_move': '±1~3%'
                                })
        
        # 고영향력 기관/인물 분류 (상위 5개)
        top_entities = entity_mentions.most_common(5)
        for entity, count in top_entities:
            if count >= 2:
                # 영향력 등급 결정
                critical_entities = ['미국연방준비제도', '제롬파월', '일론머스크', '젠슨황', '이재명']
                high_entities = ['한국은행', '블랙록', 'MSCI', '재닛옐런', '팀쿡']
                
                if entity in critical_entities:
                    significance = 'CRITICAL'
                elif entity in high_entities:
                    significance = 'HIGH'
                else:
                    significance = 'MEDIUM'
                
                impact_analysis['high_impact_entities'].append({
                    'entity': entity,
                    'mention_count': count,
                    'significance': significance
                })
        
        # 시그널 정렬 (영향력 순)
        impact_signals_sorted = sorted(
            impact_signals,
            key=lambda x: {'CRITICAL': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}[x['impact']],
            reverse=True
        )
        
        impact_analysis['entity_signals'] = impact_signals_sorted[:3]
        
        # 시장 영향 예측
        if impact_signals_sorted:
            overall_impact = max(signal['impact'] for signal in impact_signals_sorted)
            if overall_impact == 'CRITICAL':
                impact_analysis['market_impact_forecast'] = {
                    'level': 'CRITICAL',
                    'description': '중앙은행 정책 등 시장 전반에 대규모 영향 예상',
                    'volatility': '매우 높음',
                    'advice': '포지션 조정 및 리스크 관리 필수'
                }
            elif overall_impact == 'HIGH':
                impact_analysis['market_impact_forecast'] = {
                    'level': 'HIGH', 
                    'description': '대형 기업 CEO 등 특정 섹터에 강한 영향 예상',
                    'volatility': '높음',
                    'advice': '관련 섹터 집중 투자 기회'
                }
            else:
                impact_analysis['market_impact_forecast'] = {
                    'level': 'MEDIUM',
                    'description': '부분적인 시장 영향 예상',
                    'volatility': '보통',
                    'advice': '선택적 투자 접근'
                }
        
        return impact_analysis