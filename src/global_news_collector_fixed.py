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

class GlobalNewsCollector:
    def __init__(self):
        self.global_sources = [
            'https://www.cnbc.com/world/',
            'https://www.reuters.com/world/',
            'https://www.bloomberg.com/markets',
            'https://www.wsj.com/markets',
            'https://www.ft.com/markets'
        ]
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def collect_global_financial_news(self) -> List[Dict]:
        """글로벌 금융 뉴스 수집"""
        # 실제 환경에서는 웹크롤링 구현 필요
        # 현재는 최신 외부 데이터 기반 샘플 데이터로 대체
        return self._create_global_sample_news()
    
    def _create_global_sample_news(self) -> List[Dict]:
        """최신 외부 데이터 기반 샘플 뉴스 데이터 생성"""
        return [
            {
                'title': 'TSMC delivers record quarter, profit jumps 35% fueled by AI chip demand',
                'link': 'https://www.cnbc.com/2026/01/15/tsmc-q4-profit-record-ai-chip-demand',
                'source': 'CNBC',
                'date': '2026.01.15',
                'content': 'Taiwan Semiconductor Manufacturing Company (TSMC) reported record quarterly earnings with 35% profit jump, driven by unprecedented AI chip demand. CEO expects continued growth as AI applications expand globally.'
            },
            {
                'title': 'NVIDIA revenue hits $39.3B peak but margin concerns arise',
                'link': 'https://www.cnbc.com/2026/01/20/nvidia-39-3b-revenue-margin-warning',
                'source': 'CNBC',
                'date': '2026.01.20',
                'content': 'NVIDIA reported massive Q4 revenue of $39.3 billion, beating expectations, but shares declined as management warned about shrinking gross margins amid increased competition.'
            },
            {
                'title': 'OpenAI announces custom Titan chip with TSMC partnership',
                'link': 'https://markets.financialcontent.com/2026/01/20/openai-titan-chip',
                'source': 'Financial Content',
                'date': '2026.01.20',
                'content': 'OpenAI unveiled its first custom AI processor "Titan" in collaboration with Broadcom and TSMC, signaling end of "Nvidia tax" and major shift in AI chip landscape.'
            },
            {
                'title': 'Global economy shows resilience at 3.3% growth forecast',
                'link': 'https://www.imf.org/2026/01/19/global-economy-january-update',
                'source': 'IMF',
                'date': '2026.01.19',
                'content': 'IMF projects global growth at 3.3% for 2026, upward revision driven by technology investment and private sector adaptability despite trade uncertainties.'
            },
            {
                'title': 'Fed independence debate intensifies as rate decisions loom',
                'link': 'https://www.reuters.com/2026/01/26/fed-independence-battle',
                'source': 'Reuters',
                'date': '2026.01.26',
                'content': 'Federal Reserve faces increasing political pressure but shows little sign of capitulation on monetary policy independence, creating market uncertainty.'
            },
            {
                'title': 'Chip stocks rally globally on TSMC earnings beat',
                'link': 'https://www.cnbc.com/2026/01/15/chip-stocks-nvidia-amd-pop',
                'source': 'CNBC',
                'date': '2026.01.15',
                'content': 'Global semiconductor stocks surged after TSMC\'s blockbuster earnings boosted confidence in AI chip demand across the entire industry supply chain.'
            },
            {
                'title': 'Broadcom emerges as key AI infrastructure beneficiary',
                'link': 'https://www.fool.com/2026/01/22/broadcom-ai-infrastructure',
                'source': 'Motley Fool',
                'date': '2026.01.22',
                'content': 'Broadcom positioned to benefit from AI infrastructure expansion with custom silicon solutions and networking equipment essential for data centers.'
            },
            {
                'title': 'AMD prepares for Q4 earnings with AI growth momentum',
                'link': 'https://www.amd.com/2026/01/06/q4-earnings-announcement',
                'source': 'AMD IR',
                'date': '2026.01.06',
                'content': 'AMD scheduled to report fiscal Q4 2025 results with analysts expecting continued AI-driven growth in data center and enterprise markets.'
            }
        ]
        
        # 무작위로 6-10개 선택하여 반환
        selected_count = random.randint(6, min(10, len(sample_news)))
        return random.sample(sample_news, selected_count)

    def collect_global_market_data(self) -> Dict:
        """글로벌 시장 데이터 수집 (개선된 안정성)"""
        try:
            # API 호출 개선 - 더 안정적인 방식으로 시도
            tickers = {
                'sp500': '^GSPC',
                'nasdaq': '^IXIC', 
                'djia': '^DJI',
                'semiconductor_etf': 'SOXX'
            }
            
            result = {}
            
            for name, ticker_symbol in tickers.items():
                try:
                    # yfinance 세션 새로고침으로 안정성 확보
                    ticker = yf.Ticker(ticker_symbol)
                    
                    # 여러 기간으로 시도하여 데이터 확보
                    success = False
                    for period in ['5d', '1mo', '3mo']:
                        try:
                            hist = ticker.history(period=period)
                            
                            if hist is not None and len(hist) > 1 and 'Close' in hist.columns:
                                current = hist['Close'].iloc[-1]
                                prev_close = hist['Close'].iloc[-2]
                                
                                # 데이터 유효성 검사
                                if not (pd.isna(current) or pd.isna(prev_close) or prev_close == 0):
                                    change = ((current - prev_close) / prev_close * 100)
                                    
                                    result[name] = {
                                        'current': float(current),
                                        'change': float(change),
                                        'success': True
                                    }
                                    success = True
                                    logging.info(f"{ticker_symbol} ({period}) 데이터 수집 성공: {current:.2f}, {change:.2f}%")
                                    break
                                else:
                                    continue
                            else:
                                continue
                        except Exception as inner_e:
                            logging.debug(f"{ticker_symbol} ({period}) 실패: {inner_e}")
                            continue
                    
                    if not success:
                        # 모든 기간 실패 시 fallback
                        logging.warning(f"{ticker_symbol} 모든 기간 실패 - fallback 사용")
                        result[name] = self._get_fallback_data(name)
                        
                except Exception as e:
                    logging.warning(f"{ticker_symbol} 데이터 수집 실패: {e}")
                    result[name] = self._get_fallback_data(name)
            
            return result
            
        except Exception as e:
            logging.error(f"글로벌 시장 데이터 수집 전체 오류: {e}")
            # 전체 실패 시 모든 fallback 값 반환
            return {
                'sp500': self._get_fallback_data('sp500'),
                'nasdaq': self._get_fallback_data('nasdaq'),
                'djia': self._get_fallback_data('djia'),
                'semiconductor_etf': self._get_fallback_data('semiconductor_etf')
            }

    def _get_fallback_data(self, name: str) -> Dict:
        """fallback 데이터 반환"""
        fallback_values = {
            'sp500': {'current': 5800.0, 'change': 0.5, 'success': False},
            'nasdaq': {'current': 19000.0, 'change': 1.2, 'success': False},
            'djia': {'current': 43000.0, 'change': 0.3, 'success': False},
            'semiconductor_etf': {'current': 280.0, 'change': 2.1, 'success': False}
        }
        return fallback_values.get(name, {'current': 0, 'change': 0, 'success': False})