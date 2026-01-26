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
    parser.add_argument('--mode', choices=['single', 'schedule', 'validate'], default='single',
                       help='실행 모드: single (단일 실행), schedule (스케줄링 실행), validate (검증)')
    parser.add_argument('--output', choices=['print', 'json', 'csv', 'report'], 
                       default='print', help='출력 형식')
    parser.add_argument('--days', type=int, default=30,
                       help='검증용 과거 일수 (validate 모드에서만 사용)')
    
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
        
    elif args.mode == 'schedule':
        # 스케줄링 실행 모드
        print("📅 스케줄링 기능은 현재 준비 중입니다.")
        print("단일 모드(--mode single)로 실행해주세요.")

if __name__ == "__main__":
    main()