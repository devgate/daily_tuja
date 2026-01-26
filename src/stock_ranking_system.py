import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional, Union
import json
import logging
from news_collector import NewsCollector
from stock_analyzer import StockAnalyzer
# import schedule  # 동적 import로 LSP 오류 회피
import time

class StockRankingSystem:
    def __init__(self):
        self.news_collector = NewsCollector()
        self.stock_analyzer = StockAnalyzer()
        self.results_history = []
        
        # 로깅 설정
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('stock_ranking.log'),
                logging.StreamHandler()
            ]
        )

    def generate_daily_ranking(self) -> Optional[Dict]:
        """일일 주식 랭킹 생성"""
        try:
            logging.info("일일 주식 랭킹 생성 시작...")
            
            # 1. 뉴스 데이터 수집
            news_list = self.news_collector.collect_financial_news()
            logging.info(f"수집된 뉴스: {len(news_list)}개")
            
            # 2. 주식 언급 분석
            stock_mentions = self.stock_analyzer.extract_stock_mentions(news_list)
            logging.info(f"언급된 주식: {len(stock_mentions)}개")
            
            # 3. 주식 점수 계산
            stock_scores = self.stock_analyzer.calculate_stock_scores(news_list, stock_mentions)
            
            # 4. 랭킹 생성
            ranking_results = self.stock_analyzer.rank_stocks(stock_scores)
            
            # 5. 시장 동향 분석
            market_trends = self.stock_analyzer.analyze_market_trends(news_list)
            
            # 6. 결과 포맷팅
            result = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'time': datetime.now().strftime('%H:%M:%S'),
                'market_sentiment': market_trends['market_sentiment'],
                'hot_sectors': market_trends['hot_sectors'],
                'top_10_stocks': [],
                'total_news_analyzed': len(news_list),
                'total_stocks_mentioned': len(stock_mentions)
            }
            
            for rank, (stock, score, reason) in enumerate(ranking_results, 1):
                result['top_10_stocks'].append({
                    'rank': rank,
                    'stock_name': stock,
                    'score': round(score, 2),
                    'reason': reason,
                    'mention_count': stock_mentions.get(stock, 0)
                })
            
            # 7. 결과 저장
            self.save_results(result)
            self.results_history.append(result)
            
            logging.info("일일 주식 랭킹 생성 완료!")
            return result
            
        except Exception as e:
            logging.error(f"랭킹 생성 중 오류 발생: {e}")
            return None

    def save_results(self, result: Dict) -> None:
        """결과 저장"""
        try:
            # JSON 파일로 저장
            filename = f"stock_ranking_{result['date']}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            # CSV 파일로 저장
            df = pd.DataFrame(result['top_10_stocks'])
            df['date'] = result['date']
            df['market_sentiment'] = result['market_sentiment']
            csv_filename = f"stock_ranking_{result['date']}.csv"
            df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
            
            logging.info(f"결과 저장 완료: {filename}, {csv_filename}")
            
        except Exception as e:
            logging.error(f"결과 저장 중 오류 발생: {e}")

    def print_results(self, result: Dict) -> None:
        """결과 출력"""
        if not result:
            print("결과가 없습니다.")
            return
            
        print("\n" + "="*80)
        print(f"📈 다음날 오전 단타용 주식 TOP 10 ({result['date']} {result['time']})")
        print("="*80)
        
        print(f"\n📊 시장 심리: {result['market_sentiment'].upper()}")
        print(f"🔥 핫 섹터: {', '.join(result['hot_sectors'])}")
        print(f"📰 분석 뉴스: {result['total_news_analyzed']}개")
        print(f"📈 언급 주식: {result['total_stocks_mentioned']}개")
        
        print("\n" + "─"*80)
        print("🏆 TOP 10 예상 상승주")
        print("─"*80)
        
        for stock_info in result['top_10_stocks']:
            print(f"\n{stock_info['rank']:2d}위 | {stock_info['stock_name']}")
            print(f"     점수: {stock_info['score']:6.1f} | 언급횟수: {stock_info['mention_count']}")
            print(f"     선정이유: {stock_info['reason']}")
        
        print("\n" + "="*80)
        print("⚠️  투자 주의사항: 본 분석은 뉴스 기반 예측으로, 투자는 본인의 판단에 따라야 합니다.")
        print("="*80)

    def run_scheduled_analysis(self):
        """스케줄링 실행"""
        try:
            import schedule
        except ImportError:
            print("❌ schedule 라이브러리가 설치되지 않았습니다.")
            print("pip install schedule 명령으로 설치해주세요.")
            return
            
        def run_analysis():
            print(f"\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 자동 분석 실행...")
            result = self.generate_daily_ranking()
            if result:
                self.print_results(result)
            
        # 매일 저녁 9시 실행
        schedule.every().day.at("21:00").do(run_analysis)
        
        # 추가 실행 시간 설정 (22시, 23시, 23시 30분)
        schedule.every().day.at("22:00").do(run_analysis)
        schedule.every().day.at("23:00").do(run_analysis)
        schedule.every().day.at("23:30").do(run_analysis)
        
        print("🤖 자동 분석 스케줄러 시작!")
        print("실행 시간: 매일 저녁 9시, 10시, 11시, 11시 30분")
        print("종료하려면 Ctrl+C를 누르세요.")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # 1분마다 확인

    def generate_report(self) -> str:
        """분석 보고서 생성"""
        if not self.results_history:
            return "분석 결과가 없습니다."
            
        latest_result = self.results_history[-1]
        
        report = f"""
# 📈 다음날 오전 단타 매매 전략 보고서

## 📅 분석 시간: {latest_result['date']} {latest_result['time']}

### 🌡️ 시장 심리: {latest_result['market_sentiment'].upper()}
### 🔥 주요 관심 섹터: {', '.join(latest_result['hot_sectors'])}

## 🏆 TOP 3 핵심 추천 종목

{self._format_top_stocks(latest_result['top_10_stocks'][:3])}

## 📊 전체 TOP 10 랭킹

{self._format_full_ranking(latest_result['top_10_stocks'])}

## 📝 투자 전략

### 진입 전략
- **시간**: 오전 9:00-9:30 장초반
- **방식**: 시초가 상승 종목 중심으로 진입
- **수량**: 소액 분할 매매 (5-10종목)
- **손절**: -3% 원칙 철저

### 수익 실현
- **목표수익**: +5% ~ +10%
- **시간**: 오전 11시 30분 전까지 실현
- **전략**: 단기 스윙으로 접근

### 리스크 관리
- **최대손실**: -5% (원칙 철저)
- **분산투자**: 섹터별 분산
- **시장상황**: 코스피 변동성 주시

---

⚠️  본 보고서는 뉴스 데이터 기반의 예측 분석입니다.
   실제 투자는 본인의 판단과 책임 하에 진행해야 합니다.
   수익을 보장하지 않으며, 손실 가능성이 항상 존재합니다.
        """
        
        return report

    def _format_top_stocks(self, top_stocks: List[Dict]) -> str:
        """TOP 종목 포맷팅"""
        formatted = ""
        for stock in top_stocks:
            formatted += f"""
### {stock['rank']}위: {stock['stock_name']}
- **예상 점수**: {stock['score']}점
- **선정 이유**: {stock['reason']}
- **매수 시점**: 오전 9시 00분-30분
- **예상 수익률**: +5% ~ +10%
"""
        return formatted

    def _format_full_ranking(self, all_stocks: List[Dict]) -> str:
        """전체 랭킹 포맷팅"""
        formatted = "| 순위 | 종목명 | 점수 | 선정 이유 |\n"
        formatted += "|------|--------|------|----------|\n"
        
        for stock in all_stocks:
            formatted += f"| {stock['rank']} | {stock['stock_name']} | {stock['score']} | {stock['reason']} |\n"
            
        return formatted