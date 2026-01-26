"""
Vertiv(VRT) 주식 데이터를 Yahoo Finance에서 조회하는 모듈
"""
import requests
from dataclasses import dataclass
from typing import Optional


@dataclass
class StockData:
    """주식 데이터를 담는 클래스"""
    symbol: str
    name: str
    current_price: float
    previous_close: float
    change: float
    change_percent: float
    day_high: float
    day_low: float
    volume: int
    market_cap: Optional[float] = None


def fetch_vertiv_stock() -> StockData:
    """
    Vertiv Holdings(VRT) 주식 데이터를 조회합니다.

    Returns:
        StockData: 주식 데이터 객체

    Raises:
        Exception: 데이터 조회 실패 시
    """
    symbol = "VRT"
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }

    params = {
        "interval": "1d",
        "range": "2d",
    }

    response = requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    result = data["chart"]["result"][0]
    meta = result["meta"]

    current_price = meta.get("regularMarketPrice", 0)
    previous_close = meta.get("previousClose") or meta.get("chartPreviousClose", 0)

    change = current_price - previous_close
    change_percent = (change / previous_close * 100) if previous_close else 0

    return StockData(
        symbol=symbol,
        name="Vertiv Holdings Co",
        current_price=current_price,
        previous_close=previous_close,
        change=round(change, 2),
        change_percent=round(change_percent, 2),
        day_high=meta.get("regularMarketDayHigh", 0),
        day_low=meta.get("regularMarketDayLow", 0),
        volume=meta.get("regularMarketVolume", 0),
        market_cap=None,
    )


if __name__ == "__main__":
    # 테스트 실행
    data = fetch_vertiv_stock()
    print(f"종목: {data.name} ({data.symbol})")
    print(f"현재가: ${data.current_price:.2f}")
    print(f"전일 종가: ${data.previous_close:.2f}")
    print(f"등락: ${data.change:+.2f} ({data.change_percent:+.2f}%)")
    print(f"고가/저가: ${data.day_high:.2f} / ${data.day_low:.2f}")
    print(f"거래량: {data.volume:,}")
