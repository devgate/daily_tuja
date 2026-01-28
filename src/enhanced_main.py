#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
향상된 다음날 오전 상승 예측 주식 추천 프로그램
글로벌 뉴스와 시장 데이터를 포함하여 정확도 향상
"""

import sys
import argparse
from datetime import datetime
from enhanced_stock_ranking_system import EnhancedStockRankingSystem

def main():
    parser = argparse.ArgumentParser(description='향상된 다음날 오전 상승 예측 주식 추천 프로그램')
    parser.add_argument('--mode', choices=['single', 'schedule', 'validate', 'weekly', 'monthly'], default='single',
                        help='실행 모드: single (단일 실행), schedule (스케줄링 실행), validate (검증), weekly (주간 성과 분석), monthly (월간 성과 분석)')
    parser.add_argument('--output', choices=['print', 'json', 'csv', 'report'], 
                        default='print', help='출력 형식')
    parser.add_argument('--days', type=int, default=30,
                        help='검증용 과거 일수 (validate 모드에서만 사용)')
    parser.add_argument('--plot', action='store_true',
                        help='주간 성과 그래프 표시 (weekly 모드에서만 사용)')
    parser.add_argument('--ascii', action='store_true',
                        help='주간 성과 텍스트 그래프 표시 (weekly 모드에서만 사용)')
    
    args = parser.parse_args()
    
    # 시스템 초기화
    ranking_system = EnhancedStockRankingSystem()
    
    if args.mode == 'single':
        # 단일 실행 모드
        print("🚀 향상된 다음날 오전 상승 예측 주식 분석 시작...")
        result = ranking_system.generate_enhanced_daily_ranking()
        
        if result:
            if args.output == 'print':
                ranking_system.print_enhanced_results(result)
            elif args.output == 'json':
                import json
                print(json.dumps(result, ensure_ascii=False, indent=2))
            elif args.output == 'csv':
                import pandas as pd
                df = pd.DataFrame(result['top_10_stocks'])
                print(df.to_string(index=False))
            elif args.output == 'report':
                ranking_system.print_enhanced_results(result)
        else:
            print("❌ 분석 결과가 없습니다.")
            
    elif args.mode == 'validate':
        # 검증 모드
        print("🔍 알고리즘 검증 시작...")
        validation_results = ranking_system.validate_with_historical_data(args.days)
        
    elif args.mode == 'weekly':
        # 주간 성과 분석 모드
        print("📊 주간 성과 분석 시작...")
        
        # 먼저 간단한 분석 실행
        ranking_system.simple_weekly_analysis(days_back=7)
        
        # 텍스트 기반 그래프 (선택적)
        if args.ascii:
            try:
                performance_data = ranking_system.analyze_weekly_performance(days_back=7)
                
                if performance_data.get('stock_performance'):
                    print("\n📊 텍스트 그래프 생성 중...")
                    ranking_system.generate_ascii_charts(performance_data)
                else:
                    print("❌ 그래프를 생성할 데이터가 없습니다.")
            except Exception as e:
                print(f"⚠️ 텍스트 그래프 생성 중 오류 발생: {e}")
                print("   간단한 텍스트 분석만 완료되었습니다.")
        
        # 실제 주가 데이터 기반 분석 (선택적)
        if args.plot:
            try:
                performance_data = ranking_system.analyze_weekly_performance(days_back=7)
                
                if performance_data.get('stock_performance'):
                    print("\n📈 matplotlib 그래프 생성 중...")
                    ranking_system.visualize_weekly_performance(performance_data, save_plot=True)
                else:
                    print("❌ 실제 주가 데이터를 분석할 데이터가 없습니다.")
            except Exception as e:
                print(f"⚠️ matplotlib 그래프 생성 중 오류 발생: {e}")
                print("   간단한 텍스트 분석만 완료되었습니다.")
    
    elif args.mode == 'monthly':
        # 월간 성과 분석 모드
        print("📊 월간 성과 분석 시작...")
        
        # 먼저 간단한 분석 실행 (30일)
        ranking_system.simple_weekly_analysis(days_back=30)
        
        # 텍스트 기반 그래프 (선택적)
        if args.ascii:
            try:
                performance_data = ranking_system.analyze_weekly_performance(days_back=7)
                
                if performance_data.get('stock_performance'):
                    print("\n📊 텍스트 그래프 생성 중...")
                    ranking_system.generate_ascii_charts(performance_data)
                else:
                    print("❌ 그래프를 생성할 데이터가 없습니다.")
            except Exception as e:
                print(f"⚠️ 텍스트 그래프 생성 중 오류 발생: {e}")
                print("   간단한 텍스트 분석만 완료되었습니다.")
        
        # 실제 주가 데이터 기반 분석 (선택적)
        if args.plot:
            try:
                performance_data = ranking_system.analyze_weekly_performance(days_back=7)
                
                if performance_data.get('stock_performance'):
                    print("\n📈 matplotlib 그래프 생성 중...")
                    ranking_system.visualize_weekly_performance(performance_data, save_plot=True)
                else:
                    print("❌ 실제 주가 데이터를 분석할 데이터가 없습니다.")
            except Exception as e:
                print(f"⚠️ matplotlib 그래프 생성 중 오류 발생: {e}")
                print("   간단한 텍스트 분석만 완료되었습니다.")
            
    elif args.mode == 'schedule':
        # 스케줄링 실행 모드
        print("📅 스케줄링 기능은 현재 준비 중입니다.")
        print("단일 모드(--mode single)로 실행해주세요.")

if __name__ == "__main__":
    main()