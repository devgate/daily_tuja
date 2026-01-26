#!/usr/bin/env python3
"""
Vertiv(VRT) 주식 시세를 조회하는 메인 스크립트

사용법:
    python main.py          # 일반 실행
    python main.py --test   # 테스트 모드 (더미 데이터 사용)
"""
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))

from stock_fetcher import fetch_vertiv_stock, StockData


def format_market_cap(market_cap: Optional[float]) -> str:
    """시가총액을 포맷팅합니다."""
    if not market_cap:
        return "N/A"
    if market_cap >= 1_000_000_000_000:
        return f"${market_cap / 1_000_000_000_000:.2f}T"
    elif market_cap >= 1_000_000_000:
        return f"${market_cap / 1_000_000_000:.2f}B"
    else:
        return f"${market_cap / 1_000_000:.2f}M"


def print_stock_info(data: StockData) -> None:
    """주식 정보를 출력합니다."""
    # 등락에 따른 이모지 선택
    if data.change > 0:
        emoji = "📈"
    elif data.change < 0:
        emoji = "📉"
    else:
        emoji = "➖"

    print(f"\n{emoji} {data.name} ({data.symbol}) 시세")
    print("-" * 40)
    print(f"  현재가:      ${data.current_price:.2f}")
    print(f"  전일 종가:   ${data.previous_close:.2f}")
    print(f"  등락:        ${data.change:+.2f} ({data.change_percent:+.2f}%)")
    print(f"  고가 / 저가: ${data.day_high:.2f} / ${data.day_low:.2f}")
    print(f"  거래량:      {data.volume:,}")
    print(f"  시가총액:    {format_market_cap(data.market_cap)}")
    print("-" * 40)
    print("  📊 데이터 출처: Yahoo Finance")


def main(test_mode: bool = False) -> int:
    """
    메인 함수

    Args:
        test_mode: True면 더미 데이터 사용

    Returns:
        int: 종료 코드 (0: 성공, 1: 실패)
    """
    print("=" * 50)
    print("🔔 Vertiv(VRT) 주식 조회")
    print("=" * 50)

    try:
        if test_mode:
            print("⚠️  테스트 모드로 실행 중...")
            data = StockData(
                symbol="VRT",
                name="Vertiv Holdings Co",
                current_price=95.50,
                previous_close=92.30,
                change=3.20,
                change_percent=3.47,
                day_high=96.20,
                day_low=91.80,
                volume=5_234_567,
                market_cap=35_000_000_000,
            )
        else:
            print("📡 Yahoo Finance에서 데이터 조회 중...")
            data = fetch_vertiv_stock()

        print_stock_info(data)
        print("\n✅ 조회 완료!")
        return 0

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        return 1


if __name__ == "__main__":
    test_mode = "--test" in sys.argv
    exit_code = main(test_mode=test_mode)
    sys.exit(exit_code)
