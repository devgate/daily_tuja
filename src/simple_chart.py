#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
간단한 텍스트 기반 주간 성과 그래프 생성기
matplotlib 없이 순수 텍스트로 그래프 생성
"""

def create_simple_ascii_chart():
    """샘플 데이터로 ASCII 그래프 생성"""
    
    print("\n" + "="*80)
    print("📊 텍스트 기반 주간 성과 시각화")
    print("="*80)
    
    # 1. 주식별 성과 막대그래프
    print("\n📈 상위 주식별 성과 비교")
    print("="*60)
    
    stocks = [
        ("TSMC", 187.0, 8.2, "🇺🇸"),
        ("삼성전자", 102.0, 5.1, "🇰🇷"), 
        ("NVIDIA", 79.9, -2.3, "🇺🇸"),
        ("Broadcom", 79.9, 3.7, "🇺🇸"),
        ("TSM", 76.5, 4.2, "🇺🇸")
    ]
    
    for i, (stock, score, return_val, flag) in enumerate(stocks, 1):
        # 점수 막대그래프
        score_bar = create_bar(score, 50, 200)
        # 수익률 막대그래프
        return_bar = create_bar(abs(return_val), 5, 20)
        # 수익률 표시
        sign = "+" if return_val > 0 else ""
        
        print(f"{i:2d}. {flag} {stock:10s}")
        print(f"     예측: {score_bar} {score:6.1f}점")
        print(f"     실제: {return_bar} {sign}{return_val:+5.2f}%")
        print()
    
    # 2. 예측 정확도 파이차트
    print("\n🎯 주간 예측 정확도")
    print("="*40)
    
    total = 20
    correct = 15
    wrong = 5
    accuracy = 75.0
    
    # 텍스트 파이차트
    correct_bar = "■" * int(correct / total * 20)
    wrong_bar = "□" * int(wrong / total * 20)
    
    print(f"총 예측: {total}개")
    print(f"정확: {correct}개 ({accuracy:.1f}%)")
    print(f"오류: {wrong}개 ({100-accuracy:.1f}%)")
    print()
    print("시각화:")
    print(f"정확 {correct_bar}")
    print(f"오류 {wrong_bar}")
    print(f"       {'■'*int(accuracy/5)}{int(20-int(accuracy/5))*'□'} {accuracy:.1f}%")
    
    # 3. 일별 성과 추이
    print("\n📈 일별 예측 성과 추이")
    print("="*50)
    
    daily_data = [
        ("2026-01-27", 92.3, 3.5),
        ("2026-01-28", 88.7, -1.2)
    ]
    
    for date, avg_score, accuracy in daily_data:
        score_bar = create_bar(avg_score, 30, 120)
        acc_bar = create_bar(accuracy, 5, 20)
        sign = "+" if accuracy > 0 else ""
        
        print(f"{date} |")
        print(f"  예측점수: {score_bar} {avg_score:5.1f}")
        print(f"  실제수익: {acc_bar} {sign}{accuracy:+4.1f}%")
        print()
    
    # 4. 상관관계 시각화
    print("\n🔗 예측 점수 vs 실제 수익률 상관관계")
    print("="*50)
    
    corr_value = 0.73
    interpretation = "강한 상관관계"
    
    if abs(corr_value) >= 0.7:
        strength_bar = "██████████ 매우 강함"
        strength_emoji = "🔥"
    elif abs(corr_value) >= 0.5:
        strength_bar = "████████ 강함"
        strength_emoji = "📈"
    else:
        strength_bar = "██████ 중간"
        strength_emoji = "📊"
    
    print(f"상관계수: r = {corr_value:+.3f}")
    print(f"해석: {interpretation}")
    print(f"강도: {strength_emoji} {strength_bar}")
    print()
    
    # 5. 데이터 포인트 분포
    print("\n🎯 데이터 포인트 분포")
    print("="*40)
    
    data_points = [
        ("TSMC", 187.0, 8.2, "🇺🇸"),
        ("삼성전자", 102.0, 5.1, "🇰🇷"),
        ("NVIDIA", 79.9, -2.3, "🇺🇸"),
        ("Broadcom", 79.9, 3.7, "🇺🇸"),
        ("TSM", 76.5, 4.2, "🇺🇸"),
        ("OpenAI", 38.8, 6.1, "🇺🇸")
    ]
    
    for i, (stock, score, return_val, flag) in enumerate(data_points, 1):
        score_indicator = "█" * min(int(score / 200 * 10), 10)
        return_indicator = "▲" if return_val > 0 else "▼"
        return_intensity = min(int(abs(return_val) / 2) + 1, 5)
        
        print(f"{i:2d}. {flag} {stock:8s} | {score_indicator} {score:6.1f}점 | {return_indicator} {'█'*return_intensity} {return_val:+5.1f}%")
    
    print("\n" + "="*80)
    print("⚠️  위 시각화는 텍스트 기반 분석입니다.")
    print("    matplotlib 없이 순수 텍스트로 구현되었습니다.")
    print("="*80)

def create_bar(value, max_width, scale):
    """텍스트 막대그래프 생성"""
    if value <= 0:
        return "├" + "─" * max_width + "┤"
    
    bar_length = min(int(value / scale * max_width), max_width)
    if bar_length >= max_width:
        return "├" + "█" * max_width + "┤"
    
    return "├" + "█" * bar_length + "░" * (max_width - bar_length) + "┤"

if __name__ == "__main__":
    create_simple_ascii_chart()