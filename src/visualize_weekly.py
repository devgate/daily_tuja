#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
주간 주식 예측 성과 시각화 스크립트
"""

import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import defaultdict
import os

def load_past_results(days_back: int = 7):
    """과거 결과 로드"""
    past_results = {}
    current_date = datetime.now()
    
    for i in range(days_back):
        date = (current_date - timedelta(days=i)).strftime('%Y-%m-%d')
        
        # 다양한 파일명 패턴 시도
        patterns = [
            f"enhanced_stock_ranking_{date}.json",
            f"stock_ranking_{date}.json"
        ]
        
        for filename in patterns:
            if os.path.exists(filename):
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        past_results[date] = json.load(f)
                        break
                except (FileNotFoundError, json.JSONDecodeError):
                    continue
    
    return past_results

def analyze_weekly_data(past_results):
    """주간 데이터 분석"""
    analysis = {
        'dates': [],
        'daily_predictions': [],
        'daily_sentiment': [],
        'stock_mentions': defaultdict(lambda: {'count': 0, 'scores': [], 'regions': set()}),
        'sector_trends': defaultdict(int),
        'news_counts': {'domestic': [], 'global': []}
    }
    
    for date in sorted(past_results.keys()):
        result = past_results[date]
        
        analysis['dates'].append(date)
        
        # 일별 예측 수
        top_stocks = result.get('top_10_stocks', [])
        analysis['daily_predictions'].append(len(top_stocks))
        
        # 시장 심리
        sentiment = result.get('market_sentiment', 'neutral')
        analysis['daily_sentiment'].append(sentiment)
        
        # 뉴스 개수
        analysis['news_counts']['domestic'].append(result.get('domestic_news_count', 
                                                              result.get('total_news_analyzed', 0)))
        analysis['news_counts']['global'].append(result.get('global_news_count', 0))
        
        # 주식별 언급
        for stock_info in top_stocks:
            stock_name = stock_info.get('stock_name', 'Unknown')
            score = stock_info.get('score', 0)
            region = stock_info.get('region', '기타')
            
            analysis['stock_mentions'][stock_name]['count'] += 1
            analysis['stock_mentions'][stock_name]['scores'].append(score)
            analysis['stock_mentions'][stock_name]['regions'].add(region)
        
        # 섹터 트렌드
        hot_sectors = result.get('hot_sectors', [])
        for sector in hot_sectors:
            analysis['sector_trends'][sector] += 1
    
    return analysis

def create_visualizations(analysis):
    """시각화 생성"""
    
    # 한글 폰트 설정 (macOS)
    plt.rcParams['font.family'] = 'AppleGothic'
    plt.rcParams['axes.unicode_minus'] = False
    
    # 2x3 서브플롯 생성
    fig = plt.figure(figsize=(18, 12))
    fig.suptitle('📊 주간 주식 예측 성과 분석 대시보드', fontsize=20, fontweight='bold', y=0.98)
    
    # 1. 일별 예측 주식 수
    ax1 = plt.subplot(2, 3, 1)
    colors_predictions = ['#4CAF50' if count >= 8 else '#FFC107' if count >= 5 else '#F44336' 
                          for count in analysis['daily_predictions']]
    bars1 = ax1.bar(range(len(analysis['dates'])), analysis['daily_predictions'], 
                    color=colors_predictions, alpha=0.7, edgecolor='black', linewidth=1.5)
    ax1.set_xlabel('날짜', fontsize=11, fontweight='bold')
    ax1.set_ylabel('예측 주식 수', fontsize=11, fontweight='bold')
    ax1.set_title('📅 일별 예측 주식 수', fontsize=13, fontweight='bold', pad=10)
    ax1.set_xticks(range(len(analysis['dates'])))
    ax1.set_xticklabels([d.split('-')[1] + '/' + d.split('-')[2] for d in analysis['dates']], 
                         rotation=45, ha='right')
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # 값 표시
    for i, (bar, val) in enumerate(zip(bars1, analysis['daily_predictions'])):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(val)}개', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # 2. 시장 심리 추이
    ax2 = plt.subplot(2, 3, 2)
    sentiment_map = {'bullish': 1, 'neutral': 0, 'bearish': -1}
    sentiment_values = [sentiment_map.get(s.lower(), 0) for s in analysis['daily_sentiment']]
    colors_sentiment = ['#4CAF50' if v > 0 else '#F44336' if v < 0 else '#FFC107' 
                        for v in sentiment_values]
    
    ax2.plot(range(len(analysis['dates'])), sentiment_values, 
             marker='o', linewidth=3, markersize=10, color='#2196F3')
    ax2.scatter(range(len(analysis['dates'])), sentiment_values, 
                c=colors_sentiment, s=200, alpha=0.7, edgecolors='black', linewidth=2, zorder=5)
    ax2.set_xlabel('날짜', fontsize=11, fontweight='bold')
    ax2.set_ylabel('시장 심리', fontsize=11, fontweight='bold')
    ax2.set_title('📈 시장 심리 추이', fontsize=13, fontweight='bold', pad=10)
    ax2.set_xticks(range(len(analysis['dates'])))
    ax2.set_xticklabels([d.split('-')[1] + '/' + d.split('-')[2] for d in analysis['dates']], 
                         rotation=45, ha='right')
    ax2.set_yticks([-1, 0, 1])
    ax2.set_yticklabels(['Bearish 🐻', 'Neutral 🟡', 'Bullish 🐂'], fontsize=10)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    
    # 3. 뉴스 분석 추이
    ax3 = plt.subplot(2, 3, 3)
    x_pos = range(len(analysis['dates']))
    width = 0.35
    
    domestic_bars = ax3.bar([i - width/2 for i in x_pos], 
                            analysis['news_counts']['domestic'],
                            width, label='국내 뉴스', color='#2196F3', alpha=0.8, 
                            edgecolor='black', linewidth=1.5)
    global_bars = ax3.bar([i + width/2 for i in x_pos], 
                          analysis['news_counts']['global'],
                          width, label='글로벌 뉴스', color='#FF9800', alpha=0.8,
                          edgecolor='black', linewidth=1.5)
    
    ax3.set_xlabel('날짜', fontsize=11, fontweight='bold')
    ax3.set_ylabel('뉴스 개수', fontsize=11, fontweight='bold')
    ax3.set_title('📰 일별 뉴스 분석 현황', fontsize=13, fontweight='bold', pad=10)
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels([d.split('-')[1] + '/' + d.split('-')[2] for d in analysis['dates']], 
                         rotation=45, ha='right')
    ax3.legend(loc='upper left', fontsize=10, framealpha=0.9)
    ax3.grid(True, alpha=0.3, linestyle='--', axis='y')
    
    # 4. TOP 10 가장 많이 언급된 주식
    ax4 = plt.subplot(2, 3, 4)
    sorted_stocks = sorted(analysis['stock_mentions'].items(), 
                          key=lambda x: x[1]['count'], reverse=True)[:10]
    stock_names = [name[:10] + '...' if len(name) > 10 else name 
                   for name, _ in sorted_stocks]
    stock_counts = [data['count'] for _, data in sorted_stocks]
    
    # 국가별 색상
    colors_stocks = []
    for _, data in sorted_stocks:
        regions = data['regions']
        if '한국' in regions:
            colors_stocks.append('#4CAF50')
        elif '미국' in regions:
            colors_stocks.append('#2196F3')
        else:
            colors_stocks.append('#FF9800')
    
    bars4 = ax4.barh(range(len(stock_names)), stock_counts, 
                     color=colors_stocks, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax4.set_xlabel('언급 횟수', fontsize=11, fontweight='bold')
    ax4.set_ylabel('주식명', fontsize=11, fontweight='bold')
    ax4.set_title('🏆 TOP 10 가장 많이 언급된 주식', fontsize=13, fontweight='bold', pad=10)
    ax4.set_yticks(range(len(stock_names)))
    ax4.set_yticklabels(stock_names, fontsize=9)
    ax4.invert_yaxis()
    ax4.grid(True, alpha=0.3, linestyle='--', axis='x')
    
    # 값 표시
    for i, (bar, val) in enumerate(zip(bars4, stock_counts)):
        width = bar.get_width()
        ax4.text(width, bar.get_y() + bar.get_height()/2.,
                f' {int(val)}회', ha='left', va='center', fontsize=9, fontweight='bold')
    
    # 범례 추가
    kr_patch = mpatches.Patch(color='#4CAF50', label='한국 🇰🇷', alpha=0.8)
    us_patch = mpatches.Patch(color='#2196F3', label='미국 🇺🇸', alpha=0.8)
    other_patch = mpatches.Patch(color='#FF9800', label='기타 🌍', alpha=0.8)
    ax4.legend(handles=[kr_patch, us_patch, other_patch], loc='lower right', 
              fontsize=9, framealpha=0.9)
    
    # 5. 주식별 평균 점수
    ax5 = plt.subplot(2, 3, 5)
    avg_scores = [sum(data['scores']) / len(data['scores']) 
                  for _, data in sorted_stocks]
    
    bars5 = ax5.barh(range(len(stock_names)), avg_scores, 
                     color=colors_stocks, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax5.set_xlabel('평균 예측 점수', fontsize=11, fontweight='bold')
    ax5.set_ylabel('주식명', fontsize=11, fontweight='bold')
    ax5.set_title('⭐ TOP 10 주식 평균 예측 점수', fontsize=13, fontweight='bold', pad=10)
    ax5.set_yticks(range(len(stock_names)))
    ax5.set_yticklabels(stock_names, fontsize=9)
    ax5.invert_yaxis()
    ax5.grid(True, alpha=0.3, linestyle='--', axis='x')
    
    # 값 표시
    for i, (bar, val) in enumerate(zip(bars5, avg_scores)):
        width = bar.get_width()
        ax5.text(width, bar.get_y() + bar.get_height()/2.,
                f' {val:.1f}', ha='left', va='center', fontsize=9, fontweight='bold')
    
    # 6. 핫 섹터 분석
    ax6 = plt.subplot(2, 3, 6)
    if analysis['sector_trends']:
        sorted_sectors = sorted(analysis['sector_trends'].items(), 
                               key=lambda x: x[1], reverse=True)[:8]
        sector_names = [name for name, _ in sorted_sectors]
        sector_counts = [count for _, count in sorted_sectors]
        
        # 섹터별 색상
        sector_colors = ['#E91E63', '#9C27B0', '#3F51B5', '#00BCD4', 
                        '#4CAF50', '#FFEB3B', '#FF9800', '#795548']
        
        wedges, texts, autotexts = ax6.pie(sector_counts, labels=sector_names, 
                                            autopct='%1.1f%%',
                                            colors=sector_colors[:len(sector_names)],
                                            startangle=90, 
                                            textprops={'fontsize': 10, 'fontweight': 'bold'},
                                            wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(9)
            autotext.set_fontweight('bold')
    else:
        ax6.text(0.5, 0.5, '섹터 데이터 없음', 
                ha='center', va='center', fontsize=14, transform=ax6.transAxes)
    
    ax6.set_title('🔥 핫 섹터 분포', fontsize=13, fontweight='bold', pad=10)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    
    # 파일 저장
    filename = f"weekly_performance_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\n✅ 시각화 대시보드가 저장되었습니다: {filename}")
    
    # 통계 정보 출력
    print("\n" + "="*80)
    print("📊 주간 성과 요약")
    print("="*80)
    print(f"분석 기간: {analysis['dates'][0]} ~ {analysis['dates'][-1]}")
    print(f"분석 일수: {len(analysis['dates'])}일")
    print(f"총 예측 주식: {sum(analysis['daily_predictions'])}개")
    print(f"일평균 예측: {sum(analysis['daily_predictions'])/len(analysis['dates']):.1f}개")
    print(f"총 뉴스 분석: 국내 {sum(analysis['news_counts']['domestic'])}개, "
          f"글로벌 {sum(analysis['news_counts']['global'])}개")
    
    if sorted_stocks:
        print(f"\n🏆 가장 많이 언급된 주식:")
        for i, (name, data) in enumerate(sorted_stocks[:5], 1):
            avg_score = sum(data['scores']) / len(data['scores'])
            regions = ', '.join(data['regions'])
            print(f"   {i}. {name}: {data['count']}회 (평균 점수: {avg_score:.1f}, 지역: {regions})")
    
    print("="*80)
    
    plt.show()

def main():
    """메인 함수"""
    print("📊 주간 주식 예측 성과 시각화 시작...\n")
    
    # 데이터 로드
    past_results = load_past_results(days_back=7)
    
    if not past_results:
        print("❌ 최근 7일간의 과거 데이터가 없습니다.")
        print("먼저 예측 시스템을 실행하여 데이터를 축적해주세요.")
        return
    
    print(f"✅ {len(past_results)}일간의 데이터를 찾았습니다.")
    
    # 데이터 분석
    analysis = analyze_weekly_data(past_results)
    
    # 시각화 생성
    create_visualizations(analysis)

if __name__ == "__main__":
    main()
