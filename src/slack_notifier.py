"""
Slack Webhook을 통해 메시지를 전송하는 모듈
"""
import os
import requests
from typing import Optional
from stock_fetcher import StockData


def format_stock_message(data: StockData) -> dict:
    """
    주식 데이터를 Slack 메시지 포맷으로 변환합니다.

    Args:
        data: 주식 데이터 객체

    Returns:
        dict: Slack Block Kit 형식의 메시지
    """
    # 등락에 따른 이모지 선택
    if data.change > 0:
        emoji = "📈"
        color = "#36a64f"  # 녹색
    elif data.change < 0:
        emoji = "📉"
        color = "#dc3545"  # 빨간색
    else:
        emoji = "➖"
        color = "#6c757d"  # 회색

    # 시가총액 포맷팅
    market_cap_str = ""
    if data.market_cap:
        if data.market_cap >= 1_000_000_000_000:
            market_cap_str = f"${data.market_cap / 1_000_000_000_000:.2f}T"
        elif data.market_cap >= 1_000_000_000:
            market_cap_str = f"${data.market_cap / 1_000_000_000:.2f}B"
        else:
            market_cap_str = f"${data.market_cap / 1_000_000:.2f}M"

    return {
        "attachments": [
            {
                "color": color,
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"{emoji} {data.name} ({data.symbol}) 마감 시세",
                            "emoji": True,
                        },
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*현재가*\n${data.current_price:.2f}",
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*전일 종가*\n${data.previous_close:.2f}",
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*등락*\n${data.change:+.2f} ({data.change_percent:+.2f}%)",
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*거래량*\n{data.volume:,}",
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*고가 / 저가*\n${data.day_high:.2f} / ${data.day_low:.2f}",
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*시가총액*\n{market_cap_str}",
                            },
                        ],
                    },
                    {"type": "divider"},
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": "📊 미국 증시 마감 데이터 | Yahoo Finance",
                            }
                        ],
                    },
                ],
            }
        ]
    }


def send_to_slack(
    data: StockData, webhook_url: Optional[str] = None
) -> bool:
    """
    주식 데이터를 Slack으로 전송합니다.

    Args:
        data: 주식 데이터 객체
        webhook_url: Slack Webhook URL (없으면 환경변수에서 읽음)

    Returns:
        bool: 전송 성공 여부

    Raises:
        ValueError: Webhook URL이 설정되지 않은 경우
    """
    url = webhook_url or os.getenv("SLACK_WEBHOOK_URL")

    if not url:
        raise ValueError(
            "SLACK_WEBHOOK_URL 환경변수가 설정되지 않았습니다. "
            ".env 파일을 확인하세요."
        )

    message = format_stock_message(data)

    response = requests.post(url, json=message, timeout=10)

    if response.status_code == 200:
        print("✅ Slack 메시지 전송 성공")
        return True
    else:
        print(f"❌ Slack 메시지 전송 실패: {response.status_code} - {response.text}")
        return False


if __name__ == "__main__":
    # 테스트용 더미 데이터
    from dotenv import load_dotenv

    load_dotenv()

    test_data = StockData(
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

    print("테스트 메시지 전송 중...")
    send_to_slack(test_data)
