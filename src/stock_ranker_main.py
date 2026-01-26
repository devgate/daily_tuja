#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
다음날 오전 상승 예측 주식 추천 프로그램
매일 저녁 9-12시 사이 실행하여 다음날 오전 단타용 TOP 10 종목 추천
"""

import sys
import argparse
from datetime import datetime
from stock_ranking_system import StockRankingSystem

def main():
    parser = argparse.ArgumentParser(description='다음날 오전 상승 예측 주식 추천 프로그램')
    parser.add_argument('--mode', choices=['single', 'schedule'], default='single',
                       help='실행 모드: single (단일 실행), schedule (스케줄링 실행)')
    parser.add_argument('--output', choices=['print', 'json', 'csv', 'report'], 
                       default='print', help='출력 형식')
    
    args = parser.parse_args()
    
    # 시스템 초기화
    ranking_system = StockRankingSystem()
    
    if args.mode == 'single':
        # 단일 실행 모드
        print("🚀 다음날 오전 상승 예측 주식 분석 시작...")
        result = ranking_system.generate_daily_ranking()
        
        if result:
            if args.output == 'print':
                ranking_system.print_results(result)
            elif args.output == 'json':
                import json
                print(json.dumps(result, ensure_ascii=False, indent=2))
            elif args.output == 'csv':
                import pandas as pd
                df = pd.DataFrame(result['top_10_stocks'])
                print(df.to_string(index=False))
            elif args.output == 'report':
                print(ranking_system.generate_report())
        else:
            print("❌ 분석 결과가 없습니다.")
            
    elif args.mode == 'schedule':
        # 스케줄링 실행 모드
        ranking_system.run_scheduled_analysis()

if __name__ == "__main__":
    main()