#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
테스트 및 예제 데이터로 주식 랭킹 시스템을 테스트하는 스크립트
"""

import json
from datetime import datetime
from stock_ranking_system import StockRankingSystem

def create_sample_news():
    """샘플 뉴스 데이터 생성"""
    return [
        {
            'title': '삼성전자, 다음 주 실적 발표 기대감에 시간외 상승',
            'link': 'https://example.com/news1',
            'source': '네이버금융',
            'date': '2026.01.26',
            'content': '삼성전자가 다음 주 실적 발표를 앞두고 시간외 거래에서 강세를 보이고 있습니다. 반도체 업황 개선 기대감이 커지면서 낙수효과가 기대됩니다.'
        },
        {
            'title': '지니틱스, 시스템반도체 설계 분야에서 급등',
            'link': 'https://example.com/news2',
            'source': '머니투데이',
            'date': '2026.01.26',
            'content': '지니틱스가 웨어러블용 터치IC 설계 분야에서 주목받고 있습니다. 실적 시즌 기대감으로 매수세가 몰리고 있습니다.'
        },
        {
            'title': 'SK증권, 자사주 소각 의무화 정책에 긍정적',
            'link': 'https://example.com/news3',
            'source': '아시아경제',
            'date': '2026.01.26',
            'content': '정부의 3차 상법개정 추진에 따라 SK증권이 긍정적인 반응을 보이고 있습니다. 주주환원정책 강화 기대감이 높습니다.'
        },
        {
            'title': '한화에어로스페이스, 아르테미스 프로젝트 기대감 상승',
            'link': 'https://example.com/news4',
            'source': '네이버금융',
            'date': '2026.01.26',
            'content': '한화에어로스페이스가 2월 아르테미스 발사를 앞두고 투자자들의 관심을 받고 있습니다. 우주항공 산업 본격화가 기대됩니다.'
        },
        {
            'title': 'SK하이닉스, HBM4 품질 승인 소식에 강세',
            'link': 'https://example.com/news5',
            'source': '머니투데이',
            'date': '2026.01.26',
            'content': 'SK하이닉스가 HBM4 품질 승정 관련 긍정적인 소식으로 상승하고 있습니다. AI 인프라 확대 수혜가 기대됩니다.'
        }
    ]

def test_ranking_system():
    """랭킹 시스템 테스트"""
    print("🧪 주식 랭킹 시스템 테스트 시작...")
    
    # 시스템 초기화
    ranking_system = StockRankingSystem()
    
    # 샘플 뉴스 데이터 생성
    sample_news = create_sample_news()
    print(f"📰 샘플 뉴스 데이터: {len(sample_news)}개")
    
    # 뉴스 수집 메서드 오버라이드 (테스트용)
    original_method = ranking_system.news_collector.collect_financial_news
    ranking_system.news_collector.collect_financial_news = lambda: sample_news
    
    try:
        # 랭킹 생성
        result = ranking_system.generate_daily_ranking()
        
        if result:
            print("✅ 테스트 성공!")
            ranking_system.print_results(result)
            
            # 결과 파일 저장 테스트
            print("\n📁 결과 저장 테스트...")
            ranking_system.save_results(result)
            print("✅ 저장 완료!")
            
            # 보고서 생성 테스트
            print("\n📄 보고서 생성 테스트...")
            report = ranking_system.generate_report()
            print("✅ 보고서 생성 완료!")
            
            # JSON 출력 테스트
            print("\n📊 JSON 출력 테스트...")
            json_output = json.dumps(result, ensure_ascii=False, indent=2)
            print(json_output[:500] + "..." if len(json_output) > 500 else json_output)
            
        else:
            print("❌ 테스트 실패: 결과가 없습니다.")
            
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 원본 메서드 복원
        ranking_system.news_collector.collect_financial_news = original_method

def test_components():
    """개별 컴포넌트 테스트"""
    from news_collector import NewsCollector
    from stock_analyzer import StockAnalyzer
    
    print("\n🔧 개별 컴포넌트 테스트...")
    
    # NewsCollector 테스트
    print("\n📡 NewsCollector 테스트...")
    collector = NewsCollector()
    print("✅ NewsCollector 초기화 성공")
    
    # StockAnalyzer 테스트
    print("\n📈 StockAnalyzer 테스트...")
    analyzer = StockAnalyzer()
    
    sample_news = create_sample_news()
    
    # 뉴스 감성 분석 테스트
    sentiment_scores = analyzer.analyze_news_sentiment(sample_news)
    print(f"✅ 감성 분석 결과: {len(sentiment_scores)}개 뉴스")
    
    # 주식 언급 분석 테스트
    stock_mentions = analyzer.extract_stock_mentions(sample_news)
    print(f"✅ 주식 언급 결과: {len(stock_mentions)}개 종목")
    
    # 점수 계산 테스트
    stock_scores = analyzer.calculate_stock_scores(sample_news, stock_mentions)
    print(f"✅ 점수 계산 결과: {len(stock_scores)}개 종목")
    
    # 랭킹 생성 테스트
    ranking = analyzer.rank_stocks(stock_scores)
    print(f"✅ 랭킹 생성 결과: {len(ranking)}개 종목")
    
    print("\n🎯 상위 3개 종목:")
    for i, (stock, score, reason) in enumerate(ranking[:3], 1):
        print(f"{i}위: {stock} (점수: {score:.1f}) - {reason}")

if __name__ == "__main__":
    print("="*80)
    print("🧪 주식 랭킹 시스템 통합 테스트")
    print("="*80)
    
    # 개별 컴포넌트 테스트
    test_components()
    
    print("\n" + "="*80)
    
    # 전체 시스템 테스트
    test_ranking_system()
    
    print("\n" + "="*80)
    print("🎉 테스트 완료!")
    print("="*80)