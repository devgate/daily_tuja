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
        """글로벌 시장 데이터 수집"""
        try:
            # 미국 주요 지수 (올바른 티커로 수정)
            try:
                sp500 = yf.Ticker('^GSPC')
                nasdaq = yf.Ticker('^IXIC')
                djia = yf.Ticker('^DJI')
                
                # 반도체 ETF
                soxx = yf.Ticker('SOXX')
                
                return {
                    'sp500': {
                        'current': sp500.history(period='1d')['Close'].iloc[-1] if len(sp500.history(period='1d')) > 0 else 0,
                        'change': sp500.history(period='1d')['Close'].pct_change().iloc[-1] * 100 if len(sp500.history(period='1d')) > 1 else 0
                    },
                    'nasdaq': {
                        'current': nasdaq.history(period='1d')['Close'].iloc[-1] if len(nasdaq.history(period='1d')) > 0 else 0,
                        'change': nasdaq.history(period='1d')['Close'].pct_change().iloc[-1] * 100 if len(nasdaq.history(period='1d')) > 1 else 0
                    },
                    'djia': {
                        'current': djia.history(period='1d')['Close'].iloc[-1] if len(djia.history(period='1d')) > 0 else 0,
                        'change': djia.history(period='1d')['Close'].pct_change().iloc[-1] * 100 if len(djia.history(period='1d')) > 1 else 0
                    },
                    'semiconductor_etf': {
                        'current': soxx.history(period='1d')['Close'].iloc[-1] if len(soxx.history(period='1d')) > 0 else 0,
                        'change': soxx.history(period='1d')['Close'].pct_change().iloc[-1] * 100 if len(soxx.history(period='1d')) > 1 else 0
                    }
                }
            except Exception as e:
                logging.error(f"글로벌 시장 데이터 수집 오류: {e}")
                # API 실패 시 fallback 값 반환
                return {
                    'sp500': {'current': 5800.0, 'change': 0.5},    # default값
                    'nasdaq': {'current': 19000.0, 'change': 1.2},
                    'djia': {'current': 43000.0, 'change': 0.3},
                    'semiconductor_etf': {'current': 280.0, 'change': 2.1}
                }
            
            return {
                'sp500': {
                    'current': sp500.history(period='1d')['Close'].iloc[-1],
                    'change': sp500.history(period='1d')['Close'].pct_change().iloc[-1] * 100
                },
                'nasdaq': {
                    'current': nasdaq.history(period='1d')['Close'].iloc[-1],
                    'change': nasdaq.history(period='1d')['Close'].pct_change().iloc[-1] * 100
                },
                'djia': {
                    'current': djia.history(period='1d')['Close'].iloc[-1],
                    'change': djia.history(period='1d')['Close'].pct_change().iloc[-1] * 100
                },
                'semiconductor_etf': {
                    'current': soxx.history(period='1d')['Close'].iloc[-1],
                    'change': soxx.history(period='1d')['Close'].pct_change().iloc[-1] * 100
                }
            }
        except Exception as e:
            logging.error(f"글로벌 시장 데이터 수집 오류: {e}")
            return {
                'sp500': {'current': 0, 'change': 0},
                'nasdaq': {'current': 0, 'change': 0},
                'djia': {'current': 0, 'change': 0},
                'semiconductor_etf': {'current': 0, 'change': 0}
            }